from fastapi import APIRouter, status, Response, Request, File, UploadFile, Form
from fastapi.exceptions import HTTPException
import logging
from inference import Inferenceservice, InferenceserviceImpl
import json
from config.core import Core
from enum import Enum
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from bson.json_util import dumps
import io


class ResponseStatus(str, Enum):
    success = "success"
    error = "error"


class Response(BaseModel):
    status: str
    code: int
    message: str=''
    data: str



def init(core:Core) -> APIRouter:
  router = APIRouter()
  inferenceService : Inferenceservice = InferenceserviceImpl(core)

  @router.post(
    "/infoextractor",
    response_model=Response,
    status_code=status.HTTP_201_CREATED,
  )

  async def infoextractor(request: Request, 
                          csvfile: Optional[UploadFile] = File(default=None), 
                          reviewtext: Optional[str] = Form(default=None)) -> Response:
    
    try:
      logging.info("Microservice started")
      if csvfile and reviewtext:
         raise HTTPException(status_code=400, detail="Please provide either a file or text, not both.")
      elif csvfile:
        if csvfile.content_type != "text/csv":
          raise HTTPException(status_code=400, detail="Only CSV files are supported.")
        
        # Read the uploaded file
        content = await csvfile.read()
        csv_data = pd.read_csv(io.StringIO(content.decode("utf-8")))

        logging.info(csv_data.head())
        result = await inferenceService.uploadproductreview(csv_data)

      elif reviewtext:
        # Handle text input
        data = pd.DataFrame([reviewtext], columns=["input_sentence"])
        result = await inferenceService.uploadproductreview(data)
      else:
          raise HTTPException(status_code=400, detail="No input provided. Please upload a file or provide text.")
      
      # result = await inferenceService.uploadproductreview(uploadfile)

    except Exception as e:
      logging.exception(e)
      raise HTTPException(status_code=500, detail="Internal Server Error")

    return Response(
      status=ResponseStatus.success,
      code=200,
      data = dumps(result)
    )
  
  return router
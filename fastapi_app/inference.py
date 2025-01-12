from fastapi import File, UploadFile
from abc import ABCMeta, abstractmethod
import shutil
from config.config import Settings
from anthropic import Anthropic
from tools_prompts import tools, prompt
import logging

import json
import os
import logging
from config.core import Core

# logger = logging.getLogger(__name__)

from opentelemetry import trace
tracer = trace.get_tracer(__name__)


class Inferenceservice(metaclass=ABCMeta):
  @abstractmethod
  def uploadproductreview(self, uploadfile: list[UploadFile] = File(...)):
    pass


class InferenceserviceImpl(Inferenceservice):
  def __init__(self, core: Settings):
    self.core = core
    self.anthropic = Anthropic(api_key= self.core.anthropic_key)


  def parse_claude_response(self, response):
    for content in response.content:
        if content.type == 'tool_use':
            return content.input
    return None

  def extract_info(self, row):
    final_res = []
    for text in row.iloc[:, 0]:
      logging.info(text)
      response = self.anthropic.messages.create(model="claude-3-5-sonnet-20241022",                    
                                                              max_tokens=1024,
                                                              tools=tools,
                                                              messages=[
                                                                  {
                                                                      "role": "user",
                                                                      "content": prompt
                                                                  },
                                                                  {
                                                                      "role": "user",
                                                                      "content": text
                                                                  }
                                                              ]
                                                              )
      response = self.parse_claude_response(response)
      final_res.append(response)
      logging.info(final_res)
    return final_res
    


  async def uploadproductreview(self, data):
    try:
      with tracer.start_as_current_span("starting uploadproductreview API"):
        current_span = trace.get_current_span()
        current_span.set_attribute("function.name", "uploadproductreview")
        final_output = self.extract_info(data)
        logging.info(final_output)
      return json.dumps(final_output)
    
    except Exception as e:
            return [{
                "message": str(e),
            }]
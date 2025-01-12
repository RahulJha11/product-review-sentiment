import logging
import os
import random
import time
from typing import Optional
from config.core import Core
from config.config import Settings

import httpx
import uvicorn
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.propagate import inject
from utils import PrometheusMiddleware, metrics, setting_otlp
import parserapi

class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

class MicroService:
    def __init__(self, core:Core):
        self.core = core
        self.app_name = self.core.config.app_name
        self.OTLP_GRPC_ENDPOINT = "http://tempo:4317" 
        self.app = FastAPI(
        title=self.core.config.service_name,
        
        )

        origins = ["*"]
        self.app.add_middleware(
                CORSMiddleware,
                allow_origins=origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        self.app.add_middleware(PrometheusMiddleware)
        self.app.add_route("/metrics", metrics)  # for metrics with prometheus

        setting_otlp(self.app, self.app_name, self.OTLP_GRPC_ENDPOINT)

        

        self._configure_routers()

        self.headers ={}
        inject(self.headers)
        logging.critical(self.headers)

    def get_app(self) -> FastAPI:
      return self.app



    def _configure_routers(self):
        self.app.include_router(
        parserapi.init(self.core),
        prefix="/api/product-review",
        tags=["text"],

        )




if __name__ == "__main__":
    # update uvicorn access logger format
    config = Settings()
    core = Core(config)
    app =MicroService(core).get_app()
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=5000, log_config=log_config)

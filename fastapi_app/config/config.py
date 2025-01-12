import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  service_name: str
  anthropic_key:str
  app_name:str

  class Config:
        env_file = ".env"
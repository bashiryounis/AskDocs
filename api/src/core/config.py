import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Support loading envs from .env
load_dotenv(verbose=True)

class Config(BaseSettings):
    OPENAI_API_KEY: str = Field(env="OPENAI_API_KEY")
    HUGGINGFACEHUB_API_TOKEN: str = Field(env="HUGGINGFACEHUB_API_TOKEN")
    CHUNK_OVERLAP: str = Field(default=500, env="CHUNK_OVERLAP")
    CHUNK_SIZE: str = Field(default=500, env="CHUNK_SIZE")
    WEAVIATE_URL: str = Field(default="langllm_weaviate_1")
    STARTUP_PERIOD: str = Field(default=None, env="STARTUP_PERIOD")
    

    class Config:
        env_file = '.env'

config = Config()

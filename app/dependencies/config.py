from enum import Enum

from pydantic import BaseSettings


class AppEnv(str, Enum):
    """Application environment."""

    none = ''
    dev = 'dev'
    prod = 'prod'
    test = 'test'


class Settings(BaseSettings):
    """Application settings."""

    database_url: str
    app_env: AppEnv = AppEnv.none

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


SETTINGS = Settings()

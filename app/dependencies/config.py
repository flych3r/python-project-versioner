from enum import Enum
from typing import Optional

from pydantic import BaseSettings
from pydantic.networks import PostgresDsn


class AppEnv(str, Enum):
    """Application environment."""

    none = ''
    dev = 'dev'
    prod = 'prod'
    test = 'test'


class Settings(BaseSettings):
    """Application settings."""

    db_uri: PostgresDsn
    test_db_uri: Optional[str]
    app_env: AppEnv = AppEnv.none

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


SETTINGS = Settings()

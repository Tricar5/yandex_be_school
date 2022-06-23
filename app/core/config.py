import pathlib
from typing import Optional, Union, List

from pydantic import AnyHttpUrl, BaseSettings, validator

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DATABASE_PORT: str = "5432"
    DATABASE_HOST: str = "127.0.0.1"
    DATABASE_NAME: str = "yandex"
    DATABASE_USERNAME: str = "app"
    DATABASE_PASSWORD: str = "1qazxsw2"

    class Config:
        case_sensitive = True


settings = Settings()

import pathlib
from typing import Optional, Union, List

from pydantic import AnyHttpUrl, BaseSettings, validator

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # API_V1_STR: str = "/api/v1"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'

    SQLALCHEMY_DATABASE_URI: Optional[
        str
    ] = "postgresql+asyncpg://app:temp_pwd@127.0.0.1:5432/yandex"

    class Config:
        case_sensitive = True


settings = Settings()

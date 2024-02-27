import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[0]

sys.path.append(str(BASE_DIR))

from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import  PostgresDsn, field_validator
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(f"{BASE_DIR}/.env")
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SQLALCHEMY_ASYNC_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_ASYNC_DATABASE_URI", mode='before')
    def assemble_async_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            # user=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"/{values.data.get('POSTGRES_DB') or ''}",
        )


settings = Settings()

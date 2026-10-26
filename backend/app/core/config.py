from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "RagaLink API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    environment: str = "local"

    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_db: str = "ragalink"
    postgres_user: str = "ragalink_local"
    postgres_password: SecretStr = Field(..., repr=False)
    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_password: SecretStr = Field(..., repr=False)
    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "RagaLink API"
    app_version: str = "0.1.0"
    environment: str = "local"

    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_db: str = "ragalink"
    postgres_user: str = "ragalink_local"
    postgres_password: SecretStr = SecretStr("")

    redis_host: str = "127.0.0.1"
    redis_port: int = 6379
    redis_password: SecretStr = SecretStr("")

    @model_validator(mode="after")
    def validate_secrets(self) -> "Settings":
        if self.environment != "local":
            if not self.postgres_password.get_secret_value():
                raise ValueError(
                    "POSTGRES_PASSWORD must be configured outside local environment."
                )

            if not self.redis_password.get_secret_value():
                raise ValueError(
                    "REDIS_PASSWORD must be configured outside local environment."
                )

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()

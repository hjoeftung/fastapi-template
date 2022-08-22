import os
from functools import lru_cache

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "fastapi-template"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool | None = False
    SENTRY_DSN: HttpUrl | None = None
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TESTING: bool = False
    PYTEST_XDIST_WORKER: str = ""

    # Database settings
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "random"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "fastapi_template"
    POSTGRES_DRIVER: str | None = "postgresql+asyncpg"

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "driver": self.POSTGRES_DRIVER,
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "{driver}://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = "../.env"


@lru_cache
def get_settings() -> Settings:
    return Settings()

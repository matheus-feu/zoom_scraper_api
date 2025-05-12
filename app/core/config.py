import os
from functools import lru_cache

from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    app_name: str = "FastAPI Application"
    app_description: str = "A FastAPI application with a modular structure."
    app_version: str = "1.0.0"
    base_url: str = os.getenv("BASE_URL")
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = os.getenv("REDIS_PORT", 6379)
    redis_db: int = os.getenv("REDIS_DB", 0)
    redis_prefix: str = os.getenv("REDIS_PREFIX")

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """
    Get the application settings.
    Returns:
        Settings: The application settings.
    """
    return Settings()


settings: Settings = get_settings()

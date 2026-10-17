from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings, read from ``APP_*`` environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "python-github-action-example"
    database_url: str = "sqlite:///./app.db"
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    """Return process-wide settings."""
    return Settings()

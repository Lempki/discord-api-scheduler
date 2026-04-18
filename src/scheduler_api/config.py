from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    discord_api_secret: str
    scheduler_db_path: str = "/data/scheduler.db"
    log_level: str = "INFO"
    dispatcher_max_retries: int = 3


@lru_cache
def get_settings() -> Settings:
    return Settings()

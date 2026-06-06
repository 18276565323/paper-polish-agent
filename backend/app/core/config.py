from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = "local"
    modelgate_api_key: str = ""
    modelgate_base_url: str = "https://mg.aid.pub/v1"
    modelgate_model: str = ""
    database_url: str = "sqlite:///./paper_polish_dev.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()

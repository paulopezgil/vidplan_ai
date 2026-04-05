from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # OpenAI
    openai_api_key: SecretStr
    openai_model: str = "gpt-4o-mini"

    # Database
    database_url: str = "postgresql://admin:password@localhost:5432/vidplan"
    collection_name: str = "employees"
    embed_dim: int = 1536  # text-embedding-ada-002


settings = Settings()

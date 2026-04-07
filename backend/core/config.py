from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra environment variables
    )

    # AI Model
    ai_model: str = "openai:gpt-4o-mini"

    # Database - use DATABASE_URL from environment
    database_url: str = "postgresql://admin:password@localhost:5432/vidplan"
    embed_dim: int = 1536  # text-embedding-ada-002


settings = Settings()
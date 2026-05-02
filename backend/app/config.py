"""Application settings loaded via pydantic-settings.

Reads from environment + .env. Never commit a populated .env;
.env.example documents the schema.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App URLs
    app_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Anthropic (Claude Haiku live + Sonnet for one-time corpus labeling)
    anthropic_api_key: str

    # Deepgram (Nova-2 ASR + Aura TTS)
    deepgram_api_key: str

    # Clerk (auth)
    clerk_secret_key: str
    clerk_publishable_key: str

    # Cloudflare R2 (audio chunks + resume PDFs)
    r2_account_id: str = ""
    r2_access_key_id: str = ""
    r2_secret_access_key: str = ""
    r2_bucket: str = "mock-interviewer-audio"
    r2_endpoint: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()

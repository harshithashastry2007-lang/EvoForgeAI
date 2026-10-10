"""Validated configuration for the EvoForge AI backend."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    environment: Literal["development", "testing", "production"] = "development"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: str = "sqlite+aiosqlite:///./data/processed/evoforge.db"
    allowed_origins: list[str] = ["http://localhost:5173"]
    ingestion_allowed_root: Path = Path("data/controlled")
    sandbox_timeout_seconds: int = Field(default=300, ge=1, le=900)
    max_patch_candidates: int = Field(default=3, ge=1, le=3)
    llm_provider: Literal["none", "openai", "google", "anthropic", "local"] = "none"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="EVOFORGE_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached application-settings instance."""
    return Settings()
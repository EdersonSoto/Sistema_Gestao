from dataclasses import dataclass
from functools import lru_cache
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Sistema de Gestão")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    token_ttl_seconds: int = int(os.getenv("TOKEN_TTL_SECONDS", str(60 * 60 * 8)))


@lru_cache
def get_settings() -> Settings:
    return Settings()

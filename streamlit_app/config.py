from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_ROOT = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = APP_ROOT / "blood_analyzer.db"


def _database_url() -> str:
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    if all([db_user, db_password, db_host, db_port, db_name]):
        return (
            f"postgresql+psycopg2://{db_user}:{db_password}@"
            f"{db_host}:{db_port}/{db_name}"
        )

    return f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"


@dataclass(frozen=True)
class Settings:
    app_name: str
    llm_provider: str
    llm_model: str
    google_api_key: str | None
    openai_api_key: str | None
    anthropic_api_key: str | None
    groq_api_key: str | None
    azure_openai_key: str | None
    database_url: str
    log_level: str
    log_file: str
    jwt_secret_key: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "BloodIQ"),
        llm_provider=os.getenv("LLM_PROVIDER", "gemini").strip().lower(),
        llm_model=os.getenv("LLM_MODEL", "gemma-4-31b-it"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        azure_openai_key=os.getenv("AZURE_OPENAI_KEY"),
        database_url=_database_url(),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", "logs/bloodiq.log"),
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", "bloodiq-local-dev-secret-key-change-me-in-production"),
    )
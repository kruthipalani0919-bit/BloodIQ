from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SQLITE_PATH = APP_ROOT / "blood_analyzer.db"


def _build_database_url() -> str:
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
class DatabaseSettings:
    database_url: str
    echo_sql: bool
    pool_pre_ping: bool
    connect_timeout_seconds: int


@lru_cache(maxsize=1)
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings(
        database_url=_build_database_url(),
        echo_sql=os.getenv("DB_ECHO_SQL", "false").strip().lower() == "true",
        pool_pre_ping=os.getenv("DB_POOL_PRE_PING", "true").strip().lower() == "true",
        connect_timeout_seconds=int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
    )
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from database.exceptions import DatabaseConnectionError, DatabaseError
from database.settings import get_database_settings
from utils.logger import get_logger

settings = get_database_settings()
logger = get_logger(__name__)

engine_kwargs = {
    "echo": settings.echo_sql,
    "pool_pre_ping": settings.pool_pre_ping,
    "pool_recycle": 300,
}
if settings.database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.database_url, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except OperationalError as exc:
        session.rollback()
        logger.exception("Database connection failed")
        raise DatabaseConnectionError(
            "Unable to connect to the database. Check credentials, host, and server availability."
        ) from exc
    except SQLAlchemyError as exc:
        session.rollback()
        logger.exception("Database transaction failed")
        raise DatabaseError("A database transaction failed.") from exc
    finally:
        session.close()


def verify_database_connection() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def initialize_database() -> None:
    from database import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    if settings.database_url.startswith("sqlite"):
        _apply_sqlite_schema_compatibility()


def _apply_sqlite_schema_compatibility() -> None:
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        if "reports" in tables:
            report_columns = {column["name"] for column in inspector.get_columns("reports")}
            if "updated_at" not in report_columns:
                connection.execute(
                    text("ALTER TABLE reports ADD COLUMN updated_at DATETIME")
                )
                connection.execute(
                    text(
                        "UPDATE reports SET updated_at = COALESCE(updated_at, created_at, CURRENT_TIMESTAMP)"
                    )
                )

        if "chat_messages" in tables:
            message_columns = {column["name"] for column in inspector.get_columns("chat_messages")}
            if "created_at" not in message_columns:
                connection.execute(
                    text("ALTER TABLE chat_messages ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
                )
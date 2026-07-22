from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from database.exceptions import DatabaseConnectionError, DatabaseError
from database.settings import get_database_settings
from utils.logger import get_logger
from supabase import create_client
from dotenv import load_dotenv
import os

settings = get_database_settings()
logger = get_logger(__name__)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

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
    _apply_schema_migrations()


def _apply_schema_migrations() -> None:
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    with engine.begin() as connection:
        if "reports" in tables:
            columns = {column["name"] for column in inspector.get_columns("reports")}
            
            if "updated_at" not in columns:
                if settings.database_url.startswith("sqlite"):
                    connection.execute(text("ALTER TABLE reports ADD COLUMN updated_at DATETIME"))
                else:
                    connection.execute(text("ALTER TABLE reports ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
                connection.execute(
                    text("UPDATE reports SET updated_at = COALESCE(created_at, CURRENT_TIMESTAMP)")
                )

            if "user_id" not in columns:
                if settings.database_url.startswith("sqlite"):
                    connection.execute(text("ALTER TABLE reports ADD COLUMN user_id INTEGER"))
                else:
                    connection.execute(text("ALTER TABLE reports ADD COLUMN user_id INTEGER REFERENCES users(id) ON DELETE SET NULL"))
            
            if "report_name" not in columns:
                connection.execute(text("ALTER TABLE reports ADD COLUMN report_name VARCHAR(255)"))
            
            if "report_type" not in columns:
                connection.execute(text("ALTER TABLE reports ADD COLUMN report_type VARCHAR(50)"))
                
            if "uploaded_file" not in columns:
                connection.execute(text("ALTER TABLE reports ADD COLUMN uploaded_file TEXT"))
                
            if "report_date" not in columns:
                if settings.database_url.startswith("sqlite"):
                    connection.execute(text("ALTER TABLE reports ADD COLUMN report_date DATETIME"))
                else:
                    connection.execute(text("ALTER TABLE reports ADD COLUMN report_date TIMESTAMP"))

        if "chat_messages" in tables:
            columns = {column["name"] for column in inspector.get_columns("chat_messages")}
            if "created_at" not in columns:
                if settings.database_url.startswith("sqlite"):
                    connection.execute(text("ALTER TABLE chat_messages ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
                else:
                    connection.execute(text("ALTER TABLE chat_messages ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
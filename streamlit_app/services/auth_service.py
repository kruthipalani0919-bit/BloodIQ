from __future__ import annotations

from datetime import datetime, timedelta
import bcrypt
import jwt
from sqlalchemy.orm import Session
from database.models import User
from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify a hashed password against a plain password."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception as e:
        logger.error("Failed to verify password: %s", e)
        return False


def generate_token(user_id: int) -> str:
    """Generate a JWT token for the user."""
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


def verify_token(token: str) -> int | None:
    """Verify a JWT token and return the user ID."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token signature has expired")
    except jwt.InvalidTokenError:
        logger.warning("JWT token is invalid")
    except Exception as e:
        logger.error("Error decoding JWT token: %s", e)
    return None


def get_user_by_email(db: Session, email: str) -> User | None:
    """Query a user by their email address."""
    return db.query(User).filter(User.email == email.strip().lower()).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Query a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def register_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
    age: int | None = None,
    gender: str | None = None,
) -> User:
    """Register a new user in the database."""
    email_clean = email.strip().lower()
    existing = get_user_by_email(db, email_clean)
    if existing:
        raise ValueError(f"User with email '{email_clean}' already exists")

    hashed = hash_password(password)
    user = User(
        email=email_clean,
        password_hash=hashed,
        full_name=full_name.strip(),
        age=age,
        gender=gender,
    )
    db.add(user)
    db.flush()  # populate ID
    logger.info("Registered user %s (ID: %d)", email_clean, user.id)
    return user


def authenticate_user(db: Session, email: str, password: str) -> tuple[User, str] | None:
    """Authenticate a user and return the user object and a JWT token."""
    email_clean = email.strip().lower()
    user = get_user_by_email(db, email_clean)
    if not user:
        logger.info("Authentication failed: user %s not found", email_clean)
        return None

    if not verify_password(password, user.password_hash):
        logger.info("Authentication failed: invalid password for user %s", email_clean)
        return None

    token = generate_token(user.id)
    logger.info("User %s logged in successfully", email_clean)
    return user, token

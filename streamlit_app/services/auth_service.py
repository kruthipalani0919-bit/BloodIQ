from __future__ import annotations

from datetime import datetime, timedelta
import bcrypt
import jwt
from database.connection import supabase
from types import SimpleNamespace
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



def register_user(
    db,
    email,
    password,
    full_name,
    age=None,
    gender=None,
):
    email = email.strip().lower()

    existing = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if existing.data:
        raise ValueError("User already exists")

    hashed = hash_password(password)

    result = (
        supabase.table("users")
        .insert({
            "email": email,
            "password_hash": hashed,
            "full_name": full_name,
            "age": age,
            "gender": gender,
        })
        .execute()
    )

    return SimpleNamespace(**result.data[0])


def authenticate_user(db, email, password):
    email = email.strip().lower()

    result = (
        supabase.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not result.data:
        return None

    user = result.data[0]

    if not verify_password(password, user["password_hash"]):
        return None

    token = generate_token(user["id"])

    return SimpleNamespace(**user), token
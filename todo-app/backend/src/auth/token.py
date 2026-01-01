"""
JWT token generation and validation for authentication.
"""

from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from src.config import settings

ALGORITHM = "HS256"


def create_access_token(user_id: int, email: str) -> str:
    """
    Create a JWT access token for authenticated user.

    Args:
        user_id: User's database ID
        email: User's email address

    Returns:
        Encoded JWT token string
    """
    expire = datetime.utcnow() + timedelta(days=settings.session_duration_days)
    to_encode = {"sub": str(user_id), "email": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.auth_secret, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload dict with 'sub' (user_id) and 'email', or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.auth_secret, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

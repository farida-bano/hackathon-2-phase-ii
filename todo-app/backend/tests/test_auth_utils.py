"""
Unit tests for authentication utilities.
"""

from datetime import datetime, timedelta

import pytest

from src.auth.password import hash_password, verify_password
from src.auth.token import create_access_token, decode_access_token


def test_hash_password():
    """Test password hashing."""
    password = "mypassword123"
    hashed = hash_password(password)

    assert hashed != password
    assert len(hashed) > 50  # Bcrypt hashes are ~60 chars
    assert hashed.startswith("$2b$")  # Bcrypt hash prefix


def test_verify_password_success():
    """Test successful password verification."""
    password = "correctpassword"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_failure():
    """Test password verification with wrong password."""
    password = "correctpassword"
    hashed = hash_password(password)

    assert verify_password("wrongpassword", hashed) is False


def test_hash_password_different_each_time():
    """Test that hashing the same password produces different hashes (salt)."""
    password = "samepassword"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_create_access_token():
    """Test JWT token creation."""
    user_id = 123
    email = "test@example.com"

    token = create_access_token(user_id, email)

    assert isinstance(token, str)
    assert len(token) > 50  # JWT tokens are quite long


def test_decode_access_token_success():
    """Test successful JWT token decoding."""
    user_id = 456
    email = "decode@example.com"

    token = create_access_token(user_id, email)
    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["email"] == email
    assert "exp" in payload


def test_decode_access_token_invalid():
    """Test decoding invalid JWT token."""
    invalid_token = "this.is.invalid"

    payload = decode_access_token(invalid_token)

    assert payload is None


def test_decode_access_token_tampered():
    """Test decoding tampered JWT token."""
    user_id = 789
    email = "tamper@example.com"

    token = create_access_token(user_id, email)

    # Tamper with token by changing a character
    tampered_token = token[:-5] + "XXXXX"

    payload = decode_access_token(tampered_token)

    assert payload is None


def test_token_expiration_field():
    """Test that token contains expiration field."""
    from src.config import settings

    user_id = 111
    email = "expire@example.com"

    token = create_access_token(user_id, email)
    payload = decode_access_token(token)

    assert "exp" in payload

    # Check expiration is approximately correct (within 1 minute tolerance)
    expected_exp = datetime.utcnow() + timedelta(days=settings.session_duration_days)
    actual_exp = datetime.fromtimestamp(payload["exp"])

    time_diff = abs((expected_exp - actual_exp).total_seconds())
    assert time_diff < 60  # Within 1 minute

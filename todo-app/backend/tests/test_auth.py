"""
Integration tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.models.user import User


def test_signup_success(client: TestClient, session: Session):
    """Test successful user signup."""
    response = client.post(
        "/auth/signup",
        json={"email": "newuser@example.com", "password": "securepassword123"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "user_id" in data
    assert "token" in data
    assert len(data["token"]) > 0

    # Verify user exists in database
    user = session.exec(select(User).where(User.email == "newuser@example.com")).first()
    assert user is not None
    assert user.email == "newuser@example.com"


def test_signup_duplicate_email(client: TestClient, session: Session):
    """Test signup with already registered email."""
    # Create first user
    client.post(
        "/auth/signup",
        json={"email": "duplicate@example.com", "password": "password123"},
    )

    # Try to create second user with same email
    response = client.post(
        "/auth/signup",
        json={"email": "duplicate@example.com", "password": "differentpass456"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_signup_invalid_email(client: TestClient):
    """Test signup with invalid email format."""
    response = client.post(
        "/auth/signup",
        json={"email": "not-an-email", "password": "password123"},
    )

    assert response.status_code == 422  # Validation error


def test_signup_short_password(client: TestClient):
    """Test signup with password shorter than 8 characters."""
    response = client.post(
        "/auth/signup",
        json={"email": "test@example.com", "password": "short"},
    )

    assert response.status_code == 422  # Validation error


def test_signin_success(client: TestClient, session: Session):
    """Test successful user signin."""
    # First signup
    signup_response = client.post(
        "/auth/signup",
        json={"email": "signin@example.com", "password": "password123"},
    )
    assert signup_response.status_code == 201

    # Then signin
    signin_response = client.post(
        "/auth/signin",
        json={"email": "signin@example.com", "password": "password123"},
    )

    assert signin_response.status_code == 200
    data = signin_response.json()
    assert data["email"] == "signin@example.com"
    assert "user_id" in data
    assert "token" in data
    assert len(data["token"]) > 0

    # Verify last_login_at was updated
    user = session.exec(select(User).where(User.email == "signin@example.com")).first()
    assert user.last_login_at is not None


def test_signin_invalid_email(client: TestClient):
    """Test signin with non-existent email."""
    response = client.post(
        "/auth/signin",
        json={"email": "nonexistent@example.com", "password": "password123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_signin_invalid_password(client: TestClient):
    """Test signin with incorrect password."""
    # First signup
    client.post(
        "/auth/signup",
        json={"email": "wrongpass@example.com", "password": "correctpassword"},
    )

    # Try signin with wrong password
    response = client.post(
        "/auth/signin",
        json={"email": "wrongpass@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_signout_success(client: TestClient):
    """Test successful signout with valid token."""
    # Signup to get a token
    signup_response = client.post(
        "/auth/signup",
        json={"email": "signout@example.com", "password": "password123"},
    )
    token = signup_response.json()["token"]

    # Signout with token
    response = client.post(
        "/auth/signout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204


def test_signout_no_token(client: TestClient):
    """Test signout without authentication token."""
    response = client.post("/auth/signout")

    assert response.status_code == 403  # Forbidden (no token provided)


def test_signout_invalid_token(client: TestClient):
    """Test signout with invalid token."""
    response = client.post(
        "/auth/signout",
        headers={"Authorization": "Bearer invalid_token_here"},
    )

    assert response.status_code == 401


def test_password_hashing(client: TestClient, session: Session):
    """Test that passwords are properly hashed and not stored in plain text."""
    password = "mysecretpassword"

    client.post(
        "/auth/signup",
        json={"email": "hashtest@example.com", "password": password},
    )

    # Retrieve user from database
    user = session.exec(select(User).where(User.email == "hashtest@example.com")).first()

    # Verify password is hashed (not plain text)
    assert user.password_hash != password
    assert len(user.password_hash) > 50  # Bcrypt hashes are typically 60 chars


def test_token_contains_user_info(client: TestClient):
    """Test that JWT token can be decoded and contains user information."""
    from src.auth.token import decode_access_token

    # Signup to get a token
    response = client.post(
        "/auth/signup",
        json={"email": "tokentest@example.com", "password": "password123"},
    )

    token = response.json()["token"]
    user_id = response.json()["user_id"]

    # Decode token
    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == str(user_id)
    assert payload["email"] == "tokentest@example.com"
    assert "exp" in payload  # Expiration time

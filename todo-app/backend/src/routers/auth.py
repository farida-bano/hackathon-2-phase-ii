"""
Authentication endpoints: signup, signin, signout.
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.auth.dependencies import CurrentUser
from src.auth.password import hash_password, verify_password
from src.auth.token import create_access_token
from src.database import get_session
from src.models.user import User
from src.schemas.auth import SigninRequest, SigninResponse, SignupRequest, SignupResponse
from src.schemas.error import ErrorResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Email already registered"},
    },
)
def signup(
    request: SignupRequest,
    session: Annotated[Session, Depends(get_session)],
) -> SignupResponse:
    """
    Register a new user account.

    Creates a new user with hashed password and returns an access token.

    Args:
        request: Signup request with email and password
        session: Database session

    Returns:
        SignupResponse with user_id, email, and JWT token

    Raises:
        HTTPException 400: If email is already registered
    """
    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = hash_password(request.password)
    new_user = User(
        email=request.email,
        password_hash=hashed_password,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate access token
    token = create_access_token(user_id=new_user.id, email=new_user.email)

    return SignupResponse(
        user_id=new_user.id,
        email=new_user.email,
        token=token,
    )


@router.post(
    "/signin",
    response_model=SigninResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
def signin(
    request: SigninRequest,
    session: Annotated[Session, Depends(get_session)],
) -> SigninResponse:
    """
    Sign in an existing user.

    Validates credentials and returns an access token.

    Args:
        request: Signin request with email and password
        session: Database session

    Returns:
        SigninResponse with user_id, email, and JWT token

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Update last login timestamp
    user.last_login_at = datetime.utcnow()
    session.add(user)
    session.commit()

    # Generate access token
    token = create_access_token(user_id=user.id, email=user.email)

    return SigninResponse(
        user_id=user.id,
        email=user.email,
        token=token,
    )


@router.post(
    "/signout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
def signout(current_user: CurrentUser) -> None:
    """
    Sign out the current user.

    JWT tokens are stateless, so this endpoint primarily validates the token.
    Client should discard the token after calling this endpoint.

    Args:
        current_user: Currently authenticated user (from JWT token)

    Returns:
        204 No Content on success
    """
    # Token validation happens in CurrentUser dependency
    # Client should discard token after this call
    pass

"""
Authentication request/response schemas.
"""

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for user signup."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=100, description="User password (min 8 chars)")


class SignupResponse(BaseModel):
    """Response schema for successful signup."""

    user_id: int = Field(..., description="Created user ID")
    email: str = Field(..., description="User email address")
    token: str = Field(..., description="JWT access token")


class SigninRequest(BaseModel):
    """Request schema for user signin."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class SigninResponse(BaseModel):
    """Response schema for successful signin."""

    user_id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email address")
    token: str = Field(..., description="JWT access token")

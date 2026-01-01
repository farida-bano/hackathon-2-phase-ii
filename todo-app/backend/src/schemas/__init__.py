"""
Pydantic schemas for request/response validation.
"""

from src.schemas.auth import SignupRequest, SignupResponse, SigninRequest, SigninResponse
from src.schemas.error import ErrorResponse
from src.schemas.todo import (
    TodoResponse,
    TodoListResponse,
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoToggleResponse,
)

__all__ = [
    "SignupRequest",
    "SignupResponse",
    "SigninRequest",
    "SigninResponse",
    "ErrorResponse",
    "TodoResponse",
    "TodoListResponse",
    "TodoCreateRequest",
    "TodoUpdateRequest",
    "TodoToggleResponse",
]

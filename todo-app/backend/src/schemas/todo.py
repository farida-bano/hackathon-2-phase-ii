"""
Todo request/response schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoResponse(BaseModel):
    """Response schema for a single todo item."""

    id: int = Field(..., description="Todo ID")
    description: str = Field(..., description="Todo description")
    completed: bool = Field(..., description="Completion status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class TodoListResponse(BaseModel):
    """Response schema for list of todos."""

    todos: list[TodoResponse] = Field(..., description="List of todo items")
    total: int = Field(..., description="Total number of todos")


class TodoCreateRequest(BaseModel):
    """Request schema for creating a new todo."""

    description: str = Field(..., min_length=1, max_length=500, description="Todo description")


class TodoUpdateRequest(BaseModel):
    """Request schema for updating a todo."""

    description: Optional[str] = Field(
        None, min_length=1, max_length=500, description="Updated description"
    )
    completed: Optional[bool] = Field(None, description="Updated completion status")


class TodoToggleResponse(BaseModel):
    """Response schema for toggling todo completion."""

    id: int = Field(..., description="Todo ID")
    completed: bool = Field(..., description="New completion status")

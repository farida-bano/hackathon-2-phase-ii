"""
Todo model for task management.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    """
    Todo entity for task tracking.

    Attributes:
        id: Primary key, auto-incremented
        user_id: Foreign key to users table (CASCADE delete)
        description: Task description (max 500 chars)
        completed: Completion status (default False)
        created_at: Todo creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True, ondelete="CASCADE")
    description: str = Field(max_length=500, nullable=False)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)

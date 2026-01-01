"""
User model for authentication and authorization.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User entity for authentication.

    Attributes:
        id: Primary key, auto-incremented
        email: Unique email address for login
        password_hash: Bcrypt hashed password
        created_at: Account creation timestamp
        last_login_at: Last successful login timestamp
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    last_login_at: Optional[datetime] = Field(default=None, nullable=True)

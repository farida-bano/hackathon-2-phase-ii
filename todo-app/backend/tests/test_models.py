"""
Unit tests for database models.
"""

from datetime import datetime

import pytest
from sqlmodel import Session, select

from src.models import Todo, User


def test_user_model_creation(session: Session):
    """Test creating a user model instance."""
    user = User(
        email="test@example.com",
        password_hash="hashed_password_here",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_password_here"
    assert isinstance(user.created_at, datetime)
    assert user.last_login_at is None


def test_user_email_unique_constraint(session: Session):
    """Test that user email must be unique."""
    user1 = User(email="test@example.com", password_hash="hash1")
    session.add(user1)
    session.commit()

    user2 = User(email="test@example.com", password_hash="hash2")
    session.add(user2)

    with pytest.raises(Exception):  # IntegrityError from database
        session.commit()


def test_todo_model_creation(session: Session):
    """Test creating a todo model instance."""
    # First create a user (foreign key requirement)
    user = User(email="test@example.com", password_hash="hash")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create todo
    todo = Todo(
        user_id=user.id,
        description="Test todo item",
        completed=False,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    assert todo.id is not None
    assert todo.user_id == user.id
    assert todo.description == "Test todo item"
    assert todo.completed is False
    assert isinstance(todo.created_at, datetime)
    assert todo.updated_at is None


def test_todo_cascade_delete(session: Session):
    """Test that deleting a user cascades to their todos."""
    # Create user with todos
    user = User(email="test@example.com", password_hash="hash")
    session.add(user)
    session.commit()
    session.refresh(user)

    todo1 = Todo(user_id=user.id, description="Todo 1")
    todo2 = Todo(user_id=user.id, description="Todo 2")
    session.add(todo1)
    session.add(todo2)
    session.commit()

    # Verify todos exist
    todos = session.exec(select(Todo).where(Todo.user_id == user.id)).all()
    assert len(todos) == 2

    # Delete user
    session.delete(user)
    session.commit()

    # Verify todos were cascaded deleted
    todos = session.exec(select(Todo).where(Todo.user_id == user.id)).all()
    assert len(todos) == 0


def test_todo_description_max_length():
    """Test that todo description has max length constraint."""
    long_description = "x" * 501  # Exceeds 500 char limit

    # Model validation should catch this
    with pytest.raises(Exception):  # Validation error
        Todo(user_id=1, description=long_description)


def test_user_update_last_login(session: Session):
    """Test updating user's last login timestamp."""
    user = User(email="test@example.com", password_hash="hash")
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.last_login_at is None

    # Update last login
    user.last_login_at = datetime.utcnow()
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.last_login_at is not None
    assert isinstance(user.last_login_at, datetime)


def test_todo_toggle_completion(session: Session):
    """Test toggling todo completion status."""
    user = User(email="test@example.com", password_hash="hash")
    session.add(user)
    session.commit()
    session.refresh(user)

    todo = Todo(user_id=user.id, description="Test", completed=False)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    assert todo.completed is False

    # Toggle completion
    todo.completed = True
    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)

    assert todo.completed is True
    assert todo.updated_at is not None

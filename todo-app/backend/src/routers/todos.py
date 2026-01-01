"""
Todo CRUD endpoints: create, read, update, delete, toggle.
"""

from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from src.auth.dependencies import CurrentUser
from src.database import get_session
from src.models.todo import Todo
from src.schemas.error import ErrorResponse
from src.schemas.todo import (
    TodoCreateRequest,
    TodoListResponse,
    TodoResponse,
    TodoToggleResponse,
    TodoUpdateRequest,
)

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get(
    "",
    response_model=TodoListResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
def get_todos(
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
) -> TodoListResponse:
    """
    Get all todos for the authenticated user.

    Supports optional filtering by completion status.

    Args:
        current_user: Currently authenticated user
        session: Database session
        completed: Optional filter - True for completed, False for incomplete, None for all

    Returns:
        TodoListResponse with list of todos and total count
    """
    # Build query for user's todos
    statement = select(Todo).where(Todo.user_id == current_user.id)

    # Apply completion filter if provided
    if completed is not None:
        statement = statement.where(Todo.completed == completed)

    # Order by created_at descending (newest first)
    statement = statement.order_by(Todo.created_at.desc())

    # Execute query
    todos = session.exec(statement).all()

    # Convert to response schema
    todo_responses = [
        TodoResponse(
            id=todo.id,
            description=todo.description,
            completed=todo.completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
        for todo in todos
    ]

    return TodoListResponse(todos=todo_responses, total=len(todo_responses))


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
    },
)
def create_todo(
    request: TodoCreateRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> TodoResponse:
    """
    Create a new todo for the authenticated user.

    Args:
        request: Todo creation request with description
        current_user: Currently authenticated user
        session: Database session

    Returns:
        TodoResponse with created todo details
    """
    # Create new todo
    new_todo = Todo(
        user_id=current_user.id,
        description=request.description,
        completed=False,
    )

    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)

    return TodoResponse(
        id=new_todo.id,
        description=new_todo.description,
        completed=new_todo.completed,
        created_at=new_todo.created_at,
        updated_at=new_todo.updated_at,
    )


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Access denied to this todo"},
        404: {"model": ErrorResponse, "description": "Todo not found"},
    },
)
def update_todo(
    todo_id: int,
    request: TodoUpdateRequest,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> TodoResponse:
    """
    Update a todo's description and/or completion status.

    User can only update their own todos.

    Args:
        todo_id: ID of todo to update
        request: Update request with optional description and completed fields
        current_user: Currently authenticated user
        session: Database session

    Returns:
        TodoResponse with updated todo details

    Raises:
        HTTPException 404: If todo not found
        HTTPException 403: If todo belongs to another user
    """
    # Fetch todo
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    # Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this todo",
        )

    # Update fields if provided
    if request.description is not None:
        todo.description = request.description

    if request.completed is not None:
        todo.completed = request.completed

    # Update timestamp
    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return TodoResponse(
        id=todo.id,
        description=todo.description,
        completed=todo.completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )


@router.post(
    "/{todo_id}/toggle",
    response_model=TodoToggleResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Access denied to this todo"},
        404: {"model": ErrorResponse, "description": "Todo not found"},
    },
)
def toggle_todo(
    todo_id: int,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> TodoToggleResponse:
    """
    Toggle a todo's completion status.

    User can only toggle their own todos.

    Args:
        todo_id: ID of todo to toggle
        current_user: Currently authenticated user
        session: Database session

    Returns:
        TodoToggleResponse with new completion status

    Raises:
        HTTPException 404: If todo not found
        HTTPException 403: If todo belongs to another user
    """
    # Fetch todo
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    # Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this todo",
        )

    # Toggle completion
    todo.completed = not todo.completed
    todo.updated_at = datetime.utcnow()

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return TodoToggleResponse(id=todo.id, completed=todo.completed)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Access denied to this todo"},
        404: {"model": ErrorResponse, "description": "Todo not found"},
    },
)
def delete_todo(
    todo_id: int,
    current_user: CurrentUser,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    """
    Delete a todo.

    User can only delete their own todos.

    Args:
        todo_id: ID of todo to delete
        current_user: Currently authenticated user
        session: Database session

    Returns:
        204 No Content on success

    Raises:
        HTTPException 404: If todo not found
        HTTPException 403: If todo belongs to another user
    """
    # Fetch todo
    todo = session.get(Todo, todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    # Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this todo",
        )

    # Delete todo
    session.delete(todo)
    session.commit()

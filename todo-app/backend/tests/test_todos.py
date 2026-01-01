"""
Integration tests for todo CRUD endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.models.todo import Todo


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(client: TestClient) -> dict:
    """
    Create a user and return authentication headers.
    """
    response = client.post(
        "/auth/signup",
        json={"email": "todouser@example.com", "password": "password123"},
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="second_user_headers")
def second_user_headers_fixture(client: TestClient) -> dict:
    """
    Create a second user and return authentication headers.
    """
    response = client.post(
        "/auth/signup",
        json={"email": "seconduser@example.com", "password": "password123"},
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_todos_empty_list(client: TestClient, auth_headers: dict):
    """Test getting todos when user has no todos."""
    response = client.get("/todos", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["todos"] == []
    assert data["total"] == 0


def test_get_todos_unauthorized(client: TestClient):
    """Test getting todos without authentication."""
    response = client.get("/todos")

    assert response.status_code == 403  # No token provided


def test_create_todo_success(client: TestClient, auth_headers: dict, session: Session):
    """Test creating a new todo."""
    response = client.post(
        "/todos",
        headers=auth_headers,
        json={"description": "Buy groceries"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Buy groceries"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data

    # Verify in database
    todo = session.get(Todo, data["id"])
    assert todo is not None
    assert todo.description == "Buy groceries"


def test_create_todo_empty_description(client: TestClient, auth_headers: dict):
    """Test creating todo with empty description."""
    response = client.post(
        "/todos",
        headers=auth_headers,
        json={"description": ""},
    )

    assert response.status_code == 422  # Validation error


def test_create_todo_description_too_long(client: TestClient, auth_headers: dict):
    """Test creating todo with description exceeding 500 characters."""
    long_description = "x" * 501

    response = client.post(
        "/todos",
        headers=auth_headers,
        json={"description": long_description},
    )

    assert response.status_code == 422  # Validation error


def test_get_todos_with_items(client: TestClient, auth_headers: dict):
    """Test getting todos when user has multiple todos."""
    # Create todos
    client.post("/todos", headers=auth_headers, json={"description": "Todo 1"})
    client.post("/todos", headers=auth_headers, json={"description": "Todo 2"})
    client.post("/todos", headers=auth_headers, json={"description": "Todo 3"})

    response = client.get("/todos", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data["todos"]) == 3
    assert data["total"] == 3

    # Verify ordering (newest first)
    descriptions = [todo["description"] for todo in data["todos"]]
    assert descriptions == ["Todo 3", "Todo 2", "Todo 1"]


def test_get_todos_filter_completed(client: TestClient, auth_headers: dict):
    """Test filtering todos by completion status."""
    # Create todos
    todo1 = client.post("/todos", headers=auth_headers, json={"description": "Todo 1"}).json()
    todo2 = client.post("/todos", headers=auth_headers, json={"description": "Todo 2"}).json()
    client.post("/todos", headers=auth_headers, json={"description": "Todo 3"})

    # Mark todo1 as completed
    client.post(f"/todos/{todo1['id']}/toggle", headers=auth_headers)

    # Get only completed todos
    response = client.get("/todos?completed=true", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["todos"]) == 1
    assert data["todos"][0]["id"] == todo1["id"]
    assert data["todos"][0]["completed"] is True

    # Get only incomplete todos
    response = client.get("/todos?completed=false", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["todos"]) == 2
    assert all(not todo["completed"] for todo in data["todos"])


def test_user_isolation(client: TestClient, auth_headers: dict, second_user_headers: dict):
    """Test that users can only see their own todos."""
    # User 1 creates todos
    client.post("/todos", headers=auth_headers, json={"description": "User 1 Todo"})

    # User 2 creates todos
    client.post("/todos", headers=second_user_headers, json={"description": "User 2 Todo"})

    # User 1 should only see their todo
    response1 = client.get("/todos", headers=auth_headers)
    data1 = response1.json()
    assert len(data1["todos"]) == 1
    assert data1["todos"][0]["description"] == "User 1 Todo"

    # User 2 should only see their todo
    response2 = client.get("/todos", headers=second_user_headers)
    data2 = response2.json()
    assert len(data2["todos"]) == 1
    assert data2["todos"][0]["description"] == "User 2 Todo"


def test_update_todo_description(client: TestClient, auth_headers: dict):
    """Test updating a todo's description."""
    # Create todo
    todo = client.post("/todos", headers=auth_headers, json={"description": "Original"}).json()

    # Update description
    response = client.put(
        f"/todos/{todo['id']}",
        headers=auth_headers,
        json={"description": "Updated description"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"
    assert data["completed"] is False
    assert data["updated_at"] is not None


def test_update_todo_completion(client: TestClient, auth_headers: dict):
    """Test updating a todo's completion status."""
    # Create todo
    todo = client.post("/todos", headers=auth_headers, json={"description": "Test"}).json()

    # Mark as completed
    response = client.put(
        f"/todos/{todo['id']}",
        headers=auth_headers,
        json={"completed": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["description"] == "Test"  # Description unchanged


def test_update_todo_not_found(client: TestClient, auth_headers: dict):
    """Test updating a non-existent todo."""
    response = client.put(
        "/todos/99999",
        headers=auth_headers,
        json={"description": "Updated"},
    )

    assert response.status_code == 404


def test_update_todo_access_denied(client: TestClient, auth_headers: dict, second_user_headers: dict):
    """Test that users cannot update other users' todos."""
    # User 1 creates todo
    todo = client.post("/todos", headers=auth_headers, json={"description": "User 1 Todo"}).json()

    # User 2 tries to update User 1's todo
    response = client.put(
        f"/todos/{todo['id']}",
        headers=second_user_headers,
        json={"description": "Hacked"},
    )

    assert response.status_code == 403


def test_toggle_todo_completion(client: TestClient, auth_headers: dict):
    """Test toggling a todo's completion status."""
    # Create todo (initially incomplete)
    todo = client.post("/todos", headers=auth_headers, json={"description": "Test"}).json()
    assert todo["completed"] is False

    # Toggle to completed
    response = client.post(f"/todos/{todo['id']}/toggle", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True

    # Toggle back to incomplete
    response = client.post(f"/todos/{todo['id']}/toggle", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


def test_toggle_todo_not_found(client: TestClient, auth_headers: dict):
    """Test toggling a non-existent todo."""
    response = client.post("/todos/99999/toggle", headers=auth_headers)

    assert response.status_code == 404


def test_toggle_todo_access_denied(client: TestClient, auth_headers: dict, second_user_headers: dict):
    """Test that users cannot toggle other users' todos."""
    # User 1 creates todo
    todo = client.post("/todos", headers=auth_headers, json={"description": "User 1 Todo"}).json()

    # User 2 tries to toggle User 1's todo
    response = client.post(f"/todos/{todo['id']}/toggle", headers=second_user_headers)

    assert response.status_code == 403


def test_delete_todo_success(client: TestClient, auth_headers: dict, session: Session):
    """Test deleting a todo."""
    # Create todo
    todo = client.post("/todos", headers=auth_headers, json={"description": "To delete"}).json()

    # Delete todo
    response = client.delete(f"/todos/{todo['id']}", headers=auth_headers)

    assert response.status_code == 204

    # Verify deleted from database
    deleted_todo = session.get(Todo, todo["id"])
    assert deleted_todo is None


def test_delete_todo_not_found(client: TestClient, auth_headers: dict):
    """Test deleting a non-existent todo."""
    response = client.delete("/todos/99999", headers=auth_headers)

    assert response.status_code == 404


def test_delete_todo_access_denied(client: TestClient, auth_headers: dict, second_user_headers: dict):
    """Test that users cannot delete other users' todos."""
    # User 1 creates todo
    todo = client.post("/todos", headers=auth_headers, json={"description": "User 1 Todo"}).json()

    # User 2 tries to delete User 1's todo
    response = client.delete(f"/todos/{todo['id']}", headers=second_user_headers)

    assert response.status_code == 403


def test_complete_workflow(client: TestClient, auth_headers: dict):
    """Test complete CRUD workflow."""
    # 1. Start with empty list
    response = client.get("/todos", headers=auth_headers)
    assert response.json()["total"] == 0

    # 2. Create multiple todos
    todo1 = client.post("/todos", headers=auth_headers, json={"description": "Task 1"}).json()
    todo2 = client.post("/todos", headers=auth_headers, json={"description": "Task 2"}).json()
    todo3 = client.post("/todos", headers=auth_headers, json={"description": "Task 3"}).json()

    # 3. List all todos
    response = client.get("/todos", headers=auth_headers)
    assert response.json()["total"] == 3

    # 4. Toggle completion
    client.post(f"/todos/{todo1['id']}/toggle", headers=auth_headers)
    client.post(f"/todos/{todo2['id']}/toggle", headers=auth_headers)

    # 5. Filter by completed
    response = client.get("/todos?completed=true", headers=auth_headers)
    assert response.json()["total"] == 2

    # 6. Update description
    client.put(f"/todos/{todo3['id']}", headers=auth_headers, json={"description": "Updated Task 3"})

    # 7. Delete one todo
    client.delete(f"/todos/{todo1['id']}", headers=auth_headers)

    # 8. Final list
    response = client.get("/todos", headers=auth_headers)
    assert response.json()["total"] == 2

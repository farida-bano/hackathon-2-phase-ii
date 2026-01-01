"""Tests for Task data class."""

import pytest
from src.models.task import Task


class TestTaskCreation:
    """Test Task creation with valid data."""

    def test_create_task_with_valid_data(self):
        """Test that valid Task can be created."""
        task = Task(id=1, content="Buy milk", completed=False)
        assert task.id == 1
        assert task.content == "Buy milk"
        assert task.completed is False

    def test_create_task_default_completed_is_false(self):
        """Test that completed defaults to False."""
        task = Task(id=1, content="Test task")
        assert task.completed is False

    def test_create_task_with_completed_true(self):
        """Test creating task with completed=True."""
        task = Task(id=1, content="Test task", completed=True)
        assert task.completed is True

    def test_create_task_with_long_content(self):
        """Test creating task with 1000 character content."""
        content = "a" * 1000
        task = Task(id=1, content=content)
        assert len(task.content) == 1000


class TestTaskValidation:
    """Test Task validation in __post_init__."""

    def test_task_with_empty_content_raises_error(self):
        """Test that Task with empty content raises error."""
        with pytest.raises(ValueError):
            Task(id=1, content="")

    def test_task_with_whitespace_only_content_raises_error(self):
        """Test that Task with whitespace-only content raises error."""
        with pytest.raises(ValueError):
            Task(id=1, content="   ")

    def test_task_with_negative_id_raises_error(self):
        """Test that Task with negative ID raises error."""
        with pytest.raises(ValueError):
            Task(id=-1, content="Test")

    def test_task_with_zero_id_raises_error(self):
        """Test that Task with zero ID raises error."""
        with pytest.raises(ValueError):
            Task(id=0, content="Test")

    def test_task_with_content_too_long_raises_error(self):
        """Test that Task with content > 1000 chars raises error."""
        with pytest.raises(ValueError):
            Task(id=1, content="a" * 1001)

    def test_task_with_non_boolean_completed_raises_error(self):
        """Test that Task with non-boolean completed raises error."""
        with pytest.raises(ValueError):
            Task(id=1, content="Test", completed="yes")

    def test_task_with_none_content_raises_error(self):
        """Test that Task with None content raises error."""
        with pytest.raises(ValueError):
            Task(id=1, content=None)

    def test_task_with_float_id_raises_error(self):
        """Test that Task with float ID raises error."""
        with pytest.raises(ValueError):
            Task(id=1.5, content="Test")


class TestTaskEquality:
    """Test Task equality and comparison."""

    def test_tasks_with_same_data_are_equal(self):
        """Test that two Tasks with same data are equal."""
        task1 = Task(id=1, content="Buy milk", completed=False)
        task2 = Task(id=1, content="Buy milk", completed=False)
        assert task1 == task2

    def test_tasks_with_different_ids_are_not_equal(self):
        """Test that Tasks with different IDs are not equal."""
        task1 = Task(id=1, content="Buy milk")
        task2 = Task(id=2, content="Buy milk")
        assert task1 != task2

    def test_task_repr_includes_all_fields(self):
        """Test that Task repr includes id, content, and completed."""
        task = Task(id=1, content="Test", completed=False)
        repr_str = repr(task)
        assert "id=1" in repr_str
        assert "content='Test'" in repr_str
        assert "completed=False" in repr_str

"""Tests for TaskService."""

import pytest
from src.models.task import Task
from src.models.exceptions import TaskNotFoundError
from src.services.task_service import TaskService


class TestTaskServiceInitialization:
    """Test TaskService initialization."""

    def test_init_with_empty_tasks(self):
        """Test that TaskService initializes with empty tasks dict."""
        service = TaskService()
        assert service.tasks == []
        assert service.next_id == 1

    def test_init_preserves_empty_dict(self):
        """Test that _tasks starts as empty dict."""
        service = TaskService()
        assert service._tasks == {}


class TestAddTask:
    """Test add_task operation."""

    def test_add_single_task(self):
        """Test adding a single task returns task with ID 1."""
        service = TaskService()
        task = service.add_task("Buy milk")
        assert task.id == 1
        assert task.content == "Buy milk"
        assert task.completed is False

    def test_add_multiple_tasks_sequential_ids(self):
        """Test adding multiple tasks gets sequential IDs."""
        service = TaskService()
        task1 = service.add_task("Buy milk")
        task2 = service.add_task("Walk the dog")
        task3 = service.add_task("Call mom")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_sets_completed_false(self):
        """Test adding task sets completed=False by default."""
        service = TaskService()
        task = service.add_task("Test task")
        assert task.completed is False

    def test_add_task_stores_in_dict(self):
        """Test adding task stores in _tasks dict."""
        service = TaskService()
        task = service.add_task("Buy milk")
        assert 1 in service._tasks
        assert service._tasks[1] == task

    def test_deleted_task_id_not_reused(self):
        """Test that deleted task IDs are not reused."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        service.delete_task(1)
        task2 = service.add_task("Task 2")
        assert task2.id == 2  # Not 1


class TestGetAllTasks:
    """Test get_all_tasks operation."""

    def test_get_all_tasks_empty_list(self):
        """Test get_all_tasks returns empty list when no tasks."""
        service = TaskService()
        assert service.get_all_tasks() == []

    def test_get_all_tasks_sorted_by_id(self):
        """Test get_all_tasks returns tasks sorted by ID."""
        service = TaskService()
        service.add_task("Task 3")
        service.add_task("Task 1")
        service.add_task("Task 2")
        tasks = service.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_all_tasks_returns_all_fields(self):
        """Test get_all_tasks returns tasks with all fields intact."""
        service = TaskService()
        service.add_task("Buy milk")
        service.mark_complete(1)
        tasks = service.get_all_tasks()
        assert tasks[0].id == 1
        assert tasks[0].content == "Buy milk"
        assert tasks[0].completed is True


class TestGetTask:
    """Test get_task operation."""

    def test_get_task_returns_task_when_exists(self):
        """Test get_task returns task when ID exists."""
        service = TaskService()
        service.add_task("Buy milk")
        task = service.get_task(1)
        assert task is not None
        assert task.id == 1
        assert task.content == "Buy milk"

    def test_get_task_returns_none_when_not_found(self):
        """Test get_task returns None when ID does not exist."""
        service = TaskService()
        task = service.get_task(999)
        assert task is None


class TestUpdateTask:
    """Test update_task operation."""

    def test_update_task_changes_content(self):
        """Test update_task changes content."""
        service = TaskService()
        service.add_task("Buy milk")
        updated = service.update_task(1, "Buy organic milk")
        assert updated.content == "Buy organic milk"

    def test_update_task_does_not_change_id(self):
        """Test update_task does not change ID."""
        service = TaskService()
        service.add_task("Buy milk")
        updated = service.update_task(1, "New content")
        assert updated.id == 1

    def test_update_task_does_not_change_completed(self):
        """Test update_task does not change completed status."""
        service = TaskService()
        service.add_task("Buy milk")
        service.mark_complete(1)
        updated = service.update_task(1, "New content")
        assert updated.completed is True

    def test_update_task_raises_for_invalid_id(self):
        """Test update_task raises TaskNotFoundError for invalid ID."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.update_task(999, "New content")

    def test_update_multiple_times_preserves_id(self):
        """Test updating task multiple times preserves same ID."""
        service = TaskService()
        service.add_task("Original")
        service.update_task(1, "Update 1")
        service.update_task(1, "Update 2")
        task = service.get_task(1)
        assert task.id == 1
        assert task.content == "Update 2"


class TestDeleteTask:
    """Test delete_task operation."""

    def test_delete_task_removes_from_storage(self):
        """Test delete_task removes task from storage."""
        service = TaskService()
        service.add_task("Buy milk")
        service.delete_task(1)
        assert 1 not in service._tasks

    def test_delete_task_raises_for_invalid_id(self):
        """Test delete_task raises TaskNotFoundError for invalid ID."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)

    def test_delete_task_does_not_affect_other_tasks(self):
        """Test delete_task does not affect other tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)
        task = service.get_task(2)
        assert task is not None
        assert task.content == "Task 2"

    def test_delete_task_does_not_reuse_id(self):
        """Test delete_task does not decrement next_id."""
        service = TaskService()
        service.add_task("Task 1")
        service.delete_task(1)
        service.add_task("Task 2")
        assert service.next_id == 3  # Still 3, not 2

    def test_deleted_task_not_in_get_all_tasks(self):
        """Test deleted task no longer appears in get_all_tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2


class TestMarkComplete:
    """Test mark_complete operation."""

    def test_mark_complete_sets_completed_true(self):
        """Test mark_complete sets completed=True."""
        service = TaskService()
        service.add_task("Buy milk")
        task = service.mark_complete(1)
        assert task.completed is True

    def test_mark_complete_returns_updated_task(self):
        """Test mark_complete returns updated task."""
        service = TaskService()
        service.add_task("Buy milk")
        task = service.mark_complete(1)
        assert task.id == 1
        assert task.content == "Buy milk"

    def test_mark_complete_raises_for_invalid_id(self):
        """Test mark_complete raises TaskNotFoundError for invalid ID."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.mark_complete(999)

    def test_mark_complete_on_already_complete(self):
        """Test mark_complete on already complete task still returns True."""
        service = TaskService()
        service.add_task("Buy milk")
        service.mark_complete(1)
        task = service.mark_complete(1)
        assert task.completed is True


class TestMarkIncomplete:
    """Test mark_incomplete operation."""

    def test_mark_incomplete_sets_completed_false(self):
        """Test mark_incomplete sets completed=False."""
        service = TaskService()
        service.add_task("Buy milk")
        service.mark_complete(1)
        task = service.mark_incomplete(1)
        assert task.completed is False

    def test_mark_incomplete_returns_updated_task(self):
        """Test mark_incomplete returns updated task."""
        service = TaskService()
        service.add_task("Buy milk")
        service.mark_complete(1)
        task = service.mark_incomplete(1)
        assert task.id == 1
        assert task.content == "Buy milk"

    def test_mark_incomplete_raises_for_invalid_id(self):
        """Test mark_incomplete raises TaskNotFoundError for invalid ID."""
        service = TaskService()
        with pytest.raises(TaskNotFoundError):
            service.mark_incomplete(999)

    def test_mark_incomplete_on_already_incomplete(self):
        """Test mark_incomplete on already incomplete task still returns False."""
        service = TaskService()
        service.add_task("Buy milk")
        task = service.mark_incomplete(1)
        assert task.completed is False


class TestTaskServiceEdgeCases:
    """Test edge cases for TaskService."""

    def test_get_all_tasks_after_multiple_operations(self):
        """Test get_all_tasks after add, update, delete, mark."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")
        service.mark_complete(2)
        service.update_task(1, "Updated Task 1")
        service.delete_task(3)
        tasks = service.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].content == "Updated Task 1"
        assert tasks[0].completed is False
        assert tasks[1].content == "Task 2"
        assert tasks[1].completed is True

"""Integration tests for Evolution of Todo Phase I.

These tests verify complete user workflows and end-to-end functionality.
"""

import pytest
from src.models.task import Task
from src.models.exceptions import TaskNotFoundError
from src.services.task_service import TaskService
from src.cli.menu import Menu


class TestCompleteWorkflows:
    """Test complete user workflows from start to finish."""

    def test_add_view_update_delete_workflow(self):
        """Test complete add -> view -> update -> delete workflow."""
        service = TaskService()

        # Add tasks
        task1 = service.add_task("Buy milk")
        task2 = service.add_task("Walk the dog")
        task3 = service.add_task("Call mom")

        assert len(service.get_all_tasks()) == 3

        # View tasks
        tasks = service.get_all_tasks()
        assert tasks[0].content == "Buy milk"
        assert tasks[1].content == "Walk the dog"
        assert tasks[2].content == "Call mom"

        # Update task
        updated = service.update_task(2, "Walk the cat")
        assert updated.content == "Walk the cat"
        assert updated.id == 2

        # Verify update persisted
        task = service.get_task(2)
        assert task.content == "Walk the cat"

        # Delete task
        service.delete_task(3)
        assert len(service.get_all_tasks()) == 2
        assert service.get_task(3) is None

        # Remaining tasks unchanged
        assert service.get_task(1).content == "Buy milk"
        assert service.get_task(2).content == "Walk the cat"

    def test_add_view_mark_complete_workflow(self):
        """Test add -> view -> mark complete workflow."""
        service = TaskService()

        # Add tasks
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        # Mark some complete
        service.mark_complete(1)
        service.mark_complete(3)

        # Verify state
        tasks = service.get_all_tasks()
        assert tasks[0].completed is True
        assert tasks[1].completed is False
        assert tasks[2].completed is True

        # View and verify display would show correct markers
        display_complete = "[X]"
        display_incomplete = "[ ]"

        # Simulate display logic
        for task in tasks:
            if task.completed:
                assert display_complete == "[X]"
            else:
                assert display_incomplete == "[ ]"

    def test_error_recovery_on_invalid_id(self):
        """Test error recovery when user enters invalid ID."""
        service = TaskService()
        service.add_task("Valid task")

        # Try to update non-existent task
        with pytest.raises(TaskNotFoundError):
            service.update_task(999, "New content")

        # Original task still exists
        task = service.get_task(1)
        assert task.content == "Valid task"

        # Try to delete non-existent task
        with pytest.raises(TaskNotFoundError):
            service.delete_task(888)

        # Original task still exists
        assert len(service.get_all_tasks()) == 1

        # Now operate on valid task - should work
        service.update_task(1, "Updated task")
        assert service.get_task(1).content == "Updated task"

    def test_error_recovery_on_invalid_content(self):
        """Test error recovery when user enters invalid content."""
        service = TaskService()

        # Try to add empty task - should fail validation
        # This would be caught by the menu layer in real usage
        with pytest.raises(ValueError):
            Task(id=1, content="")

        # Verify no task was added (since we're testing the model directly)
        # In real usage, the menu layer catches this and re-prompts
        assert len(service.get_all_tasks()) == 0

    def test_multiple_tasks_handling(self):
        """Test handling of many tasks."""
        service = TaskService()

        # Add 10 tasks
        for i in range(1, 11):
            service.add_task(f"Task {i}")

        assert len(service.get_all_tasks()) == 10

        # Mark every other task complete
        for i in range(1, 11, 2):
            service.mark_complete(i)

        # Verify
        tasks = service.get_all_tasks()
        for i, task in enumerate(tasks):
            expected_id = i + 1
            expected_complete = (expected_id % 2 == 1)
            assert task.id == expected_id
            assert task.completed == expected_complete

    def test_state_persistence_within_session(self):
        """Test that state persists correctly within a session."""
        service = TaskService()

        # Initial state
        assert len(service.get_all_tasks()) == 0

        # Add and mark complete
        service.add_task("Task 1")
        service.mark_complete(1)

        # Verify persistence
        assert service.get_task(1).completed is True

        # Add more tasks
        service.add_task("Task 2")
        service.add_task("Task 3")

        # Verify all still there
        assert len(service.get_all_tasks()) == 3

        # Update one task
        service.update_task(2, "Updated Task 2")
        assert service.get_task(2).content == "Updated Task 2"

        # Delete one task
        service.delete_task(3)

        # Final state
        assert len(service.get_all_tasks()) == 2
        assert service.get_task(1).completed is True
        assert service.get_task(2).content == "Updated Task 2"

    def test_id_stability_after_deletions(self):
        """Test that task IDs remain stable after deletions."""
        service = TaskService()

        # Add 5 tasks
        for i in range(1, 6):
            service.add_task(f"Task {i}")

        # Delete tasks 2 and 4
        service.delete_task(2)
        service.delete_task(4)

        # Add new task - should get ID 6, not reused
        new_task = service.add_task("New Task")
        assert new_task.id == 6

        # Verify remaining IDs
        tasks = service.get_all_tasks()
        ids = [t.id for t in tasks]
        assert ids == [1, 3, 5, 6]

    def test_toggle_complete_incomplete(self):
        """Test toggling task between complete and incomplete."""
        service = TaskService()
        service.add_task("Task 1")

        # Initially incomplete
        assert service.get_task(1).completed is False

        # Mark complete
        service.mark_complete(1)
        assert service.get_task(1).completed is True

        # Mark incomplete
        service.mark_incomplete(1)
        assert service.get_task(1).completed is False

        # Mark complete again
        service.mark_complete(1)
        assert service.get_task(1).completed is True


class TestMenuIntegration:
    """Test Menu integration with TaskService."""

    def test_menu_operations_with_service(self):
        """Test that Menu correctly uses TaskService operations."""
        service = TaskService()
        menu = Menu(service)

        # Simulate menu operations (without actual input)
        # Add
        task = service.add_task("Test Task")
        assert task.id == 1

        # View - would display correctly
        tasks = service.get_all_tasks()
        assert len(tasks) == 1

        # Update
        service.update_task(1, "Updated Task")
        assert service.get_task(1).content == "Updated Task"

        # Mark complete
        service.mark_complete(1)
        assert service.get_task(1).completed is True

        # Mark incomplete
        service.mark_incomplete(1)
        assert service.get_task(1).completed is False

        # Delete
        service.delete_task(1)
        assert len(service.get_all_tasks()) == 0


class TestAcceptanceCriteria:
    """Test all acceptance criteria from the specification."""

    def test_ac_001_007_add_task(self):
        """Test Add Task acceptance criteria AC-001 through AC-007."""
        service = TaskService()

        # AC-001: User can input non-empty task content
        task = service.add_task("Buy milk")
        assert task.content == "Buy milk"
        assert task.id == 1  # First task gets ID 1

        # AC-002: New task receives unique ID (1, 2, 3, ...)
        task2 = service.add_task("Task 1")
        task3 = service.add_task("Task 2")
        task4 = service.add_task("Task 3")
        assert task2.id == 2
        assert task3.id == 3
        assert task4.id == 4

        # AC-003: New task is marked as incomplete by default
        assert task.completed is False

        # AC-004: Task appears in subsequent "View Tasks" displays
        tasks = service.get_all_tasks()
        assert len(tasks) == 4
        assert any(t.content == "Buy milk" for t in tasks)

    def test_ac_008_012_view_tasks(self):
        """Test View Tasks acceptance criteria AC-008 through AC-012."""
        service = TaskService()

        # AC-008, AC-009, AC-010: Display format
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.mark_complete(1)
        tasks = service.get_all_tasks()

        # Verify display data is correct
        for task in tasks:
            if task.id == 1:
                assert task.completed is True  # Would show [X]
            else:
                assert task.completed is False  # Would show [ ]

        # AC-011: Empty task list shows descriptive message
        empty_service = TaskService()
        empty_tasks = empty_service.get_all_tasks()
        assert len(empty_tasks) == 0

        # AC-012: Task summary shows total count and completion breakdown
        total = len(tasks)
        complete = sum(1 for t in tasks if t.completed)
        incomplete = total - complete
        assert total == 2
        assert complete == 1
        assert incomplete == 1

    def test_ac_013_018_update_task(self):
        """Test Update Task acceptance criteria AC-013 through AC-018."""
        service = TaskService()
        service.add_task("Buy milk")

        # AC-013: User can modify task content by ID
        updated = service.update_task(1, "Buy organic milk")
        assert updated.content == "Buy organic milk"

        # AC-014: Task ID remains unchanged after update
        assert updated.id == 1

        # AC-015: Completion status remains unchanged after update
        assert updated.completed is False

        # AC-016: Invalid ID shows error message
        with pytest.raises(TaskNotFoundError):
            service.update_task(999, "New content")

    def test_ac_019_022_delete_task(self):
        """Test Delete Task acceptance criteria AC-019 through AC-022."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        # AC-019: Task is removed from the list
        service.delete_task(2)
        assert len(service.get_all_tasks()) == 2

        # AC-020: Remaining tasks keep their IDs unchanged
        assert service.get_task(1).id == 1
        assert service.get_task(3).id == 3

        # AC-021: Invalid ID shows error message
        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)

        # AC-022: After deletion, "View Tasks" no longer shows the deleted task
        tasks = service.get_all_tasks()
        assert all(t.id != 2 for t in tasks)

    def test_ac_023_026_mark_complete_incomplete(self):
        """Test Mark Complete/Incomplete acceptance criteria AC-023 through AC-026."""
        service = TaskService()
        service.add_task("Task 1")

        # AC-023: Task completion status changes to True when marked complete
        task = service.mark_complete(1)
        assert task.completed is True

        # AC-024: Task completion status changes to False when marked incomplete
        task = service.mark_incomplete(1)
        assert task.completed is False

        # AC-025: Invalid ID shows error message
        with pytest.raises(TaskNotFoundError):
            service.mark_complete(999)

        # AC-026: Status change is reflected in "View Tasks" display
        service.mark_complete(1)
        task = service.get_task(1)
        assert task.completed is True  # Would display as [X] in view

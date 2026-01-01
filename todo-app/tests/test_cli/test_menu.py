"""Tests for CLI Menu."""

import pytest
from io import StringIO
from unittest.mock import patch

from src.services.task_service import TaskService
from src.cli.menu import Menu


class TestMenuInitialization:
    """Test Menu class initialization."""

    def test_menu_can_be_instantiated(self):
        """Test Menu can be instantiated with TaskService."""
        service = TaskService()
        menu = Menu(service)
        assert menu.service is service


class TestDisplayMenu:
    """Test display_menu method."""

    def test_display_menu_output_format(self):
        """Test display_menu output matches expected format."""
        service = TaskService()
        menu = Menu(service)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            menu.display_menu()
            output = mock_stdout.getvalue()
            assert "EVOLUTION OF TODO" in output
            assert "1. Add Task" in output
            assert "2. View Tasks" in output
            assert "3. Update Task" in output
            assert "4. Delete Task" in output
            assert "5. Mark Task Complete" in output
            assert "6. Mark Task Incomplete" in output
            assert "7. Exit" in output


class TestDisplayTasks:
    """Test display_tasks method."""

    def test_display_tasks_empty_list(self):
        """Test display_tasks with no tasks shows empty message."""
        service = TaskService()
        menu = Menu(service)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            menu.display_tasks()
            output = mock_stdout.getvalue()
            assert "No tasks yet" in output or "TASK LIST" in output

    def test_display_tasks_with_tasks(self):
        """Test display_tasks with tasks shows table format."""
        service = TaskService()
        service.add_task("Buy milk")
        service.add_task("Walk the dog")
        service.mark_complete(2)
        menu = Menu(service)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            menu.display_tasks()
            output = mock_stdout.getvalue()
            assert "Buy milk" in output
            assert "Walk the dog" in output
            assert "[ ]" in output
            assert "[X]" in output

    def test_display_tasks_shows_completed_marker(self):
        """Test display_tasks shows [X] for completed tasks."""
        service = TaskService()
        service.add_task("Task 1")
        service.mark_complete(1)
        menu = Menu(service)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            menu.display_tasks()
            output = mock_stdout.getvalue()
            assert "[X]" in output

    def test_display_tasks_shows_incomplete_marker(self):
        """Test display_tasks shows [ ] for incomplete tasks."""
        service = TaskService()
        service.add_task("Task 1")
        menu = Menu(service)
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            menu.display_tasks()
            output = mock_stdout.getvalue()
            assert "[ ]" in output


class TestGetMenuChoice:
    """Test get_menu_choice method."""

    def test_get_menu_choice_accepts_valid_input(self):
        """Test get_menu_choice accepts valid input 1-7."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", return_value="1"):
            choice = menu.get_menu_choice()
        assert choice == 1

    def test_get_menu_choice_accepts_7(self):
        """Test get_menu_choice accepts 7 (exit)."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", return_value="7"):
            choice = menu.get_menu_choice()
        assert choice == 7

    def test_get_menu_choice_rejects_non_numeric(self):
        """Test get_menu_choice rejects non-numeric input."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", side_effect=["abc", "1"]):
            with patch("sys.stdout", new_callable=StringIO):
                choice = menu.get_menu_choice()
        assert choice == 1

    def test_get_menu_choice_rejects_out_of_range(self):
        """Test get_menu_choice rejects numbers outside 1-7."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", side_effect=["0", "8", "1"]):
            with patch("sys.stdout", new_callable=StringIO):
                choice = menu.get_menu_choice()
        assert choice == 1

    def test_get_menu_choice_strips_whitespace(self):
        """Test get_menu_choice strips leading/trailing whitespace."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", return_value="  3  "):
            choice = menu.get_menu_choice()
        assert choice == 3


class TestGetTaskContent:
    """Test get_task_content method."""

    def test_get_task_content_accepts_valid_input(self):
        """Test get_task_content accepts valid input."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", return_value="Buy milk"):
            content = menu.get_task_content("Enter task content: ")
        assert content == "Buy milk"

    def test_get_task_content_strips_whitespace(self):
        """Test get_task_content strips whitespace."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", return_value="  Buy milk  "):
            content = menu.get_task_content("Enter task content: ")
        assert content == "Buy milk"

    def test_get_task_content_rejects_empty(self):
        """Test get_task_content rejects empty input."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", side_effect=["", "Buy milk"]):
            with patch("sys.stdout", new_callable=StringIO):
                content = menu.get_task_content("Enter task content: ")
        assert content == "Buy milk"

    def test_get_task_content_rejects_whitespace_only(self):
        """Test get_task_content rejects whitespace-only input."""
        service = TaskService()
        menu = Menu(service)
        with patch("builtins.input", side_effect=["   ", "Buy milk"]):
            with patch("sys.stdout", new_callable=StringIO):
                content = menu.get_task_content("Enter task content: ")
        assert content == "Buy milk"


class TestGetTaskId:
    """Test get_task_id method."""

    def test_get_task_id_accepts_valid_existing_id(self):
        """Test get_task_id accepts valid existing ID."""
        service = TaskService()
        service.add_task("Buy milk")
        menu = Menu(service)
        with patch("builtins.input", return_value="1"):
            task_id = menu.get_task_id("Enter task ID: ")
        assert task_id == 1

    def test_get_task_id_rejects_non_numeric(self):
        """Test get_task_id rejects non-numeric input."""
        service = TaskService()
        service.add_task("Buy milk")
        menu = Menu(service)
        with patch("builtins.input", side_effect=["abc", "1"]):
            with patch("sys.stdout", new_callable=StringIO):
                task_id = menu.get_task_id("Enter task ID: ")
        assert task_id == 1

    def test_get_task_id_rejects_negative(self):
        """Test get_task_id rejects negative numbers."""
        service = TaskService()
        service.add_task("Buy milk")
        menu = Menu(service)
        with patch("builtins.input", side_effect=["-1", "1"]):
            with patch("sys.stdout", new_callable=StringIO):
                task_id = menu.get_task_id("Enter task ID: ")
        assert task_id == 1

    def test_get_task_id_rejects_zero(self):
        """Test get_task_id rejects zero."""
        service = TaskService()
        service.add_task("Buy milk")
        menu = Menu(service)
        with patch("builtins.input", side_effect=["0", "1"]):
            with patch("sys.stdout", new_callable=StringIO):
                task_id = menu.get_task_id("Enter task ID: ")
        assert task_id == 1

    def test_get_task_id_rejects_non_existent_id(self):
        """Test get_task_id rejects non-existent ID."""
        service = TaskService()
        service.add_task("Buy milk")
        menu = Menu(service)
        with patch("builtins.input", side_effect=["999", "1"]):
            with patch("sys.stdout", new_callable=StringIO):
                task_id = menu.get_task_id("Enter task ID: ")
        assert task_id == 1

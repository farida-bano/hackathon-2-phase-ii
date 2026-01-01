"""Tests for exception classes."""

import pytest
from src.models.exceptions import (
    TodoError,
    ValidationError,
    EmptyContentError,
    WhitespaceContentError,
    ContentTooLongError,
    InvalidIdError,
    NonNumericInputError,
    TaskNotFoundError,
)


class TestExceptionHierarchy:
    """Test exception class hierarchy."""

    def test_todo_error_is_base_exception(self):
        """Test that TodoError is the base exception."""
        assert issubclass(TodoError, Exception)

    def test_validation_error_inherits_from_todo_error(self):
        """Test that ValidationError inherits from TodoError."""
        assert issubclass(ValidationError, TodoError)

    def test_empty_content_error_inherits_from_validation(self):
        """Test that EmptyContentError inherits from ValidationError."""
        assert issubclass(EmptyContentError, ValidationError)

    def test_whitespace_content_error_inherits_from_validation(self):
        """Test that WhitespaceContentError inherits from ValidationError."""
        assert issubclass(WhitespaceContentError, ValidationError)

    def test_content_too_long_error_inherits_from_validation(self):
        """Test that ContentTooLongError inherits from ValidationError."""
        assert issubclass(ContentTooLongError, ValidationError)

    def test_invalid_id_error_inherits_from_validation(self):
        """Test that InvalidIdError inherits from ValidationError."""
        assert issubclass(InvalidIdError, ValidationError)

    def test_non_numeric_input_error_inherits_from_validation(self):
        """Test that NonNumericInputError inherits from ValidationError."""
        assert issubclass(NonNumericInputError, ValidationError)

    def test_task_not_found_error_inherits_from_todo_error(self):
        """Test that TaskNotFoundError inherits from TodoError."""
        assert issubclass(TaskNotFoundError, TodoError)


class TestExceptionMessages:
    """Test exception messages."""

    def test_empty_content_error_has_message(self):
        """Test EmptyContentError has appropriate message."""
        error = EmptyContentError()
        assert "empty" in str(error).lower()

    def test_whitespace_content_error_has_message(self):
        """Test WhitespaceContentError has appropriate message."""
        error = WhitespaceContentError()
        assert "whitespace" in str(error).lower()

    def test_content_too_long_error_has_message(self):
        """Test ContentTooLongError has appropriate message."""
        error = ContentTooLongError()
        assert "1000" in str(error) or "characters" in str(error).lower()

    def test_task_not_found_error_stores_task_id(self):
        """Test TaskNotFoundError stores the task_id."""
        error = TaskNotFoundError(task_id=42)
        assert error.task_id == 42

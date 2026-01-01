"""Custom exception classes for Evolution of Todo."""


class TodoError(Exception):
    """Base exception for all Todo application errors."""

    pass


class ValidationError(TodoError):
    """Base exception for validation errors."""

    pass


class EmptyContentError(ValidationError):
    """Raised when task content is empty."""

    def __init__(self):
        super().__init__("Task content cannot be empty.")


class WhitespaceContentError(ValidationError):
    """Raised when task content is whitespace only."""

    def __init__(self):
        super().__init__("Task content cannot be empty or whitespace.")


class ContentTooLongError(ValidationError):
    """Raised when task content exceeds 1000 characters."""

    def __init__(self):
        super().__init__("Task content must be 1000 characters or fewer.")


class InvalidIdError(ValidationError):
    """Raised when task ID is invalid (not positive)."""

    def __init__(self):
        super().__init__("Task ID must be a positive number.")


class NonNumericInputError(ValidationError):
    """Raised when input is not a valid number."""

    def __init__(self):
        super().__init__("Please enter a valid number.")


class TaskNotFoundError(TodoError):
    """Raised when a task ID is not found in storage."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found.")

"""Task data class for Evolution of Todo."""

from dataclasses import dataclass


@dataclass
class Task:
    """Domain entity representing a single task.

    Attributes:
        id: Unique positive integer identifier for the task.
        content: The task description (1-1000 characters).
        completed: Whether the task is complete (default False).
    """

    id: int
    content: str
    completed: bool = False

    def __post_init__(self):
        """Validate task after construction."""
        # Validate ID
        if not isinstance(self.id, int):
            raise ValueError("Task ID must be an integer")
        if self.id < 1:
            raise ValueError("Task ID must be a positive integer")

        # Validate content
        if not isinstance(self.content, str):
            raise ValueError("Task content must be a string")
        stripped = self.content.strip()
        if not stripped:
            raise ValueError("Task content cannot be empty")
        if len(stripped) > 1000:
            raise ValueError("Task content must be 1000 characters or fewer")

        # Validate completed
        if not isinstance(self.completed, bool):
            raise ValueError("Task completed status must be a boolean")

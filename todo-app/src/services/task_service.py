"""TaskService for managing todo tasks."""

from typing import Dict, List, Optional

from src.models.task import Task
from src.models.exceptions import TaskNotFoundError


class TaskService:
    """Application service for task business logic.

    Manages in-memory storage of tasks and provides CRUD operations.
    """

    def __init__(self):
        """Initialize TaskService with empty storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    @property
    def tasks(self) -> List[Task]:
        """Return all tasks as a sorted list."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    @property
    def next_id(self) -> int:
        """Return the next available task ID."""
        return self._next_id

    def add_task(self, content: str) -> Task:
        """Create and store a new task.

        Args:
            content: The task description (will be stripped).

        Returns:
            The created Task with assigned ID.
        """
        task = Task(id=self._next_id, content=content.strip())
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks sorted by ID.

        Returns:
            List of all tasks in ID order (empty if no tasks).
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, new_content: str) -> Task:
        """Update a task's content.

        Args:
            task_id: The ID of the task to update.
            new_content: The new task description.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If task_id not found.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        task = self._tasks[task_id]
        task.content = new_content.strip()
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Raises:
            TaskNotFoundError: If task_id not found.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        del self._tasks[task_id]
        # Note: We do NOT decrement _next_id to maintain ID stability

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If task_id not found.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        task = self._tasks[task_id]
        task.completed = True
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If task_id not found.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)
        task = self._tasks[task_id]
        task.completed = False
        return task

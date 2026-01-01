"""CLI Menu for Evolution of Todo."""

from typing import Optional

from src.models.exceptions import (
    EmptyContentError,
    WhitespaceContentError,
    ContentTooLongError,
    NonNumericInputError,
    InvalidIdError,
    TaskNotFoundError,
    TodoError,
)
from src.services.task_service import TaskService


class Menu:
    """Presentation layer for CLI interaction.

    Handles menu display, user input collection, and output formatting.
    """

    def __init__(self, task_service: TaskService):
        """Initialize Menu with TaskService.

        Args:
            task_service: The TaskService instance for business logic.
        """
        self.service = task_service

    # ==================== Display Methods ====================

    def display_menu(self) -> None:
        """Display the main menu."""
        print()
        print("========================================")
        print("         EVOLUTION OF TODO")
        print("========================================")
        print()
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print()
        print("========================================")

    def display_tasks(self) -> None:
        """Format and display all tasks."""
        tasks = self.service.get_all_tasks()
        print()
        print("========================================")
        print("              TASK LIST")
        print("========================================")
        print("ID | Status    | Content")
        print("---+-----------+--------------------------")

        if not tasks:
            print("No tasks yet. Add your first task!")
        else:
            for task in tasks:
                status = "[X]" if task.completed else "[ ]"
                # Truncate content if too long for display
                display_content = task.content
                if len(display_content) > 30:
                    display_content = display_content[:27] + "..."
                print(f"{task.id:<2} | {status:<9} | {display_content}")

        print("========================================")
        # Show summary
        total = len(tasks)
        complete = sum(1 for t in tasks if t.completed)
        incomplete = total - complete
        if total > 0:
            print(f"{total} tasks total ({complete} complete, {incomplete} incomplete)")
        print()

    # ==================== Input Methods ====================

    def get_menu_choice(self) -> int:
        """Get and validate menu choice from user.

        Returns:
            Valid menu choice (1-7).
        """
        while True:
            try:
                choice = input("Enter your choice (1-7): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= 7:
                    return choice_num
                else:
                    print("Invalid choice. Please enter a number 1-7.")
            except ValueError:
                print("Error: Please enter a valid number.")

    def get_task_content(self, prompt: str) -> str:
        """Get and validate task content from user.

        Args:
            prompt: The prompt to display.

        Returns:
            Validated task content (stripped).

        Raises:
            ContentTooLongError: If content exceeds 1000 characters.
        """
        while True:
            content = input(prompt).strip()
            if not content:
                print("Error: Task content cannot be empty.")
                continue
            if content != content.strip():
                print("Error: Task content cannot be empty or whitespace.")
                continue
            if len(content) > 1000:
                print("Error: Task content must be 1000 characters or fewer.")
                continue
            return content

    def get_task_id(self, prompt: str) -> int:
        """Get and validate task ID from user.

        Args:
            prompt: The prompt to display.

        Returns:
            Valid task ID that exists in storage.
        """
        while True:
            task_id_str = input(prompt).strip()
            try:
                task_id = int(task_id_str)
            except ValueError:
                print("Error: Please enter a valid number.")
                continue

            if task_id < 1:
                print("Error: Task ID must be a positive number.")
                continue

            if task_id not in self.service._tasks:
                print(f"Error: Task with ID {task_id} not found.")
                continue

            return task_id

    # ==================== Operation Handlers ====================

    def handle_add_task(self) -> None:
        """Handle add task operation."""
        content = self.get_task_content("Enter task content: ")
        task = self.service.add_task(content)
        print(f"Task added successfully! (ID: {task.id})")

    def handle_update_task(self) -> None:
        """Handle update task operation."""
        self.display_tasks()
        task_id = self.get_task_id("Enter task ID to update: ")
        current_task = self.service.get_task(task_id)
        print(f"Current content: {current_task.content}")
        new_content = self.get_task_content("Enter new content: ")
        self.service.update_task(task_id, new_content)
        print("Task updated successfully!")

    def handle_delete_task(self) -> None:
        """Handle delete task operation."""
        task_id = self.get_task_id("Enter task ID to delete: ")
        self.service.delete_task(task_id)
        print("Task deleted successfully!")

    def handle_mark_complete(self) -> None:
        """Handle mark complete operation."""
        task_id = self.get_task_id("Enter task ID to mark complete: ")
        self.service.mark_complete(task_id)
        print("Task marked as complete!")

    def handle_mark_incomplete(self) -> None:
        """Handle mark incomplete operation."""
        task_id = self.get_task_id("Enter task ID to mark incomplete: ")
        self.service.mark_incomplete(task_id)
        print("Task marked as incomplete!")

    # ==================== Main Loop ====================

    def run(self) -> None:
        """Run the main application loop."""
        while True:
            self.display_menu()
            choice = self.get_menu_choice()

            if choice == 7:
                print("Goodbye!")
                break

            try:
                if choice == 1:
                    self.handle_add_task()
                elif choice == 2:
                    self.display_tasks()
                    input("Press Enter to continue...")
                elif choice == 3:
                    self.handle_update_task()
                elif choice == 4:
                    self.handle_delete_task()
                elif choice == 5:
                    self.handle_mark_complete()
                elif choice == 6:
                    self.handle_mark_incomplete()
            except TodoError as e:
                print(str(e))
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

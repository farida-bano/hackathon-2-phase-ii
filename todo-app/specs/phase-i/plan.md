# Phase I Technical Plan: Evolution of Todo

**Feature Branch**: `phase-i`
**Created**: 2025-12-28
**Status**: Draft
**Specification Reference**: `specs/phase-i/spec.md`
**Constitution Reference**: `.specify/memory/constitution.md`

## Document Metadata

| Field | Value |
|-------|-------|
| **Phase** | I - Foundation |
| **Language** | Python 3.8+ |
| **Interface** | Console (CLI) |
| **Storage** | In-memory |

---

## 1. High-Level Application Structure

### 1.1 Single Python Program Approach

Phase I will be implemented as a single Python module (`main.py`) with the following structure:

```
todo-app-phase-i/
├── main.py              # Application entry point and CLI controller
├── models/
│   └── task.py          # Task data class
├── services/
│   └── task_service.py  # Business logic for task operations
└── cli/
    └── menu.py          # Menu display and user interaction
```

**Rationale**: Phase I is intentionally simple. A single file would suffice, but organizing into packages establishes patterns for future phases while maintaining minimal complexity.

### 1.2 Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│              cli/menu.py                 │  (Presentation Layer)
│    Menu display, input prompts, output  │
├─────────────────────────────────────────┤
│           services/task_service.py      │  (Application Layer)
│      Business logic, validation, CRUD   │
├─────────────────────────────────────────┤
│             models/task.py              │  (Domain Layer)
│           Task data class               │
└─────────────────────────────────────────┘
        │
        ▼
   In-memory dict
   (Infrastructure)
```

**Dependency Rule**: Dependencies point inward. `cli` depends on `services`, `services` depends on `models`. No reverse dependencies.

---

## 2. In-Memory Data Structures

### 2.1 Primary Storage

**Structure**: Dictionary keyed by task ID

```python
tasks: Dict[int, Task] = {}
```

**Example State**:
```python
{
    1: Task(id=1, content="Buy milk", completed=False),
    2: Task(id=2, content="Walk the dog", completed=True),
    3: Task(id=3, content="Call mom", completed=False)
}
```

### 2.2 ID Counter

```python
next_task_id: int = 1
```

**Behavior**:
- Starts at 1
- Increments after each task addition
- Never decrements (deleted IDs are not reused)

### 2.3 Data Structure Justification

| Alternative | Why Not Used |
|-------------|--------------|
| List of Task objects | O(n) lookup for ID-based operations |
| List of dicts | No type safety, harder to validate |
| dict with Task objects | O(1) lookup, clean encapsulation |

**Performance**: Dictionary provides O(1) average-case for all operations, satisfying NFR-001 (100ms response).

---

## 3. Task Identification Strategy

### 3.1 ID Generation Algorithm

```
next_task_id = 1
When adding a task:
    assigned_id = next_task_id
    next_task_id += 1
    return assigned_id
```

### 3.2 ID Properties

| Property | Value |
|----------|-------|
| Starting Value | 1 |
| Increment | 1 per task |
| Uniqueness | Guaranteed within session |
| Reuse After Delete | NO (IDs remain stable) |
| Type | Positive integer |

### 3.3 ID Validation

Before any ID-based operation:
1. Check if input is a valid integer
2. Check if integer is positive (> 0)
3. Check if integer exists in `tasks` dictionary

---

## 4. CLI Control Flow

### 4.1 Main Application Loop

```python
def main():
    task_service = TaskService()
    while True:
        display_menu()
        choice = get_user_choice()
        if choice == 7:
            break
        handle_choice(choice, task_service)
```

### 4.2 Menu Display

```
========================================
         EVOLUTION OF TODO
========================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

========================================
Enter your choice (1-7):
```

### 4.3 Input Handling Flow

```
Get Menu Choice
       │
       ▼
┌──────────────────┐
│ Validate 1-7?    │
└────────┬─────────┘
         │ No
         ▼
Display Error
Return to Menu
         │
         Yes
         ▼
Handle Selection
(Add/View/Update/Delete/Complete/Incomplete/Exit)
```

### 4.4 Input Sanitization

All user input undergoes:
1. Strip whitespace (leading/trailing)
2. Empty string check
3. Length validation (for task content)
4. Type conversion (for numeric inputs)

---

## 5. Separation of Responsibilities

### 5.1 Layer Responsibilities

| Layer | Class | Responsibilities |
|-------|-------|------------------|
| **Domain** | `Task` | Data container with field validation |
| **Application** | `TaskService` | CRUD operations, business rules |
| **Presentation** | `Menu` | Display formatting, input collection |

### 5.2 Task Class (models/task.py)

```python
@dataclass
class Task:
    """Domain entity representing a single task."""
    id: int
    content: str
    completed: bool

    def __post_init__(self):
        """Validate task after construction."""
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")
        if not isinstance(self.content, str):
            raise ValueError("Task content must be a string")
        if len(self.content) == 0 or len(self.content) > 1000:
            raise ValueError("Task content must be 1-1000 characters")
        if not isinstance(self.completed, bool):
            raise ValueError("Task completed status must be boolean")
```

### 5.3 TaskService Class (services/task_service.py)

```python
class TaskService:
    """Application service for task business logic."""

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    # CRUD Operations
    def add_task(self, content: str) -> Task:
        """Create and store a new task."""

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks sorted by ID."""

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID, return None if not found."""

    def update_task(self, task_id: int, new_content: str) -> Task:
        """Update task content, raise if not found."""

    def delete_task(self, task_id: int) -> None:
        """Delete task by ID, raise if not found."""

    def mark_complete(self, task_id: int) -> Task:
        """Mark task as complete."""

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark task as incomplete."""
```

### 5.4 Menu Class (cli/menu.py)

```python
class Menu:
    """Presentation layer for CLI interaction."""

    def __init__(self, task_service: TaskService):
        self.service = task_service

    def run(self) -> None:
        """Main application loop."""

    def display_tasks(self) -> None:
        """Format and display all tasks."""

    def get_task_content(self, prompt: str) -> str:
        """Get validated task content from user."""

    def get_task_id(self, prompt: str) -> int:
        """Get and validate task ID from user."""
```

---

## 6. Error Handling Strategy

### 6.1 Exception Hierarchy

```
TodoError (base exception)
├── ValidationError (invalid input)
│   ├── EmptyContentError
│   ├── WhitespaceContentError
│   ├── ContentTooLongError
│   ├── InvalidIdError
│   └── NonNumericInputError
└── TaskNotFoundError (ID not in storage)
```

### 6.2 Error Handling Flow

```
Operation Request
       │
       ▼
Try Operation
       │
       ├─ Success → Return result to user
       │
       └─ ValidationError → Display error message, retry prompt
       │
       └─ TaskNotFoundError → Display error message, retry prompt
       │
       └─ KeyboardInterrupt → Exit cleanly
       │
       └─ Other Exception → Display "Unexpected error", suggest retry
```

### 6.3 User-Facing Error Messages

| Error Type | Message | Recovery |
|------------|---------|----------|
| Empty Content | "Error: Task content cannot be empty." | Re-prompt for content |
| Whitespace | "Error: Task content cannot be empty or whitespace." | Re-prompt for content |
| Content Too Long | "Error: Task content must be 1000 characters or fewer." | Re-prompt for content |
| Non-Numeric ID | "Error: Please enter a valid number." | Re-prompt for ID |
| Negative ID | "Error: Task ID must be a positive number." | Re-prompt for ID |
| Task Not Found | "Error: Task with ID {id} not found." | Re-prompt for ID or return to menu |
| Invalid Menu Choice | "Invalid choice. Please enter a number 1-7." | Re-prompt for choice |

### 6.4 Input Validation Functions

```python
def validate_content(content: str) -> str:
    """Validate task content meets requirements."""
    stripped = content.strip()
    if not stripped:
        raise EmptyContentError()
    if stripped != content:
        raise WhitespaceContentError()
    if len(stripped) > 1000:
        raise ContentTooLongError()
    return stripped

def validate_task_id(input_str: str, tasks: Dict[int, Task]) -> int:
    """Validate and parse task ID."""
    try:
        task_id = int(input_str)
    except ValueError:
        raise NonNumericInputError()
    if task_id < 1:
        raise InvalidIdError()
    if task_id not in tasks:
        raise TaskNotFoundError(task_id)
    return task_id
```

---

## 7. Output Formatting

### 7.1 Task List Display Format

```
========================================
              TASK LIST
========================================
ID | Status    | Content
---+-----------+--------------------------
1  | [ ]       | Buy milk
2  | [X]       | Walk the dog
3  | [ ]       | Call mom
========================================
3 tasks total (1 complete, 2 incomplete)
```

### 7.2 Success Messages

| Operation | Message |
|-----------|---------|
| Add | "Task added successfully! (ID: {id})" |
| Update | "Task updated successfully!" |
| Delete | "Task deleted successfully!" |
| Mark Complete | "Task marked as complete!" |
| Mark Incomplete | "Task marked as incomplete!" |

### 7.3 Empty State Display

```
========================================
              TASK LIST
========================================
No tasks yet. Add your first task!
========================================
```

---

## 8. Code Organization (File-by-File)

### 8.1 File: `models/task.py`

| Component | Purpose |
|-----------|---------|
| `Task` dataclass | Domain entity with validation |
| Exception classes | Domain-specific errors |

### 8.2 File: `services/task_service.py`

| Component | Purpose |
|-----------|---------|
| `TaskService` class | Business logic container |
| CRUD methods | `add()`, `get_all()`, `get()`, `update()`, `delete()`, `mark_complete()`, `mark_incomplete()` |

### 8.3 File: `cli/menu.py`

| Component | Purpose |
|-----------|---------|
| `Menu` class | Presentation logic |
| `run()` | Main loop |
| Display methods | `display_menu()`, `display_tasks()` |
| Input methods | `get_task_content()`, `get_task_id()`, `get_menu_choice()` |

### 8.4 File: `main.py`

```python
"""Evolution of Todo - Phase I"""

from cli.menu import Menu
from services.task_service import TaskService

def main():
    """Application entry point."""
    service = TaskService()
    menu = Menu(service)
    menu.run()

if __name__ == "__main__":
    main()
```

---

## 9. Dependencies

### 9.1 Python Standard Library Only

| Module | Usage |
|--------|-------|
| `dataclasses` | Task class definition |
| `typing` | Type hints |
| `sys` | Exit handling |

### 9.2 No External Dependencies

Phase I uses ONLY Python standard library. No `pip install` required.

---

## 10. Testing Strategy

### 10.1 Unit Test Coverage

| Component | Tests |
|-----------|-------|
| `Task` validation | Invalid inputs raise correct exceptions |
| `TaskService` CRUD | All operations work correctly |
| `TaskService` edge cases | Empty list, single item, many items |
| `validate_content` | All content validation cases |
| `validate_task_id` | All ID validation cases |
| Menu integration | Full user flows work |

### 10.2 Test Structure

```
tests/
├── test_models/
│   └── test_task.py
├── test_services/
│   └── test_task_service.py
└── test_cli/
    └── test_menu.py
```

---

## 11. Compliance Verification

### 11.1 Constitution Compliance Checklist

- [x] SDD workflow followed: Constitution → Spec → Plan → Tasks → Implement
- [x] No databases (in-memory only)
- [x] No file storage
- [x] No web frameworks
- [x] No external services
- [x] No future phase concepts
- [x] No new features introduced (plan only describes approved spec)
- [x] Clean architecture followed
- [x] Separation of concerns maintained
- [x] Error handling strategy defined

### 11.2 Specification Compliance Checklist

- [x] All 5 user stories addressed
- [x] Task data model matches spec (id, content, completed)
- [x] CLI flow matches spec menu structure
- [x] All acceptance criteria addressed
- [x] All error cases handled
- [x] No advanced features included

---

**Document Version**: 1.0.0
**Status**: Pending Human Approval
**Approval Required**: Before proceeding to Tasks

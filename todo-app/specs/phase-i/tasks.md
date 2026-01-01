# Phase I Implementation Tasks: Evolution of Todo

**Feature Branch**: `phase-i`
**Created**: 2025-12-28
**Status**: Draft
**Specification Reference**: `specs/phase-i/spec.md`
**Plan Reference**: `specs/phase-i/plan.md`
**Constitution Reference**: `.specify/memory/constitution.md`

---

## Task List Overview

| ID | Task Name | Type | Layer | Dependencies |
|----|-----------|------|-------|--------------|
| T-001 | Task Data Class | Core | Domain | None |
| T-002 | Exception Classes | Core | Domain | None |
| T-003 | TaskService Init & Storage | Service | Application | T-001, T-002 |
| T-004 | Add Task Operation | Service | Application | T-003 |
| T-005 | Get All Tasks Operation | Service | Application | T-003 |
| T-006 | Get Task by ID Operation | Service | Application | T-003 |
| T-007 | Update Task Operation | Service | Application | T-003 |
| T-008 | Delete Task Operation | Service | Application | T-003 |
| T-009 | Mark Complete Operation | Service | Application | T-003 |
| T-010 | Mark Incomplete Operation | Service | Application | T-003 |
| T-011 | Menu Class Skeleton | CLI | Presentation | None |
| T-012 | Display Main Menu | CLI | Presentation | None |
| T-013 | Display Task List | CLI | Presentation | T-005, T-011 |
| T-014 | Get Validated Menu Choice | CLI | Presentation | None |
| T-015 | Get Validated Task Content | CLI | Presentation | None |
| T-016 | Get Validated Task ID | CLI | Presentation | None |
| T-017 | Main Application Loop | CLI | Presentation | T-011, T-014 |
| T-018 | Integration Tests | Test | All | All above |

---

## Task Details

### T-001: Task Data Class

**Description**: Create the `Task` dataclass in `models/task.py` with id, content, and completed fields.

**Preconditions**:
- None

**Expected Output**:
- `models/task.py` file created
- `Task` dataclass with three fields: `id: int`, `content: str`, `completed: bool`
- `__post_init__` validation that:
  - ID is a positive integer
  - Content is a string
  - Content length is 1-1000 characters
  - Completed is a boolean

**Artifacts**:
- Create: `models/__init__.py`
- Create: `models/task.py`

**References**:
- Spec: Section "Task Data Model" (fields and constraints)
- Plan: Section 5.2 "Task Class"

**Test Cases**:
- Test that valid Task can be created
- Test that Task with empty content raises error
- Test that Task with content > 1000 chars raises error
- Test that Task with negative ID raises error
- Test that Task with non-boolean completed raises error

---

### T-002: Exception Classes

**Description**: Create custom exception classes for domain-specific errors.

**Preconditions**:
- None

**Expected Output**:
- `models/exceptions.py` file created
- Exception hierarchy:
  - `TodoError` (base exception)
  - `ValidationError` (subclass of TodoError)
    - `EmptyContentError`
    - `WhitespaceContentError`
    - `ContentTooLongError`
    - `InvalidIdError`
    - `NonNumericInputError`
  - `TaskNotFoundError`

**Artifacts**:
- Create: `models/exceptions.py`

**References**:
- Plan: Section 6.1 "Exception Hierarchy"

**Test Cases**:
- Test that all exceptions inherit from TodoError
- Test that ValidationError catches all validation subclasses
- Test that TaskNotFoundError stores task_id

---

### T-003: TaskService Initialization and Storage

**Description**: Create TaskService class with in-memory dictionary storage and ID counter.

**Preconditions**:
- T-001 (Task class exists)
- T-002 (Exception classes exist)

**Expected Output**:
- `services/task_service.py` file created
- `TaskService` class with:
  - `__init__`: Initializes `_tasks` as empty dict, `_next_id` as 1
  - Read-only properties: `tasks` (returns list), `next_id` (returns int)

**Artifacts**:
- Create: `services/__init__.py`
- Create: `services/task_service.py`

**References**:
- Plan: Section 2 "In-Memory Data Structures"
- Plan: Section 5.3 "TaskService Class"

**Test Cases**:
- Test that TaskService initializes with empty tasks dict
- Test that TaskService initializes with next_id = 1
- Test that tasks property returns list
- Test that next_id property returns int

---

### T-004: Add Task Operation

**Description**: Implement add_task method in TaskService that creates and stores a new task.

**Preconditions**:
- T-003 (TaskService initialized)

**Expected Output**:
- `add_task(content: str) -> Task` method in TaskService
- Creates Task with unique ID from counter
- Stores in _tasks dict
- Increments _next_id counter
- Returns created Task

**Artifacts**:
- Modify: `services/task_service.py`

**References**:
- Spec: User Story 1 "Add New Task"
- Spec: AC-001 through AC-007
- Plan: Section 5.3 "CRUD Operations"

**Test Cases**:
- Test adding single task returns task with ID 1
- Test adding multiple tasks gets sequential IDs (1, 2, 3...)
- Test adding task sets completed=False by default
- Test adding task stores in _tasks dict
- Test that deleted tasks' IDs are not reused (counter still increments)

---

### T-005: Get All Tasks Operation

**Description**: Implement get_all_tasks method that returns all tasks sorted by ID.

**Preconditions**:
- T-003 (TaskService initialized)

**Expected Output**:
- `get_all_tasks() -> List[Task]` method in TaskService
- Returns empty list if no tasks
- Returns tasks sorted by ID ascending

**Artifacts**:
- Modify: `services/task_service.py`

**References**:
- Spec: User Story 2 "View Task List"
- Spec: AC-008, AC-011, AC-012
- Plan: Section 5.3 "CRUD Operations"

**Test Cases**:
- Test get_all_tasks returns empty list when no tasks
- Test get_all_tasks returns tasks sorted by ID
- Test get_all_tasks returns tasks with all fields intact

---

### T-006: Get Task by ID Operation

**Description**: Implement get_task method for retrieving a single task by ID.

**Preconditions**:
- T-003 (TaskService initialized)

**Expected Output**:
- `get_task(task_id: int) -> Optional[Task]` method in TaskService
- Returns Task if ID exists
- Returns None if ID not found

**Artifacts**:
- Modify: `services/task_service.py`

**References**:
- Plan: Section 5.3 "CRUD Operations"

**Test Cases**:
- Test get_task returns task when ID exists
- Test get_task returns None when ID does not exist
- Test get_task with valid positive ID works

---

### T-007: Update Task Operation

**Description**: Implement update_task method to modify task content.

**Preconditions**:
- T-003 (TaskService initialized)
- T-006 (get_task exists)

**Expected Output**:
- `update_task(task_id: int, new_content: str) -> Task` method in TaskService
- Updates task content (not ID, not completed status)
- Raises TaskNotFoundError if ID not found
- Returns updated Task

**Artifacts**:
- Modify: `services/task_service.py`

**References**:
- Spec: User Story 3 "Update Task"
- Spec: AC-013 through AC-018
- Plan: Section 5.3 "CRUD Operations"

**Test Cases**:
- Test update_task changes content
- Test update_task does not change ID
- Test update_task does not change completed status
- Test update_task raises TaskNotFoundError for invalid ID
- Test updating task multiple times preserves same ID

---

### T-008: Delete Task Operation

**Description**: Implement delete_task method to remove a task from storage.

**Preconditions**:
- T-003 (TaskService initialized)

**Expected Output**:
- `delete_task(task_id: int) -> None` method in TaskService
- Removes task from _tasks dict
- Raises TaskNotFoundError if ID not found
- Does NOT decrement next_id counter

**Artifacts**:
- Modify: `services/task_service.py`

**References**:
- Spec: User Story 4 "Delete Task"
- Spec: AC-019 through AC-022
- Plan: Section 5.3 "CRUD Operations"

**Test Cases**:
- Test delete_task removes task from storage
- Test delete_task raises TaskNotFoundError for invalid ID
- Test delete_task does not affect other tasks
- Test delete_task does not reuse ID (next_id unchanged)
- Test deleted task no longer appears in get_all_tasks

---

### T-009: Mark Task Complete Operation

**Description**: Implement mark_complete method to set task completed status to True.

**Preconditions**:
- T-003 (TaskService initialized)

**Expected Output**:
- `mark_complete(task_id: int) -> Task` method in TaskService
- Sets task.completed = True
- Returns updated Task
- Raises TaskNotFoundError if ID not found

**Artifacts**:
- Modify: `services/task_service.py`

**References**:
- Spec: User Story 5 "Mark Task Complete/Incomplete"
- Spec: AC-023, AC-026
- Plan: Section 5.3 "CRUD Operations"

**Test Cases**:
- Test mark_complete sets completed=True
- Test mark_complete returns updated task
- Test mark_complete raises TaskNotFoundError for invalid ID
- Test mark_complete on already complete task still returns True

---

### T-010: Mark Task Incomplete Operation

**Description**: Implement mark_incomplete method to set task completed status to False.

**Preconditions**:
- T-003 (TaskService initialized)

**Expected Output**:
- `mark_incomplete(task_id: int) -> Task` method in TaskService
- Sets task.completed = False
- Returns updated Task
- Raises TaskNotFoundError if ID not found

**Artifacts**:
- Modify: `services/task_service.py`

**References**:
- Spec: User Story 5 "Mark Task Complete/Incomplete"
- Spec: AC-024, AC-026
- Plan: Section 5.3 "CRUD Operations"

**Test Cases**:
- Test mark_incomplete sets completed=False
- Test mark_incomplete returns updated task
- Test mark_incomplete raises TaskNotFoundError for invalid ID
- Test mark_incomplete on incomplete task still returns False

---

### T-011: Menu Class Skeleton

**Description**: Create Menu class with constructor and basic structure.

**Preconditions**:
- None

**Expected Output**:
- `cli/menu.py` file created
- `Menu` class with:
  - `__init__(self, task_service: TaskService)`
  - `service` attribute (TaskService instance)
  - Placeholder methods for all operations

**Artifacts**:
- Create: `cli/__init__.py`
- Create: `cli/menu.py`

**References**:
- Plan: Section 5.4 "Menu Class"
- Plan: Section 8.3 "File: cli/menu.py"

**Test Cases**:
- Test Menu can be instantiated with TaskService
- Test Menu.service returns the TaskService instance

---

### T-012: Display Main Menu

**Description**: Implement display_menu method to show the main menu.

**Preconditions**:
- T-011 (Menu class exists)

**Expected Output**:
- `display_menu() -> None` method in Menu
- Prints menu exactly as specified in spec:
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

**Artifacts**:
- Modify: `cli/menu.py`

**References**:
- Spec: Section "Main Menu"
- Plan: Section 4.2 "Menu Display"

**Test Cases**:
- Test display_menu output matches expected format
- Test all 7 menu options are displayed

---

### T-013: Display Task List

**Description**: Implement display_tasks method to format and display all tasks.

**Preconditions**:
- T-005 (get_all_tasks exists in service)
- T-011 (Menu class exists)

**Expected Output**:
- `display_tasks() -> None` method in Menu
- Displays tasks in table format:
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
- Shows "No tasks yet. Add your first task!" when empty

**Artifacts**:
- Modify: `cli/menu.py`

**References**:
- Spec: Section "View Tasks" (menu options detail)
- Plan: Section 7.1 "Task List Display Format"
- Plan: Section 7.3 "Empty State Display"

**Test Cases**:
- Test display_tasks with no tasks shows empty message
- Test display_tasks with tasks shows correct table format
- Test display_tasks shows [X] for completed tasks
- Test display_tasks shows [ ] for incomplete tasks
- Test display_tasks shows correct summary count

---

### T-014: Get Validated Menu Choice

**Description**: Implement get_menu_choice method with validation.

**Preconditions**:
- T-012 (display_menu exists)

**Expected Output**:
- `get_menu_choice() -> int` method in Menu
- Prompts user for input
- Validates input is integer 1-7
- Re-prompts on invalid input with error message
- Returns valid choice as int

**Artifacts**:
- Modify: `cli/menu.py`

**References**:
- Spec: Error Cases - "Invalid menu choice"
- Plan: Section 4.3 "Input Handling Flow"

**Test Cases**:
- Test get_menu_choice accepts valid input 1-7
- Test get_menu_choice rejects non-numeric input
- Test get_menu_choice rejects numbers outside 1-7
- Test get_menu_choice strips whitespace

---

### T-015: Get Validated Task Content

**Description**: Implement get_task_content method with validation.

**Preconditions**:
- T-011 (Menu class exists)

**Expected Output**:
- `get_task_content(prompt: str) -> str` method in Menu
- Takes optional prompt string
- Gets user input
- Validates:
  - Not empty
  - Not whitespace-only
  - Not > 1000 characters
- Re-prompts on validation failure with appropriate error message
- Returns validated content

**Artifacts**:
- Modify: `cli/menu.py`

**References**:
- Spec: Error Cases - "Empty task content", "Whitespace-only content", "Content too long"
- Plan: Section 4.4 "Input Sanitization"

**Test Cases**:
- Test get_task_content accepts valid input
- Test get_task_content rejects empty input
- Test get_task_content rejects whitespace-only input
- Test get_task_content rejects > 1000 chars
- Test get_task_content strips leading/trailing whitespace

---

### T-016: Get Validated Task ID

**Description**: Implement get_task_id method with validation against storage.

**Preconditions**:
- T-003 (TaskService with tasks dict exists)
- T-011 (Menu class exists)

**Expected Output**:
- `get_task_id(prompt: str) -> int` method in Menu
- Prompts user for input
- Validates:
  - Is a valid integer
  - Is positive (> 0)
  - Exists in tasks storage
- Re-prompts on validation failure with appropriate error message
- Returns valid task_id as int

**Artifacts**:
- Modify: `cli/menu.py`

**References**:
- Spec: Error Cases - "Non-numeric ID input", "Negative ID input", "Invalid task ID"
- Plan: Section 6.4 "Input Validation Functions"

**Test Cases**:
- Test get_task_id accepts valid existing ID
- Test get_task_id rejects non-numeric input
- Test get_task_id rejects negative numbers
- Test get_task_id rejects zero
- Test get_task_id rejects non-existent ID

---

### T-017: Main Application Loop

**Description**: Implement run method as the main application loop.

**Preconditions**:
- T-011 (Menu class exists)
- T-012 (display_menu exists)
- T-014 (get_menu_choice exists)
- T-004 through T-010 (all TaskService operations exist)

**Expected Output**:
- `run() -> None` method in Menu
- Main loop:
  1. Clear screen (optional)
  2. Display menu
  3. Get user choice
  4. Handle choice (call appropriate service method or exit)
  5. Show result/success message
  6. Loop until choice == 7
- Choice 7 (Exit) breaks loop and ends application

**Artifacts**:
- Modify: `cli/menu.py`

**References**:
- Spec: Section "Main Menu" (7. Exit)
- Plan: Section 4.1 "Main Application Loop"

**Test Cases**:
- Test run method exists and is callable
- Test loop exits on choice 7
- Test choice 1 triggers add task flow
- Test choice 2 triggers view tasks flow
- Test choice 3 triggers update task flow
- Test choice 4 triggers delete task flow
- Test choice 5 triggers mark complete flow
- Test choice 6 triggers mark incomplete flow

---

### T-018: Integration Tests

**Description**: Create integration tests that verify complete user workflows.

**Preconditions**:
- All other tasks (T-001 through T-017) are complete

**Expected Output**:
- `tests/test_integration.py` file created
- Tests covering full user journeys:
  1. Add task → View task → Update task → Delete task
  2. Add multiple tasks → View all → Mark complete → View all
  3. Error handling paths (invalid ID, empty content)

**Artifacts**:
- Create: `tests/__init__.py`
- Create: `tests/test_integration.py`

**References**:
- Spec: All acceptance criteria (AC-001 through AC-026)
- Plan: Section 10 "Testing Strategy"

**Test Cases**:
- Test complete add-view-update-delete workflow
- Test complete add-view-mark workflow
- Test error recovery on invalid ID
- Test error recovery on invalid content
- Test multiple tasks handling
- Test state persistence within session

---

## Implementation Order

```
Phase 1: Foundation
├── T-001: Task Data Class
├── T-002: Exception Classes
└── T-003: TaskService Init & Storage

Phase 2: Business Logic
├── T-004: Add Task
├── T-005: Get All Tasks
├── T-006: Get Task by ID
├── T-007: Update Task
├── T-008: Delete Task
├── T-009: Mark Complete
└── T-010: Mark Incomplete

Phase 3: Presentation Layer
├── T-011: Menu Class Skeleton
├── T-012: Display Main Menu
├── T-013: Display Task List
├── T-014: Get Validated Menu Choice
├── T-015: Get Validated Task Content
├── T-016: Get Validated Task ID
└── T-017: Main Application Loop

Phase 4: Testing
└── T-018: Integration Tests
```

---

## Running Tasks

Each task should be implemented using the Red-Green-Refactor cycle:

```bash
# 1. Write failing test
pytest tests/test_models/test_task.py::test_task_with_empty_content_raises_error -v

# 2. Implement feature
# ... write code ...

# 3. Run test to verify it passes
pytest tests/test_models/test_task.py -v

# 4. Refactor if needed
# ... improve code while tests pass ...
```

---

## Success Criteria

All tasks complete when:
- [X] T-001 through T-018 are implemented
- [X] All tests pass: `pytest tests/ -v`
- [X] Application runs without errors: `python main.py`
- [X] All 26 acceptance criteria from spec are verified
- [X] No future phase features are present
- [X] Code follows clean architecture principles

---

**Document Version**: 1.0.0
**Status**: Pending Human Approval
**Approval Required**: Before proceeding to Implementation

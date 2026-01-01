# Phase I Specification: Evolution of Todo

**Feature Branch**: `phase-i`
**Created**: 2025-12-28
**Status**: Draft
**Constitution Reference**: `.specify/memory/constitution.md`

## Document Metadata

| Field | Value |
|-------|-------|
| **Phase** | I - Foundation |
| **Scope** | Console Application |
| **Storage** | In-memory |
| **Users** | Single user |
| **Persistence** | None (runtime only) |

## Phase Overview

Phase I establishes the foundation of the Evolution of Todo project: a Python console application with in-memory task management. This specification defines EXACTLY what Phase I delivers. Future phase features are explicitly excluded and must not be implemented.

**Out of Scope for Phase I:**
- Database persistence
- File-based storage
- User authentication
- Web interface or API
- Advanced features (priorities, tags, search, sorting, recurring tasks, due dates)
- Multi-user support
- Export/import functionality
- Configuration files
- Any references to Next.js, FastAPI, Neon DB, OpenAI Agents SDK, MCP, Docker, Kubernetes, Kafka, or Dapr

---

## User Scenarios & Testing

### User Story 1 - Add New Task (Priority: P1)

As a user, I want to add new tasks to my todo list so I can capture things I need to do.

**Why this priority**: Adding tasks is the fundamental purpose of a todo application. Without this feature, no other functionality has value.

**Independent Test**: Can be tested by running the application, selecting "Add Task," entering task content, and verifying the task appears in the list.

**Acceptance Scenarios:**

1. **Given** the application is running, **When** I select "Add Task" and enter "Buy milk", **Then** the task is added with a unique ID and displayed in subsequent views.

2. **Given** the application is running, **When** I add multiple tasks ("Buy milk", "Walk the dog", "Call mom"), **Then** all tasks are stored and each has a unique ID.

3. **Given** the task list is empty, **When** I add a task, **Then** the task list is no longer empty and shows one task.

---

### User Story 2 - View Task List (Priority: P1)

As a user, I want to see all my tasks so I can review what I need to do.

**Why this priority**: Users must be able to review their tasks to prioritize and plan their work. This is essential for any task management workflow.

**Independent Test**: Can be tested by adding tasks and selecting "View Tasks" to verify all tasks display correctly.

**Acceptance Scenarios:**

1. **Given** I have added three tasks, **When** I select "View Tasks", **Then** all three tasks are displayed with their ID, content, and completion status.

2. **Given** the task list is empty, **When** I select "View Tasks", **Then** I see a message indicating no tasks exist.

3. **Given** I have tasks with different completion statuses, **When** I view the list, **Then** each task shows whether it is complete or incomplete.

---

### User Story 3 - Update Task (Priority: P1)

As a user, I want to modify existing tasks so I can correct mistakes or refine my task descriptions.

**Why this priority**: Users frequently need to change task content after creation. This is essential for maintaining accurate task lists.

**Independent Test**: Can be tested by creating a task, viewing it, updating it, and verifying the changes.

**Acceptance Scenarios:**

1. **Given** I have a task with content "Buy milk", **When** I update it to "Buy organic milk", **Then** the task content changes to "Buy organic milk" and the ID remains the same.

2. **Given** I have multiple tasks, **When** I update task with ID 2, **Then** only task 2's content changes; other tasks remain unchanged.

3. **Given** I provide an invalid task ID, **When** I attempt to update, **Then** I receive an error message and no tasks are modified.

---

### User Story 4 - Delete Task (Priority: P1)

As a user, I want to remove tasks that are no longer needed so my list stays relevant.

**Why this priority**: Completed or obsolete tasks should be removable to keep the task list focused and manageable.

**Independent Test**: Can be tested by creating tasks, deleting one, and verifying it no longer appears in the list.

**Acceptance Scenarios:**

1. **Given** I have three tasks, **When** I delete task with ID 2, **Then** only two tasks remain and the remaining tasks keep their original IDs.

2. **Given** I have tasks, **When** I delete a task, **Then** the task is permanently removed from memory.

3. **Given** I provide an invalid task ID, **When** I attempt to delete, **Then** I receive an error message and no tasks are deleted.

---

### User Story 5 - Mark Task Complete/Incomplete (Priority: P1)

As a user, I want to mark tasks as complete or incomplete so I can track my progress.

**Why this priority**: The core value proposition of a todo app is tracking what is done versus what remains. This is essential for productivity tracking.

**Independent Test**: Can be tested by creating tasks, marking some complete, and verifying status changes in the view.

**Acceptance Scenarios:**

1. **Given** I have an incomplete task, **When** I mark it as complete, **Then** the task status changes to complete.

2. **Given** I have a complete task, **When** I mark it as incomplete, **Then** the task status changes to incomplete.

3. **Given** I provide an invalid task ID, **When** I attempt to change status, **Then** I receive an error message and no statuses are modified.

---

## Requirements

### Functional Requirements

- **FR-001**: The system MUST allow users to add tasks with text content.
- **FR-002**: Each task MUST be assigned a unique positive integer ID upon creation.
- **FR-003**: The system MUST display all tasks with their ID, content, and completion status.
- **FR-004**: The system MUST allow users to update the content of existing tasks by ID.
- **FR-005**: The system MUST allow users to delete tasks by ID.
- **FR-006**: The system MUST allow users to mark tasks as complete.
- **FR-007**: The system MUST allow users to mark complete tasks as incomplete.
- **FR-008**: The system MUST validate that task IDs exist before operations that require them.
- **FR-009**: The system MUST provide a menu-based command-line interface.
- **FR-010**: The system MUST store all tasks in memory for the duration of the application session.
- **FR-011**: The system MUST clear all tasks when the application exits.

### Non-Functional Requirements

- **NFR-001**: Task list operations MUST complete within 100 milliseconds.
- **NFR-002**: The application MUST start within 2 seconds on standard hardware.
- **NFR-003**: The application MUST handle at least 100 tasks without performance degradation.
- **NFR-004**: All user input MUST be validated and sanitized.
- **NFR-005**: Error messages MUST be clear and actionable.

---

## Task Data Model

### Task Entity

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Auto-generated, unique, positive | Unique identifier for the task |
| `content` | String | Non-empty, max 1000 characters | The task description |
| `completed` | Boolean | Default: `False` | Whether the task is complete |

### Model Constraints

1. Task IDs start at 1 and increment by 1 for each new task.
2. Deleted task IDs are NOT reused (to maintain ID stability during session).
3. Task content cannot be empty or whitespace-only.
4. Task content maximum length is 1000 characters.

---

## CLI Interaction Flow

### Main Menu

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

### Menu Options Detail

#### 1. Add Task
```
Enter task content: [user input]
Task added successfully! (ID: 1)
```

#### 2. View Tasks
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

#### 3. Update Task
```
Enter task ID to update: [user input]
Current content: [display current]
Enter new content: [user input]
Task updated successfully!
```

#### 4. Delete Task
```
Enter task ID to delete: [user input]
Task deleted successfully!
```

#### 5. Mark Task Complete
```
Enter task ID to mark complete: [user input]
Task marked as complete!
```

#### 6. Mark Task Incomplete
```
Enter task ID to mark incomplete: [user input]
Task marked as incomplete!
```

---

## Acceptance Criteria

### Add Task (AC)

- [X] AC-001: User can input non-empty task content
- [X] AC-002: New task receives unique ID (1, 2, 3, ...)
- [X] AC-003: New task is marked as incomplete by default
- [X] AC-004: Task appears in subsequent "View Tasks" displays
- [X] AC-005: Empty input shows error message
- [X] AC-006: Whitespace-only input shows error message
- [X] AC-007: Input exceeding 1000 characters shows error message

### View Tasks (AC)

- [X] AC-008: All tasks display with ID, status, and content
- [X] AC-009: Complete tasks show `[X]` marker
- [X] AC-010: Incomplete tasks show `[ ]` marker
- [X] AC-011: Empty task list shows descriptive message
- [X] AC-012: Task summary shows total count and completion breakdown

### Update Task (AC)

- [X] AC-013: User can modify task content by ID
- [X] AC-014: Task ID remains unchanged after update
- [X] AC-015: Completion status remains unchanged after update
- [X] AC-016: Invalid ID shows error message
- [X] AC-017: Empty new content shows error message
- [X] AC-018: Whitespace-only new content shows error message

### Delete Task (AC)

- [X] AC-019: Task is removed from the list
- [X] AC-020: Remaining tasks keep their IDs unchanged
- [X] AC-021: Invalid ID shows error message
- [X] AC-022: After deletion, "View Tasks" no longer shows the deleted task

### Mark Complete/Incomplete (AC)

- [X] AC-023: Task completion status changes to `True` when marked complete
- [X] AC-024: Task completion status changes to `False` when marked incomplete
- [X] AC-025: Invalid ID shows error message
- [X] AC-026: Status change is reflected in "View Tasks" display

---

## Error Cases

### Error Scenarios and Handling

| Error Condition | User Message | Behavior |
|-----------------|--------------|----------|
| Invalid menu choice | "Invalid choice. Please enter a number 1-7." | Return to main menu |
| Empty task content | "Error: Task content cannot be empty." | Return to add flow |
| Whitespace-only content | "Error: Task content cannot be empty or whitespace." | Return to add flow |
| Content too long (>1000 chars) | "Error: Task content must be 1000 characters or fewer." | Return to add flow |
| Invalid task ID for update | "Error: Task with ID {id} not found." | Return to update flow |
| Invalid task ID for delete | "Error: Task with ID {id} not found." | Return to delete flow |
| Invalid task ID for complete | "Error: Task with ID {id} not found." | Return to complete flow |
| Invalid task ID for incomplete | "Error: Task with ID {id} not found." | Return to incomplete flow |
| Non-numeric ID input | "Error: Please enter a valid number." | Return to ID input |
| Negative ID input | "Error: Task ID must be a positive number." | Return to ID input |

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can add a task and see it in the list within 5 seconds of application start.
- **SC-002**: All 5 CRUD operations (Create, Read, Update, Delete, Update Status) work correctly.
- **SC-003**: Application handles invalid inputs gracefully with clear error messages.
- **SC-004**: Task data persists correctly within a single application session.
- **SC-005**: Application exits cleanly with no data loss warnings needed (data loss expected on exit).

---

## Out of Scope (For Reference)

### Explicitly Excluded Features

These features are reserved for future phases and MUST NOT be implemented in Phase I:

- Priorities (high/medium/low)
- Tags or categories
- Search functionality
- Sorting (by date, priority, alphabetical)
- Recurring tasks
- Due dates or time-based reminders
- Data persistence (files, databases)
- User authentication
- Multiple users
- Configuration files or settings
- Export/import functionality
- Undo/redo operations
- Keyboard shortcuts
- Colored output
- Any form of persistence beyond runtime

---

**Document Version**: 1.0.0
**Status**: Pending Human Approval
**Approval Required**: Before proceeding to Plan and Tasks

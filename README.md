# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

Advanced features for efficient pet care planning:

- **Task Filtering**: Filter tasks by completion status (e.g., pending) and/or pet name for quick views.
- **Priority-Based Sorting**: Automatically sort tasks by priority and due date to generate optimized daily plans.
- **Recurring Tasks**: Daily and weekly tasks auto-create new instances upon completion, scheduled for the next occurrence.
- **Conflict Detection**: Warns about overlapping tasks for the same pet or across different pets, preventing scheduling errors without crashing the app.

## Testing PawPal+

Run the test suite using: python -m pytest

The test suite covers:
- Basic task and pet management functionality
- Task filtering by status and pet name
- **Sorting Correctness**: Verifies tasks are returned in chronological order
- **Recurrence Logic**: Confirms that marking a daily task complete creates a new task for the following day
- **Conflict Detection**: Verifies that the Scheduler flags duplicate times and overlapping tasks

**Confidence Level**: 4.5/5 stars - The core scheduling features are well-tested and reliable, with comprehensive coverage of sorting, recurrence, and conflict detection. All tests pass successfully, indicating solid implementation of the key requirements.

## Features

### Core Algorithms Implemented

- **Priority-Based Sorting**: Tasks are sorted by priority level (1-5, where 1 is highest) and due date to create optimized daily plans. Implemented in `Schedule.generate_plan()` and `Schedule.sort_by_priority()`.
- **Time-Based Sorting**: Tasks can be sorted by their scheduled time (HH:MM) for chronological ordering. Implemented in `Schedule.sort_by_time()`.
- **Conflict Detection**: Automatically detects time overlaps between tasks, warning users of conflicts for the same pet or different pets. Implemented in `Schedule.detect_conflicts()`.
- **Daily/Weekly Recurrence**: Completed recurring tasks (daily or weekly) automatically generate the next occurrence. Implemented in `Schedule.mark_task_complete()`.
- **Task Filtering**: Filter tasks by completion status (pending, in-progress, done) and/or pet name for targeted views. Implemented in `Schedule.filter_tasks()`.
- **Due Task Identification**: Identifies and lists all overdue tasks based on current time and due dates. Implemented in `Schedule.due_tasks()`.
- **Next Task Selection**: Selects the highest-priority pending task for immediate action. Implemented in `Schedule.next_task()`.
- **Owner Dashboard**: Provides a summary of pets, tasks, and available slots for quick overview. Implemented in `Owner.dashboard()`.
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional

@dataclass
class Pet:
    species: str
    name: str
    age: int
    breed: Optional[str] = None
    notes: str = ""
    tasks: List['Task'] = field(default_factory=list)

    def update_age(self, years: int = 1) -> None:
        """Increment pet age by the specified number of years."""
        self.age += years

    def add_notes(self, text: str) -> None:
        """Append text to the pet's notes."""
        self.notes = f"{self.notes}\n{text}".strip()

    def add_task(self, task: 'Task') -> None:
        """Add a task to this pet's task list."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def remove_task(self, task: 'Task') -> None:
        """Remove a task from this pet's task list."""
        self.tasks = [t for t in self.tasks if t is not task]
        if task.pet is self:
            task.pet = None

    def all_task_summaries(self) -> List[str]:
        """Return summaries of all tasks for this pet."""
        return [t.summary() for t in self.tasks]

    def info(self) -> str:
        """Return a human-readable info string for this pet."""
        return f"{self.name} ({self.species}, {self.age} y/o){' - ' + self.breed if self.breed else ''}"

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int = 3  # 1 high, 5 low
    frequency: str = "one-time"
    status: str = "pending"  # pending, in-progress, done
    due_datetime: Optional[datetime] = None
    pet: Optional[Pet] = None
    owner: Optional['Owner'] = None

    def assign_pet(self, pet: Pet) -> None:
        """Assign this task to a specific pet."""
        self.pet = pet
        if self not in pet.tasks:
            pet.tasks.append(self)

    def assign_owner(self, owner: 'Owner') -> None:
        """Assign this task to a specific owner."""
        self.owner = owner
        if self not in owner.tasks:
            owner.tasks.append(self)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.status = "done"

    def reschedule(self, new_datetime: datetime) -> None:
        """Update the task's due date and time."""
        self.due_datetime = new_datetime

    def is_overdue(self) -> bool:
        """Check if this task is overdue (past due date and not completed)."""
        return bool(self.due_datetime and self.due_datetime < datetime.now() and self.status != "done")

    def summary(self) -> str:
        """Return a human-readable summary of this task."""
        pet_name = self.pet.name if self.pet else "No pet"
        owner_name = self.owner.name if self.owner else "No owner"
        due_str = self.due_datetime.isoformat() if self.due_datetime else "unscheduled"
        return f"[{self.status}] {self.title} (Priority {self.priority}, {self.duration_minutes}m) for {pet_name}, owner {owner_name}, due {due_str}"

class Owner:
    def __init__(self, name: str, email: str):
        """Initialize an owner with name and email."""
        self.name = name
        self.email = email
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []
        self.available_slots: int = 0
        self.preferred_times: List[str] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list and clear its tasks."""
        self.pets = [p for p in self.pets if p is not pet]
        tasks_to_clear = [t for t in self.tasks if t.pet is pet]
        for task in tasks_to_clear:
            task.pet = None

    def add_task(self, task: Task, pet: Optional[Pet] = None) -> None:
        """Add a task to this owner, optionally assigning it to a pet."""
        if pet and pet not in self.pets:
            raise ValueError("Task pet must belong to the owner")
        self.tasks.append(task)
        task.owner = self
        if pet:
            task.assign_pet(pet)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this owner's task list."""
        self.tasks = [t for t in self.tasks if t is not task]
        if task.pet:
            task.pet.remove_task(task)
        task.owner = None

    def set_availability(self, slots: int) -> None:
        """Set the number of available time slots for this owner."""
        self.available_slots = slots

    def set_preferred_times(self, times: List[str]) -> None:
        """Set the owner's preferred times for scheduling."""
        self.preferred_times = times

    def all_tasks(self) -> List[Task]:
        return self.tasks

    def tasks_by_pet(self, pet: Pet) -> List[Task]:
        return [t for t in self.tasks if t.pet is pet]

    def dashboard(self) -> str:
        """Return a human-readable dashboard summary for this owner."""
        pet_list = ", ".join(p.name for p in self.pets) or "No pets"
        task_list = ", ".join(t.title for t in self.tasks) or "No tasks"
        return f"Owner: {self.name}, Pets: {pet_list}, Tasks: {task_list}, Slots: {self.available_slots}"

class Schedule:
    def __init__(self, owner: Owner):
        """Initialize a schedule for a specific owner."""
        self.owner = owner
        self.tasks: List[Task] = []
        self.created_at = datetime.now()
        self.last_updated = self.created_at

    def add_task(self, task: Task) -> Optional[str]:
        """Add a task to the schedule, validating owner and pet ownership."""
        if task.owner is not self.owner:
            raise ValueError("Task owner must match schedule owner")
        if task.pet and task.pet not in self.owner.pets:
            raise ValueError("Task pet must belong to the schedule owner")
        if task not in self.tasks:
            self.tasks.append(task)
        # Check for conflicts
        warning = self.detect_conflicts(task)
        self.last_updated = datetime.now()
        return warning

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        self.tasks = [t for t in self.tasks if t is not task]
        self.last_updated = datetime.now()

    def all_tasks(self) -> List[Task]:
        """Return all tasks in the schedule."""
        return self.tasks

    def tasks_by_pet(self, pet: Pet) -> List[Task]:
        """Return all tasks assigned to a specific pet in the schedule."""
        return [t for t in self.tasks if t.pet is pet]

    def due_tasks(self) -> List[Task]:
        """Return all overdue tasks in the schedule."""
        return [t for t in self.tasks if t.is_overdue()]

    def sort_by_priority(self) -> None:
        """Sort tasks by priority and due date in place."""
        self.tasks.sort(key=lambda t: (t.priority, t.due_datetime or datetime.max))

    def sort_by_time(self) -> None:
        """Sort tasks by time in HH:MM format."""
        self.tasks.sort(key=lambda t: t.due_datetime.time() if t.due_datetime else datetime.max.time())

    def generate_plan(self) -> List[Task]:
        """Generate and return a prioritized task plan."""
        self.sort_by_priority()
        return self.tasks

    def next_task(self) -> Optional[Task]:
        """Return the next highest-priority pending task."""
        pending = [t for t in self.tasks if t.status != "done"]
        if not pending:
            return None
        return min(pending, key=lambda t: (t.priority, t.due_datetime or datetime.max))

    def assign_task_to_pet(self, task: Task, pet: Pet) -> None:
        """Assign a task to a pet and add it to the schedule."""
        if pet not in self.owner.pets:
            raise ValueError("Pet must belong to schedule owner")
        task.assign_pet(pet)
        self.add_task(task)

    def filter_tasks(self, status: Optional[str] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name."""
        filtered = self.tasks
        if status:
            filtered = [t for t in filtered if t.status == status]
        if pet_name:
            filtered = [t for t in filtered if t.pet and t.pet.name == pet_name]
        return filtered

    def detect_conflicts(self, new_task: Task) -> Optional[str]:
        """Detect time conflicts for the new task with existing tasks for same or different pets."""
        if not new_task.due_datetime:
            return None
        new_start = new_task.due_datetime
        new_end = new_start + timedelta(minutes=new_task.duration_minutes)
        for existing_task in self.tasks:
            if existing_task == new_task or existing_task.status == "done" or not existing_task.due_datetime:
                continue
            existing_start = existing_task.due_datetime
            existing_end = existing_start + timedelta(minutes=existing_task.duration_minutes)
            if new_start < existing_end and existing_start < new_end:
                conflict_type = "same pet" if existing_task.pet == new_task.pet else "different pet"
                same_pet_text = " for pet '" + new_task.pet.name + "'" if new_task.pet and existing_task.pet == new_task.pet else ""
                pet_text = (f" for pet '{new_task.pet.name}' and pet '{existing_task.pet.name}'" if new_task.pet and existing_task.pet and existing_task.pet != new_task.pet else same_pet_text)
                return f"Warning: Task '{new_task.title}' conflicts with '{existing_task.title}' ({conflict_type}){pet_text}."
        return None

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task as completed and automatically create the next occurrence for recurring tasks."""
        task.status = "done"
        if task.frequency in ["daily", "weekly"]:
            delta = timedelta(days=1 if task.frequency == "daily" else 7)
            if task.due_datetime:
                new_date = datetime.now().date() + delta
                new_due = datetime.combine(new_date, task.due_datetime.time())
            else:
                new_due = datetime.now() + delta
            new_task = Task(
                title=task.title,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                status="pending",
                due_datetime=new_due,
                pet=task.pet,
                owner=task.owner
            )
            self.owner.add_task(new_task, pet=task.pet)
            self.add_task(new_task)
        self.last_updated = datetime.now()


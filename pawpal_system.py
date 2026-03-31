from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Pet:
    species: str
    name: str
    age: int
    breed: Optional[str] = None
    notes: str = ""

    def update_age(self, years: int = 1) -> None:
        self.age += years

    def add_notes(self, text: str) -> None:
        self.notes = f"{self.notes}\n{text}".strip()

    def info(self) -> str:
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
    owner: Optional["Owner"] = None

    def assign_pet(self, pet: Pet) -> None:
        self.pet = pet

    def assign_owner(self, owner: "Owner") -> None:
        self.owner = owner

    def mark_complete(self) -> None:
        self.status = "done"

    def reschedule(self, new_datetime: datetime) -> None:
        self.due_datetime = new_datetime

    def summary(self) -> str:
        pet_name = self.pet.name if self.pet else "No pet"
        due_str = self.due_datetime.isoformat() if self.due_datetime else "unscheduled"
        return f"[{self.status}] {self.title} (Priority {self.priority}, {self.duration_minutes}m) for {pet_name} due {due_str}"

class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []
        self.tasks: List[Task] = []
        self.available_slots: int = 0
        self.preferred_times: List[str] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        self.pets = [p for p in self.pets if p is not pet]

    def add_task(self, task: Task) -> None:
        task.owner = self
        if task.pet and task.pet not in self.pets:
            raise ValueError("Task pet must belong to the owner")
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks = [t for t in self.tasks if t is not task]
        task.owner = None

    def set_availability(self, slots: int) -> None:
        self.available_slots = slots

    def set_preferred_times(self, times: List[str]) -> None:
        self.preferred_times = times

    def dashboard(self) -> str:
        pet_list = ", ".join(p.name for p in self.pets) or "No pets"
        task_list = ", ".join(t.title for t in self.tasks) or "No tasks"
        return f"Owner: {self.name}, Pets: {pet_list}, Tasks: {task_list}, Slots: {self.available_slots}"

class Schedule:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: List[Task] = []
        self.created_at = datetime.now()
        self.last_updated = self.created_at

    def add_task(self, task: Task) -> None:
        if task.owner is not self.owner:
            raise ValueError("Task owner must match schedule owner")
        if task.pet and task.pet not in self.owner.pets:
            raise ValueError("Task pet must belong to the schedule owner")
        self.tasks.append(task)
        self.last_updated = datetime.now()

    def remove_task(self, task: Task) -> None:
        self.tasks = [t for t in self.tasks if t is not task]
        self.last_updated = datetime.now()

    def sort_by_priority(self) -> None:
        self.tasks.sort(key=lambda t: t.priority)

    def filter_by_pet(self, pet: Pet) -> List[Task]:
        return [t for t in self.tasks if t.pet is pet]

    def generate_plan(self) -> List[Task]:
        self.sort_by_priority()
        return self.tasks

    def next_task(self) -> Optional[Task]:
        pending = [t for t in self.tasks if t.status != "done"]
        return min(pending, key=lambda t: (t.priority, t.due_datetime or datetime.max), default=None)


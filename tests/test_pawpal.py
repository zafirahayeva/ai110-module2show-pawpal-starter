import pytest
from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Owner, Schedule


def test_task_mark_complete():
    task = Task(title="Feed Cat", duration_minutes=10, priority=2)
    assert task.status == "pending"
    task.mark_complete()
    assert task.status == "done"


def test_pet_add_task_increases_task_count():
    pet = Pet(species="Cat", name="Milo", age=2)
    assert len(pet.tasks) == 0
    task = Task(title="Play", duration_minutes=15)
    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task
    assert task.pet is pet
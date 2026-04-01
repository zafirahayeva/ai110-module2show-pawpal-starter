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


def test_schedule_filter_tasks():
    owner = Owner("Alice", "alice@example.com")
    pet1 = Pet("Dog", "Buddy", 3)
    pet2 = Pet("Cat", "Whiskers", 2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    task1 = Task("Walk", 30, priority=1, status="pending")
    task2 = Task("Feed", 10, priority=2, status="done")
    task3 = Task("Play", 20, priority=3, status="pending")
    
    owner.add_task(task1, pet=pet1)
    owner.add_task(task2, pet=pet2)
    owner.add_task(task3, pet=pet1)
    
    schedule = Schedule(owner)
    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)
    
    # Filter by status
    pending_tasks = schedule.filter_tasks(status="pending")
    assert len(pending_tasks) == 2
    assert task1 in pending_tasks
    assert task3 in pending_tasks
    
    # Filter by pet name
    buddy_tasks = schedule.filter_tasks(pet_name="Buddy")
    assert len(buddy_tasks) == 2
    assert task1 in buddy_tasks
    assert task3 in buddy_tasks
    
    # Filter by both
    pending_buddy_tasks = schedule.filter_tasks(status="pending", pet_name="Buddy")
    assert len(pending_buddy_tasks) == 2
    assert task1 in pending_buddy_tasks
    assert task3 in pending_buddy_tasks
    
    # No filters
    all_tasks = schedule.filter_tasks()
    assert len(all_tasks) == 3
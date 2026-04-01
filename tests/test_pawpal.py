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


def test_sorting_correctness_chronological_order():
    """Verify tasks are returned in chronological order."""
    owner = Owner("Alice", "alice@example.com")
    pet = Pet("Dog", "Buddy", 3)
    owner.add_pet(pet)
    
    # Create tasks with different due times
    now = datetime.now()
    task1 = Task("Morning Walk", 30, priority=1, due_datetime=now.replace(hour=8, minute=0))
    task2 = Task("Afternoon Feed", 15, priority=2, due_datetime=now.replace(hour=12, minute=0))
    task3 = Task("Evening Play", 20, priority=3, due_datetime=now.replace(hour=18, minute=0))
    
    owner.add_task(task1, pet=pet)
    owner.add_task(task2, pet=pet)
    owner.add_task(task3, pet=pet)
    
    schedule = Schedule(owner)
    schedule.add_task(task1)
    schedule.add_task(task2)
    schedule.add_task(task3)
    
    # Sort by time and verify chronological order
    schedule.sort_by_time()
    sorted_tasks = schedule.all_tasks()
    
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].title == "Morning Walk"
    assert sorted_tasks[1].title == "Afternoon Feed"
    assert sorted_tasks[2].title == "Evening Play"


def test_recurrence_logic_daily_task():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    owner = Owner("Alice", "alice@example.com")
    pet = Pet("Cat", "Whiskers", 2)
    owner.add_pet(pet)
    
    # Create a daily task for today at 9 AM
    today_9am = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    daily_task = Task("Daily Feed", 10, priority=2, frequency="daily", due_datetime=today_9am)
    
    owner.add_task(daily_task, pet=pet)
    schedule = Schedule(owner)
    schedule.add_task(daily_task)
    
    # Initially, only one task
    assert len(schedule.all_tasks()) == 1
    assert schedule.all_tasks()[0].status == "pending"
    
    # Mark complete
    schedule.mark_task_complete(daily_task)
    
    # Should now have two tasks: completed one and new one for tomorrow
    tasks = schedule.all_tasks()
    assert len(tasks) == 2
    
    # Find the completed and pending tasks
    completed_tasks = [t for t in tasks if t.status == "done"]
    pending_tasks = [t for t in tasks if t.status == "pending"]
    
    assert len(completed_tasks) == 1
    assert len(pending_tasks) == 1
    
    # Check the new task is for the next day at the same time
    new_task = pending_tasks[0]
    assert new_task.title == "Daily Feed"
    assert new_task.frequency == "daily"
    assert new_task.due_datetime.date() == (datetime.now().date() + timedelta(days=1))
    assert new_task.due_datetime.time() == today_9am.time()


def test_conflict_detection_duplicate_times():
    """Verify that the Scheduler flags duplicate times."""
    owner = Owner("Alice", "alice@example.com")
    pet = Pet("Dog", "Buddy", 3)
    owner.add_pet(pet)
    
    # Create schedule
    schedule = Schedule(owner)
    
    # Add first task at 10 AM
    task1_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    task1 = Task("Walk", 30, priority=1, due_datetime=task1_time)
    owner.add_task(task1, pet=pet)
    schedule.add_task(task1)
    
    # Add second task at same time (10 AM) - should conflict
    task2 = Task("Feed", 15, priority=2, due_datetime=task1_time)
    owner.add_task(task2, pet=pet)
    
    # Adding should detect conflict (we'll capture the print output)
    import io
    import sys
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    schedule.add_task(task2)
    
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    # Verify conflict was detected
    assert "conflicts with" in output.lower()
    assert "Walk" in output
    assert "Feed" in output
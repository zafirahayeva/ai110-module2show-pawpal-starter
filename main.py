from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Schedule

owner = Owner("Zafirah", "zafi@example.com")
pet1 = Pet("Dog", "Luna", 4)
pet2 = Pet("Cat", "Whiskers", 2)
owner.add_pet(pet1)
owner.add_pet(pet2)

# Add tasks out of order (not in priority order)
task1 = Task("Walk", 30, priority=1, frequency="daily", due_datetime=datetime.now() + timedelta(hours=1))
task2 = Task("Feed", 10, priority=3, frequency="daily", due_datetime=datetime.now() + timedelta(hours=2))
task3 = Task("Play", 20, priority=2, frequency="daily", due_datetime=datetime.now() + timedelta(hours=3))
task4 = Task("Groom", 45, priority=4, frequency="weekly", due_datetime=datetime.now() + timedelta(days=1))
task5 = Task("Vet Check", 60, priority=1, frequency="monthly", due_datetime=datetime.now() + timedelta(days=7))

# Assign tasks to pets
owner.add_task(task1, pet=pet1)
owner.add_task(task2, pet=pet2)
owner.add_task(task3, pet=pet1)
owner.add_task(task4, pet=pet2)
owner.add_task(task5, pet=pet1)

# Add a conflicting task for Luna
task6 = Task("Brush", 20, priority=2, due_datetime=datetime.now() + timedelta(hours=1, minutes=15))
owner.add_task(task6, pet=pet1)

schedule = Schedule(owner)
# Add tasks to schedule (out of order)
schedule.add_task(task3)  # priority 2
schedule.add_task(task1)  # priority 1
schedule.add_task(task5)  # priority 1
schedule.add_task(task2)  # done
schedule.add_task(task4)  # done
schedule.add_task(task6)  # conflicting

# Mark some tasks as done
schedule.mark_task_complete(task2)
schedule.mark_task_complete(task4)

print("\n=== SCHEDULE PLAN (Sorted by Priority) ===")
for task in schedule.generate_plan():
    print(f"  {task.summary()}")

print("\n=== NEXT TASK ===")
next_task = schedule.next_task()
if next_task:
    print(f"  {next_task.summary()}")
else:
    print("  No pending tasks")

print("\n=== FILTERED: Pending Tasks ===")
for task in schedule.filter_tasks(status="pending"):
    print(f"  {task.summary()}")

print("\n=== FILTERED: Tasks for Luna ===")
for task in schedule.filter_tasks(pet_name="Luna"):
    print(f"  {task.summary()}")

print("\n=== FILTERED: Pending Tasks for Whiskers ===")
for task in schedule.filter_tasks(status="pending", pet_name="Whiskers"):
    print(f"  {task.summary()}")
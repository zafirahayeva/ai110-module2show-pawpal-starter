from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task, Schedule

owner = Owner("Zafirah", "zafi@example.com")
pet = Pet("Dog", "Luna", 4)
owner.add_pet(pet)

task1 = Task("Walk", 30, priority=1, frequency="daily", due_datetime=datetime.now() + timedelta(hours=1))
owner.add_task(task1, pet=pet)

schedule = Schedule(owner)
schedule.add_task(task1)

# print(schedule.generate_plan()[0].summary())
# print(schedule.next_task().summary())
print("\n=== SCHEDULE PLAN ===")
for task in schedule.generate_plan():
    print(f"  {task.summary()}")

print("\n=== NEXT TASK ===")
print(f"  {schedule.next_task().summary()}")
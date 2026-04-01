import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Setup Owner and Pet")
owner_name = st.text_input("Owner name", value="Jordan")
owner_email = st.text_input("Owner email", value="jordan@example.com")
pet_name = st.text_input("Pet name", value="Mochi")
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=2)
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Initialize Owner and Pet"):
    if 'owner' not in st.session_state:
        owner = Owner(name=owner_name, email=owner_email)
        pet = Pet(species=species, name=pet_name, age=pet_age)
        owner.add_pet(pet)
        st.session_state.owner = owner
        st.success("Owner and pet initialized!")
    else:
        st.info("Owner and pet already initialized.")

st.markdown("### Add Tasks")
st.caption("Add tasks for your pet. These will be scheduled automatically.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)

priority_map = {"high": 1, "medium": 3, "low": 5}
priority = priority_map[priority_str]

if st.button("Add task"):
    if 'owner' in st.session_state:
        owner = st.session_state.owner
        if owner.pets:
            pet = owner.pets[0]  # Assume one pet for now
            task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
            owner.add_task(task, pet)
            st.success(f"Task '{task_title}' added!")
        else:
            st.error("No pet found. Initialize owner and pet first.")
    else:
        st.error("Initialize owner and pet first.")

if 'owner' in st.session_state:
    owner = st.session_state.owner
    tasks = owner.all_tasks()
    if tasks:
        st.write("Current tasks:")
        task_data = [{"Title": t.title, "Duration": f"{t.duration_minutes}m", "Priority": t.priority, "Status": t.status} for t in tasks]
        st.table(task_data)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Initialize owner and pet to add tasks.")

st.divider()

st.subheader("Generate Schedule")
st.caption("Generate a prioritized schedule for your pet care tasks.")

if st.button("Generate schedule"):
    if 'owner' in st.session_state:
        owner = st.session_state.owner
        if owner.tasks:
            schedule = Schedule(owner)
            for task in owner.tasks:
                schedule.add_task(task)
            plan = schedule.generate_plan()
            st.success("Schedule generated!")
            st.write("### Scheduled Tasks (by priority):")
            for i, task in enumerate(plan, 1):
                st.write(f"{i}. {task.summary()}")
        else:
            st.warning("No tasks to schedule. Add some tasks first.")
    else:
        st.error("Initialize owner and pet first.")

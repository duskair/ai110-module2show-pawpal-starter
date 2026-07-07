import streamlit as st

# Step 1: bring the logic layer into the UI.
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a pet owner plan daily care tasks for their pets based on
constraints like time and priority.
"""
)

# Step 2: manage application memory.
# Streamlit reruns this script top-to-bottom on every interaction, so we keep
# a single Owner instance in st.session_state instead of recreating it (which
# would wipe out all pets/tasks on each rerun).
PRIORITY_LABELS = {1: "high", 2: "medium", 3: "low"}
PRIORITY_VALUES = {"high": 1, "medium": 2, "low": 3}

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner: Owner = st.session_state.owner

st.divider()

# --- Owner + pet setup ---
st.subheader("Owner & Pets")
owner.name = st.text_input("Owner name", value=owner.name)

with st.form("add_pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

# Step 3: wire the UI action to the logic method.
if add_pet:
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), species=species))
        st.success(f"Added {pet_name.strip()} ({species}).")
    else:
        st.warning("Please enter a pet name.")

if owner.pets:
    st.caption("Current pets: " + ", ".join(owner.pets.keys()))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Task assignment ---
st.subheader("Add a Task")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        target_pet = st.selectbox("For pet", list(owner.pets.keys()))
        task_title = st.text_input("Task title", value="Morning walk")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            task_time = st.text_input("Time (HH:MM)", value="08:00")
        with c2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with c3:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        with c4:
            frequency = st.selectbox("Repeats", ["daily", "weekly", "once"])
        add_task = st.form_submit_button("Add task")

    if add_task:
        pet = owner.get_pet(target_pet)
        pet.add_task(
            Task(
                description=task_title,
                time=task_time,
                duration=int(duration),
                priority=PRIORITY_VALUES[priority],
                frequency=frequency,
            )
        )
        st.success(f"Added '{task_title}' ({frequency}) for {target_pet}.")
else:
    st.info("Add a pet before assigning tasks.")

st.divider()

# --- Schedule ---
st.subheader("Daily Plan")
if st.button("Generate schedule"):
    st.session_state.show_plan = True

if st.session_state.get("show_plan"):
    # Surface conflicts FIRST so a busy owner sees double-bookings before the plan.
    warnings = Scheduler.conflict_warnings(owner.all_tasks())
    for warning in warnings:
        st.warning(warning)
    if not warnings:
        st.success("No scheduling conflicts — you're all set! 🐾")

    plan = Scheduler.build_daily_plan(owner)
    if plan:
        rows = [
            {
                "time": t.time,
                "task": t.description,
                "duration (min)": t.duration,
                "priority": PRIORITY_LABELS.get(t.priority, t.priority),
            }
            for t in plan
        ]
        st.table(rows)
        st.caption(f"{len(plan)} task(s) planned, sorted by time then priority.")
    else:
        st.info("No pending daily tasks yet. Add one above.")

st.divider()

# --- Mark tasks complete (demonstrates recurrence) ---
st.subheader("Mark a Task Done")
st.caption("Completing a daily/weekly task automatically schedules its next occurrence.")
pending = Scheduler.filter_by_status(owner.all_tasks(), completed=False)
if pending:
    labels = {f"{t.time} — {t.description} ({t.frequency})": t for t in pending}
    choice = st.selectbox("Pending tasks", list(labels.keys()))
    if st.button("Complete task"):
        task = labels[choice]
        # Find the owning pet so the follow-up occurrence lands on it.
        for pet in owner.pets.values():
            if task in pet.tasks:
                follow_up = pet.complete_task(task)
                st.success(f"Completed '{task.description}'.")
                if follow_up is not None:
                    st.info(f"Next '{follow_up.description}' scheduled for {follow_up.due_date}.")
                break
else:
    st.info("No pending tasks to complete.")

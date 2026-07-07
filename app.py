import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet care management assistant.")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# --- Application "memory" -------------------------------------------------
# Streamlit reruns this script top-to-bottom on every interaction, so we store
# the Owner in st.session_state to keep pets/tasks alive across reruns.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner: Owner = st.session_state.owner

# --- Owner info -----------------------------------------------------------
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Add a pet ------------------------------------------------------------
st.subheader("🐶 Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Biscuit")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if pet_name.strip():
            owner.add_pet(Pet(name=pet_name.strip(), species=species))
            st.success(f"Added {pet_name} the {species}!")
        else:
            st.error("Please enter a pet name.")

# --- Add a task -----------------------------------------------------------
st.subheader("📋 Add a Task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_names = [pet.name for pet in owner.pets]
        target_pet_name = st.selectbox("For which pet?", pet_names)
        col1, col2, col3 = st.columns(3)
        with col1:
            description = st.text_input("Task", value="Morning walk")
        with col2:
            task_time = st.text_input("Time (HH:MM)", value="08:00")
        with col3:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            target_pet = next(p for p in owner.pets if p.name == target_pet_name)
            target_pet.add_task(
                Task(description=description, time=task_time, frequency=frequency)
            )
            st.success(f"Added '{description}' at {task_time} for {target_pet_name}.")

st.divider()

# --- Today's schedule -----------------------------------------------------
st.subheader("🗓️ Today's Schedule")
scheduler = Scheduler(owner)

if not owner.get_all_tasks():
    st.info("No tasks yet. Add a pet and some tasks above.")
else:
    # Conflict warnings from the Scheduler.
    for warning in scheduler.detect_conflicts():
        st.warning(warning)

    # A single, chronologically sorted table across all pets. We pair each task
    # with its pet name, then sort by the Scheduler's ordering.
    pet_of = {id(task): pet.name for pet in owner.pets for task in pet.tasks}
    rows = [
        {
            "Time": task.time,
            "Pet": pet_of[id(task)],
            "Task": task.description,
            "Frequency": task.frequency,
            "Done": "✅" if task.completed else "⬜",
        }
        for task in scheduler.todays_schedule()
    ]
    st.table(rows)

    pending = scheduler.filter_by_status(completed=False)
    done = scheduler.filter_by_status(completed=True)
    st.caption(f"{len(pending)} pending · {len(done)} completed")

    # --- Complete a task (shows recurrence in action) ---------------------
    if pending:
        st.markdown("**✔️ Complete a task**")
        labels = [
            f"{pet_of[id(t)]} — {t.time} {t.description} [{t.frequency}]"
            for t in pending
        ]
        choice = st.selectbox("Which task did you finish?", range(len(pending)),
                              format_func=lambda i: labels[i])
        if st.button("Mark complete"):
            follow_up = scheduler.complete_task(pending[choice])
            if follow_up is not None:
                st.success(
                    f"Done! Since it's a {follow_up.frequency} task, the next one "
                    f"is scheduled for {follow_up.due_date}."
                )
            else:
                st.success("Done! Marked complete.")
            st.rerun()

"""CLI demo for PawPal+.

Verifies the backend logic in pawpal_system.py before it's wired to the
Streamlit UI. Run with:  python main.py
"""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(owner: Owner) -> None:
    """Print each pet's tasks in a readable 'Today's Schedule' format."""
    print("=" * 40)
    print(f"Today's Schedule for {owner.name}")
    print("=" * 40)
    for pet in owner.pets:
        print(f"\n🐾 {pet.name} ({pet.species})")
        if not pet.tasks:
            print("   (no tasks scheduled)")
        for task in pet.tasks:
            status = "✅" if task.completed else "⬜"
            print(f"   {status} {task.time}  {task.description}  [{task.frequency}]")
    print()


def main() -> None:
    # 1. Create an owner and two pets.
    owner = Owner(name="Jordan")
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # 2. Add tasks OUT OF ORDER (to prove the scheduler sorts them).
    biscuit.add_task(Task(description="Dinner", time="18:00", frequency="daily"))
    biscuit.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    mochi.add_task(Task(description="Vet appointment", time="14:30", frequency="once"))
    mochi.add_task(Task(description="Litter box clean", time="09:00", frequency="daily"))
    # A deliberate conflict: both pets need attention at 08:00.
    mochi.add_task(Task(description="Morning meds", time="08:00", frequency="daily"))

    scheduler = Scheduler(owner)

    # 3. Show the schedule grouped by pet.
    print_schedule(owner)

    # 4. Show the SORTED, cross-pet schedule from the Scheduler.
    print("Sorted schedule (all pets, by time):")
    for task in scheduler.todays_schedule():
        print(f"   {task.time}  {task.description}")
    print()

    # 5. Conflict detection.
    print("Checking for conflicts...")
    conflicts = scheduler.detect_conflicts()
    for warning in conflicts:
        print(f"   {warning}")
    if not conflicts:
        print("   No conflicts found.")
    print()

    # 6. Recurring tasks: completing a daily task spawns tomorrow's instance.
    walk = biscuit.get_tasks()[1]  # "Morning walk", daily
    print(f"Completing Biscuit's '{walk.description}' (daily)...")
    follow_up = scheduler.complete_task(walk)
    print(f"   -> auto-created next occurrence due {follow_up.due_date}\n")

    print_schedule(owner)

    # 7. Filtering.
    pending = scheduler.filter_by_status(completed=False)
    print(f"Pending tasks: {len(pending)}   Completed tasks: "
          f"{len(scheduler.filter_by_status(completed=True))}")


if __name__ == "__main__":
    main()

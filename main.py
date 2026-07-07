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

    # 2. Add a few tasks with different times.
    biscuit.add_task(Task(description="Morning walk", time="08:00", frequency="daily"))
    biscuit.add_task(Task(description="Dinner", time="18:00", frequency="daily"))
    mochi.add_task(Task(description="Litter box clean", time="09:00", frequency="daily"))
    mochi.add_task(Task(description="Vet appointment", time="14:30", frequency="once"))

    # 3. Show the schedule, complete a task, and show it again.
    print_schedule(owner)

    print("Marking Biscuit's morning walk complete...\n")
    biscuit.tasks[0].mark_complete()

    print_schedule(owner)

    # 4. Report the total task count via the Scheduler.
    scheduler = Scheduler(owner)
    print(f"Total tasks tracked by scheduler: {len(scheduler.todays_schedule())}")


if __name__ == "__main__":
    main()

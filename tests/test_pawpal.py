"""Automated tests for the PawPal+ logic layer."""

from datetime import date

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


# --- Phase 2 basics -------------------------------------------------------

def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task's completed flag to True."""
    task = Task(description="Morning walk", time="08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a Pet increases that pet's task count by one."""
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(description="Dinner", time="18:00"))
    assert len(pet.get_tasks()) == 1


def test_owner_gathers_tasks_across_pets():
    """Owner.get_all_tasks collects tasks from every pet."""
    owner = Owner(name="Jordan")
    dog = Pet(name="Biscuit", species="dog")
    cat = Pet(name="Mochi", species="cat")
    dog.add_task(Task(description="Walk", time="08:00"))
    cat.add_task(Task(description="Feed", time="09:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    assert len(owner.get_all_tasks()) == 2


# --- Sorting --------------------------------------------------------------

def test_sort_returns_tasks_in_chronological_order():
    """Scheduler orders tasks by their HH:MM time, earliest first."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(description="Dinner", time="18:00"))
    pet.add_task(Task(description="Walk", time="08:00"))
    pet.add_task(Task(description="Lunch", time="12:30"))
    owner.add_pet(pet)

    times = [t.time for t in Scheduler(owner).todays_schedule()]
    assert times == ["08:00", "12:30", "18:00"]


# --- Filtering ------------------------------------------------------------

def test_filter_by_status_separates_done_and_pending():
    owner = Owner(name="Jordan")
    pet = Pet(name="Biscuit", species="dog")
    done = Task(description="Walk", time="08:00")
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(Task(description="Dinner", time="18:00"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert len(scheduler.filter_by_status(completed=True)) == 1
    assert len(scheduler.filter_by_status(completed=False)) == 1


def test_filter_by_pet_returns_only_that_pets_tasks():
    owner = Owner(name="Jordan")
    dog = Pet(name="Biscuit", species="dog")
    cat = Pet(name="Mochi", species="cat")
    dog.add_task(Task(description="Walk", time="08:00"))
    cat.add_task(Task(description="Feed", time="09:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    assert [t.description for t in scheduler.filter_by_pet("Mochi")] == ["Feed"]
    assert scheduler.filter_by_pet("Unknown") == []  # missing pet -> empty


# --- Recurrence -----------------------------------------------------------

def test_completing_daily_task_creates_next_day_instance():
    """Completing a daily task spawns a fresh task due the following day."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Biscuit", species="dog")
    walk = Task(
        description="Walk", time="08:00", frequency="daily", due_date=date(2026, 7, 7)
    )
    pet.add_task(walk)
    owner.add_pet(pet)

    follow_up = Scheduler(owner).complete_task(walk)

    assert walk.completed is True
    assert follow_up is not None
    assert follow_up.completed is False
    assert follow_up.due_date == date(2026, 7, 8)
    assert len(pet.get_tasks()) == 2  # original + next occurrence


def test_completing_weekly_task_advances_seven_days():
    task = Task(
        description="Bath", time="10:00", frequency="weekly", due_date=date(2026, 7, 7)
    )
    assert task.next_occurrence().due_date == date(2026, 7, 14)


def test_completing_one_off_task_creates_no_follow_up():
    owner = Owner(name="Jordan")
    pet = Pet(name="Biscuit", species="dog")
    vet = Task(description="Vet visit", time="14:00", frequency="once")
    pet.add_task(vet)
    owner.add_pet(pet)

    follow_up = Scheduler(owner).complete_task(vet)
    assert follow_up is None
    assert len(pet.get_tasks()) == 1


def test_next_occurrence_rejects_non_recurring_task():
    with pytest.raises(ValueError):
        Task(description="Vet visit", time="14:00", frequency="once").next_occurrence()


# --- Conflict detection ---------------------------------------------------

def test_detect_conflicts_flags_same_time_tasks():
    owner = Owner(name="Jordan")
    dog = Pet(name="Biscuit", species="dog")
    cat = Pet(name="Mochi", species="cat")
    dog.add_task(Task(description="Walk", time="08:00"))
    cat.add_task(Task(description="Meds", time="08:00"))
    owner.add_pet(dog)
    owner.add_pet(cat)

    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflict_when_times_differ():
    owner = Owner(name="Jordan")
    pet = Pet(name="Biscuit", species="dog")
    pet.add_task(Task(description="Walk", time="08:00"))
    pet.add_task(Task(description="Dinner", time="18:00"))
    owner.add_pet(pet)

    assert Scheduler(owner).detect_conflicts() == []


# --- Edge cases -----------------------------------------------------------

def test_pet_with_no_tasks_produces_empty_schedule():
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Biscuit", species="dog"))

    scheduler = Scheduler(owner)
    assert scheduler.todays_schedule() == []
    assert scheduler.detect_conflicts() == []

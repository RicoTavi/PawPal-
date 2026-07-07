"""PawPal+ logic layer.

Class skeletons generated from the UML in diagrams/uml.mmd (Phase 1).
Method bodies are implemented in Phase 2 — for now they are stubs.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """A single pet-care activity (walk, feeding, medication, etc.)."""

    description: str
    time: str  # 24-hour "HH:MM"
    frequency: str = "once"  # "once" | "daily" | "weekly"
    completed: bool = False
    due_date: date | None = None

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self) -> "Task":
        """Return a fresh Task for the next daily/weekly occurrence."""
        step = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}.get(
            self.frequency
        )
        if step is None:
            raise ValueError(f"{self.frequency!r} tasks do not recur")
        base = self.due_date or date.today()
        return Task(
            description=self.description,
            time=self.time,
            frequency=self.frequency,
            completed=False,
            due_date=base + step,
        )


@dataclass
class Pet:
    """A pet, along with the care tasks that belong to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The 'brain': organizes and reasons about tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def todays_schedule(self) -> list[Task]:
        """Return all of the owner's tasks sorted chronologically by time."""
        return self.sort_by_time(self.owner.get_all_tasks())

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted chronologically by their HH:MM time."""
        return sorted(tasks, key=lambda task: task.time)

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the given completion status."""
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks belonging to the named pet (empty list if not found)."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.get_tasks()
        return []

    def detect_conflicts(self) -> list[str]:
        """Return a warning per time slot that has more than one task."""
        by_time: dict[str, list[str]] = defaultdict(list)
        for pet in self.owner.pets:
            for task in pet.tasks:
                by_time[task.time].append(f"{pet.name}'s {task.description}")
        warnings = []
        for time in sorted(by_time):
            if len(by_time[time]) > 1:
                warnings.append(
                    f"⚠️ Conflict at {time}: " + " & ".join(by_time[time])
                )
        return warnings

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task complete; if recurring, add its next occurrence.

        Returns the newly created follow-up Task, or None for one-off tasks.
        """
        task.mark_complete()
        if task.frequency not in ("daily", "weekly"):
            return None
        follow_up = task.next_occurrence()
        for pet in self.owner.pets:
            if task in pet.tasks:
                pet.add_task(follow_up)
                break
        return follow_up

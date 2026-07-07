"""PawPal+ logic layer.

Class skeletons generated from the UML in diagrams/uml.mmd (Phase 1).
Method bodies are implemented in Phase 2 — for now they are stubs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


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
        raise NotImplementedError

    def next_occurrence(self) -> "Task":
        """Return the next Task instance for a recurring (daily/weekly) task."""
        raise NotImplementedError


@dataclass
class Pet:
    """A pet, along with the care tasks that belong to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        raise NotImplementedError

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        raise NotImplementedError


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        raise NotImplementedError

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of the owner's pets."""
        raise NotImplementedError


class Scheduler:
    """The 'brain': organizes and reasons about tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def todays_schedule(self) -> list[Task]:
        """Return today's tasks, ordered for display."""
        raise NotImplementedError

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted chronologically by their HH:MM time."""
        raise NotImplementedError

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the given completion status."""
        raise NotImplementedError

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks belonging to the named pet."""
        raise NotImplementedError

    def detect_conflicts(self) -> list[str]:
        """Return warning strings for tasks scheduled at the same time."""
        raise NotImplementedError

    def complete_task(self, task: Task) -> None:
        """Complete a task, spawning its next occurrence if recurring."""
        raise NotImplementedError

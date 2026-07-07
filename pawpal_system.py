"""PawPal+ system classes.

Implements the design from diagrams/uml.mmd: Owner holds Pets, each Pet
holds Tasks, and Scheduler is a stateless utility that sorts, filters,
detects conflicts, and plans tasks across all of an owner's pets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """A single pet care task."""

    description: str
    time: str  # "HH:MM"
    duration: int  # minutes
    priority: int  # 1 = High, 3 = Low
    frequency: str = "daily"  # "daily", "weekly", or "once"
    completed: bool = False
    due_date: date | None = None

    def mark_complete(self) -> "Task | None":
        """Mark this task done; return its next occurrence if recurring, else None."""
        self.completed = True
        return self.next_occurrence()

    def next_occurrence(self) -> "Task | None":
        """Build the next instance of a recurring task using timedelta, or None."""
        deltas = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}
        if self.frequency not in deltas:
            return None
        base = self.due_date or date.today()
        return Task(
            description=self.description,
            time=self.time,
            duration=self.duration,
            priority=self.priority,
            frequency=self.frequency,
            completed=False,
            due_date=base + deltas[self.frequency],
        )


@dataclass
class Pet:
    """A pet and its care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Detach a task from this pet (no error if it isn't present)."""
        if task in self.tasks:
            self.tasks.remove(task)

    def complete_task(self, task: Task) -> Task | None:
        """Complete a task and, if recurring, queue its next occurrence on this pet."""
        follow_up = task.mark_complete()
        if follow_up is not None:
            self.add_task(follow_up)
        return follow_up


@dataclass
class Owner:
    """The pet owner and the pets they care for."""

    name: str
    pets: dict[str, Pet] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet, keyed by its name."""
        self.pets[pet.name] = pet

    def get_pet(self, name: str) -> Pet:
        """Look up a pet by name, or None if not found."""
        return self.pets.get(name)

    def all_tasks(self) -> list[Task]:
        """Every task across every pet."""
        tasks: list[Task] = []
        for pet in self.pets.values():
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    """Stateless utility for sorting, filtering, planning, and conflict-checking tasks."""

    @staticmethod
    def sort_by_time(tasks: list[Task]) -> list[Task]:
        """Sort tasks by "HH:MM" time, breaking ties by priority (1 = High first)."""
        return sorted(tasks, key=lambda t: (t.time, t.priority))

    @staticmethod
    def filter_by_status(tasks: list[Task], completed: bool = False) -> list[Task]:
        """Keep only tasks whose completion status matches `completed`."""
        return [t for t in tasks if t.completed == completed]

    @staticmethod
    def filter_by_pet(owner: Owner, pet_name: str) -> list[Task]:
        """Return the tasks belonging to a single named pet (empty if unknown)."""
        pet = owner.get_pet(pet_name)
        return list(pet.tasks) if pet else []

    @staticmethod
    def filter_by_frequency(tasks: list[Task], frequency: str = "daily") -> list[Task]:
        """Keep only tasks matching the given frequency (default: daily)."""
        return [t for t in tasks if t.frequency == frequency]

    @staticmethod
    def find_conflicts(tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Return pairs of tasks scheduled at the exact same "HH:MM" time.

        Tradeoff: only exact collisions are caught, not overlapping durations.
        This keeps the check simple and fast for a daily planner.
        """
        conflicts: list[tuple[Task, Task]] = []
        ordered = Scheduler.sort_by_time(tasks)
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                if ordered[i].time == ordered[j].time:
                    conflicts.append((ordered[i], ordered[j]))
        return conflicts

    @staticmethod
    def conflict_warnings(tasks: list[Task]) -> list[str]:
        """Turn detected conflicts into human-readable warning strings (never raises)."""
        return [
            f"⚠️ Conflict at {a.time}: '{a.description}' overlaps '{b.description}'"
            for a, b in Scheduler.find_conflicts(tasks)
        ]

    @staticmethod
    def build_daily_plan(owner: Owner) -> list[Task]:
        """Collect every pending daily task for the owner and order it for the day."""
        daily = Scheduler.filter_by_frequency(owner.all_tasks(), frequency="daily")
        pending = Scheduler.filter_by_status(daily, completed=False)
        return Scheduler.sort_by_time(pending)
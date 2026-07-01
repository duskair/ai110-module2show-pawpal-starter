"""PawPal+ system classes.

Skeleton generated from diagrams/uml.mmd. Method bodies are stubs
(no logic yet) — implement scheduling behavior in small increments.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care task."""

    description: str
    time: str  # "HH:MM"
    duration: int  # minutes
    priority: int  # 1 = High, 3 = Low
    frequency: str  # e.g. "daily", "weekly"


@dataclass
class Pet:
    """A pet and its care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        ...

    def remove_task(self, task: Task) -> None:
        ...


@dataclass
class Owner:
    """The pet owner and the pets they care for."""

    name: str
    pets: dict[str, Pet] = field(default_factory=dict)

    def add_pet(self, pet: Pet) -> None:
        ...

    def get_pet(self, name: str) -> Pet:
        ...


class Scheduler:
    """Utility class for sorting, filtering, and planning tasks."""

    @staticmethod
    def sort_tasks(tasks: list[Task]) -> list[Task]:
        ...

    @staticmethod
    def filter_tasks(tasks: list[Task]) -> list[Task]:
        ...

    @staticmethod
    def find_conflicts(tasks: list[Task]) -> list[Task]:
        ...

    @staticmethod
    def build_daily_plan(owner: Owner) -> list[Task]:
        ...

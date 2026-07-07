"""PawPal+ system classes.

Implements the design from diagrams/uml.mmd: Owner holds Pets, each Pet
holds Tasks, and Scheduler is a stateless utility that sorts, filters,
and plans tasks across all of an owner's pets.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care task."""

    description: str
    time: str  # "HH:MM"
    duration: int  # minutes
    priority: int  # 1 = High, 3 = Low
    frequency: str = "daily"  # e.g. "daily", "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


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
    """Stateless utility for sorting, filtering, and planning tasks."""

    @staticmethod
    def sort_tasks(tasks: list[Task]) -> list[Task]:
        """Order tasks by time, breaking ties by priority (1 = High first)."""
        return sorted(tasks, key=lambda t: (t.time, t.priority))

    @staticmethod
    def filter_tasks(tasks: list[Task], frequency: str = "daily") -> list[Task]:
        """Keep only tasks matching the given frequency (default: daily)."""
        return [t for t in tasks if t.frequency == frequency]

    @staticmethod
    def find_conflicts(tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Return pairs of tasks scheduled at the exact same time.

        Tradeoff: only exact "HH:MM" collisions are caught, not overlapping
        time blocks. This keeps the check simple and fast for a daily planner.
        """
        conflicts: list[tuple[Task, Task]] = []
        ordered = Scheduler.sort_tasks(tasks)
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                if ordered[i].time == ordered[j].time:
                    conflicts.append((ordered[i], ordered[j]))
        return conflicts

    @staticmethod
    def build_daily_plan(owner: Owner) -> list[Task]:
        """Collect every daily task for the owner and order it for the day."""
        daily = Scheduler.filter_tasks(owner.all_tasks(), frequency="daily")
        return Scheduler.sort_tasks(daily)

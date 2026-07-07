"""Automated tests for PawPal+ core behaviors.

Covers the happy paths (sorting, filtering, recurrence) and the edge cases
that matter for a pet scheduler (empty pet, exact-time conflicts).
"""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


# --- Basic object behavior ---

def test_mark_complete_changes_status():
    """Calling mark_complete() flips the task's status to done."""
    task = Task("Morning walk", "08:00", 30, priority=2)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task increases the pet's task count by one."""
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", "08:00", 10, priority=1))

    assert len(pet.tasks) == 1


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    """Tasks added out of order come back sorted by time."""
    tasks = [
        Task("Meds", "09:00", 5, priority=1),
        Task("Walk", "08:00", 30, priority=2),
        Task("Dinner", "18:00", 10, priority=1),
    ]

    ordered = Scheduler.sort_by_time(tasks)

    assert [t.time for t in ordered] == ["08:00", "09:00", "18:00"]


def test_sort_by_time_breaks_ties_by_priority():
    """Same time -> higher priority (lower number) comes first."""
    walk = Task("Walk", "08:00", 30, priority=2)
    feed = Task("Feed", "08:00", 10, priority=1)

    ordered = Scheduler.sort_by_time([walk, feed])

    assert ordered == [feed, walk]


# --- Recurrence logic ---

def test_completing_daily_task_creates_next_day_occurrence():
    """Marking a daily task complete creates a fresh task due the next day."""
    task = Task("Walk", "08:00", 30, priority=2, frequency="daily", due_date=date(2026, 7, 7))

    follow_up = task.mark_complete()

    assert follow_up is not None
    assert follow_up.completed is False
    assert follow_up.due_date == date(2026, 7, 8)
    assert follow_up.description == "Walk"


def test_completing_weekly_task_advances_seven_days():
    """A weekly task's next occurrence is seven days later."""
    task = Task("Bath", "10:00", 20, priority=3, frequency="weekly", due_date=date(2026, 7, 7))

    follow_up = task.mark_complete()

    assert follow_up.due_date == date(2026, 7, 7) + timedelta(weeks=1)


def test_one_off_task_has_no_next_occurrence():
    """A non-recurring task returns None when completed."""
    task = Task("Vet visit", "14:00", 60, priority=1, frequency="once")

    assert task.mark_complete() is None


def test_pet_complete_task_queues_next_occurrence():
    """complete_task adds the recurring follow-up back onto the pet."""
    pet = Pet(name="Biscuit", species="dog")
    walk = Task("Walk", "08:00", 30, priority=2, frequency="daily", due_date=date(2026, 7, 7))
    pet.add_task(walk)

    pet.complete_task(walk)

    assert len(pet.tasks) == 2
    assert any(not t.completed and t.due_date == date(2026, 7, 8) for t in pet.tasks)


# --- Conflict detection ---

def test_find_conflicts_flags_duplicate_times():
    """Two tasks at the exact same time are reported as a conflict."""
    walk = Task("Walk", "08:00", 30, priority=2)
    feed = Task("Feed", "08:00", 10, priority=1)
    meds = Task("Meds", "09:00", 5, priority=1)

    conflicts = Scheduler.find_conflicts([walk, feed, meds])

    assert len(conflicts) == 1


def test_conflict_warnings_returns_readable_message():
    """conflict_warnings returns a human-readable string, not an exception."""
    tasks = [Task("Walk", "08:00", 30, priority=2), Task("Feed", "08:00", 10, priority=1)]

    warnings = Scheduler.conflict_warnings(tasks)

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflicts_returns_empty_list():
    """Distinct times produce no conflicts."""
    tasks = [Task("Walk", "08:00", 30, priority=2), Task("Meds", "09:00", 5, priority=1)]

    assert Scheduler.find_conflicts(tasks) == []


# --- Edge cases ---

def test_empty_pet_produces_empty_plan():
    """An owner whose pet has no tasks yields an empty daily plan."""
    owner = Owner(name="Jordan")
    owner.add_pet(Pet(name="Mochi", species="cat"))

    assert Scheduler.build_daily_plan(owner) == []


def test_build_daily_plan_excludes_completed_tasks():
    """Completed tasks should not appear in the day's pending plan."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Biscuit", species="dog")
    owner.add_pet(pet)
    done = Task("Walk", "08:00", 30, priority=2)
    done.mark_complete()
    pet.add_task(done)
    pet.add_task(Task("Meds", "09:00", 5, priority=1))

    plan = Scheduler.build_daily_plan(owner)

    assert [t.description for t in plan] == ["Meds"]
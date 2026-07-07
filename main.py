"""CLI demo for PawPal+.

Exercises sorting, filtering, conflict detection, and recurring tasks.
Run with: python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler

PRIORITY_LABELS = {1: "high", 2: "medium", 3: "low"}


def show(task: Task) -> str:
    label = PRIORITY_LABELS.get(task.priority, str(task.priority))
    mark = "x" if task.completed else " "
    return f"[{mark}] {task.time} — {task.description} ({task.duration} min) [priority: {label}]"


def main() -> None:
    owner = Owner(name="Jordan")

    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Add tasks intentionally OUT OF ORDER to prove sorting works.
    biscuit.add_task(Task("Give medicine", "09:00", 5, priority=1))
    biscuit.add_task(Task("Morning walk", "08:00", 30, priority=2))
    mochi.add_task(Task("Feeding", "08:00", 10, priority=1))  # conflicts with the walk

    # --- Sorting ---
    print("Daily plan for", owner.name, "(sorted by time, then priority):")
    for task in Scheduler.build_daily_plan(owner):
        print(" ", show(task))

    # --- Conflict detection (returns warnings, never crashes) ---
    print("\nConflict check:")
    warnings = Scheduler.conflict_warnings(owner.all_tasks())
    for w in warnings or ["  none found"]:
        print(" ", w)

    # --- Filtering by pet ---
    print("\nBiscuit's tasks only:")
    for task in Scheduler.sort_by_time(Scheduler.filter_by_pet(owner, "Biscuit")):
        print(" ", show(task))

    # --- Recurring task: completing a daily task queues the next occurrence ---
    print("\nCompleting Biscuit's morning walk (daily → auto-reschedules):")
    walk = biscuit.tasks[1]
    follow_up = biscuit.complete_task(walk)
    print("  completed:", show(walk))
    if follow_up:
        print("  next occurrence due:", follow_up.due_date)

    # --- Filtering by status ---
    pending = Scheduler.filter_by_status(owner.all_tasks(), completed=False)
    done = Scheduler.filter_by_status(owner.all_tasks(), completed=True)
    print(f"\nStatus summary: {len(pending)} pending, {len(done)} completed")


if __name__ == "__main__":
    main()
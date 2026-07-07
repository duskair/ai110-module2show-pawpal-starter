"""CLI demo for PawPal+.

Builds a small owner/pet/task scenario and prints the generated daily plan.
Run with: python main.py
"""

from pawpal_system import Owner, Pet, Task, Scheduler

PRIORITY_LABELS = {1: "high", 2: "medium", 3: "low"}


def main() -> None:
    # 1. Create an owner.
    owner = Owner(name="Jordan")

    # 2. Add two pets.
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # 3. Assign three tasks across the pets.
    biscuit.add_task(Task("Morning walk", "08:00", 30, priority=2))
    biscuit.add_task(Task("Give medicine", "09:00", 5, priority=1))
    mochi.add_task(Task("Feeding", "08:00", 10, priority=1))

    # Build and print the daily plan.
    plan = Scheduler.build_daily_plan(owner)

    print(f"Daily plan for {owner.name}:")
    for task in plan:
        label = PRIORITY_LABELS.get(task.priority, str(task.priority))
        print(f"  {task.time} — {task.description} ({task.duration} min) [priority: {label}]")

    # Flag any exact-time conflicts.
    conflicts = Scheduler.find_conflicts(owner.all_tasks())
    if conflicts:
        print("\nConflicts (same time slot):")
        for a, b in conflicts:
            print(f"  {a.time}: '{a.description}' vs '{b.description}'")


if __name__ == "__main__":
    main()

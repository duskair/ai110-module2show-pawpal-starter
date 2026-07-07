"""Basic tests for PawPal+ core behaviors."""

from pawpal_system import Pet, Task


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

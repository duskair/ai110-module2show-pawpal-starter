# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Daily plan for Jordan:
  08:00 — Morning walk (30 min) [priority: medium]
  09:00 — Give medicine (5 min) [priority: high]
  10:00 — Feeding (10 min) [priority: high]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
pytest --cov
```

**What the tests cover** (`tests/test_pawpal.py`, 13 tests):

- **Object behavior** — `mark_complete()` flips status; `add_task()` grows the pet's task list.
- **Sorting correctness** — out-of-order tasks return in chronological order, with priority breaking exact-time ties.
- **Recurrence logic** — completing a `daily` task creates a follow-up due the next day; `weekly` advances 7 days; `once` returns none; `Pet.complete_task()` re-queues the follow-up.
- **Conflict detection** — duplicate times are flagged and surfaced as readable warnings; distinct times produce none.
- **Edge cases** — a pet with no tasks yields an empty plan; completed tasks are excluded from the daily plan.

Successful test run:

```
============================= test session starts =============================
platform win32 -- Python 3.12.0, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\cynth\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 13 items

tests\test_pawpal.py .............                                       [100%]

============================= 13 passed in 0.06s ==============================
```

**Confidence level: ★★★★☆ (4/5)** — Core sorting, recurrence, and conflict logic are well covered and green. Docked one star because conflict detection only catches exact `"HH:MM"` matches (not overlapping durations), and time strings aren't yet validated.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by `"HH:MM"` time; ties broken by priority (1 = High first) via a `sorted()` key lambda. |
| Filtering | `Scheduler.filter_by_pet()`, `Scheduler.filter_by_status()`, `Scheduler.filter_by_frequency()` | Narrow tasks by pet name, completion status, or frequency. |
| Conflict handling | `Scheduler.find_conflicts()`, `Scheduler.conflict_warnings()` | Detects exact same-time collisions; returns human-readable warnings instead of raising. |
| Recurring tasks | `Task.mark_complete()`, `Task.next_occurrence()`, `Pet.complete_task()` | Completing a `daily`/`weekly` task auto-creates the next occurrence using `timedelta`. |
| Daily plan | `Scheduler.build_daily_plan()` | Collects all pending daily tasks across pets and sorts them for the day. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

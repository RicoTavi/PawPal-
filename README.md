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

Running the CLI demo (`python main.py`) exercises sorting, conflict detection,
recurrence, and filtering:

```
========================================
Today's Schedule for Jordan
========================================

🐾 Biscuit (dog)
   ⬜ 18:00  Dinner  [daily]
   ⬜ 08:00  Morning walk  [daily]

🐾 Mochi (cat)
   ⬜ 14:30  Vet appointment  [once]
   ⬜ 09:00  Litter box clean  [daily]
   ⬜ 08:00  Morning meds  [daily]

Sorted schedule (all pets, by time):
   08:00  Morning walk
   08:00  Morning meds
   09:00  Litter box clean
   14:30  Vet appointment
   18:00  Dinner

Checking for conflicts...
   ⚠️ Conflict at 08:00: Biscuit's Morning walk & Mochi's Morning meds

Completing Biscuit's 'Morning walk' (daily)...
   -> auto-created next occurrence due 2026-07-08

Pending tasks: 5   Completed tasks: 1
```

## 🧪 Testing PawPal+

Run the automated suite from the project root:

```bash
python -m pytest
```

The suite (`tests/test_pawpal.py`) covers the core behaviors and edge cases:

- **Basics** — `mark_complete` flips status; adding a task grows a pet's task
  count; `Owner` gathers tasks across pets.
- **Sorting** — tasks are returned in chronological `HH:MM` order.
- **Filtering** — by completion status and by pet (including an unknown pet).
- **Recurrence** — completing a daily task creates a next-day instance; weekly
  advances 7 days; one-off tasks create no follow-up; recurring a `once` task
  raises.
- **Conflict detection** — same-time tasks are flagged; different times are not.
- **Edge cases** — a pet with no tasks yields an empty, conflict-free schedule.

Sample test run:

```
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0
collected 13 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  7%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 15%]
tests/test_pawpal.py::test_owner_gathers_tasks_across_pets PASSED        [ 23%]
tests/test_pawpal.py::test_sort_returns_tasks_in_chronological_order PASSED [ 30%]
tests/test_pawpal.py::test_filter_by_status_separates_done_and_pending PASSED [ 38%]
tests/test_pawpal.py::test_filter_by_pet_returns_only_that_pets_tasks PASSED [ 46%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_day_instance PASSED [ 53%]
tests/test_pawpal.py::test_completing_weekly_task_advances_seven_days PASSED [ 61%]
tests/test_pawpal.py::test_completing_one_off_task_creates_no_follow_up PASSED [ 69%]
tests/test_pawpal.py::test_next_occurrence_rejects_non_recurring_task PASSED [ 76%]
tests/test_pawpal.py::test_detect_conflicts_flags_same_time_tasks PASSED [ 84%]
tests/test_pawpal.py::test_no_conflict_when_times_differ PASSED          [ 92%]
tests/test_pawpal.py::test_pet_with_no_tasks_produces_empty_schedule PASSED [100%]

============================== 13 passed in 0.03s ==============================
```

**Confidence level: ⭐⭐⭐⭐☆ (4/5).** All core scheduling behaviors are covered
and passing. Docking one star because conflict detection only matches exact
start times (durations/overlaps aren't modeled yet) — that's the first edge case
I'd test next.

## 📐 Smarter Scheduling

The `Scheduler` class in `pawpal_system.py` adds the algorithmic intelligence:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.todays_schedule()` | Sorts tasks chronologically by their `HH:MM` string via a `sorted()` key. |
| Filtering | `Scheduler.filter_by_status()`, `Scheduler.filter_by_pet()` | Filter by completion status (pending/done) or by pet name. |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags any time slot shared by more than one task and returns a warning string (never crashes). Exact-time match only — durations are not modeled. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.complete_task()` | Completing a `daily`/`weekly` task auto-creates the next instance using `timedelta` (`+1 day` / `+1 week`). |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

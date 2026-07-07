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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

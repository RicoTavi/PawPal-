# PawPal+ Project Reflection

## 1. System Design

**Three core actions a user can perform:**

1. **Add a pet** — register a pet (name + species) under the owner.
2. **Schedule a care task** — add a task (e.g., walk, feeding, medication) to a
   pet with a time (HH:MM) and a frequency (once/daily/weekly).
3. **View today's schedule** — see all tasks across every pet, sorted by time,
   with any same-time conflicts flagged.

**a. Initial design**

My initial UML has four classes with clear, separated responsibilities:

- **`Task`** (dataclass): holds one activity's data — description, time,
  frequency, completion status, and due date. It owns the small behaviors that
  only concern a single task (`mark_complete`, `next_occurrence`).
- **`Pet`** (dataclass): stores pet details and its own list of `Task`s, plus
  `add_task` / `get_tasks`. A pet knows nothing about scheduling — it's just a
  container for its tasks.
- **`Owner`**: manages a list of `Pet`s and provides `get_all_tasks` to gather
  every task across pets. This is the aggregation point.
- **`Scheduler`**: the "brain." It takes an `Owner` and does the algorithmic
  work — sorting, filtering, conflict detection, and recurrence — without
  storing any data of its own. Keeping the logic here means the data classes
  stay simple and the smart behavior lives in one place.

The relationships are compositional: an `Owner` has many `Pet`s, a `Pet` has
many `Task`s, and the `Scheduler` reads from the `Owner`.

**b. Design changes**

_(Filled in after implementation — Phase 2/4.)_

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

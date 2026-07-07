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

The biggest change came with recurring tasks. My first instinct was to put all
recurrence logic on `Task` (a task "reschedules itself"). During implementation
I split the responsibility: `Task.next_occurrence()` only builds the next
`Task` object (pure, easy to test), while `Scheduler.complete_task()` owns the
side effect of attaching that new task to the correct pet. This kept `Task`
free of any knowledge about pets or lists, and made recurrence testable in
isolation. I also added a `due_date` field so recurrence could compute real
dates with `timedelta` instead of just repeating a time string.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler reasons about three things: **time of day** (tasks are ordered
chronologically by their `HH:MM` value), **completion status** (pending vs.
done, used for filtering), and **frequency** (once/daily/weekly, which drives
recurrence). Time mattered most because a pet owner's real question is "what do
I need to do next?" — so a correctly ordered, conflict-aware timeline is the
core value. Status and frequency support that timeline rather than competing
with it.

**b. Tradeoffs**

My conflict detection only flags tasks that share the **exact same start time**;
it does not model task *durations* or detect overlapping windows. For example,
a 30-minute walk at 08:00 and a feeding at 08:15 would not be flagged even
though they overlap in practice. I chose exact-time matching because it's simple
to reason about, fast, and needs no duration data from the user — a reasonable
trade for a lightweight pet-care planner where most tasks are short and the
owner just needs a heads-up about obvious double-bookings. Modeling durations
would be the natural next iteration.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI as a phase-by-phase building partner rather than a one-shot code
generator. We worked through the project in order — UML, then class skeletons,
then core logic, then the algorithmic layer, then tests, then the UI — and I
reviewed the output at each checkpoint before moving on. The most helpful prompts
were scoped and concrete: "generate dataclass skeletons from this UML," "implement
recurrence with `timedelta`," "add tests for sorting, recurrence, and conflicts."
Keeping each request tied to a single phase made the AI's output easy to check and
kept the design from drifting.

**b. Judgment and verification**

The clearest moment was when the AI reported that the Streamlit UI "worked." I
didn't accept that at face value — a claim that code runs isn't evidence that it
does. I had it *prove* the UI by driving the app headlessly with Streamlit's
`AppTest`: adding a pet, adding a task, and completing a recurring task, then
asserting that the objects actually persisted in `st.session_state` and that a
follow-up task was created. Only after seeing those assertions pass did I trust
the integration. More generally, I verified AI output by running `python main.py`
and `python -m pytest` after every change instead of reading the code and
assuming it was correct.

---

## 4. Testing and Verification

**a. What you tested**

I wrote 13 tests covering the behaviors most likely to break or matter most:
chronological sorting, filtering by status and by pet (including an unknown
pet), recurrence (daily → next day, weekly → +7 days, one-off → no follow-up,
and that recurring a `once` task raises), conflict detection (same time flagged,
different times not), and the empty edge case of a pet with no tasks. These were
important because they *are* the product — a scheduler that sorts wrong, drops
tasks, or silently mishandles recurrence would give the owner a wrong plan. I
used a fixed `due_date` in the recurrence tests so they don't depend on the
current date.

**b. Confidence**

Fairly confident — 4 out of 5. Every core path is tested and green. The main
gap I'm aware of is that conflict detection only compares exact start times, so
overlapping *durations* aren't caught. With more time I'd test tasks that
overlap without sharing a start time, invalid time strings (e.g. `"25:00"`),
and recurrence across month/year boundaries.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the clean separation of responsibilities and how well the
CLI-first workflow paid off. Because the backend logic was solid and tested before
I touched the UI, wiring up Streamlit was quick and low-drama — the hard thinking
was already done. The recurrence feature working end-to-end (complete a daily task
in the browser and watch tomorrow's task appear) is the moment it felt like a real
product.

**b. What you would improve**

I'd upgrade conflict detection from exact-time matching to true overlap detection
by giving tasks a duration, so a 08:00 walk and an 08:15 feeding could be flagged.
I'd also add input validation on the time field (reject values like `"25:00"`) and
persist pets/tasks to disk so data survives a restart.

**c. Key takeaway**

AI executes; I decide. The AI was genuinely fast at turning a design into working
code, but the important calls — how to split responsibilities between classes, what
tradeoffs were acceptable, and whether a result could actually be trusted — were
mine to own. Being the "lead architect" meant setting the structure up front,
verifying every claim, and treating the AI as a very capable implementer working
under my direction rather than an oracle to defer to.

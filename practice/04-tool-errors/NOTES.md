# Lesson 04 — build notes

Goal: **three strings.** Not a number this time. The strings are the deliverable — write them
here first, then make the code return them.

Run with `uv run python practice/04-tool-errors/failing_tools.py "<name>"`.
The loop prints every `tool_result` exactly as the model receives it.

## 1. Watch it fail

Run it for `Marcus Dubois` and for `priya raman`. Read the printed `tool_result` — the string
the model was handed — and then read the final answer it gave the user.

- `Marcus Dubois` — what the model was told →

      what it then told the user →

- `priya raman` — what the model was told →

      what it then told the user →

- Did either run retry the same call? How many API calls? →

## 2. Write the three strings — BEFORE touching the code

This is the deliverable. Paste these three into the terminal when you are done.

**a. Unknown customer name.** (`is_error: true`)

>

**b. Marcus Dubois.** One order, NW-4421, promised 2025-09-18, never shipped, no tickets.
Decide first whether `is_error` belongs on this at all.

>

**c. Priya Raman with nothing late.** (Pretend both her orders arrived on time.)

>

Check each against the three beats: *what happened*, *why*, *what to do instead*.

## 3. Make them true

Fix `failing_tools.py` so it returns exactly what you wrote above.

- [ ] Unknown name → a real error result, not a traceback
- [ ] Null `shipped_at_epoch_ms` → handled, and the overdue unshipped order **surfaced**
- [ ] Empty late-order list → an ordinary result that says so in words, no `is_error`

> Trap: `if o["shipped_at_epoch_ms"] is None: continue` stops the traceback and makes the
> agent say Marcus has no delivery problem. That is worse than the crash, because nothing
> will tell you it happened.

## 4. Re-run all three names

Final answer to the user, correct? (y/n)

- `Marcus Dubois` →
- `priya raman` →
- `Sofia Almeida` →

## 5. One line, out loud

Which of the three failures should not have been an error message at all, but a change to
the tool?

>

## Questions for the teacher

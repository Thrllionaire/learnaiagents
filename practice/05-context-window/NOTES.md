# Lesson 05 — build notes

Run with `uv run python practice/05-context-window/growing_context.py`. It runs the same
tool as Lesson 03's `good_tools.py`, but as **one five-turn conversation** — `messages` is
never reset between turns, so turn 5 carries everything from turns 1-4 with it.

## 1. Watch it grow

Run it once, unmodified. For each turn, read the `input tokens (this turn)` and
`input tokens (cumulative)` lines it prints.

| turn | messages in context | input tokens (this turn) | cumulative |
|------|---------------------|---------------------------|------------|
| 1    |              3       |             1618              1618|            |
| 2    |               6      |                1922           |   3540         |
| 3    |                9     |                  2144         |   5684         |
| 4    |                  10   |                  1139         |   6823         |
| 5    |            11         |                    1164       |   7987         |

- Is turn 5 roughly 5&times; turn 1, or something faster than that? → yes

- Where do you think most of those tokens are going: the growing transcript, or the tool
  schema being resent five times? (You measured this trade-off once already, in Lesson 04 — growing transcript
  what's different about a five-turn run versus a two-call run?) → messages and cumulative input tokens

## 2. Add compaction

`compact(messages)` in `growing_context.py` is currently the identity function — it does
nothing. Make it real:

- [ x] Calls the model once (a plain `client.messages.create`, no tools) asking it to
      summarize everything in `messages` into the facts a support agent handing off this
      conversation would need to keep going
- [x ] Returns a **new** messages list containing just that summary as a single user turn
- [x ] Wire it into `run_turn` (or between turns in `__main__`) behind a condition you choose
      — message count, cumulative tokens, or a fixed turn number are all defensible; pick
      one and say why in step 4

> You are the one deciding *when* to compact. There is no framework doing this for you —
> that decision is the entire skill.

## 3. Re-run and compare

Run it again with compaction wired in. Cumulative tokens after turn 5, before and after:

- Before → 7987
- After → 1763

## 4. Break it on purpose

Turn 4 asks "whose ticket is most urgent" and turn 5 asks for a summary of all three
customers. If compaction fires **before** turn 4, does the answer to turn 4 still correctly
mention all three customers — including the ones the summary compressed?

- What you chose to trigger compaction on, and why → based on cumulative tokens because of the cost

- Did turn 4 or 5 lose anything a real support agent would have needed? → yes

## 5. One line, out loud

Compaction traded tokens for something. Name the specific fact (not "some detail") that a
tighter summary could plausibly have dropped, and say whether losing it would matter here.

> if summary misses one of the persons in the conversation, it's a loss in further conversations

## Questions for the teacher

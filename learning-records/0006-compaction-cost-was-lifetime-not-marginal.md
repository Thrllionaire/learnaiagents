# The compaction bug was bigger than "count one more call" — it was discarding history

Lesson 05's build task asked him to notice that `compact()`'s own summarization call has a
token cost. He found the right symptom (before/after didn't look apples-to-apples) but
proposed the wrong fix: add `response.usage.output_tokens` to `cumulative`.

## Why that fix was wrong

`cumulative` in `growing_context.py` only ever tracked `input_tokens` — deliberately, since
window growth (this lesson's subject) is an input-token phenomenon, distinct from the
output-token cost dimension Lesson 02 measured separately. Adding `output_tokens` here would
have blurred two metrics the course has kept apart on purpose.

## The real bug

`cumulative = 0` after a compaction fire didn't just drop the compaction call's own cost —
it discarded turns 1–3's cost from the total *entirely*. His reported "after" figure (1763)
was turn 4 + turn 5 only, not the whole run's cost with compaction included. Compared against
the naive run's 7987, that overstates the savings by roughly 3x.

The fix separates two things that were living in one variable:
1. **Lifetime total** (`total_input_tokens`) — every turn's cost plus every compaction call's
   cost, monotonically increasing, never reset. This is the number worth reporting.
2. **Trigger signal** (`last_turn_tokens`) — the size of the *current* window, which is what
   should decide whether to compact. Conflating this with the lifetime total is what made
   resetting look necessary in the first place.

## Read on this

Consistent with the pattern in [[0005-lesson-04-closed-in-conversation]]: the instinct to
notice something's off was right and came quickly. The fix proposed without being asked to
re-derive it was wrong in a specific, diagnosable way (reached for the other token count that
was on screen — `output_tokens` — rather than tracing why the *existing* number was wrong).
Worth watching in Lesson 06 (memory) whether, given a metric that looks off, he re-derives
what should be tracked from the definition, or pattern-matches to the nearest number already
visible.

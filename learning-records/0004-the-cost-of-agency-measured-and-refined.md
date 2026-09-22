# The cost of agency, measured — and two refinements to how Lesson 02 taught it

Lesson 02's build task was completed on 2026-09-20 (out of order, after Lesson 03). Same
question, same model (`claude-haiku-4-5`), two architectures:

|            | API calls | input tokens | output tokens |
|------------|-----------|--------------|---------------|
| Agent      | 2         | 1,511        | 163           |
| Workflow   | 1         | 67           | 45            |

**22.6× the input tokens** to produce the same sentence. The number he now owns.

Two refinements came out of the measurement that the lesson did not teach, and both are
sharper than what it did teach.

## 1. On short runs the tool schemas dominate, not the transcript

Lesson 02's recall question answers "why does an agent cost more?" with *the whole transcript
is re-sent every call* — quadratic growth in run length. True, and it is the right answer for a
ten-step run. But it does not explain **this** result. On a two-call run there is barely any
transcript to re-send; the 22.6× is mostly the **tool schemas**, which are sent in full on
every single call and which the workflow never sends at all. The workflow's 67 input tokens are
the entire prompt; the agent pays several hundred tokens per call just to describe what it
could do, before it does anything.

Statement worth using instead of the loose one: *an agent pays for its tool schemas on every
turn and its transcript on every turn after the first; which term dominates depends on run
length.*

## 2. Input-token ratio is not the cost ratio

At Haiku's $1/$5 per MTok, the same two runs cost **$0.00233 against $0.00029 — 8.0×**, not
22.6×. Output tokens are five times the price per token and the workflow's answer is nearly as
long as the agent's, so the cheap dimension is where the agent's advantage in verbosity is
largest. Quoting "22× the tokens" when the bill is 8× is the kind of imprecision that loses an
argument to anyone who checks. Pick the ratio that matches the claim: tokens for a context
argument, dollars for a budget argument, calls for a latency argument.

## Related: the Lesson 03 re-run contradicted a character-count prediction

`good_tools.py` after the description rewrite and the semantic result: **1,618 input tokens,
down from 1,630** — flat, where a character-count estimate predicted a rise of roughly 140.
Payload fell 735 → 244 characters while the tool definition grew ~250 → ~776.

The estimate was wrong because characters are a poor proxy for tokens and the two sides of the
trade have very different densities. UUIDs, 13-digit epoch milliseconds, and snake_case field
names fragment into many tokens per character; ordinary English prose is roughly four
characters per token. **Deleting identifiers buys more tokens than the same number of
characters of prose costs.** High-signal context is not only easier for the model to reason
over — it is cheaper per character than the identifiers it replaces.

Not yet measured directly. `client.messages.count_tokens` on the two payloads would settle it
in one call and is worth doing if the point comes up again.

## Still outstanding

The two *written* steps of Lesson 02 — the input that breaks the workflow, and the
ship-or-switch paragraph with a concrete trigger — remain blank, as does the Lesson 03
paragraph. Third occurrence of the pattern in
[[0003-consolidation-learned-description-still-documentation]]: measured steps get done,
written ones do not. Lesson 04 should treat the written artefact as the deliverable and ask
for it in conversation rather than leaving it as the last unticked box on a checklist.

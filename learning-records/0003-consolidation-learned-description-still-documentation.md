# Structure consolidated, text left behind: the description is still treated as documentation

Lesson 03's build task was completed and the headline win landed: `naive_tools.py` took three
tool calls and 4,112 input tokens; the redesigned `good_tools.py` took one tool call and 1,630,
a 2.5× reduction. The structural move — collapse a sequence a human would perform into one
tool — was made correctly and unaided.

The two *textual* moves from the same lesson were not made, and the shape of the omission is
the finding.

**1. The description was left stale.** `good_tools.py` defines
`"name": "list_late_orders_and_tickets"` with `"description": "Gets a customer record."` —
copy-pasted from the naive surface and never updated. This is the flaw he had correctly
identified in the lesson's audit widget twenty minutes earlier ("the description says nothing
the name does not"). Recognition in someone else's code did not transfer to production in his
own.

**2. The result was not transformed.** The tool computes *which* orders are late, then returns
the raw records: `uuid`, `customer_uuid`, `status_code`, `promised_at_epoch_ms`,
`line_total_minor_units`, `carrier_uuid`. The payload is 735 characters where a semantic
version of the same answer is 242 — roughly a third. The 2.5× ratio he measured is real but is
most of the available win left unclaimed, and the part left unclaimed is exactly the part that
looks like formatting rather than engineering.

**The unifying diagnosis:** the lesson's claim is "the schema and the result text are prompt,
not documentation." He accepted it as a proposition and acted on the half of it that shows up
as control flow. Changing a call graph feels like engineering; rewriting a description feels
like writing docs, and docs get deferred. The misconception from
[[0002-schema-dispatch-are-two-contracts]] has narrowed but not closed: he no longer forgets
that the schema is a separate contract, but he still under-weights what is written in it.

**Evidence also recorded:**
- Prediction miss in the safe direction: he guessed the endpoint-shaped surface would need
  **1** tool call; it needed 3. He predicted the consolidated answer for the naive surface,
  which suggests the cost of endpoint-shaped surfaces is understood in principle but not yet
  felt as a default expectation.
- Step 5 ("find what consolidation cost you") was answered with the *same* question the tool
  was built for, not a question the tool cannot answer. The trade-off — his tool hardcodes both
  lateness and `state_code == 1`, so it cannot answer "what is Priya's email" or "show closed
  tickets too" — was not articulated. This is the interview-grade half of the lesson and it did
  not land.
- The design-review paragraph was left blank, as was the "run the checklist over the four
  definitions" step. The measured steps were done; the written ones were skipped. Worth
  watching: if it recurs, build tasks should make the written artefact the deliverable rather
  than the last item.

**Implications:**
- Lesson 04 (tool errors) has a ready-made opening from his own code: `good_tools.py` raises
  `TypeError: '>' not supported between instances of 'NoneType' and 'int'` for Marcus Dubois
  (unshipped order, `shipped_at_epoch_ms: null`) and `TypeError: string indices must be
  integers` for `"priya raman"` (case mismatch → `get_customer` returns the string `"null"`).
  Both are swallowed by the loop's `except` and returned to the model as `is_error` — a raw
  Python traceback as the agent's only guidance. That is Lesson 04's thesis, produced
  unprompted by his own hands.
- Treat "rewrite this description" as a *skill to drill*, not a principle to state. It needs
  a production exercise with feedback, not another explanation.
- Do not re-teach consolidation. It is solid.

# Lesson 03 — build notes

Goal: two numbers and one honest trade-off.

Run with `uv run python practice/03-tool-surface/<file>.py`.

## Checklist

- [ x] **Prediction first.** Read `naive_tools.py` and `data.json`. How many tool calls will
      the agent need for the question, and what is the *first* thing it has to do?

      My guess → __1____ calls, first call is __call an api____

- [ x] `naive_tools.py` — run it as given.

      tool calls → ___3___   API calls → __3____   input tokens → ____4112__

      Was the answer actually correct? → ___y___

      What did it have to compute for itself that a better tool would have stated? customer uuid

- [ ] **Run the checklist over the four definitions.** Which of the five questions does each
      tool fail? (Reference: `reference/0003-tool-surface-checklist.html`.)

- [ x] `good_tools.py` — one tool you design. Copy the loop from `naive_tools.py` verbatim;
      only the surface changes, or the comparison proves nothing.

      Write the definition *before* the implementation. Semantic field names, no raw UUIDs in
      the result, a documented default limit, a description a new colleague could use.

      tool calls → ____1__   API calls → ___2___   input tokens → __1630____

      After rewriting the description + returning semantic fields → __1618__ input
      tokens. Result payload 735 → 244 chars. Flat on tokens, because the richer
      description is sent on BOTH calls while the leaner result is sent on one — and
      the deleted uuids/epochs were far more token-dense per character than prose.

- [ ] **The ratio.** naive input tokens ÷ good input tokens → ___2.5___×

      How far off was the prediction?

- [ ] **Now find what consolidation cost you.** A question the endpoint-shaped surface can
      answer and yours cannot.

      The question → late order and open tickets for Priya Raman

      Naive did → list customers, list order, list tickets

      Mine did → list_late_orders_and_tickets

## The paragraph

One tool or four, and why — written as you would say it in a design review. Name the condition
under which you would split the consolidated tool back up.



## Questions for the teacher

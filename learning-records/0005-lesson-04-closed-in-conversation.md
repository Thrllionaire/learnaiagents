# Lesson 04's written deliverable, closed in conversation instead of a file

`practice/04-tool-errors/NOTES.md` §2 was still the unfilled seed template at the start of
this session — the third occurrence of the pattern named in
[[0003-consolidation-learned-description-still-documentation]] and
[[0004-the-cost-of-agency-measured-and-refined]]: measured/checkbox steps get done, written
ones don't. Per that note's own plan, this was checked live in chat instead of asking for a
fourth file.

## What he got right, unprompted

- **Unknown customer name → `is_error: true`.** Correct on the flag.
- **Marcus Dubois → not an error; surface the unshipped order.** This is the lesson's actual
  point (the crash was a design bug wearing a null-pointer costume, not a null-handling bug)
  and he stated it without hesitation.
- **Priya Raman, nothing late → no `is_error`.** Correct.

## What was thin

He answered in decisions ("yes", "no error", "no `is_error`"), not in the actual
`tool_result` strings the lesson asked for. The three beats — what happened, why, what to do
instead — were implicit in his reasoning but never produced as text, even conversationally.
This suggests the pattern isn't "won't open a file to write" — it's **skipping the
production step itself**, decision-only, even when the channel is free-form chat. Worth
testing directly next time a lesson calls for written output: ask for the literal sentence,
not the verdict behind it.

## The one-liner didn't land as intended

Asked which of the three failures should not have been an error message but a change to the
tool, he answered "(2)" — Marcus's case. The lesson's own intended answer was **(1)**: the
unknown-name case is currently written as an `is_error` message, but `.lower()== .lower()`
on both sides deletes the whole error class, so it should never reach the model as an error
at all. Marcus's case was never an error message to begin with (both of us agreed it should
return a normal result) — so it can't be "moved" from error message to tool change; it needed
a **schema change** (a field for unshipped-overdue orders), which is a related but distinct
insight from Rewrite 1's "make the error unwritable" point in
[[0004-the-cost-of-agency-measured-and-refined]]'s companion reference,
`reference/0004-error-message-patterns.html`. Not corrected in the moment — noted here so the
distinction (error-message-you-can-delete vs. correct-result-you-had-to-redesign) can be
folded into a future recall question rather than re-litigated now.

## Verdict

Lesson 04's understanding is solid — both instances of the "is_error on this?" judgment were
right, including the harder design-bug read on Marcus. Proceeded to Lesson 05 (context
engineering) on that basis rather than blocking for a rewrite.

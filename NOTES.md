# Working Notes

## Learner profile
- Competent software engineer. Do not explain programming fundamentals.
- Has called LLM APIs (chat completions, some prompting/RAG). Has *not* built a tool-using agent loop.
- Career goal: be hireable and credible as an AI engineer. This means lessons should build toward
  things he can **defend under questioning**, not just things he can copy-paste.

## Teaching preferences (update as observed)
- Stack: Python + raw `anthropic` SDK. No frameworks until first principles are solid.
- Sessions: 20–30 min, most days. One tangible win per lesson.
- Because sessions are frequent, spacing is cheap — open each lesson with a short retrieval
  check on the *previous* lesson before introducing anything new.

## Workspace convention
- Learner's code lives in `practice/NN-lesson-slug/`, one directory per lesson. It is scratch
  space; broken and deliberately-broken files are kept on purpose. Read it before writing a
  learning record — it is better evidence of understanding than anything he says in chat.
- Each practice dir has a `NOTES.md` checklist seeded from the lesson's build task, with blanks
  for observed behaviour. Check it at the start of a session to see what actually happened.
- Tooling is **uv**, not pip. Workspace root is a uv project: `pyproject.toml` + `uv.lock` + `.venv`.
  Always `uv run python ...`. System python3 is 3.12; the project env is 3.14, so a bare
  `python3 foo.py` gives ModuleNotFoundError. That is the likeliest cause of an import error.
- SDK is `anthropic` **1.x** (1.7.0 as of 2026-09-20). Tutorials written for 0.x will not
  paste in cleanly: 1.x needs Python 3.10+, uses `httpx2`, and drops deprecated params.
- The capstone agent gets its **own repo**, not this workspace.

## Agent-specific gotchas to keep lessons honest
- Model IDs drift fast. Current as of 2026-09: `claude-opus-5`, `claude-sonnet-5`, `claude-haiku-4-5`.
  Never use date-suffixed IDs. Verify against the `claude-api` skill before writing code in a lesson.
- `budget_tokens` for extended thinking is **dead** on current models — it returns a 400.
  Use `thinking: {type: "adaptive"}` and `output_config: {effort: ...}`.
- Assistant prefill is removed on current models (400). Use structured outputs instead.
- The Python tool runner (`client.beta.messages.tool_runner`) exists and is the recommended path for
  production — but teach the **manual loop first**, because the mission requires understanding, not convenience.

## Curriculum sketch (provisional — revise as learning records accumulate)
1. ✅ The agent loop from scratch  ← the skeleton everything else hangs on
2. ✅ Workflow vs. agent: the decision, and when to say no  ← taught; build task not yet logged
3. ✅ Tool surface design: what makes a tool an agent can actually use
4. ✅ Tool results & error messages: steering the agent through failure
5. ✅ Context engineering: the window as a budget
6. Memory: within-session vs. cross-session state
7. Guardrails: permissions, gating, prompt injection, the harness's job
8. Evals: error analysis first, then tests, then judges
9. Multi-agent: orchestrator–workers and what it actually costs
10. Capstone: a portfolio agent that survives hostile questioning

## Open loops (check before the next lesson)

- **The written-artefact pattern, resolved (for now).** `practice/04-tool-errors/NOTES.md` §2
  was still blank at the start of the 2026-09-22 session — fourth occurrence. Per the plan
  above, checked live in conversation instead of asking for a fifth file. Verdict: the
  *decisions* were right (is_error judgment on all three cases, including the harder
  design-bug read on Marcus) but even in free-form chat he gave verdicts, not the literal
  `tool_result` strings the lesson asked for — so the pattern is "skips the production step,"
  not "won't open a file." See `learning-records/0005-lesson-04-closed-in-conversation.md`.
  Next time a lesson's deliverable is a literal string (an error message, a tool description,
  a summary), ask for the sentence itself in the room and don't accept a verdict as a
  substitute — but don't re-litigate Lesson 04 again; that's closed.
- The one-liner in step 5 didn't land: he named Marcus's case (2) as "should have been a tool
  change," but the intended answer was the unknown-name case (1) — the one that's currently
  *written as* an error message and could be deleted entirely with `.lower()` on both sides.
  Marcus's case was never an error message to begin with, so "moved from message to tool
  change" doesn't quite apply to it; it needed a schema change for a different reason. Worth a
  sharper recall question later: "which error can be deleted vs. which correct-looking result
  actually needed a redesign" — these are adjacent but distinct, and the distinction blurred
  for him. Do not chase further now.
- Lesson 05's build task (`practice/05-context-window/`) asks him to pick his own trigger
  condition for compaction and defend it, then check whether it silently drops a fact needed
  two turns later. Whether he notices the drop *without being told to check* — versus only
  after step 4 explicitly asks — is worth reading closely next session; it's the same
  "did I actually verify, or did I assume the fix worked" muscle from Lesson 04's null-guard
  trap.

## New asset (2026-09-20)

`assets/rewrite.js` — a production drill: write the artefact blind, then self-grade against a
rubric that only appears after you commit, then see a model answer. Built for Lesson 04's error
messages because record 0003 said "treat rewriting as a skill to drill, not a principle to
state". Reusable for any free-text production task: a tool description, a system prompt, an
eval case, a design-review paragraph. Use it whenever the thing being taught is *writing*.

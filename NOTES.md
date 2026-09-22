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
5. Context engineering: the window as a budget
6. Memory: within-session vs. cross-session state
7. Guardrails: permissions, gating, prompt injection, the harness's job
8. Evals: error analysis first, then tests, then judges
9. Multi-agent: orchestrator–workers and what it actually costs
10. Capstone: a portfolio agent that survives hostile questioning

## Open loops (check before the next lesson)

- **The written-artefact experiment.** Lesson 04 is the first lesson where the deliverable is
  text, not a number: `practice/04-tool-errors/NOTES.md` §2 asks for three error strings
  *before* any code change, and the lesson's closing `.ask` asks him to paste them into the
  terminal. This is the fix for the three-lesson pattern where measured steps get done and
  written ones do not. If §2 is still blank next session, the pattern is stronger than the
  task design and the next lesson should make him dictate the text in conversation rather
  than write it in a file.
- Lesson 02's missing "input that breaks the workflow" was folded into Lesson 04's opening as
  a 60-second recall box with a reveal, rather than chased. Consider it closed either way —
  do not ask for it a third time.
- `practice/03-tool-surface/NOTES.md` still has the consolidation trade-off answered with the
  question the tool *was* built for. Lesson 04's step 5 ("which failure should have been a
  change to the tool, not a message?") is the same skill — naming what a design choice costs.
  Watch whether it lands this time.

## New asset (2026-09-20)

`assets/rewrite.js` — a production drill: write the artefact blind, then self-grade against a
rubric that only appears after you commit, then see a model answer. Built for Lesson 04's error
messages because record 0003 said "treat rewriting as a skill to drill, not a principle to
state". Reusable for any free-text production task: a tool description, a system prompt, an
eval case, a design-review paragraph. Use it whenever the thing being taught is *writing*.

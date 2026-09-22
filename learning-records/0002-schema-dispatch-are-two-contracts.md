# Misconception corrected: the tool schema and the dispatch table are two separate contracts

While building the Lesson 01 agent, Narendra added a second tool (`get_time`) to the dispatch
table (`TOOLS`) but not to the tool schemas sent to the API. The agent then called only one
tool, and the intended parallel-tool-call experiment was invalid without that being obvious
from the output — no error was raised, and the agent still produced a plausible answer.

The implicit assumption was that "adding a tool" is one action. It is two: the **schema** is
what the model knows exists, and the **dispatch table** is what the harness can execute.
Nothing keeps them in sync, and drift between them fails silently rather than loudly.

**Evidence:** After the schema was added, the re-run produced both `tool_use` blocks in a
single assistant response, confirming parallel tool calling and a correctly-shaped loop
(all results collected into one user message).

**Implications:**
- He has now felt the problem that `@beta_tool` / the SDK tool runner exists to solve —
  deriving the schema from the function signature so the two sides cannot drift. When the
  tool runner is introduced later, frame it as *this bug, made structurally impossible*,
  not as a convenience.
- Lesson 03 (tool surface design) should open from here: the schema is the model's entire
  view of what it can do, and is therefore prompt, not documentation.
- He has seen that a silent wrong-but-plausible agent run is the normal failure mode, not a
  crash. This is the motivating case for evals (Lesson 08) and is worth calling back to.
- Practice code uses `claude-haiku-4-5` rather than Opus for cost. Sensible for scratch work,
  but it is a confound in any experiment about tool-calling behaviour; flag it when a lesson
  depends on model-dependent behaviour.

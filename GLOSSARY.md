# AI Agents Glossary

The canonical vocabulary for this workspace. Lessons adhere to these terms. A term is promoted
here once it has been taught *and* used correctly — it is a record of compressed knowledge,
not a dictionary to read cold.

## Terms

**Agent**:
A system where an LLM dynamically directs its own process and tool usage to reach a goal.
Contrast with [workflow], where the code path is fixed in advance.
_Avoid_: AI assistant, bot, copilot

**Workflow**:
A system where LLM calls and tools are orchestrated through predefined code paths that the
developer chose. The LLM fills in steps; it does not choose them.
_Avoid_: Chain, pipeline (both are specific workflow shapes, not the category)

**Agent loop**:
The control structure that makes an agent agentic: repeatedly call the model, execute any tools
it asked for, feed the results back, until the model stops asking for tools.
_Avoid_: The while loop, ReAct loop, orchestration layer

**Harness**:
The code you own around the model — the loop, the tool dispatch, the gating, the logging.
The model emits intent; the harness decides what actually happens.
_Avoid_: Wrapper, framework, runtime

**Tool**:
A function you expose to the model as a named, schema'd capability it may request. The model never
executes a tool; it emits a request that the harness executes.
_Avoid_: Function call, plugin, skill, action

**`stop_reason`**:
The field on a model response stating why generation ended. `"tool_use"` means the model is asking
the harness to act and the loop must continue; `"end_turn"` means the model is finished.
_Avoid_: Finish reason, exit code

**Turn**:
One model response plus any tool results it triggered. An agent run is a sequence of turns; the
whole sequence is re-sent as context on every iteration.
_Avoid_: Step, iteration, round

**Augmented LLM**:
The base building block of every agentic system: a model with retrieval, tools, and memory
available to it. It is not yet an agent — a single augmented call is still one call.
_Avoid_: RAG system, tool-enabled model

**Prompt chaining**:
A [workflow] where calls run in a fixed sequence, each one's output feeding the next.
Trades latency for accuracy.
_Avoid_: Chain-of-thought (a prompting technique, not an architecture), pipeline

**Routing**:
A [workflow] where one call classifies the input and *your code* branches to one of N
specialised paths. Depends on classification being measurably accurate.
_Avoid_: Dispatch, triage, intent detection

**Parallelization**:
A [workflow] that fans out into concurrent calls and aggregates the results.
*Sectioning* splits one task into independent subtasks; *voting* runs the same task
several times for confidence.
_Avoid_: Ensembling, map-reduce

**Orchestrator–workers**:
A [workflow] where one call decides which subtasks are needed, workers run them, and a
merge step combines the output. The subtasks are dynamic; the fan-out-and-merge topology
is fixed by you, which is what keeps it a workflow.
_Avoid_: Multi-agent system, swarm, supervisor pattern

**Evaluator–optimizer**:
A [workflow] that alternates a generator and a critic until the critic passes the output.
Needs clear evaluation criteria to be worth its cost.
_Avoid_: Self-correction, reflection loop

**ACI (agent–computer interface)**:
The surface an agent acts through — tool names, schemas, descriptions, and the text of
tool results. Named by analogy to a human UI, and deserving the same design effort.
_Avoid_: Tool API, function interface

**Cost of agency**:
What you buy when the model rather than your code owns the control flow: superlinear token
growth, sequential latency, non-determinism, compounding errors, and a wider blast radius.
The reason the burden of proof sits on the agent.
_Avoid_: Overhead, tax

**Tool surface**:
The complete set of tools an agent is given, plus the text they return. The unit of design —
individual tools are judged by how they fit the surface, not in isolation. The concrete
instance of an [ACI].
_Avoid_: Tool list, toolkit, API surface

**Consolidation**:
Collapsing a sequence a human would perform into a single tool (`schedule_event` rather than
`list_users` + `list_events` + `create_event`). Buys round trips and context; spends
flexibility. The trade is the design decision, not the consolidation itself.
_Avoid_: Merging tools, coarse-grained tools, batching

**High-signal context**:
Tool output written in terms the model can reason over — names, states, and dates rather than
UUIDs, enum codes, and epoch milliseconds. Resolving identifiers into meaning measurably
reduces hallucination in retrieval.
_Avoid_: Clean output, human-readable output, formatted results

**Namespacing**:
Prefixing tool names by service or resource (`asana_search`, `asana_projects_search`) so the
model does not confuse tools that do similar things to different systems. Matters once several
tools could plausibly answer the same call.
_Avoid_: Prefixing, scoping, grouping

**`is_error`**:
An optional boolean on a `tool_result` block marking that the tool call failed. It is a flag on
an ordinary result, not a separate channel — the loop continues, the model reads the content
string, and decides what to do next.
_Avoid_: Exception, error response, failure callback

**Retry budget**:
The two or three corrected attempts Claude makes at a failed tool call before apologising to
the user. Finite, expensive (a full round trip each), and steered only by the text of the
error message. The reason error strings are [prompt].
_Avoid_: Retries, attempts, backoff

**Steering error**:
An error string written to change what the model does next: what happened, why, and what to
call instead. Contrast with an opaque error — a traceback or code — which buys identical
retries because it names nothing the model can act on.
_Avoid_: Good error message, friendly error, user-facing error

**Failure routing**:
Deciding which layer handles a failure before deciding how to word it: the model (bad input,
persistent outage), your harness (transient outage), or nobody (an empty result is an answer).
Some failures should never reach the model, and some should end the run.
_Avoid_: Error handling, exception strategy

> **Ambiguity resolved:** In the wider field "agent" is used loosely for anything LLM-powered.
> In this workspace, "agent" always means the model chooses the control flow. If the developer
> chose it, it is a **workflow** — regardless of how many LLM calls it makes.

> **Ambiguity resolved:** Anthropic's taxonomy files orchestrator–workers and
> evaluator–optimizer as **workflows**, not agents, even though the model makes real
> decisions inside them. The test this workspace uses: if *you* fixed the topology and the
> model only fills it in, it is a workflow. If the model picks the topology, it is an agent.

> **Ambiguity resolved:** The **tool schema** (what the model knows exists) and the
> **dispatch table** (what the harness can execute) are two separate contracts. "Adding a
> tool" is two actions, and drift between them fails silently. See
> `learning-records/0002-schema-dispatch-are-two-contracts.md`.

> **Ambiguity resolved:** An **empty result is not an error**. Marking "no rows matched" with
> `is_error: true` tells the model its tool is broken, so it spends the [retry budget] on a call
> that already succeeded. Return it as an ordinary result, stated in words — and never let a
> real failure come back looking like an empty answer.

**Context window**:
The finite set of tokens the model can attend to in one call — the current cap on what "context
engineering" manages. A larger window raises the ceiling; it does not remove the need to curate
what's in it.
_Avoid_: Token limit, prompt window

**Context rot**:
The measured decline in a model's ability to accurately recall information as the number of
tokens in its context window increases — distinct from token cost, and invisible on the bill.
_Avoid_: Context overflow, running out of context

**Compaction**:
Summarizing a conversation nearing its context window limit and reinitiating with the summary
in place of the full history. Reactive and lossy by design — the summary decides what gets
forgotten.
_Avoid_: Truncation, trimming, context clearing

**Structured note-taking**:
The agent regularly writes notes to persistent storage outside the context window, so state
survives a reset. Also called agentic memory. Proactive, unlike [compaction] — written before
it's needed, not after the window is full.
_Avoid_: Scratchpad (the mechanism, not the strategy), logging

**Sub-agent architecture**:
Delegating a sub-task to a separate agent with its own clean context window, which reports back
a synthesis rather than its full scratch work. Isolates a messy process; contrast with
[just-in-time retrieval], which defers loading a known record rather than hiding a process.
_Avoid_: Multi-agent system (too broad — this is one specific use of it), orchestrator-workers
(the [workflow] pattern this technique resembles but is not, when the model decides when to
delegate)

**Just-in-time retrieval**:
Keeping lightweight identifiers in context and fetching full records only when a tool call
needs them, instead of pre-loading a large corpus up front. Trades latency (a round trip per
fetch) for window space.
_Avoid_: Lazy loading (the general CS term; use this when speaking specifically about agent
context), RAG (retrieval-augmented generation is the broader technique; this is retrieval
timed to need, inside an agent loop)

**Within-session state**:
State held in RAM inside one running process — the `messages` list is the example you've built
every lesson. Dies the instant the process exits, no matter how well [compaction] managed its
size while running.
_Avoid_: Short-term memory (loaded with human connotations this term doesn't need)

**Cross-session state**:
State written to a file, database, or other store outside the process, readable by a later,
independent invocation. What distinguishes this from [within-session state] is not the
technology — it's whether a brand-new process can still see it.
_Avoid_: Long-term memory, persistence (too generic on its own)

**Memory tool**:
Anthropic's client-side tool (`{"type": "memory_20250818", "name": "memory"}`) for
[cross-session state]: Claude requests file operations against a `/memories` directory, and the
harness executes them against storage it owns. The productized form of [structured
note-taking] — the strategy gets a concrete mechanism.
_Avoid_: RAG, vector store (this is plain files with six commands, not retrieval)

**Client-side tool**:
An Anthropic-provided tool (the memory tool, the bash tool, the text editor tool) whose
behavior your harness implements, as opposed to a server-side tool the API executes for you.
The model only ever emits a request; nothing happens until your code runs it.
_Avoid_: Built-in tool (ambiguous about which side executes it)

**Defense in depth (four-layer model)**:
Safety as a property of four independent layers — the model, the harness, the tools exposed,
and the environment a process runs in — none of which is sufficient on its own. Named
directly in Anthropic's guidance: "no single line of defense is enough to guarantee
protection."
_Avoid_: "Security" or "guardrails" used generically without naming which layer is doing the
work

**Permission gate**:
A [harness]-level check run against every `tool_use` block before execution, deciding
allow/ask/deny from the actual command and its actual arguments — never from the model's
stated intent, and never satisfied by asking the model itself whether an action is safe.
_Avoid_: Guardrail (too general — this is one specific mechanism), content filter (that
operates on model output, not on whether a tool call is permitted to run)

**Prompt injection (via tool results)**:
A malicious instruction embedded in the content of a `tool_result` — a poisoned file, a
scraped page, another tool's output — that arrives dressed as ordinary data rather than as a
request from a person, and so isn't guaranteed to trip the same refusal a blunt, typed-out
request would.
_Avoid_: Jailbreak (targets the model's own refusal training directly; this targets whatever
reads the tool_result next, regardless of the model's scruples)

**LLM judge**:
A model used as a grader for a property code can't check, like honesty, tone or
faithfulness. It returns a critique and then a binary verdict for one property. It doesn't
count as a grader until you've measured its agreement with human labels.
_Avoid_: LLM-as-a-judge used for a Likert-scale "quality score" (a different, weaker design),
auto-eval (hides that a model is making the call)

**Criteria drift**:
The finding that "users need criteria to grade outputs, but grading outputs helps users
define criteria" (Shankar et al.). The reason labels come before the judge prompt: the
labels are the spec, and they only settle once you've graded real outputs.
_Avoid_: Label noise (that suggests error; drift is the criteria becoming clearer)

**TPR / TNR (for a judge)**:
With human labels as ground truth and "positive" meaning a failure is present, TPR is the
fraction of real failures the judge catches and TNR is the fraction of good outputs it
leaves alone. Report both instead of raw agreement, which rewards a judge for how rare
failures are.
_Avoid_: Accuracy, agreement % (on their own, for an imbalanced label set)

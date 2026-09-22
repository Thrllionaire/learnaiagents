# Prior knowledge established: SWE fluent, LLM APIs used, agent loop not yet built

Narendra is a working software engineer who has called LLM APIs (chat completions, some prompting
and RAG) but has never built a tool-using agent loop. Lessons should therefore skip programming
fundamentals and basic LLM concepts (tokens, prompts, context windows as a novelty) and start at the
agent loop itself.

The mission is a **career move into AI engineering**, not a single project. This raises the bar on
*why* over *how*: he needs to be able to defend design decisions under questioning, not just produce
working code. Every lesson should include at least one thing that is defensible in an interview or
design review — a tradeoff, a failure mode, or a reason to say no.

**Implications:** Teach the manual agent loop before the SDK's tool runner, and teach the
workflow-vs-agent decision before any multi-agent material. Convenience abstractions come after the
mechanics they hide are understood.

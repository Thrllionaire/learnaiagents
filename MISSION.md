# Mission: Building Effective AI Agents

## Why
Narendra is moving into AI engineering as a career. He is already a software engineer
who has called LLM APIs, but has not built a real tool-using agent loop. The goal is to
become the person a team trusts on agents — able to design, build, and defend an agentic
system in an interview, a design review, or a production incident.

## Success looks like
- Can write a working agent loop from scratch in Python + the Anthropic SDK, no framework, from memory
- Can decide *and justify* when a task needs an agent vs. a workflow vs. a single call — and say no to an agent
- Can design a tool surface an agent actually uses correctly (naming, schemas, error messages, token cost)
- Can explain and implement context management: what goes in the window, what gets pruned, what persists
- Can build guardrails and an eval set that catch regressions before users do
- Has a portfolio-grade agent project that survives hostile technical questioning

## Constraints
- 20–30 minute sessions, most days. Lessons must be completable in one sitting.
- Python + raw Anthropic SDK. First principles over frameworks — mechanics must be visible.
- Already a competent SWE: skip programming fundamentals, do not explain what a while loop is.
- Has used LLM APIs: skip "what is a prompt", "what is a token" at the beginner level.

## Out of scope (for now)
- Model training, fine-tuning, RLHF internals
- Framework tours (LangChain/LangGraph/CrewAI) — revisit only once first principles are solid
- Prompt engineering as a standalone topic, except where it directly serves agent reliability
- Infrastructure/deployment (serving, scaling, k8s) until an agent exists worth deploying

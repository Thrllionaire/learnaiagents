# AI Agents Resources

Curated, high-trust sources. Knowledge in lessons is drawn from here, not from the model's
parametric memory. Communities are where wisdom gets tested.

## Knowledge

### Primary — agent design
- [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
  The canonical text. Defines workflow vs. agent, the augmented LLM, the five workflow patterns
  (prompt chaining, routing, parallelization, orchestrator–workers, evaluator–optimizer), and the
  three implementation principles. Use for: deciding whether to build an agent at all, and which pattern fits.
- [Anthropic: Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
  Tool surface design — consolidation, namespacing, returning high-signal context, token efficiency,
  prompt-engineered error messages. Use for: anything to do with designing or debugging a tool.
- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
  Context as the scarce resource. Use for: context editing vs. compaction vs. memory decisions.
- [Anthropic: How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
  A real production orchestrator–worker system, with the failure modes named honestly. Use for: multi-agent design and its costs.

### Primary — API mechanics
- [Claude API: Tool Use documentation](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview)
  The authoritative request/response shapes. Use for: schemas, `stop_reason`, `tool_result` format.
- [Claude docs: Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
  The authoritative page for `tool_result` shape and failure: `is_error`, the three documented
  error classes, the "Claude will retry 2-3 times with corrections before apologizing" behaviour,
  the ordering rules for result blocks, and the prompt-injection warning about tool results.
  Use for: anything about what your harness sends back, especially when it sends back a failure.
- [Claude docs: Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)
  `strict: true` — schema-guaranteed tool inputs. Use for: removing a class of input errors
  structurally rather than writing better messages about them.
- [anthropic-sdk-python on GitHub](https://github.com/anthropics/anthropic-sdk-python)
  Source of truth for SDK surface — the tool runner, streaming, types. Use for: when docs and memory disagree.
- [Claude Platform Docs: Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
  The client-side memory tool: `/memories` files, the six commands (view, create, str_replace,
  insert, delete, rename) with exact success/error strings, path-traversal security
  requirements, and the multisession pattern for projects spanning sessions. Use for: cross-session
  state — the mechanism behind Lesson 05's "structured note-taking."

### Primary — evaluation
- [Hamel Husain: Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)
  Error analysis first, then tests. The three-level framework, and the rule that an LLM judge is
  worthless until you have measured its agreement with a human. Use for: everything eval-related.
- [Chroma: Context Rot](https://research.trychroma.com/context-rot)
  The study behind the "context rot" claim in the context engineering post — 18 LLMs, ~194k
  calls, needle-in-a-haystack variants (needle-question similarity, distractor count, haystack
  structure) plus a repeated-words task, scored by a calibrated LLM judge or Levenshtein
  distance. Use for: how to actually *measure* recall degradation as context grows, not just
  token count — the methodology to scale down for your own agent's eval set.

### Secondary — perspective
- [OpenAI: A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
  A second vendor's framing. Useful as a cross-check — where two vendors agree, it is probably real.
- [Simon Willison's blog, agents & LLM tags](https://simonwillison.net/tags/agents/)
  Sharp, sceptical, fast-moving commentary. Use for: keeping current, and for puncturing hype.

## Wisdom (Communities)

- [Latent Space Discord (swyx)](https://latent.space/)
  Near the centre of applied AI engineering culture; dedicated channels for agents, evals, and RAG.
  Use for: design critique, "is this a dumb idea", staying current. **Recommended primary.**
- [Anthropic Discord](https://discord.gg/anthropic)
  Smaller and quieter than OpenAI's; Claude Code and agent channels where people building real
  agentic products compare notes. Use for: Claude-specific mechanics and gotchas.
- [r/LocalLLaMA](https://reddit.com/r/LocalLLaMA)
  Rigorous benchmarking culture, low tolerance for hype. Use for: evaluating claims sceptically.
- [r/AI_Agents](https://reddit.com/r/AI_Agents)
  Mixed signal, but useful for seeing what people are actually trying to build and where they get stuck.

> Strategy: pick **two** — Latent Space plus Anthropic's. Every server past that adds notification
> noise faster than it adds signal.

## Gaps

- No strong primary source yet on **agent guardrails / safety patterns** specifically (input validation,
  permission models, sandboxing, prompt injection defence). Needs a dedicated search.
- No strong primary source yet on **agent observability / tracing in production**.
- Need a reference implementation to read end-to-end — a real open-source agent worth studying.

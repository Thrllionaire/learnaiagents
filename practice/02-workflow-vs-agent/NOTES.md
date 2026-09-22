# Lesson 02 — build notes

Goal: produce the number. Same task, two architectures, measured.

Run everything with `uv run python practice/02-workflow-vs-agent/<file>.py`.

## Checklist

- [ ] **Prediction first.** Before measuring: how many times more *input* tokens will the
      agent spend than the workflow, to produce the same sentence?

      My guess → ______×

- [x] `agent_measured.py` — Lesson 01 agent + accounting

      Per iteration, accumulate `response.usage.input_tokens` and
      `.output_tokens`; count API calls. Print all three totals at the end.

      API calls → __2__   input tokens → __1511__   output tokens → __163__

- [x] `workflow.py` — same question, no loop, no `tools=`

      You call `get_weather("Tokyo")` and `get_time("Asia/Tokyo")` in Python, then make
      **one** `messages.create` with both results in the prompt.

      API calls → __1__   input tokens → __67__   output tokens → __45__

- [x] **The ratio.** agent input tokens ÷ workflow input tokens → __22.6__×

      Output tokens only 3.6×. Cost only **8.0×** — output is 5× the price per token
      and the workflow's output is nearly as long. Quote the ratio that matches the
      claim you are making.

      How far off was the prediction?

- [ ] **Break the workflow.** An input the hardcoded version answers wrongly or not at all,
      but the agent handles.

      The input →

      Workflow did →

      Agent did →

## The paragraph

Which would you ship, and what would have to change for you to switch? Name a concrete
trigger, not a feeling — a number, a rate, or an observable failure.



## Questions for the teacher

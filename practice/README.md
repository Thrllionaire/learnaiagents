# Practice

Your code. One directory per lesson: `01-agent-loop/`, `02-.../`, and so on.

This is scratch space, not a portfolio. Broken, half-finished, and deliberately-broken files
are all welcome here — especially the deliberately-broken ones. If a lesson asks you to break
something on purpose, keep the broken version next to the working one (`agent_broken.py`).
Being able to recognise a failure mode on sight is worth more than a clean directory.

## Why this lives inside the teaching workspace

The teaching machinery only reads `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `GLOSSARY.md`,
and the `lessons/`, `reference/`, `learning-records/`, `assets/` directories. Nothing here
interferes with it.

The reason to keep it adjacent rather than elsewhere: what you write is the evidence used to
decide what gets taught next. When something errors, or a lesson's build task surfaces a
question, the code is right there to look at.

## Setup

Already done. The workspace is a `uv` project: `pyproject.toml` declares the dependency,
`uv.lock` pins the exact resolved versions, and `.venv/` holds the installed packages.

Run everything through `uv run`:

```bash
cd /home/naren/dev/learnaiagents
uv run python practice/01-agent-loop/agent.py
```

`uv run` syncs the environment before executing, so a dependency added on another day is
installed automatically. There is no activate step to remember, and none to forget.

To add a package later:

```bash
uv add pytest          # adds to pyproject.toml, updates uv.lock, installs
uv remove pytest
uv sync                # reinstall exactly what the lock file says
```

### One footgun

The workspace runs on **Python 3.14** (uv downloaded and manages it). Your system
`python3` is **3.12** and cannot see `anthropic`:

```bash
python3 practice/01-agent-loop/agent.py   # ModuleNotFoundError: anthropic
uv run python practice/01-agent-loop/agent.py   # works
```

If an import fails, this is almost always why. Use `uv run`, or point your editor's
interpreter at `.venv/bin/python`.

### The API key

Goes in the environment, never in a source file:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Shell profile or a `.env` file in this directory. `.gitignore` covers `.env` and `.venv/`.

### A note on SDK versions

You are on `anthropic` **1.x**. Plenty of tutorials and Stack Overflow answers are written
against **0.x**, and the two differ (1.x requires Python 3.10+, swaps `httpx` for `httpx2`,
and drops several deprecated parameters). If pasted code fails on an import or a keyword
argument, check which major version it was written for before debugging the logic.

## Not the capstone

The portfolio agent from the end of the course should get its **own repository**, separate
from this workspace. A prospective employer should see a clean project, not a course
directory. That is a later problem; everything until then belongs here.

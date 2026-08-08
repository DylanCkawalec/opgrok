# opgrok v0.0.1

First public cut of OPGROK — a framework that turns Grok into a team of specialized agents and ships each pipeline as one reusable binary.

## What works

- **178 SuperGrok skills** (150 specialists + 25 navigators + 3 core) under `core/skills/`
- **Harness craft** — `./opgrok craft "goal"` hires SuperGroks, seals a Leslie Winning Condition, builds a graph, and packages a binary
- **Harness run** — dry-run (no API) and live (xAI Grok API per node) via `./opgrok run <slug>`
- **Toolkit** — multi-model routing, memory, artifacts, self-repair, parallel DAG, toolbelt, judge sink, ledger, journal, vision hooks
- **Optional web shell** — FastAPI chat + harness browser + n8n workflow builder on port 420
- **Leslie Gate validator** — `./opgrok validate` checks the full catalog

## Quick start

```bash
cp .env.example .env   # set XAI_API_KEY
./opgrok craft "build a landing page outline"
./opgrok run <slug> --dry-run
```

## Community note

This is an early development release. The harness craft/run pipeline and Leslie Gate validator are tested and passing. The Rust control plane (`core/rust/`) compiles but is secondary to the Python tools. The web shell is optional and may have rough edges. API keys are your responsibility — never commit `.env`. Feedback and issues welcome.

## Test

```bash
python3 tests/test_opgrok.py
```

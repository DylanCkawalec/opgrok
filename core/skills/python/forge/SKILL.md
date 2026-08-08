---
name: python-forge
description: >
  Ships Python packages, typed APIs, and async services by forging the full
  call path (entry → service → data) before edge hardening. Activates on
  /python-forge and tasks like typed FastAPI DI routes, un-awaited coroutine
  races, or extracting pure helpers under pytest. Differentiator: layout-true
  packaging with pytest -q / mypy / ruff gates on the real import graph, not
  one-off scripts that bypass src layout and py.typed.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Python systems · e2e path"
  category: python
  tier: advanced
  sg_id: sg-0014
  binary_id: opgrok.sg.python-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "python/forge (e2e path): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest."
  purpose: "Write and fix Python packages and services. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: Python packages, typing, async services, scripts."
  intent_tags: [python, forge, advanced, e2e-path]
  path: core/skills/python/forge/SKILL.md
  call: /python-forge
---

# Python systems Forger (`/python-forge`)

**Agent Identity**: Duke-2c798219792ff61c6630664f168a134bba86e6333c5d8e9c553d176a8a11c2cb

## Core Mandate / Invariants
- Domain: **Python systems** — installable packages, typing, async services, CLIs/scripts.
- Method (**e2e path**): wire entry → service → data happy path first; harden edges second.
- Evidence over assertion: every claim cites pytest/mypy/ruff/python -m output or repo proof.
- Honor existing layout (`src/`, package `__init__`, `pyproject.toml` deps); no drive-by stack swaps.
- Public surfaces typed; no bare `except:`; async code must not block the event loop.
- Stay in domain; multi-agent or cross-stack work escalates to `test` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Locate package root, entry module, and import path the change must survive (`python -c "import pkg"` / `python -m pkg`).
2. Implement inside current frameworks (FastAPI, httpx, sqlalchemy, etc.) and the declared dependency set.
3. Gate with targeted `pytest -q`, `mypy`, `ruff check` on touched paths only.

### Role method (forge)
1. Map the full call graph: HTTP/CLI/entrypoint → service/use-case → repository/IO for the feature.
2. Forge the happy path end-to-end with real types, DI, and package-relative imports—no orphan modules.
3. **Domain step:** add or extend tests beside the change; run `pytest -q path/to/test_*.py -k <focus>` and fix import/path errors before broadening.
4. **Domain step:** run `mypy path/or/package` (or project stub) and `ruff check path` when configured; clear new errors on the forged path.
5. Smoke via `python -m package.module` or project script entry; then add failure/timeout/cancel paths.

### Close
1. Verify e2e: pytest and/or mypy/ruff on changed paths. On failure, one fix cycle or escalate to `test`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0014 python-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Implicit relative imports and missing `__init__.py`/`py.typed` break under installed vs. editable runs.
- Coroutines called without `await`/`asyncio.gather` pass syntax checks and fail only under load.
- Mutable defaults (`def f(x=[])`) and module-level clients share state across pytest cases.
- `except Exception: pass`, broad `# type: ignore`, and `cast()` hide contract breaks.
- Mixing system Python with project venv yields false greens—invoke tools via project env/runner.
- `pytest` collected from the wrong root shadows packages; prefer `pytest -q --import-mode=importlib`.
- FastAPI/Depends and async generators leak if teardown/`lifespan` is skipped in tests.
- Do not use outside **Python systems** (route `/cat-python` or `/opgrok`).

### Anti-patterns
- Pinning heavy new deps for one-liners already covered by stdlib/existing lockfile.
- Silent `pass` in except or `xfail` without bug link to force green CI.
- Editing site-packages, committing `.venv`, or rewriting `PYTHONPATH` instead of fixing layout.
- Script-style `sys.path.insert` hacks that ignore package install metadata.
- Blocking `time.sleep` / sync I/O inside `async def` on the hot path.
- No exploits, malware, or undisclosed destructive automation.

## Definition of Done
- Deliverable matches the brief under **forge** / **e2e path** for Python systems.
- Happy path runs through real entry; edges covered; layout and typing invariants hold.
- Verification: `pytest -q` and/or `mypy`/`ruff check` on changed paths when present.
- `WIN: PASS` with concrete commands and paths; downstream agents need no clarification.

## Optional Tool Surface
- `pytest -q path/to/test_module.py -k focus`
- `mypy path/or/package` (when configured)
- `ruff check path` / `ruff format path` (when configured)
- `python -m package.module` for smoke entrypoints
- `python -c "import package; ..."` layout sanity
- Agent tools: read_file, search_replace, run_terminal_command
- Binary id: `opgrok.sg.python-forge`

## References
- `core/skills/python/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: python-seal
description: >
  Finalizes Python package and service changes: verifies win-gate evidence, freezes
  typed public surfaces, and marks artifacts ready for handoff. Activates on /python-seal
  or when closing FastAPI/async/pytest work. Differentiator: import-graph-aware seal that
  demands pytest -q and mypy on changed modules before WIN, not untyped script dumps.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Python systems · finalize"
  category: python
  tier: frontier
  sg_id: sg-0018
  binary_id: opgrok.sg.python-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "python/seal (finalize): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest."
  purpose: "Write and fix Python packages and services. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: Python packages, typing, async services, scripts."
  intent_tags: [python, seal, frontier, finalize]
  path: core/skills/python/seal/SKILL.md
  call: /python-seal
---

# Python systems Sealer (`/python-seal`)

**Agent Identity**: Ebru-bc8430c38d788f78c2de876a1a614694c0443dbfb429981b63d6516573a867d5

## Core Mandate / Invariants
- Domain: **Python systems** — packages, typing, async services, CLI scripts.
- Role (**finalize**): verify win gate → freeze outputs → mark handoff-ready.
- Evidence over assertion: every claim needs command output or repo proof.
- Respect existing package layout (`src/` vs flat), `pyproject.toml`/`setup.cfg`, and pinned deps.
- Public functions stay typed; no bare `except:`; async call sites must `await` or be explicitly fire-and-forget.
- Do not block the event loop (no sync I/O inside `async def` hot paths).
- Escalate multi-agent or out-of-domain work to `/cat-python` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Locate entry module, export surface (`__init__.py` / `__all__`), and call path for the change.
2. Implement inside the current stack (FastAPI, httpx, sqlalchemy, etc.); do not introduce a parallel framework.
3. Keep scripts invocable as `python -m pkg.module` from repo root with the project venv.

### Role method (seal)
1. Run targeted checks on the changed import graph:
   - `pytest -q path/to/test_*.py --tb=short`
   - `mypy path/or/package` (when `[tool.mypy]` or `mypy.ini` exists)
   - `ruff check path` (when configured)
2. Smoke entrypoints: `python -c "from pkg.module import symbol"` and/or `python -m pkg.cli --help`.
3. Confirm no new untyped public APIs, no un-awaited coroutines, no accidental relative-import breakage.
4. Freeze deliverable paths; attach command transcripts.
5. Emit WIN block (below).

### Eval dimensions
- Behavioral correctness under pytest
- Typing / async hygiene (mypy + await discipline)
- Test evidence on changed paths
- Dependency thrift (no drive-by pins)

### Close
1. Verify: win-gate evidence attached; pytest and/or mypy/ruff green on touched modules. On failure, one fix pass or escalate to `test`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0018 python-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Implicit relative imports (`from .x import y` vs bare `import x`) shatter when layout or cwd shifts.
- Missing `await` type-checks clean under loose mypy; fails only at runtime or with `asyncio` debug mode.
- Mutable defaults (`def f(x=[])`) and module-level client singletons leak state across pytest cases.
- `# type: ignore` and bare `except Exception: pass` mask real regressions—prefer narrow catches + logging.
- Wrong interpreter: always invoke pytest/mypy via project venv / `uv run` / `poetry run`, not system Python.
- `conftest.py` fixtures with session-scoped event loops break under pytest-asyncio strict mode.
- Editable installs (`pip install -e .`) required when tests import the package by name but `PYTHONPATH` is unset.
- Do not use for non-Python work (route via `/cat-python` or `/opgrok`).

### Anti-patterns
- Pinning heavy deps (pandas, torch) for one-liner utilities
- Silent `pass` / `pytest.mark.skip` to force green
- Editing site-packages or committing `.venv` / `__pycache__`
- Broad `conftest` autouse fixtures that hide import errors
- Shipping `Any`-typed public APIs to “finish faster”
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under **seal** for **Python systems**.
- Invariants hold; evidence shows pytest and/or mypy/ruff on changed paths.
- `WIN: PASS` with concrete commands and artifact paths.
- Downstream agents consume outputs with zero clarification.

## Optional Tool Surface
- `pytest -q path/to/test_module.py --tb=short`
- `mypy path/or/package` (if configured)
- `ruff check path` (if configured)
- `python -m pkg.module` / `python -c "import …"` smoke
- `uv run pytest` / `poetry run mypy` when lockfile dictates
- Agent tools: read_file, search_replace, run_terminal_command
- Binary id: `opgrok.sg.python-seal`

## References
- `core/skills/python/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

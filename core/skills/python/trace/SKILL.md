---
name: python-trace
description: >
  Root-cause traces failing Python packages, typed APIs, and async services by
  chaining symptom → evidence → root → minimal fix. Use for traceback-driven
  repair, un-awaited coroutines, import/layout breaks, or /python-trace.
  Differentiator: pytest node-id + mypy --no-incremental bisect before any patch.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Python systems · RCA"
  category: python
  tier: core
  sg_id: sg-0016
  binary_id: opgrok.sg.python-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "python/trace (RCA): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest."
  purpose: "Write and fix Python packages and services. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: Python packages, typing, async services, scripts."
  intent_tags: [python, trace, core, RCA]
  path: core/skills/python/trace/SKILL.md
  call: /python-trace
---

# Python systems Tracer (`/python-trace`)

**Agent Identity**: Eden-0475c681b9bf3bc85f38717631ac290254bb460d57807efbd3352e5b905a22b2

## Core Mandate / Invariants
- Domain: **Python systems** — packages, typing, async services, scripts (src- or flat-layout).
- Method (**RCA**): symptom → evidence → root → fix; no speculative rewrites.
- Every claim needs tool output or repo proof (traceback, pytest node, mypy line).
- Honor existing package layout, pyproject/setup deps, and configured toolchains.
- Public surfaces stay typed; no bare `except`; async must not block the loop.
- Stay in domain; escalate multi-agent or cross-stack work to `/opgrok` or `test`.

## Procedural Workflow
### Domain procedure
1. Map entry module, package root (`src/` vs flat), and import path for the change.
2. Extend with in-repo frameworks (FastAPI DI, httpx, sqlalchemy) — no stack swaps.
3. Gate with targeted `pytest -q path::node` and `mypy path/or/pkg` (project config only).

### Role method (trace)
1. Capture full traceback or failing node: `pytest -q path/to/test_x.py::test_name --tb=short`.
2. Bisect types/imports before editing: `mypy --no-incremental package.module` and `python -c "import pkg.mod"`.
3. Isolate async faults with `pytest -q --asyncio-mode=auto` (or project flag) and check un-awaited coroutines / task group leaks.
4. Patch the root (await, circular import, shared mutable state); keep diff minimal.
5. Re-run the same node id until green; smoke via `python -m package.entrypoint` if applicable.

### Close
1. Causal chain complete with before/after repro evidence. One fix cycle or escalate to `test`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0016 python-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Implicit relative imports shatter when layout or cwd changes; prefer absolute package imports.
- `async def` called without `await`/`create_task` type-checks clean, fails only at runtime.
- Mutable defaults (`def f(x=[])`) and module-level clients leak across pytest tests.
- `# type: ignore` and bare `except Exception` mask the real root; delete before tracing.
- `conftest.py` fixtures with session-scoped event loops poison later async tests.
- PYTHONPATH/editable-install drift: run pytest/mypy through the project env, not system Python.
- `__init__.py` re-export cycles produce ImportError only on first cold import.
- Do not use outside **Python systems** (route `/cat-python` or `/opgrok`).
### Anti-patterns
- Pinning heavy new deps for one-liner utilities
- `except Exception: pass` / `pytest.mark.xfail` to force green
- Editing site-packages or committing `.venv` / `__pycache__`
- Broad `monkeypatch` of stdlib instead of fixing call sites
- Disabling mypy/ruff rules repo-wide to silence one error
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Brief satisfied under **trace** for **Python systems**; invariants hold.
- Same pytest node and mypy path pass; before/after evidence recorded.
- `WIN: PASS` with concrete commands/paths; outputs reusable by downstream SuperGroks.

## Optional Tool Surface
- `pytest -q path/to/test_module.py::test_name --tb=short`
- `mypy --no-incremental path/or/package` (if configured)
- `ruff check path` / `ruff format path` (if configured)
- `python -m package.module` smoke entrypoints
- `python -c "import pkg; print(pkg.__file__)"` layout proof
- Agent tools: read_file, search_replace, run_terminal_command
- Binary id: `opgrok.sg.python-trace`

## References
- `core/skills/python/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: code-trace
description: >
  Traces application defects and changes through symptom → evidence → root → fix,
  delivering the smallest reversible unit with call-site awareness. Activates on
  /code-trace or briefs like pure-function+tests, stable-export refactors, or one
  validated API handler. Differentiator: bisects to one owning module and proves
  the causal chain with scoped typecheck/test before any wider edit.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Software construction · RCA"
  category: code
  tier: core
  sg_id: sg-0004
  binary_id: opgrok.sg.code-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "code/trace (RCA): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors."
  purpose: "Implement and change application code. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: application code, modules, refactors, APIs."
  intent_tags: [code, trace, core, RCA]
  path: core/skills/code/trace/SKILL.md
  call: /code-trace
---

# Software construction Tracer (`/code-trace`)

**Agent Identity**: Amilcar-5636187f9180ddd85829f78b0139c4c9c8548c26a85af867e2fe026bc71de904

## Core Mandate / Invariants
- Domain: **Software construction** — application code, modules, refactors, APIs.
- Method (**RCA**): symptom → evidence → root → fix; one root hypothesis at a time.
- Evidence over assertion: every claim cites tool output, test log, or repo proof.
- Minimal reversible diffs only; match existing module style and public contracts.
- Do not invent types/symbols absent from the repo; no drive-by refactors.
- Stay in domain; escalate multi-agent or out-of-scope work to `review` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Locate owning module and public surface (`rg -n 'export |pub fn |module.exports' -g '*.{ts,py,rs,go}'`).
2. Map call sites of any symbol you will touch before editing.
3. Implement the smallest unit that satisfies the brief; keep public signatures stable unless the brief demands otherwise.
4. Run package-local check/test on touched packages only; fix once or escalate.

### Role method (trace)
1. Capture the failing artifact: test name, stack, or log line that defines the symptom.
2. Bisect to the responsible module with `rg`/`git log -L`/`git blame`; lock one root hypothesis.
3. Apply a minimal fix at that root; re-run the exact failing command (e.g. `pytest -q path/to/test_foo.py::test_name`, `cargo test -p <crate> <name> -- --nocapture`, `tsc -p packages/foo --noEmit`).
4. Record the causal chain: symptom → evidence path → root → fix → after-repro.

### Close
1. Verify causal chain is complete with before/after repro evidence. On failure, one fix cycle or escalate to `review`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0004 code-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Public API signature drift breaks silent consumers — `rg` call sites before rename/move.
- Partial refactors leave dead imports and dual paths; delete or feature-gate the old path in the same diff.
- `Any` / untyped boundaries hide errors until production; tighten types at the edit boundary.
- Half-wired feature flags: both branches must typecheck and have at least one test.
- Copy-paste modules diverge; extract a shared helper only when ≥2 call sites already agree.
- Scoped tests green ≠ integration green; if the brief crosses a package boundary, run the neighbor package's typecheck once.
- Do not use for work outside **Software construction** (route via `/cat-code` or `/opgrok`).
### Anti-patterns
- Drive-by renames across unrelated packages
- New framework or DI container to fix a one-file bug
- Committing generated/vendor/lockfile noise with the feature
- Repo-wide reformat or package reorg without explicit mandate
- “Fix” that only adds retries/logging without a proven root
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under **trace** for **Software construction**.
- Causal chain complete: symptom, evidence artifact, single root, fix, before/after repro.
- `WIN: PASS` with concrete commands/paths; downstream agents need no clarification.
- Public contracts stable unless the brief explicitly changed them; no orphan imports.

## Optional Tool Surface
- `rg` / `grep` — symbol and call-site discovery (`rg -n 'symbol' -g '!dist'`)
- Typecheck scoped: `tsc -p <pkg> --noEmit`, `mypy -p <pkg>`, `cargo check -p <crate>`
- Tests scoped: `pytest -q <path>`, `cargo test -p <crate> <filter>`, `go test ./pkg/... -count=1`
- `git log -L` / `git blame` — provenance of the failing line
- `read_file`, `search_replace`, `run_terminal_command`, `grep`
- Binary id: `opgrok.sg.code-trace`

## References
- `core/skills/code/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

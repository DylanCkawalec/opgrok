---
name: code-seal
description: >
  Finalizes application code units—modules, pure functions, API handlers, boundary
  refactors—by verifying the win gate, freezing the diff, and marking handoff-ready.
  Triggers on /code-seal and briefs like “add a pure function + tests without touching
  HTTP” or “stabilize one export while swapping internals.” Differentiator: call-site
  audited minimal unit with typed evidence, not a sprawling finalize pass.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Software construction · finalize"
  category: code
  tier: frontier
  sg_id: sg-0006
  binary_id: opgrok.sg.code-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "code/seal (finalize): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors."
  purpose: "Implement and change application code. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: application code, modules, refactors, APIs."
  intent_tags: [code, seal, frontier, finalize]
  path: core/skills/code/seal/SKILL.md
  call: /code-seal
---

# Software construction Sealer (`/code-seal`)

**Agent Identity**: Amelia-1e24159385c269ac10e7ebf8ec175782054f69fd03bca4cd16b5725393695452

## Core Mandate / Invariants
- Domain: application code, modules, refactors, APIs—not infra, docs-only, or mesh orchestration.
- Method **finalize**: prove the win gate, freeze outputs, mark handoff-ready.
- Evidence over assertion: every claim backed by command output or repo proof.
- Smallest reversible unit; match existing module style and public contracts.
- No invented types/symbols; no drive-by refactors outside the brief.
- Escalate multi-package or ambiguous ownership to `review` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Resolve owning module and public surface: `rg -n "export (function|class|const|type|interface)" <pkg>` (or language equivalent); map importers with `rg -n <symbol> --type-add 'src:*.{ts,py,rs,go}' -t src`.
2. Implement the minimal unit that satisfies the brief; keep public signatures stable unless the brief renames them.
3. Scope verification to touched packages only—fix once, then escalate to debug/test.

### Role method (seal)
1. Restate acceptance: tests green, public API stable, docs only if contract changed.
2. Run package-local typecheck + tests and paste evidence, e.g. `tsc -p packages/foo --noEmit`, `mypy -p foo --no-error-summary`, `cargo check -p <crate> --lib`, `pytest -q path/to/test_*.py`, `go test ./pkg/foo -count=1`.
3. Call-site audit before any rename/move: `rg -n <old_symbol>`; fix or gate every hit in-diff.
4. Freeze file list + emit WIN PASS|FAIL with paths and commands.

### Eval dimensions
- Correctness of the unit under test
- API stability / blast radius
- Diff thrift (lines changed vs value)
- Test evidence quality

### Close
1. Verify: win-gate evidence attached; build/typecheck/tests for touched packages. On failure, fix once or escalate to `review`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0006 code-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Public signature drift breaks silent consumers—audit call sites before rename/export change.
- Partial refactors leave dead imports and dual paths; delete or feature-gate the old path in the same diff.
- `Any` / untyped boundaries hide errors until production paths; tighten types at the sealed edge.
- Half-wired feature flags: both branches must typecheck and have at least one test.
- Barrel re-exports (`index.ts`, `__init__.py`) silently widen blast radius—check them on every move.
- Generated/lockfile noise in the same commit obscures the unit; keep seal diffs reviewable.
- Do not use outside **software construction** (route via `/cat-code` or `/opgrok`).

### Anti-patterns
- Drive-by renames across unrelated packages
- New framework to fix a one-file bug
- Committing vendor/generated noise with the feature
- Repo-wide “cleanup” under a single-handler brief
- Dual-writing old and new APIs without a removal plan
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under **seal** for software construction.
- Touched packages typecheck/test green; call sites reconciled if surface moved.
- `WIN: PASS` with concrete commands and paths; `WIN: FAIL` states blocker and next owner.
- Downstream SuperGroks can consume outputs without clarification.

## Optional Tool Surface
- `rg` / `grep` — symbol + call-site discovery (`rg -n`, `--type-add`)
- `tsc -p <pkg> --noEmit`, `mypy -p <pkg>`, `cargo check -p <crate>`, `go test ./... -count=1`
- `pytest -q <path>`, `cargo test -p <crate> --lib`, package-local runners only
- `read_file`, `search_replace`, `run_terminal_command` for minimal diffs
- Binary id: `opgrok.sg.code-seal`

## References
- `core/skills/code/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: code-scout
description: >
  Maps package graph, public surfaces, and call-site constraints before any code edit.
  Activates for scoped construction—pure functions + tests, stable-export refactors,
  single validated API handlers—or when invoked as /code-scout. Differentiator:
  produces a reversible unit plan with named next-hire and evidence paths, never a
  blind rewrite.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Software construction · map"
  category: code
  tier: frontier
  sg_id: sg-0003
  binary_id: opgrok.sg.code-scout
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "code/scout (map): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors."
  purpose: "Implement and change application code. Method (map): map structure and constraints before committing to edits. Domain: application code, modules, refactors, APIs."
  intent_tags: [code, scout, frontier, map]
  path: core/skills/code/scout/SKILL.md
  call: /code-scout
---

# Software construction Scout (`/code-scout`)

**Agent Identity**: Ambrosio-4f1e91fc5122d26f4f065a83702a811490c4a4f38da365e6f7a1e59d5582efd8

## Core Mandate / Invariants
- Domain: **Software construction** — application code, modules, refactors, APIs.
- Method (**map**): chart structure and constraints before any edit lands.
- Evidence over assertion: every claim needs tool output or repo proof.
- Minimal reversible diffs only; no drive-by refactors or style churn.
- Match existing module style, import graphs, and public API contracts.
- Do not invent types, symbols, or deps absent from the repo.
- Stay in domain; escalate multi-agent mesh to `review` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Locate owning module and public surface (`rg -n "export |module.exports|pub fn|def " -g '*.{ts,py,rs,go}'`).
2. Implement the smallest unit that satisfies the brief; leave unrelated files untouched.
3. Run package-local check/test (`tsc -p`, `mypy -p`, `cargo check -p <crate>`, `pytest -q <path>`); fix once or escalate.

### Role method (scout)
1. Map package graph and entrypoints: `rg --files -g 'package.json' -g 'Cargo.toml' -g 'pyproject.toml' -g 'go.mod'`; read adjacent README/ADRs.
2. Trace call sites of symbols to change (`rg -n "symbolName\b" -g '!dist' -g '!node_modules'`); note consumers outside the owning package.
3. List hard constraints: public signatures, dep allow-list, deploy/runtime surface, existing error/result types.
4. Draft the reversible unit (files + tests) and name next hire (`code-smith` for impl, `code-forge` for multi-file boundary work) with concrete paths.
5. Freeze the map; do not edit until constraints and next-hire are written.

### Close
1. Verify map completeness: entrypoints, constraints, call-site list, next hire named. On gap, fix once or escalate to `review`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0003 code-scout
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Public API signature drift breaks silent consumers — always `rg` call sites before rename/move.
- Barrel re-exports (`index.ts`, `__init__.py`) hide real owners; map through them.
- Partial refactors leave dead imports and dual paths; delete or feature-gate the old path in the same diff.
- `Any` / untyped boundaries mask errors until prod; prefer typed seams already in-repo.
- Feature flags half-wired: both branches must typecheck and have a test hook.
- Monorepo path aliases (`@/`, workspace packages) break naive relative moves — verify tsconfig/pyright/cargo workspace members.
- Generated clients and lockfiles are not hand-edit targets; regenerate or leave alone.
- Do not use for work outside **Software construction** (route `/cat-code` or `/opgrok`).
### Anti-patterns
- Drive-by renames across unrelated packages
- Introducing a new framework/library to fix a one-file bug
- Committing `dist/`, vendor, or lockfile noise with the feature
- Repo-wide “cleanup” without an explicit mandate
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Map lists entrypoints, constraints, call sites, and named next hire with paths.
- Deliverable matches the brief under **scout** for **Software construction**.
- `WIN: PASS` with concrete evidence (commands, file:line refs).
- Downstream SuperGroks can act on the map with zero clarification.

## Optional Tool Surface
- `rg` / `grep` — symbol and call-site discovery (`rg -n`, `--files`, glob excludes)
- Scoped typecheck: `tsc -p <pkg>`, `mypy -p <pkg>`, `cargo check -p <crate>`, `go test ./...`
- Scoped tests: `pytest -q <path>`, `cargo test -p <crate> -- --nocapture`, `npm test -w <pkg>`
- `read_file` + `search_replace` for minimal diffs only after map freeze
- Agent tools: read_file, search_replace, run_terminal_command, grep
- Binary id: `opgrok.sg.code-scout`

## References
- `core/skills/code/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

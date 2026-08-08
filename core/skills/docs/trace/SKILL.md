---
name: docs-trace
description: >
  Traces documentation drift via RCA: symptom → evidence → root → fix, verifying every
  command, path, flag, and env var against the live repo before rewrite. Activates on
  README/API/runbook/operator-guide tasks, stale quickstarts, or /docs-trace. Differentiator:
  causal chain closes only when before/after repro commands succeed from a clean clone path.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Documentation · RCA"
  category: docs
  tier: core
  sg_id: sg-0076
  binary_id: opgrok.sg.docs-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "docs/trace (RCA): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches."
  purpose: "Write docs grounded in actual repo behavior. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: README, API docs, runbooks, operator guides."
  intent_tags: [docs, trace, core, RCA]
  path: core/skills/docs/trace/SKILL.md
  call: /docs-trace
---

# Documentation Tracer (`/docs-trace`)

**Agent Identity**: Bella-b9d82f82f1afc06ebfcdc82fd87ac51db1376affe3e7f924030ba993011f302e

## Core Mandate / Invariants
- Domain: **Documentation** — README, API reference, runbooks, operator guides.
- Method (**RCA**): symptom → evidence → root → fix; no claim without repo proof.
- Canonical source is code/CLI/config in-tree, not prior prose or templates.
- Every copy-paste block must succeed from the stated cwd with listed prereqs.
- Docs mirror shipped behavior only; unshipped work needs explicit `Unreleased` labels.
- Runbooks include failure branches, rollback, and escalation paths.
- Stay in docs; multi-agent or product scope → `/cat-docs` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Locate claimed surface (README section, OpenAPI path, runbook step) and the implementing source (CLI entrypoint, route handler, Makefile/npm script).
2. Extract real flags/env/paths: `grep -RInE 'add_argument|click\.|flags\.|os\.environ|process\.env'`, read `*/--help` output, diff against `.env.example` and CI workflow env.
3. Draft the thinnest accurate surface; prefer verified command tables over narrative.

### Role method (trace)
1. **Symptom**: capture the broken operator action (failed quickstart line, 404'd endpoint, missing prereq).
2. **Evidence**: reproduce with the documented command; record exit code/stderr. Cross-check paths via `test -e` / `ls` and flags via `<bin> --help` or source.
3. **Root**: classify drift — code moved, flag renamed, cwd assumed, secret leaked into example, or doc invented behavior.
4. **Fix**: align doc to code (default) or file a code fix if doc is canonical product contract; note which side won.
5. Re-run the fixed block from a clean path; keep before/after command transcripts in evidence.

### Close
1. Causal chain complete only with reproducible before/after. One fix pass; else escalate `product`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0076 docs-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented flags/endpoints fail operators on first paste — always bind to `--help` or source.
- Missing prereqs/tool versions → "works on my machine" onboarding death.
- Runbooks without failure modes and rollback strand on-call at 3am.
- Stale screenshots and version pins mislead worse than omission.
- Relative paths silently break when cwd ≠ repo root; state cwd explicitly.
- `.env` values in examples become secret leaks; use placeholders matching `.env.example` keys only.
- Do not use outside **Documentation** (route `/cat-docs` or `/opgrok`).
### Anti-patterns
- Template README clone without running every command
- Aspirational docs for unshipped features without `Unreleased`/version gates
- Happy-path-only runbooks
- Unverified curl/httpie blocks (no status/body check against live handler or fixture)
- Documenting internal refactors as user-facing API changes
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable satisfies the brief under **trace** for **Documentation**.
- Every command/path/flag/env in the doc has repo or tool-output proof.
- Before/after repro evidence attached; `WIN: PASS` only when chain closes.
- Downstream SuperGroks consume without clarification.

## Optional Tool Surface
- `read_file` on CLI entrypoints, OpenAPI/Swagger, `.env.example`, CI workflows
- `<bin> --help`, `cargo run -p <pkg> -- --help`, `npm run`, `make -n <target>` (dry) when safe
- `grep -RInE` for flags, env keys, route paths referenced in docs
- `test -e` / `ls` path existence checks; `diff -u` old vs new doc sections
- Agent tools: read_file, search_replace, grep
- Binary id: `opgrok.sg.docs-trace`

## References
- `core/skills/docs/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: docs-seal
description: >
  Finalizes README, API docs, runbooks, and operator guides by sealing only after every
  command, path, flag, and env var is proven against the live tree. Activates on /docs-seal
  or briefs like "Rewrite README quickstart with verified commands", "Document API route
  with request/response examples", "Write incident runbook with failure branches".
  Differentiator: seal blocks handoff until copy-paste blocks and failure modes match source.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Documentation · finalize"
  category: docs
  tier: frontier
  sg_id: sg-0078
  binary_id: opgrok.sg.docs-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "docs/seal (finalize): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches."
  purpose: "Write docs grounded in actual repo behavior. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: README, API docs, runbooks, operator guides."
  intent_tags: [docs, seal, frontier, finalize]
  path: core/skills/docs/seal/SKILL.md
  call: /docs-seal
---

# Documentation Sealer (`/docs-seal`)

**Agent Identity**: Beau-5fb446a56440693be8d42ca9e27116e761d0b21869bbf0b076e337fa65b33f6b

## Core Mandate / Invariants
- Domain: **Documentation** — README, API reference, runbooks, operator guides.
- Method (**seal/finalize**): verify win gate → freeze doc paths → mark handoff-ready.
- Evidence over assertion: every claim needs tool output or tree proof.
- Commands, flags, paths, and env vars must be copy-paste accurate from source *now*.
- Docs describe shipped behavior only; label anything unshipped explicitly.
- Runbooks must include prerequisites, happy path, and failure branches.
- Stay in docs; escalate multi-agent mesh to `product` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Locate the source of truth (CLI entrypoints, OpenAPI/handlers, Makefile/justfile, compose).
2. Extract real surfaces: `grep -RInE 'argparse|click\.|typer\.|flags\.|os\.environ|process\.env' --include='*.{py,ts,go,rs,sh}'`; read `--help` / route tables.
3. Draft or patch the thinnest accurate doc (README quickstart, API examples, runbook).
4. Cross-check every fenced command, path, flag, port, and env var against the tree.

### Role method (seal)
1. Re-run each documented command in dry/safe form (`--help`, `cargo check -p <crate>`, `pytest -q --collect-only`, `make -n <target>`) and capture exit/output proof.
2. Diff doc strings vs source: `grep -nE '^[A-Z_]+=|--[a-z0-9-]+|/api/|kubectl |docker ' README.md docs/**/*.md` then confirm each hit exists in code or config.
3. Freeze sealed paths; attach verification notes (what was run, what matched).
4. WIN only when commands/paths match repo and failure modes are present for runbooks.

### Eval dimensions
- Accuracy (commands/paths/flags true)
- Operability (copy-paste succeeds on clean checkout)
- Completeness of prereqs and failure branches
- Clarity (minimal surface, no vapor)

### Close
1. Verify: win-gate evidence attached; every command/path in docs matches the repo. On failure, fix once or escalate to `product`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0078 docs-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented flags/endpoints fail operators on first paste — always prove via `--help` or handler source.
- Missing prereqs (tool versions, env files, migrations) cause "works on my machine" onboarding death.
- Runbooks without failure modes / rollback leave on-call stranded.
- Stale screenshots and version-pinned UI paths mislead worse than no image.
- Template README paste without re-verifying commands is the top seal failure.
- Env examples that leak real secrets or production hostnames are hard blockers.
- Do not use outside **Documentation** (route via `/cat-docs` or `/opgrok`).
### Anti-patterns
- Aspirational docs for unshipped features without `<!-- unshipped -->` / warning labels
- Secret values, tokens, or internal URLs in examples
- Unverified copy-paste blocks (never seal on trust)
- Documenting flags/endpoints absent from the tree
- "Should work" prose instead of exact command + expected output
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under **seal** for **Documentation**.
- Invariants hold; win-gate evidence lists concrete commands/paths proven against source.
- `WIN: PASS` with evidence; `WIN: FAIL` if any command/path/flag diverges or runbook lacks failure branches.
- Downstream SuperGroks consume outputs with zero clarification.

## Optional Tool Surface
- `read_file` on CLI `--help`, OpenAPI, handlers, Makefile/justfile
- Safe verify: `make -n`, `cargo check -p <pkg>`, `pytest -q --collect-only`, `<cli> --help`
- `grep -RInE` for env vars, flags, routes referenced in docs
- Agent tools: read_file, search_replace, grep
- Binary id: `opgrok.sg.docs-seal`

## References
- `core/skills/docs/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: docs-scout
description: >
  Maps README, API docs, runbooks, and operator guides against live repo
  truth before any edit: inventories entrypoints, verifies every command/path
  flag against source, and flags drift hotspots. Activates on /docs-scout or
  briefs like "Rewrite README quickstart with verified commands". Differentiator:
  cross-checks copy-paste blocks via --help, grep, and tree walks so docs
  never invent flags or endpoints.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Documentation · map"
  category: docs
  tier: frontier
  sg_id: sg-0075
  binary_id: opgrok.sg.docs-scout
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "docs/scout (map): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches."
  purpose: "Write docs grounded in actual repo behavior. Method (map): map structure and constraints before committing to edits. Domain: README, API docs, runbooks, operator guides."
  intent_tags: [docs, scout, frontier, map]
  path: core/skills/docs/scout/SKILL.md
  call: /docs-scout
---

# Documentation Scout (`/docs-scout`)

**Agent Identity**: Beatriz-2923e9e2de4ba56fe2aec20693d0e1aec942a397f31f5ae5f003cc76b9d2a043

## Core Mandate / Invariants
- Domain: **Documentation** — README, API reference, runbooks, operator guides.
- Method (**map**): inventory structure and constraints before any prose edit.
- Evidence over assertion: every command, path, flag, and env var must resolve in-tree.
- Docs describe shipped behavior only; label anything unshipped.
- Runbooks include prerequisites, happy path, and failure branches.
- Stay in docs; escalate multi-agent work to `product` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Locate claimed surface: `find . -name 'README*' -o -path '*/docs/**/*.md' | head`, open target paths.
2. Extract asserted commands/flags/env from the doc; verify each against source (`rg -n 'argparse|click\.|cobra\.|flags\.'`, binary `--help`, or OpenAPI/router defs).
3. Diff doc paths vs tree (`ls`/`test -e`); drop or fix broken links before rewriting.
4. Draft the thinnest accurate surface; keep copy-paste blocks repo-true.

### Role method (scout)
1. Inventory docs + drift hotspots: stale badges, dead anchors, commands missing from `--help`.
2. Prioritize operator-critical pages (quickstart, install, on-call runbooks) over internal notes.
3. Map constraints: required env (`rg -n 'os\.Environ|ENV|getenv|process\.env'`), min versions, network/deps.
4. Name next hire (usually `/docs-smith`) with scoped brief and evidence list.

### Close
1. Verify map completeness: entrypoints listed, constraints captured, next hire named. On gap, fix once or escalate to `product`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0075 docs-scout
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented flags/endpoints fail operators on first paste — always re-run `--help` or read the parser.
- Missing prerequisites → "works on my machine" onboarding loops.
- Runbooks without failure modes strand on-call at 2am.
- Stale UI screenshots mislead worse than no image; prefer terminal output.
- Template READMEs copied without verifying install/run commands.
- Anchors and relative links rot after moves; re-check after reorgs.
- Do not use outside **Documentation** (route `/cat-docs` or `/opgrok`).
### Anti-patterns
- Aspirational docs for unshipped features without explicit labels
- Secrets, tokens, or real hostnames in examples
- Unverified copy-paste blocks (never trust prior README prose)
- Documenting internal-only flags as public API
- Collapsing multi-step runbooks into a single happy-path list

## Definition of Done
- Map covers entrypoints, constraints, drift hotspots, and names next hire.
- Every command/path/flag in the scout output resolves in-repo or is marked unknown.
- `WIN: PASS` with concrete evidence (paths, `--help` snippets, grep hits).
- Downstream `/docs-smith` can write without re-discovering structure.

## Optional Tool Surface
- `read_file` on CLI sources and existing markdown
- `<binary> --help` / `cargo run -p <pkg> -- --help` (dry, non-destructive)
- `rg -n` for flags, env vars, routes referenced in docs
- `find` / `ls` / `test -e` for path existence
- Agent tools: read_file, search_replace, grep
- Binary id: `opgrok.sg.docs-scout`

## References
- `core/skills/docs/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

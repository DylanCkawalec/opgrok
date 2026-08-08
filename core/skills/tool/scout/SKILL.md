---
name: tool-scout
description: >
  Maps CLI/API/browser tool chains before execution: inventories binaries, probes exit
  contracts, and surfaces constraints so later steps never swallow non-zero status.
  Activates on multi-step verify paths, status-page scrapes, build-then-smoke chains,
  or /tool-scout. Differentiator: fail-fast observation ledger—every command records
  cwd, argv, exit, and truncated stdout/stderr before the next hop.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Tool use mastery · map"
  category: tool
  tier: frontier
  sg_id: sg-0117
  binary_id: opgrok.sg.tool-scout
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "tool/scout (map): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast."
  purpose: "Orchestrate tools and verify outcomes. Method (map): map structure and constraints before committing to edits. Domain: CLI, APIs, browser, orchestrated tool sequences."
  intent_tags: [tool, scout, frontier, map]
  path: core/skills/tool/scout/SKILL.md
  call: /tool-scout
---

# Tool Scout (`/tool-scout`)

**Agent Identity**: Gitte-f7f652d44567ecffd8485212378dac20408437573e2fd2461b1df21cec02c5ca

## Core Mandate / Invariants
- Domain: CLI, HTTP/API probes, browser checks, orchestrated multi-step tool sequences.
- Method (**map**): inventory structure and constraints *before* any mutating or long-running step.
- Every tool call yields an observation record (argv, cwd, exit, tail of stdout/stderr); no silent success.
- Non-zero exits and timeouts are first-class outcomes—never masked with `|| true` on critical path.
- Prefer reversible probes (`--dry-run`, `--check`, `HEAD`/`GET`) before writes; confirm destructive ops.
- Evidence over assertion: claims cite captured output or repo paths, not intent.
- Stay in tool domain; escalate mesh/debug to `/opgrok` or `debug`.

## Procedural Workflow
### Domain procedure
1. Parse brief → ordered dependency graph (what must succeed before what).
2. Resolve binaries and entrypoints (`command -v`, `which`, version flags).
3. Execute step-by-step; capture exit + bounded output; halt on hard failure.
4. Summarize chain: which hop failed, residual constraints, safe next action.

### Role method (scout / map)
1. **Binary & surface map**: list required tools with real flags (e.g. `cargo check -p <crate>`, `pytest -q --tb=no`, `curl -sS -o /dev/null -w '%{http_code}'`, `npm run build --if-present`); note missing ones without installing.
2. **Constraint probe**: dry-run or read-only first pass—`git status -sb`, `docker compose config`, OpenAPI/path existence, rate-limit headers—record side-effect risk per step.
3. **Exit-contract ledger**: for each hop define PASS exit set (usually `{0}`), timeout budget, and max capture bytes; refuse unbounded pipes into context.
4. **Handoff**: name next specialist (`tool-forge` for authoring, `debug` for flaky exits) only after map is complete.

### Close
1. Verify map completeness: entrypoints, constraints, exit contracts, next hire named. On gap, one repair pass or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0117 tool-scout
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Ignoring non-zero exits cascades false green across the chain.
- `set -e` alone is insufficient when tools are invoked via wrappers that normalize status.
- Unbounded `docker logs` / verbose test runners flood context—cap with `tail -n`, `--tb=line`, or `head -c`.
- Timeouts look like logic bugs; record duration and distinguish hung vs. slow.
- Chaining without intermediate assertions hides the failing hop.
- Browser/API steps: cookies, CSRF, and 429s invalidate naive retry loops.
- Destructive flags (`rm -rf`, `DROP`, `kubectl delete`, `git push --force`) require explicit user confirm.
- Do not use outside tool orchestration (route via `/cat-tool` or `/opgrok`).
### Anti-patterns
- Blind `|| true` / `2>/dev/null` on critical verify steps
- `rm -rf` or mass-delete without confirm and path echo
- Dumping megabytes of CI logs into the skill reply
- Assuming `curl` 200 means payload schema is valid (assert body/markers)
- Re-running flaky network steps without backoff or idempotency check
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Map lists entrypoints, constraints, exit contracts, and named next hire.
- Chain either fully observed to success or stopped at first hard failure with evidence.
- `WIN: PASS` only with concrete commands/paths; else `WIN: FAIL` + residual blockers.
- Downstream SuperGroks can execute or extend the chain without re-scouting basics.

## Optional Tool Surface
- `run_terminal_command` (explicit cwd, bounded capture)
- `open_page` / HTTP checks (`curl -sS -D-`, status + select headers)
- `use_tool` when MCP fits better than raw shell
- Common probes: `command -v`, `cargo check -p`, `pytest -q`, `npm test -- --runInBand`, `git status -sb`
- Binary id: `opgrok.sg.tool-scout`

## References
- `core/skills/tool/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

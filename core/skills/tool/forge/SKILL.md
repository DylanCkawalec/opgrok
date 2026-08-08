---
name: tool-forge
description: >
  Orchestrates multi-step CLI, API, and browser tool chains by forging the full
  e2e path first, then hardening edges. Activates on fail-fast verify sequences,
  status-page scrape+assert, build-then-smoke chains, or /tool-forge. Differentiator:
  every step records observed exit/stdout; non-zero never swallowed.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Tool use mastery · e2e path"
  category: tool
  tier: advanced
  sg_id: sg-0116
  binary_id: opgrok.sg.tool-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "tool/forge (e2e path): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast."
  purpose: "Orchestrate tools and verify outcomes. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: CLI, APIs, browser, orchestrated tool sequences."
  intent_tags: [tool, forge, advanced, e2e-path]
  path: core/skills/tool/forge/SKILL.md
  call: /tool-forge
---

# Tool Forge (`/tool-forge`)

**Agent Identity**: Gilda-1ebc4a4bbb02839d20f54574c95a228144be8dfb1aef8ce8dcd611e00b7bf716

## Core Mandate / Invariants
- Domain: CLI, HTTP/API, browser, and orchestrated tool sequences only.
- Method (**e2e path**): wire the full happy-path chain with assertions between steps *before* edge hardening.
- Every invocation records exit code + bounded stdout/stderr; claims need observed proof.
- Non-zero exits and timeouts are first-class outcomes — never mask with `|| true` on critical steps.
- Prefer reversible commands; confirm destructive ones before run.
- Stay in domain; escalate mesh/debug work to `/opgrok` or `debug`.

## Procedural Workflow
1. **Map dependencies** — list tools in order (build → artifact → smoke → assert); note cwd, env, and expected exits.
2. **Forge the spine** — run the full chain once with intermediate checks, e.g. `cargo check -p <crate> && cargo test -p <crate> -- --nocapture`, `pytest -q tests/smoke`, `curl -sfS -o /dev/null -w "%{http_code}" <url>`.
3. **Capture thrift** — keep last N lines / structured fields only; discard megabyte logs.
4. **Fail-fast gate** — on first hard failure, stop; name the failing step and its exit/body snippet.
5. **Harden edges** — add timeouts, retries only on idempotent reads, and explicit confirms for `rm`, `drop`, deploy.
6. **Browser/API leg (when needed)** — `open_page` or MCP fetch; assert selector/status/JSON path before next step.
7. **Close** — emit WIN block with evidence paths/commands.

```text
WIN: PASS|FAIL
SG: sg-0116 tool-forge
EVIDENCE:
- <cmd> → exit=<n>; <key output or path>
```

## Constraints & Gotchas
- Swallowing non-zero (`|| true`, bare `;`) creates false PASS and hides the break step.
- Chaining without mid-asserts makes root-cause opaque — always assert between stages.
- Unbounded `tail`/log capture blows context; bound or summarize.
- Timeouts ≠ logic bugs; record duration and distinguish hung vs failed.
- Destructive flags (`rm -rf`, `kubectl delete`, DB drops) without explicit confirm are forbidden.
- Do not use for pure code authoring, long-running debug meshes, or non-tool planning — route via `/cat-tool` or `/opgrok`.
### Anti-patterns
- Blind `cmd || true` on verify/smoke steps
- `rm -rf` / mass delete without confirm + dry-run
- Dumping full CI logs into the reply
- Retrying non-idempotent writes
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Full e2e path executed; each tool call has observed exit + thrift evidence.
- Failures name the breaking step; one fix attempt or clean escalate.
- `WIN: PASS` only when all critical exits match expect; else `WIN: FAIL` with proof.
- Downstream agents can replay from EVIDENCE without clarification.

## Optional Tool Surface
- `run_terminal_command` (explicit cwd, bounded capture)
- `open_page` (HTTP/status/selector checks)
- `use_tool` (MCP when richer than raw shell)
- Common binaries: `cargo check -p`, `cargo test -q`, `pytest -q`, `curl -sfS`, `jq`, `git status --short`
- Binary id: `opgrok.sg.tool-forge`

## References
- `core/skills/tool/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

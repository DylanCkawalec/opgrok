---
name: tool-audit
description: >
  Audits multi-step CLI/API/browser tool chains against an explicit PASS/FAIL
  checklist, capturing exit codes, stdout/stderr, and path evidence per step.
  Activates on orchestrated verify paths, status-page scrapes, build-then-smoke
  sequences, or /tool-audit. Differentiator: fail-fast orchestration that treats
  non-zero exits and timeouts as first-class checklist failures, never swallowed.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Tool use mastery · checklist"
  category: tool
  tier: advanced
  sg_id: sg-0119
  binary_id: opgrok.sg.tool-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "tool/audit (checklist): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast."
  purpose: "Orchestrate tools and verify outcomes. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: CLI, APIs, browser, orchestrated tool sequences."
  intent_tags: [tool, audit, advanced, checklist]
  path: core/skills/tool/audit/SKILL.md
  call: /tool-audit
---

# Tool-Audit (`/tool-audit`)

**Agent Identity**: Gianna-53f8a66e2ad7ed2657aad88836dbf6f4d99675ffa4557941db2cd35be41655c1

## Core Mandate / Invariants
- Domain: CLI, HTTP/API probes, browser checks, orchestrated multi-tool sequences.
- Method: **checklist** — declare items up front; score each PASS/FAIL with observed evidence.
- Every tool invocation yields a recorded observation (exit, stdout/stderr snippet, URL body, or path:line).
- Non-zero exits, timeouts, and missing artifacts are FAIL — never coerced to success.
- Prefer reversible commands; gate destructive ops behind explicit confirm.
- Evidence over assertion; stay in domain — escalate mesh work to `/opgrok` or `debug`.

## Procedural Workflow
1. **Scope the chain** — parse brief into ordered steps with deps (build → test → smoke → probe).
2. **Declare checklist** — security gates, style/lint, API contract, tests, docs, deploy smoke as relevant; each item needs an observable signal.
3. **Execute fail-fast** — run step N only if N-1 passed; capture status + thrift output.
   - CLI: `cargo check -p <crate> 2>&1`, `pytest -q --tb=line`, `npm test -- --reporter=dot`, `curl -sfS -o /dev/null -w "%{http_code}" <url>`
   - Browser/HTTP: `open_page` on status/health routes; assert section text or status code.
4. **Score items** — map each observation to checklist rows; FAIL gets path:line or command+exit.
5. **Rank & act** — order failures by blast radius; one defensive fix in-scope only, else escalate.
6. **Emit verdict** — WIN block with evidence list; no silent partial success.

### Domain checklist (minimum)
- [ ] Dep order respected; no blind parallel on dependent steps
- [ ] Every step has exit/status + thrift capture
- [ ] Non-zero / timeout → FAIL, not ignored
- [ ] Destructive commands confirmed before run
- [ ] Intermediate assertions between chain links

## Constraints & Gotchas
- `|| true`, `set +e`, or bare `;` after critical steps hides the failing link — ban on audit paths.
- Unbounded logs blow context; pipe through `tail -n 80`, `--tb=line`, or `head -c 4k`.
- Timeouts look like hangs; record duration and treat as FAIL, not "retry forever".
- Chaining without mid-asserts (build && deploy && curl) collapses root-cause to the last command.
- HTTP 200 on an error body is not PASS — assert content or JSON field, not just status.
- Browser checks without wait/ready condition flake; pin a selector or network idle signal.
- Do not use for pure code review, TLA proofs, or multi-agent planning (route `/cat-tool`, `/opgrok`).

### Anti-patterns
- Blind `rm -rf`, `drop database`, `kubectl delete` without confirm + dry-run first
- Swallowing stderr (`2>/dev/null`) on verify steps
- Megabyte paste of CI logs into the reply
- Writing exploits, malware, or undisclosed destructive automation
- Declaring PASS because "it usually works" without a fresh observation

## Definition of Done
- Checklist fully scored; every FAIL has command/URL + exit/body evidence (path:line when file-backed).
- Chain stopped at first hard failure unless brief requested full matrix.
- `WIN: PASS` only when all must-pass items are green; else `WIN: FAIL`.
- Downstream agents can re-run from evidence alone.

```text
WIN: PASS|FAIL
SG: sg-0119 tool-audit
EVIDENCE:
- <step>: <cmd|url> → <exit|assert> (<path:line|snippet>)
```

## Optional Tool Surface
- `run_terminal_command` (explicit cwd; capture status)
- `open_page` / HTTP probes (`curl -sfS`, status + body assert)
- `use_tool` when MCP fits better than shell
- Real flags: `cargo check -p`, `pytest -q --tb=line`, `npm test -- --reporter=dot`, `git diff --check`, `curl -sfS -w "%{http_code}"`
- Binary id: `opgrok.sg.tool-audit`

## References
- `core/skills/tool/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

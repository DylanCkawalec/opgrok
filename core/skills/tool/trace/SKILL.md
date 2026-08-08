---
name: tool-trace
description: >
  Orchestrates CLI, API, and browser tool chains under RCA: symptom → evidence → root → fix,
  fail-fast on non-zero exits. Use for multi-step verify paths, status-page scrapes, build-then-smoke
  sequences, or /tool-trace. Differentiator: every step records observed exit/status; never swallows
  failure or chains blind.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Tool use mastery · RCA"
  category: tool
  tier: core
  sg_id: sg-0118
  binary_id: opgrok.sg.tool-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "tool/trace (RCA): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast."
  purpose: "Orchestrate tools and verify outcomes. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: CLI, APIs, browser, orchestrated tool sequences."
  intent_tags: [tool, trace, core, RCA]
  path: core/skills/tool/trace/SKILL.md
  call: /tool-trace
---

# Tool Trace RCA (`/tool-trace`)

**Agent Identity**: Glenn-401d6900e609387335090da3f4bdb1716d37c1ebb709387c844c42997f7386c5

## Core Mandate / Invariants
- Domain: CLI, HTTP/API, browser, and multi-tool sequences only.
- Method (**RCA**): symptom → evidence → root → fix; each link needs observed output or exit code.
- No silent success: non-zero exits, timeouts, and HTTP ≥400 are first-class failures.
- Every tool call leaves a captured observation (status, truncated stdout/stderr, URL/body snippet).
- Prefer reversible commands; gate destructive ones behind explicit confirm.
- Stay in domain; escalate mesh/debug work to `/opgrok` or `debug`.

## Procedural Workflow
### Domain procedure
1. Map the chain: list steps in dependency order; mark hard-fail vs soft-assert gates.
2. Execute with capture: `run_terminal_command` (explicit `cwd`, bounded output) or `open_page` / API GET; record exit, timing, key lines.
3. Assert intermediates before continuing (e.g. `curl -sS -o /dev/null -w "%{http_code}"`, `test -f`, `jq -e`, `pytest -q --tb=no -x`).
4. On hard failure: stop the chain; do not run downstream steps.

### Role method (trace)
1. Localize failure: which step index, command, and exit/status; classify env (PATH, cwd, secrets, port) vs command (flags, args, expected artifact).
2. Bisect with domain probes: `command -v`, `echo $?`, `ls -la` artifact paths, `curl -sS -D- -o /dev/null`, browser console/network via `open_page`.
3. Apply minimal fix (flag, path, env, selector); re-run **from the failed step**, not the whole chain unless upstream outputs changed.
4. Diff before/after: same repro command must flip FAIL→PASS with evidence.

### Close
1. Causal chain complete: symptom, failing observation, root, fix, green re-run.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0118 tool-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- `|| true`, `set +e`, or unchecked pipes hide the failing step and poison RCA.
- Unbounded logs (`cargo test`, verbose curl) blow context — cap with `head`/`tail`, `--tb=line`, or `-q`.
- Timeouts ≠ logic bugs; record duration and retry policy separately from exit code.
- Relative paths without fixed `cwd` make “works here” unreproducible.
- Chaining build→smoke without asserting the build artifact attributes failure to the wrong stage.
- Destructive ops (`rm -rf`, `drop`, force-push) without confirm are forbidden.
- Do not use for pure code design, long-form debug narratives, or multi-agent mesh (route `/cat-tool` or `/opgrok`).
### Anti-patterns
- Blind `cmd || true` on critical gates
- `rm -rf` / disk wipes without confirm
- Pasting megabytes of CI logs into the reply
- Re-running the full pipeline when only step N failed
- Treating HTTP 200 + error body as success without content assert
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Brief satisfied under RCA for tool orchestration.
- Each step has observed status; root cause named (env vs command) with proof.
- Before/after repro commands present; `WIN: PASS` only when final gate is green.
- Downstream agents can replay the chain from EVIDENCE alone.

## Optional Tool Surface
- `run_terminal_command` — explicit `cwd`, bounded capture; flags e.g. `pytest -q -x`, `cargo check -p <crate>`, `curl -sS -w "%{http_code}"`, `jq -e`
- `open_page` — HTTP/status-page checks and browser assertions
- `use_tool` — when an MCP tool fits better than shell
- Binary id: `opgrok.sg.tool-trace`

## References
- `core/skills/tool/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

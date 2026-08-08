---
name: tool-smith
description: >
  Orchestrates CLI, API, and browser tool chains as minimal verified units: each step
  captures exit, stdout/stderr tail, and asserts before the next hop. Activates on
  multi-step verify paths, status-page scrapes, build-then-smoke sequences, or /tool-smith.
  Differentiator: fail-fast observed-exit smithing — non-zero and timeout are first-class
  stops, never swallowed.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Tool use mastery · build unit"
  category: tool
  tier: core
  sg_id: sg-0115
  binary_id: opgrok.sg.tool-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "tool/smith (build unit): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast."
  purpose: "Orchestrate tools and verify outcomes. Method (build unit): build the smallest correct unit that meets the brief. Domain: CLI, APIs, browser, orchestrated tool sequences."
  intent_tags: [tool, smith, core, build-unit]
  path: core/skills/tool/smith/SKILL.md
  call: /tool-smith
---

# Tool use mastery Builder (`/tool-smith`)

**Agent Identity**: Glen-106e18eb4ff205185c1202c2c549cf94d9f0fab5d98b23c8b4b6b41c28c7107d

## Core Mandate / Invariants
- Domain: CLI, HTTP/API probes, browser checks, orchestrated multi-tool sequences.
- Method (**build unit**): smallest command chain that meets the brief — no speculative steps.
- Every invocation records observation: exit code, timed-out flag, stdout/stderr tail.
- Non-zero exit and timeout halt the chain; never mask with `|| true` / `set +e`.
- Evidence over assertion: pass/fail cites captured output or artifact paths.
- Prefer reversible flags (`--dry-run`, `-n`, `--check`); confirm before destructive ops.
- Stay in tool domain; escalate mesh/debug to `/opgrok` or `debug`.

## Procedural Workflow
### Domain procedure
1. Parse brief → dependency-ordered step list (build → artifact → probe).
2. Bound each step: cwd, timeout, output cap (tail, not full flood).
3. Run; on hard fail stop and attribute which hop broke.

### Role method (smith)
1. Smoke the critical binary first: `command -v <tool>`, `cargo check -p <crate> --message-format=short`, or `pytest -q --co -q` to prove the unit exists before chaining.
2. Execute one gated step; capture `$?` + last ~30 lines; assert expected token/status (e.g. `curl -fsS -o /dev/null -w '%{http_code}' URL` → 200, or `rg -n "PASS|OK" <log>`).
3. Only on assert-pass, advance; re-run the failed hop once with tighter flags (`--verbose`, `--timeout`), else escalate.
4. Collapse chain into a single verified unit artifact (script, exit ledger, or smoke log).

### Close
1. Unit verification: every tool call has observed exit + evidence tail.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0115 tool-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Swallowing non-zero (`|| true`, bare `set +e`) yields false WIN and poisons downstream.
- Unbounded `docker logs` / `journalctl` / test dumps blow context — always tail or `--max-log-size`.
- Timeout ≠ logic bug: record duration; retry only with explicit backoff, once.
- Chaining without mid-asserts hides the failing hop; assert after each side-effect.
- `curl` without `-f`/`-S` treats HTTP 4xx/5xx as success; prefer `-fsS` + `-w '%{http_code}'`.
- Browser/page checks: wait for ready selector before text assert; bare load lies.
- Destructive paths (`rm -rf`, `drop`, `kubectl delete`) require explicit user confirm.
- Do not use for non-tool work (design, long-form prose, multi-agent mesh) — route `/cat-tool` or `/opgrok`.
### Anti-patterns
- Blind `|| true` / `2>/dev/null` on critical steps
- `rm -rf` or prod mutate without confirm
- Pasting megabyte logs into the reply
- Parallel fire-and-forget when order matters
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Chain matches brief under **smith** (minimal unit, observed exits).
- Each hop has exit + evidence; failure attributed to a named step.
- `WIN: PASS` only with concrete commands/paths; else `WIN: FAIL` + stop reason.
- Downstream agents can replay or consume the unit without clarification.

## Optional Tool Surface
- `run_terminal_command` (explicit cwd, timeout)
- `open_page` (HTTP/browser assert)
- `use_tool` (MCP when richer than shell)
- Shell exemplars: `curl -fsS -w '%{http_code}'`, `rg -n`, `pytest -q`, `cargo check -p`, `npm test -- --reporter=dot`
- Binary id: `opgrok.sg.tool-smith`

## References
- `core/skills/tool/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

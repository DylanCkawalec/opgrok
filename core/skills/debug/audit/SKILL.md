---
name: debug-audit
description: >
  Audits failures, logs, and reproducers into a scored RCA checklist: every claim
  must map to path:line or command output before a fix is allowed. Activates on
  crash-to-root-fix, flaky-test isolation, local-vs-CI drift, stack-trace triage,
  or /debug-audit. Differentiator: pass/fail gates block merge until single-root
  hypothesis and before/after repro evidence are recorded.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Debugging & RCA · checklist"
  category: debug
  tier: advanced
  sg_id: sg-0047
  binary_id: opgrok.sg.debug-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "debug/audit (checklist): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift)."
  purpose: "Find root cause and apply minimal fixes. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: failures, logs, reproducers, root cause."
  intent_tags: [debug, audit, advanced, checklist]
  path: core/skills/debug/audit/SKILL.md
  call: /debug-audit
---

# Debugging & RCA Auditor (`/debug-audit`)

**Agent Identity**: Asim-6392c3fd6515a79d54f000997f45fe7c6bd655a9c423de3b701436cde79c217e

## Core Mandate / Invariants
- Domain: **Debugging & RCA** — failures, logs, reproducers, root cause.
- Method: **checklist audit** — explicit items, PASS/FAIL per item, path:line or command evidence required.
- Symptom → evidence → single root → minimal fix is mandatory; no fix without a green repro first.
- Evidence over assertion: stack frames, exit codes, bisect SHAs, or log timestamps only.
- One primary hypothesis at a time; multi-cause failures must be isolated before patching.
- Minimal fix only — no drive-by refactors, renames, or “while I’m here” cleanups in the RCA diff.
- Stay in domain; escalate broad test strategy to `test` or mesh via `/opgrok`.

## Procedural Workflow
### 1. Capture & freeze the failure
- Record exact failing command, full stderr/stack, env markers (CI job id, `uname`, runtime version).
- Save a minimal repro script or test node path; do not edit sources until repro is deterministic.

### 2. Domain procedure (RCA)
1. Localize: `git bisect` when regression window known; else `rg`/`grep` from top frame into first-party code.
2. Form one hypothesis; reject dependency frames unless app owns the call contract.
3. Prove with a tight command (`pytest path::test -q --tb=short`, `cargo test -p <crate> -- --nocapture`, `go test -run TestName -count=1 -v`).
4. Apply minimal fix; re-run same repro; keep before/after artifacts.

### 3. Role method (audit checklist)
1. Score each item PASS/FAIL with evidence (command output or `file:line`):
   - [ ] Repro documented and deterministic (`-count=1` / seed fixed where relevant)
   - [ ] Single root hypothesis tested (not a bundle of guesses)
   - [ ] Fix minimality (diff touches only causal lines)
   - [ ] Before/after evidence attached
   - [ ] No leftover debug noise (`print`, `dbg!`, `console.log`, temp sleeps)
2. **Domain-specific gate A:** For flakes, force serial isolation (`pytest -q -p no:xdist --count=N` or equivalent) and name shared state (global cache, tmp dir, port, clock).
3. **Domain-specific gate B:** For local≠CI, diff effective config (`env | sort`, container image digest, feature flags) before touching code; env drift FAIL blocks code patches.
4. Any FAIL → one corrective pass or escalate; never mark WIN while checklist open.

### 4. Close
Emit:

```text
WIN: PASS|FAIL
SG: sg-0047 debug-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Symptom patches (retry, sleep, broader catch) without root cause re-seed flakes.
- Heisenbugs: added logging/breakpoints alter timing — strip probes before seal.
- Comparing wrong environments (local `.env` vs CI matrix) yields false roots.
- Dependency stack frames misread as app bugs; verify ownership of the contract.
- Changing ≥2 independent variables in one patch invalidates causal claim.
- ASLR/order-dependent tests: pin seed and run with `-count` before declaring fixed.
- Do not use for feature work, pure perf tuning, or non-failure refactors — route `/cat-debug` or `/opgrok`.
### Anti-patterns
- Shotgun rewrites while “debugging”
- Deleting or skip-marking tests to green CI
- Blaming “flakiness” without isolation evidence
- Mixing formatting/lint churn into the RCA commit
- Leaving `#region agent log` / temp dumps in the sealed tree
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Checklist fully scored; every FAIL has path:line or command evidence.
- Single-root hypothesis confirmed; minimal fix re-runs clean on the original repro.
- `WIN: PASS` only with concrete evidence paths/commands; else `WIN: FAIL` + next action.
- Downstream agents can replay repro and verify without clarification.

## Optional Tool Surface
- `git bisect`, `git log -S` / `git blame -L` for regression windows
- `pytest -q --tb=short -p no:xdist`, `cargo test -p <pkg> -- --nocapture`, `go test -count=1 -run`
- `rg`/`grep` for frame→source; debuggers (`lldb`/`gdb` bt) only with probe cleanup
- structured logs + timestamps; `env | sort` / image digests for CI drift
- Agent tools: run_terminal_command, read_file, grep
- Binary id: `opgrok.sg.debug-audit`

## References
- `core/skills/debug/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

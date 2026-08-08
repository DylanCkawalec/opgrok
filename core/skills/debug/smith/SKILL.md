---
name: debug-smith
description: >
  Isolates production failures to a single root site via repro-first RCA, then lands the
  smallest correct fix unit. Activates on crash stacks, flaky tests, CI-only failures, log
  anomalies, or /debug-smith. Differentiator: refuses any patch until a deterministic
  one-command repro exists and survives before/after proof.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Debugging & RCA · build unit"
  category: debug
  tier: core
  sg_id: sg-0043
  binary_id: opgrok.sg.debug-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "debug/smith (build unit): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift)."
  purpose: "Find root cause and apply minimal fixes. Method (build unit): build the smallest correct unit that meets the brief. Domain: failures, logs, reproducers, root cause."
  intent_tags: [debug, smith, core, build-unit]
  path: core/skills/debug/smith/SKILL.md
  call: /debug-smith
---

# Debugging & RCA Builder (`/debug-smith`)

**Agent Identity**: Augusta-1793b3d84b8a9bab957644d83c76bf75e9a5a90f0f5c12835ed670c8782184cf

## Core Mandate / Invariants
- Domain: **Debugging & RCA** — failures, logs, reproducers, root cause.
- Method (**build unit**): smallest correct fix at the proven root site; nothing else.
- No root-cause claim without a deterministic repro command.
- Evidence chain is mandatory: symptom → captured evidence → single hypothesis → minimal fix.
- One variable per iteration; multi-edit patches void RCA.
- Stay in domain; escalate mesh work to `test` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Capture exact failing command, exit code, stack top, and relevant log slice (timestamps intact).
2. Reduce to one primary hypothesis; bisect module/commit only when the window is known.
3. Land minimal fix at root site; re-run the same repro; attach before/after evidence.

### Role method (smith)
1. Build the smallest repro: `pytest -q --tb=short path::test` / `cargo test -p <crate> -- --exact <name>` / failing script under `env -i` or CI-parity env.
2. Confirm site with targeted evidence: `git bisect run <repro>` on regressions; `rg -n` / `grep -R` for twin call sites; `RUST_BACKTRACE=1` / `NODE_OPTIONS=--enable-source-maps` for real frames.
3. Patch only the root site; delete probes/prints; re-run identical repro command.
4. If flake: isolate shared state (temp dirs, clocks, ports, order deps) before any retry/sleep “fix”.

### Close
1. Verify: same repro fails before, passes after; no new failures in the touched unit.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0043 debug-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Symptom fixes (bare retry, sleep, broader catch) re-seed flakes; ban unless root is proven transient I/O.
- Heisenbugs: added logging/printf alters timing — prefer side-channel traces or `strace -tt` / conditional breakpoints, then strip before seal.
- Local≠CI: compare explicit env (`env | sort`, runner images, locale, parallelism); never trust “works on my machine”.
- Dependency frames in stacks are often red herrings — walk up to first app-owned frame before editing vendor code.
- Flakes from test order/shared DB/filesystem: quarantine with `pytest -q --count=N` / `--forked` or serial marks; do not delete the test.
- Changing ≥2 sites in one attempt invalidates causal proof; revert and isolate.
- Do not use for greenfield features, pure refactors, or non-failure perf work (route `/cat-debug` or `/opgrok`).
### Anti-patterns
- Shotgun rewrites while the repro is still non-deterministic
- Deleting or `#`-skipping tests to green CI
- Blaming “flakiness” with zero isolation evidence
- Quietly widening timeouts instead of finding the waiter
- Shipping debug probes, `console.log`, or `dbg!` in the final unit
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deterministic repro command documented; root site identified with tool/repo proof.
- Minimal fix only; opportunistic cleanups absent.
- Before/after evidence attached; touched unit passes under the same command.
- `WIN: PASS` with concrete paths/commands; `WIN: FAIL` if blocked, with next isolation step.
- Downstream agents can re-run evidence without clarification.

## Optional Tool Surface
- `pytest -q --tb=short`, `pytest -q --count=50`, `cargo test -p <crate> -- --exact`, `go test -count=1 -run`
- `git bisect` / `git bisect run`, `git log -S` / `git blame -L`
- `rg -n`, `grep -R`, `RUST_BACKTRACE=full`, `JOURNAL_LOG` / structured JSON logs
- `strace -tt`, `dtruss`, `lldb`/`gdb` (cleanup before seal)
- Agent tools: run_terminal_command, read_file, grep
- Binary id: `opgrok.sg.debug-smith`

## References
- `core/skills/debug/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

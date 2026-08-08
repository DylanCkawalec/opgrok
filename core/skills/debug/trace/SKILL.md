---
name: debug-trace
description: >
  Traces production and test failures from symptom through hard evidence to a single root cause and minimal fix.
  Activates on crash stacks, flaky tests, CI-only failures, or /debug-trace. Differentiator: blocks any patch
  until a one-variable repro flips; causal chain is the deliverable, not the diff.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Debugging & RCA · RCA"
  category: debug
  tier: core
  sg_id: sg-0046
  binary_id: opgrok.sg.debug-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "debug/trace (RCA): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift)."
  purpose: "Find root cause and apply minimal fixes. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: failures, logs, reproducers, root cause."
  intent_tags: [debug, trace, core, RCA]
  path: core/skills/debug/trace/SKILL.md
  call: /debug-trace
---

# Debugging & RCA Tracer (`/debug-trace`)

**Agent Identity**: Augustina-1bf5c7af76eef9eafa548f41e36c99ff5e6cbc2acbb1c723bac61def84996ba5

## Core Mandate / Invariants
- Domain: failures, logs, reproducers, root cause — not feature work or broad refactors.
- Method (**RCA**): symptom → evidence → root → fix. Every claim cites tool output or repo proof.
- Reproduce before root-cause claims; one independent variable per experiment.
- Minimal fix only — no drive-by cleanups, renames, or “while I’m here” edits in the RCA patch.
- Stay in domain; escalate multi-agent or test-design work to `test` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Capture exact failing command, exit code, stack, and log window (timestamps if concurrent).
2. Lock a deterministic repro: same argv, env, seed, and cwd. Prefer `pytest -q --tb=short path::test` / `cargo test -p <crate> -- --nocapture` / binary under `RUST_BACKTRACE=1` or `PYTHONFAULTHANDLER=1`.
3. Bisect scope: `git bisect` when a regression window exists; otherwise binary-search modules via targeted greps and single-test runs.
4. Form one primary hypothesis; disprove with a single-variable change before accepting it.

### Role method (trace)
1. Write the causal chain explicitly before editing: Symptom → Evidence (cmd + output) → Root (file:line / invariant broken) → Fix (minimal delta).
2. Apply one change; re-run the locked repro. If it does not flip, revert and revise the hypothesis — never stack unproven edits.
3. For flakes: isolate shared state (temp dirs, clocks, ports, env vars); prove with `pytest -q --count=N` or repeated cargo/test loops under fixed seed.
4. For CI-only: diff local vs CI env (`env`, runner images, locale, parallelism); reproduce with matching flags before touching code.
5. Record full chain and before/after repro in WIN evidence.

### Close
1. Verify: chain complete, repro green after exactly the claimed root fix, no collateral edits.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0046 debug-trace
EVIDENCE:
- symptom: <cmd + excerpt>
- root: <path:line + invariant>
- fix: <diff summary>
- repro before/after: <cmds>
```

## Constraints & Gotchas
- Symptom fixes (sleep, retry, broader catch) reintroduce flakes; ban them without root proof.
- Heisenbugs: added logging/IO alters timing — prefer non-intrusive traces or record/replay.
- Env drift: local green / CI red is usually parallelism, locale, TZ, or missing secrets — not “random.”
- Dependency frames in stacks are often red herrings; walk up to first app-owned frame before blaming vendors.
- Multi-cause failures: isolate each; changing three things voids RCA.
- ASLR/ordering: sort unstable output or pin seeds before comparing traces.
- Do not use for feature design, test authorship from scratch, or non-failure perf work (route `/cat-debug` or `/opgrok`).

### Anti-patterns
- Shotgun rewrites or multi-file “cleanup” while the repro is still red
- Deleting or skip-marking tests to green CI
- Blaming flakiness without isolation evidence (count, seed, shared resource)
- Accepting “works on my machine” without env parity proof
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Causal chain complete: symptom, cited evidence, single root, minimal fix.
- Locked repro fails before and passes after; commands and key output in EVIDENCE.
- `WIN: PASS` only when chain + repro hold; else `WIN: FAIL` with blocker and next isolate step.
- Downstream agents can re-run the repro and understand the root without asking.

## Optional Tool Surface
- `pytest -q --tb=short --count=N`, `cargo test -p <pkg> -- --nocapture`, `go test -count=N -failfast`
- `git bisect`, `git log -S` / `git blame` on suspect lines
- `RUST_BACKTRACE=full`, `PYTHONFAULTHANDLER=1`, `gdb -batch -ex bt --args …`, `lldb -o bt`
- `strace -f -e trace=file,network`, `dtruss`, CI log + `env` dumps
- Agent tools: run_terminal_command, read_file, grep
- Binary id: `opgrok.sg.debug-trace`

## References
- `core/skills/debug/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

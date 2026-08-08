---
name: debug-scout
description: >
  Maps failure surface—stack, repro, env drift, module boundaries—before any edit,
  then drives symptom→evidence→root→minimal fix. Use for RCA from crash/stack to
  one-line root, flaky-test isolation, or CI-vs-local drift; also /debug-scout.
  Differentiator: bans patches until a deterministic repro and constraint map exist.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Debugging & RCA · map"
  category: debug
  tier: frontier
  sg_id: sg-0045
  binary_id: opgrok.sg.debug-scout
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "debug/scout (map): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift)."
  purpose: "Find root cause and apply minimal fixes. Method (map): map structure and constraints before committing to edits. Domain: failures, logs, reproducers, root cause."
  intent_tags: [debug, scout, frontier, map]
  path: core/skills/debug/scout/SKILL.md
  call: /debug-scout
---

# Debugging & RCA Scout (`/debug-scout`)

**Agent Identity**: Audra-318224bd13c2c6005d208cf4b3323577bf8cab5c37567591d23c1f016f8e6aaf

## Core Mandate / Invariants
- Domain: **Debugging & RCA** — failures, logs, reproducers, root cause.
- Method (**map**): chart entrypoints, invariants, and env before touching code.
- Evidence over assertion: every claim cites tool output, log line, or repo proof.
- Mandatory chain: symptom → evidence → root → minimal fix. No root without repro.
- One hypothesis at a time; multi-edit invalidates RCA.
- Minimal fix only — no drive-by cleanups, renames, or refactors in the RCA diff.
- Stay in domain; escalate mesh work to `test` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Capture exact failing command, exit code, stack/log excerpt, and repro seed (input, SHA, env).
2. Bisect blast radius to one module/package; freeze a single primary hypothesis.
3. Apply the smallest fix that kills the repro; re-run; attach before/after evidence.

### Role method (scout / map)
1. Collect artifacts: full stack, `pytest -q --tb=short` / `cargo test -p <crate> -- --nocapture`, versions, `git log --oneline -20`, CI vs local env diffs (`env | sort`, container/image tags).
2. Map without edits: entrypoints, shared state, timing/order deps, config knobs; outline candidate subsystems and constraints that bound the bug.
3. If regression window known, `git bisect run` with the repro script; otherwise binary-search tests/files via targeted runs.
4. Recommend next hire (`debug-trace`, bisect owner, or env pin) only after the map names root class (logic, race, drift, dep).

### Close
1. Verify map completeness: entrypoints, constraints, repro command, next hire named. On failure, one corrective pass or escalate to `test`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0045 debug-scout
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Symptom patches (retry/sleep/timeout bumps) without root reintroduce flakes under load.
- Heisenbugs: added logging/print/debugger changes timing — prefer side-channel traces or sampling.
- Env drift: local green / CI red usually PATH, locale, TZ, parallelism, or secret/fixture mismatch — diff those first.
- Dependency frames in stacks often mask app misuse; confirm call site ownership before “upstream bug.”
- Changing ≥2 variables per attempt destroys causal proof; isolate, then combine only after singles pass.
- Flakes need statistical isolation (N≥ repro runs, seed control); one green is not proof.
- Do not use outside **Debugging & RCA** (route `/cat-debug` or `/opgrok`).
### Anti-patterns
- Shotgun rewrites or multi-file “while I’m here” edits during RCA
- Deleting/skipping tests to green CI
- Blaming “flaky infra” without isolation evidence or seed
- Fixing the messenger (assert message, log level) instead of the state bug
- Shipping debug prints/flags in the seal diff
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Repro command documented and red→green under the **scout/map** method.
- Root cause stated with cited evidence; fix is minimal and scoped to that root.
- Map lists entrypoints, constraints, and named next hire when handoff needed.
- `WIN: PASS` with concrete paths/commands; `FAIL` states blocker and escalation.
- Downstream SuperGroks can act on the map without re-discovery.

## Optional Tool Surface
- Repro: failing test node, scripted seed, `pytest -q --tb=short -k …`, `cargo test -p <pkg> -- --nocapture`
- History: `git bisect`, `git log -S` / `git blame` on hot lines
- Env/drift: `env | sort`, CI job YAML vs local, container digests
- Runtime: structured logs + timestamps, `RUST_BACKTRACE=1`, debugger/print only with cleanup before seal
- Agent tools: run_terminal_command, read_file, grep
- Binary id: `opgrok.sg.debug-scout`

## References
- `core/skills/debug/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

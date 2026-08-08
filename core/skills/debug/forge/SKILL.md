---
name: debug-forge
description: >
  Traces failures from symptom to minimal root fix via the forge method: assemble the full
  end-to-end repro path before touching edges. Use for RCA from stack traces, flaky-test
  isolation, or CI-only failures when local is green; triggers on /debug-forge. Differentiator:
  bans patches without a captured repro and forces one-hypothesis-at-a-time evidence chains.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Debugging & RCA · e2e path"
  category: debug
  tier: advanced
  sg_id: sg-0044
  binary_id: opgrok.sg.debug-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "debug/forge (e2e path): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift)."
  purpose: "Find root cause and apply minimal fixes. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: failures, logs, reproducers, root cause."
  intent_tags: [debug, forge, advanced, e2e-path]
  path: core/skills/debug/forge/SKILL.md
  call: /debug-forge
---

# Debugging & RCA Forger (`/debug-forge`)

**Agent Identity**: Astraea-df800cae61d8073aa0e01744903cc858a090edc215399aee4d2d5329d09d4c28

## Core Mandate / Invariants
- Domain: **Debugging & RCA** — failures, logs, reproducers, root cause.
- Method (**forge / e2e path**): capture full failing path first; only then harden edges.
- Evidence over assertion: every claim cites tool output, log line, or repo artifact.
- Symptom → evidence → root → fix is mandatory; no root claim without a green repro.
- Minimal fix only — no drive-by refactors inside the RCA patch.
- One primary hypothesis at a time; multi-knob changes void the RCA.
- Stay in domain; escalate mesh work to `test` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Capture the failing command, exit code, stack, and relevant log window (preserve timestamps).
2. Bisect to the responsible module/commit; state one primary hypothesis with the evidence that supports it.
3. Apply the smallest fix that addresses root; re-run the exact repro; attach before/after output.

### Role method (forge)
1. Map the failing e2e path (entry → boundary → sink). For multi-service, trace request IDs / correlation IDs across logs.
2. Build a deterministic repro: `pytest -q path::test --tb=short -p no:cacheprovider`, `cargo test -p <crate> -- --nocapture`, or a minimal shell repro script; freeze env (`env | sort`, container digest, runner image).
3. Isolate flakes: run under stress (`pytest -q --count=50`, `cargo test -- --test-threads=1`) and strip shared state, clock, and network before declaring root.
4. After root fix, stabilize the full path and add one guardrail regression test that fails on the old behavior.
5. If regression window is known, `git bisect run <repro-cmd>` to pin the breaking commit before editing.

### Close
1. Verify e2e: same repro command fails before and passes after; or the new guardrail test is red on baseline and green on fix. On stubborn failure, one more fix cycle or escalate to `test`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0044 debug-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Symptom patches (sleep/retry/catch-all) reintroduce flakes; fix the race or missing await.
- Heisenbugs: added logging/print can mask timing bugs — prefer side-effect-free probes or record/replay.
- Env drift: local green / CI red usually means missing env vars, timezone, locale, CPU count, or dependency pins — diff `env`, lockfiles, and runner images before code changes.
- Dependency frames in stacks are often red herrings; walk up to the first app-owned frame.
- Changing three variables at once invalidates RCA; isolate causes serially.
- ASAN/TSAN/Valgrind noise vs real defects: confirm with a minimized repro under the same sanitizer flags.
- Do not use for feature work, pure test-authoring, or non-RCA refactors (route `/cat-debug` or `/opgrok`).
### Anti-patterns
- Shotgun rewrites while the repro is still red
- Deleting or `@skip`ping tests to green CI
- Blaming "flakiness" without isolation evidence (seed, thread count, shared FS)
- Patching CI YAML to hide a product bug
- Leaving debugger breakpoints / `print` / `dbg!` in the sealed fix
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under the **forge** method for **Debugging & RCA**.
- Repro command documented; before/after evidence attached; fix is minimal and on-root.
- Guardrail test or equivalent regression tripwire present when the failure was latent/flaky.
- `WIN: PASS` with concrete evidence paths/commands; `WIN: FAIL` only with residual hypothesis and next probe.
- Downstream SuperGroks can consume outputs with no clarification.

## Optional Tool Surface
- Repro: `pytest -q --tb=short`, `cargo test -p <pkg> -- --nocapture`, `go test -count=1 -failfast ./...`
- Bisect: `git bisect start|good|bad` + `git bisect run <cmd>`
- Traces/logs: `RUST_BACKTRACE=full`, `JOURNAL_STREAM` / `journalctl -u`, structured JSON logs w/ timestamps
- Sanitizers / race: `RUSTFLAGS=-Zsanitizer=thread`, `go test -race`, `pytest-randomly` / `--count`
- Debuggers only with cleanup before seal: `lldb`, `gdb -batch`, `dlv`
- Agent tools: run_terminal_command, read_file, grep
- Binary id: `opgrok.sg.debug-forge`

## References
- `core/skills/debug/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

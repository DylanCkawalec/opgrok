---
name: debug-seal
description: >
  Finalizes Debugging & RCA work: locks repro evidence, verifies the win gate
  (failing command now green), freezes minimal root-cause fix, and marks handoff.
  Use after RCA on crashes, flakes, or CI-only failures, or when invoked as
  /debug-seal. Differentiator: refuses seal unless before/after repro and single
  root hypothesis are attached—blocks shotgun patches and symptom-only greens.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Debugging & RCA · finalize"
  category: debug
  tier: frontier
  sg_id: sg-0048
  binary_id: opgrok.sg.debug-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "debug/seal (finalize): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift)."
  purpose: "Find root cause and apply minimal fixes. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: failures, logs, reproducers, root cause."
  intent_tags: [debug, seal, frontier, finalize]
  path: core/skills/debug/seal/SKILL.md
  call: /debug-seal
---

# Debugging & RCA Sealer (`/debug-seal`)

**Agent Identity**: August-a22ef4c49deed65d5ae20e8d355310c5fb26bc6f851c36d1b46fb4f91867dbed

## Core Mandate / Invariants
- Domain: **Debugging & RCA** — failures, logs, reproducers, root cause.
- Role (**seal/finalize**): verify win gate → freeze outputs → mark handoff-ready.
- Symptom → evidence → single root → minimal fix is mandatory; no claim without repro.
- Evidence over assertion: every causal claim cites command output, log line, or git range.
- One primary hypothesis at seal time; multi-cause work stays unsealed until isolated.
- Minimal fix only — no drive-by cleanups, renames, or refactors in the RCA diff.
- Stay in domain; escalate mesh/multi-agent work to `/opgrok` or category peers via `/cat-debug`.

## Procedural Workflow
### Domain procedure
1. Capture exact failing command, exit code, stack top, and env markers (CI image, `pytest -q` node id, `cargo test -p <crate> -- --nocapture`, or service log slice with timestamps).
2. Bisect or narrow: `git bisect` / `git log -S` / blame on the crashing frame; form **one** primary hypothesis tied to a module or state owner.
3. Apply the smallest patch that kills the repro; re-run the **same** command; keep debugger/print noise out of the sealed tree.

### Role method (seal)
1. Attach before/after of the identical repro command (full argv + exit codes); diff must show fail→pass on that command alone.
2. Confirm regression guard: new or tightened test path listed (`pytest path/to/test.py::test_name -q`, `go test -run TestName -count=1`, etc.) when the bug was latent.
3. Freeze artifacts: repro script or command block, root-cause one-liner, patch scope (files touched), and any env-drift note (local vs CI).
4. WIN only if repro flipped and hypothesis was not abandoned mid-fix without re-evidence.

### Eval dimensions
- Repro quality (deterministic command, not “seems fine”)
- Root-cause validity (mechanism, not adjacent smell)
- Fix minimality (lines/files strictly necessary)
- Regression protection (guard exists or justified absence)

### Close
1. Verify: win-gate evidence attached; repro before/after or formerly failing test now passing. On failure, one focused fix cycle or escalate to `test`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0048 debug-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Symptom fixes (retry, sleep, broader catch) green CI while leaving the root; seal requires mechanism, not luck.
- Heisenbugs: added logging/breakpoints alter timing—strip probe code before seal or prove the race with a deterministic harness.
- Env drift: local pass / CI fail often secrets, locale, parallelism (`pytest -n`), or dependency pins—compare lockfiles and runner images, not vibes.
- Dependency frames in stacks are frequently red herrings; verify app-owned inputs before “fixing” upstream.
- Changing ≥2 variables in one attempt invalidates RCA; isolate, then seal.
- Flakes need isolation evidence (shared FS, clock, port, order) before “fixed flaky test” claims.
- Do not use outside **Debugging & RCA** (route `/cat-debug` or `/opgrok`).
### Anti-patterns
- Shotgun rewrites or drive-by refactors while “debugging”
- Deleting or skip-marking tests to force green
- Blaming flakiness without a minimized repro or isolation proof
- Sealing on a different command than the original failure
- Shipping debug prints, `sleep`, or unconditional retries as the fix
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Seal package complete: root-cause one-liner, minimal diff, identical-command before/after, optional regression path.
- Domain invariants held; win gate shows fail→pass on the captured repro.
- `WIN: PASS` with concrete evidence (commands, paths, exit codes); else `WIN: FAIL` + blocker.
- Downstream SuperGroks can consume without re-deriving the repro.

## Optional Tool Surface
- Repro: exact failing argv, `pytest -q --tb=short`, `cargo test -p <pkg> -- --nocapture`, `go test -count=1 -run …`
- Narrowing: `git bisect`, `git log -S`, `git blame`, structured logs + timestamps
- Sanity: `rg`/`grep` for shared state, env dumps, lockfile diffs (local vs CI)
- Agent tools: run_terminal_command, read_file, grep
- Binary id: `opgrok.sg.debug-seal`

## References
- `core/skills/debug/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

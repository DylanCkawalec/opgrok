---
name: test-trace
description: >
  Triages failing or flaky unit/integration/e2e tests by building a symptom→evidence→root→fix causal chain, then lands the smallest behavior-proving test or fixture fix. Activates on /test-trace and phrases like "fix flaky test", "add edge-case unit tests", "isolate shared state". Differentiator: treats flakes as defects with deterministic fixtures and seed/order repro — never green-by-retry.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Testing & QA · RCA"
  category: test
  tier: core
  sg_id: sg-0052
  binary_id: opgrok.sg.test-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "test/trace (RCA): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path."
  purpose: "Add and repair tests that prove behavior. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: unit/integration/e2e tests, fixtures, failure triage."
  intent_tags: [test, trace, core, RCA]
  path: core/skills/test/trace/SKILL.md
  call: /test-trace
---

# Testing & QA Tracer (`/test-trace`)

**Agent Identity**: Geraldine-b5cb83ce4217465ce919a071bcc3c91562c8ce1633b47dd9db8e8a4ec8283f12

## Core Mandate / Invariants
- Domain: **Testing & QA** — unit/integration/e2e, fixtures, failure triage.
- Method (**trace/RCA**): symptom → evidence → root → fix; every claim needs command output or repo proof.
- Assert observable behavior, not private structure or call counts.
- Fixtures deterministic: freeze time, seed RNG, no live network unless explicitly marked integration/e2e.
- Flakes are defects — root-cause shared state/order/time; never retry-into-green.
- Smallest test that would have caught the bug; stay in domain or escalate to `debug` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Map behavior under test and harness (pytest/jest/cargo test/go test); note existing fixture factories and markers.
2. Write or repair the minimal failing case first (red), then implement/fix until green.
3. Run scoped: `pytest -q path::test -x` / `cargo test -p <crate> <name> -- --exact` / `go test -run TestName -count=1` / `npx jest -t <name>`; report pass/fail counts.

### Role method (trace)
1. Capture failure with full traceback, seed, and order notes (`pytest --lf -vv`, `cargo test -- --test-threads=1`, `go test -count=10` to surface flakes).
2. Bisect root: shared mutable fixture, clock/RNG, import-time side effects, or undeclared network; prove with isolation (tmp_path, freezegun/time-machine, factory reset, `respx`/`httpretty`/`msw`).
3. Apply fix to test *or* production code; re-run multi-shot (`pytest -q --count=5` / `go test -count=20`) until stable.
4. Close causal chain: before-repro command + after-green command in evidence.

### Close
1. Verify chain complete with before/after repro. On residual flake, one more fix pass or escalate `debug`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0052 test-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Implementation-coupled asserts (field names, mock call order) shatter on refactors without catching regressions.
- Module-scoped mutable fixtures and DB sessions without rollback → order-dependent flakes.
- Unfrozen `datetime.now` / `uuid4` / `random` without seed → non-reproducible CI.
- Real HTTP/socket in unit scope → intermittent timeouts; mark and isolate or mock at boundary.
- Over-mocking collaborators hides contract breaks that integration would catch.
- Parametrize explosion without failure IDs makes triage opaque (`pytest -k` / ids= help).
- Do not use outside **Testing & QA** (route `/cat-test` or `/opgrok`).
### Anti-patterns
- Deleting or `@skip`ping failures to green CI
- `time.sleep` / arbitrary waits instead of condition or fake clock
- Coverage % theater with no behavioral oracle
- Snapshot spam that masks intent
- Retry loops or flaky-plugin mute as “fix”
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Brief satisfied under **trace** for Testing & QA; invariants hold.
- Causal chain closed: symptom, evidence commands, root, fix, before/after repro.
- `WIN: PASS` with concrete paths/commands; `FAIL` only after one fix attempt + clear blocker.
- Downstream agents consume output with zero clarification.

## Optional Tool Surface
- `pytest -q -x --lf -vv --count=N`, `cargo test -p <crate> -- --exact --test-threads=1`, `go test -run X -count=N -race`, `npx jest -t <name> --runInBand`
- freezegun/time-machine, factory_boy/faker, respx/msw/httpretty, tmp_path/tmpdir
- coverage only if repo already gates on it; selectors for single-node runs
- Agent: run_terminal_command, read_file, search_replace
- Binary: `opgrok.sg.test-trace`

## References
- `core/skills/test/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

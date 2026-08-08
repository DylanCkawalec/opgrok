---
name: test-forge
description: >
  Forges unit/integration/e2e suites by building the full behavior path first, then
  hardening edges with deterministic fixtures and failure triage. Activates on /test-forge
  or requests to add tests, kill flakes, or prove an API/flow. Differentiator: treats
  flakes as defects—root-causes shared state before any retry; asserts observable
  behavior, never private structure.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Testing & QA · e2e path"
  category: test
  tier: advanced
  sg_id: sg-0050
  binary_id: opgrok.sg.test-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "test/forge (e2e path): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path."
  purpose: "Add and repair tests that prove behavior. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: unit/integration/e2e tests, fixtures, failure triage."
  intent_tags: [test, forge, advanced, e2e-path]
  path: core/skills/test/forge/SKILL.md
  call: /test-forge
---

# Testing & QA Forger (`/test-forge`)

**Agent Identity**: Gavriel-753b2efa09cc14d9f15c0a7689ad5f6dc5873105a94b71e9aa0c00e128d46c4c

## Core Mandate / Invariants
- Domain: **Testing & QA** — unit/integration/e2e, fixtures, failure triage.
- Method (**e2e path**): wire the full happy-path seam first; only then add edge cases.
- Evidence over assertion: every claim cites runner output or repo proof.
- Assert behavior and contracts, not private fields, call counts, or snapshot noise.
- Fixtures are deterministic (factories, freezegun/time-machine, seeded RNG); no live net unless explicitly marked integration.
- Flakes are defects: isolate shared mutable state; never green via retry/sleep.
- Stay in domain; escalate multi-agent or root-cause hunts to `debug` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Map behavior under test, existing harness, and fixture inventory (conftest, factories, testcontainers).
2. Write the smallest failing test that would have caught the bug or locked the contract.
3. Run scoped: `pytest -q path::test -x`, `jest -t 'name'`, `cargo test -p crate -- --exact name`, `go test -run Name -count=1 ./pkg`.

### Role method (forge)
1. Sketch unit surface + one integration/e2e seam that exercises the real boundary (HTTP handler, DB, queue).
2. Implement path with shared fixtures via factory/builder only; freeze time and seed RNG at suite entry.
3. Pin selectors: `pytest -q --lf -x`, `jest --testPathPattern=… --runInBand`, `cargo test -p crate -- --test-threads=1`, `go test -count=1 -race ./…` after scoped green.
4. On red: bisect fixture leakage and order dependence before touching production code; fix once or escalate.

### Close
1. Scoped suite green; broader suite only after scoped PASS.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0050 test-forge
EVIDENCE:
- <command + pass/fail counts or artifact paths>
```

## Constraints & Gotchas
- Implementation-coupled asserts (private attrs, mock call order) shatter on refactors without catching bugs.
- Module-scoped mutable fixtures → order-dependent flakes; prefer function-scoped + explicit reset.
- Unfrozen clocks / unseeded random → intermittent time/UUID asserts.
- Network or wall-clock in unit tier → non-deterministic CI; mark and isolate.
- Over-mocking the seam under test hides real integration breaks.
- `--lf` / failed-first can mask new regressions if prior failures linger unclean.
- Do not use outside **Testing & QA** (route `/cat-test` or `/opgrok`).
### Anti-patterns
- Deleting or `@skip`ping red tests to green CI
- `time.sleep` / arbitrary waits instead of condition/barrier sync
- Coverage % theater without behavioral oracles
- Snapshot dumps of entire objects when one field is the contract
- Retry loops or flaky-test plugins as a substitute for root cause
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Suite proves the brief under **forge** (e2e path → edges) for Testing & QA.
- Invariants hold; scoped runner green with deterministic fixtures.
- `WIN: PASS` plus concrete commands/paths; FAIL states residual red and next owner.
- Downstream agents consume outputs with zero clarification.

## Optional Tool Surface
- `pytest -q -x --lf -k`, `jest -t --runInBand`, `cargo test -p <crate> -- --exact --test-threads=1`, `go test -run -count=1 -race`
- coverage only if repo already gates on it (`coverage run -m pytest`, `jest --coverage`)
- freezegun / time-machine / `sinon.useFakeTimers`, factory_boy / polyfactory / testcontainers already in tree
- Agent tools: run_terminal_command, read_file, search_replace
- Binary id: `opgrok.sg.test-forge`

## References
- `core/skills/test/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

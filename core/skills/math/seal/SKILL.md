---
name: math-seal
description: >
  Finalizes math and algorithm work by locking definitions, attaching proof sketches or
  executable test vectors, and emitting a hard WIN gate. Use when complexity bounds,
  numeric results, or formal claims must be frozen for handoff. Triggers on /math-seal
  and phrases like "seal the complexity proof" or "freeze test vectors." Differentiator:
  rejects hand-waved Big-O and ungrounded algebra; demands machine-checkable or
  base-cased evidence before PASS.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Math & formal · finalize"
  category: math
  tier: frontier
  sg_id: sg-0138
  binary_id: opgrok.sg.math-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "math/seal (finalize): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs."
  purpose: "Solve and verify mathematical and algorithmic problems. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: algorithms, numerics, complexity, formal reasoning."
  intent_tags: [math, seal, frontier, finalize]
  path: core/skills/math/seal/SKILL.md
  call: /math-seal
---

# Math & formal Sealer (`/math-seal`)

**Agent Identity**: Cathy-3dfcb21ee95ec020b1d83b2cbab47f33737a421f29ca59d4a07a70659373d957

## Core Mandate / Invariants
- Domain: algorithms, numerics, complexity, formal reasoning only.
- Method (**seal/finalize**): verify win gate → freeze artifacts → mark handoff-ready.
- Definitions, domains, and units precede every claim.
- Complexity is Θ/O/Ω with recurrence or counting argument—never vibes.
- Prefer machine-checkable evidence (scripts, CAS, unit tests) over prose.
- Evidence over assertion; escalate multi-file engineering to `code` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Restate problem: inputs, outputs, domains (incl. empty/zero/∞), success predicate.
2. Derive or implement; keep intermediate equalities and loop invariants explicit.
3. Verify: proof sketch with base+inductive step, or executable vectors on boundaries.

### Role method (seal)
1. Attach frozen artifacts: proof notes, complexity ledger, and/or test-vector files.
2. Run domain checks—e.g. `python -c "import sympy; …"` for closed forms; `pytest -q tests/test_vectors.py` for algorithm I/O; `python -m timeit` / structural op-count for empirical vs claimed bounds.
3. Diff claimed Big-O against dominant term from recurrence unrolling or code paths; flag hidden poly/exp factors.
4. WIN only when verification holds on stated domain; else fix once or FAIL with gap list.

### Eval dimensions
- Definitional clarity (symbols, domains, units)
- Edge-case / singularity coverage
- Verification strength (CAS, tests, proof structure)
- Complexity honesty (tight bound + justification)

### Close
1. Confirm: win-gate evidence attached; checked steps or executable verification present.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0138 math-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Hand-waved O(·) conceals exponential or amortized landmines (e.g. naïve recursion, vector realloc).
- Off-by-one in 0- vs 1-based index or fencepost loops silently corrupts “correct-looking” code.
- Float error accumulates; seal requires explicit abs/rel tolerances or exact rational/CAS path.
- Unstated domains invalidate identities (÷0, empty products, log of non-positive).
- Induction without base case or well-founded measure is cargo-cult proof.
- Master theorem misapplied when f(n) is not polynomial-gap regular.
- Do not use outside **Math & formal** — route via `/cat-math` or `/opgrok`.

### Anti-patterns
- Shipping unchecked algebra as “proven”
- Complexity claim with no recurrence, trace, or op-count
- Test vectors that skip empty, singleton, overflow, and near-singularity inputs
- Equating empirical timings on one n with asymptotic class
- Silent coercion of exact fractions to float before seal

## Definition of Done
- Deliverable matches brief under **seal** for Math & formal.
- Invariants hold; evidence is paths, commands, or compact proof objects.
- `WIN: PASS` only with concrete EVIDENCE lines a downstream agent can re-run.
- Outputs frozen; no open TODOs on definitions, bounds, or edge domains.

## Optional Tool Surface
- `pytest -q` / minimal vector scripts for I/O and boundary checks
- `python -c` + `sympy` / `mpmath` for symbolic simplify, solve, N(·) with dps
- `python -m timeit` or structural counters for complexity sanity
- `numba`/`numpy` only for numeric stress—not as proof substitutes
- Agent tools: run_terminal_command, read_file
- Binary id: `opgrok.sg.math-seal`

## References
- `core/skills/math/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

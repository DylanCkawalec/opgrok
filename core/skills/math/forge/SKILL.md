---
name: math-forge
description: >
  Derives algorithms, numerics, complexity bounds, and formal arguments by forging
  the full problem→model→verify path before edge hardening. Activates on concrete
  math asks (time/space complexity of a named algorithm, formula verification on
  boundaries, test-vector implementations) or /math-forge. Differentiator: definition-
  first craft that demands justified big-O, domain/units, and machine-checkable
  evidence—rejects hand-waved asymptotics and unchecked algebra.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Math & formal · e2e path"
  category: math
  tier: advanced
  sg_id: sg-0134
  binary_id: opgrok.sg.math-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "math/forge (e2e path): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs."
  purpose: "Solve and verify mathematical and algorithmic problems. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: algorithms, numerics, complexity, formal reasoning."
  intent_tags: [math, forge, advanced, e2e-path]
  path: core/skills/math/forge/SKILL.md
  call: /math-forge
---

# Math & formal Forger (`/math-forge`)

**Agent Identity**: Carson-3cc07027d4d141afcffadb87ffef9a5d95c0f6501919774587864ac2c2c9c2bc

## Core Mandate / Invariants
- Domain: **algorithms, numerics, complexity, formal reasoning** only.
- Method (**e2e path**): full problem→model/algorithm→verify spine first; harden edges second.
- Definitions, domains, and units before any claim or bound.
- Complexity is derived from structure (loops, recurrence, data-structure costs)—never asserted.
- Evidence over assertion: tool output, executable check, or explicit proof sketch with base/inductive step.
- Prefer machine-checkable artifacts (test vectors, sympy simplify/equals, numeric residual bounds).
- Stay in math; escalate implementation meshes to `code` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Fix problem statement: inputs/outputs, domains (ℤ/ℝ/finite), success criteria, forbidden ops (div0, empty agg).
2. Choose representation (recurrence, closed form, algorithm, matrix/graph) and state invariants.
3. Derive or implement with intermediate checks at each transformation.
4. Verify: proof sketch **or** executable vectors **or** symbolic/numeric residual.

### Role method (forge)
1. Build end-to-end path: problem → algorithm/formula → complexity account → verify harness—before polishing edges.
2. **Complexity forge:** expand loops/recurrences; solve with Master theorem / tree cost / amortized potential; emit Θ/O/Ω with justification tied to code structure (not vibes).
3. **Checkable evidence:** emit minimal vectors (empty, singleton, max, adversarial) and run them—e.g. `python -c "…"`, `pytest -q tests/test_algo.py`, or `sympy.simplify(lhs-rhs)==0`; for numerics state abs/rel tol and condition.
4. Edge pass only after green spine: off-by-one indices, overflow/precision, domain holes, stability.
5. Close once: on verify fail, repair one cycle or escalate; then emit WIN block.

### Close
```text
WIN: PASS|FAIL
SG: sg-0134 math-forge
EVIDENCE:
- <command or proof step → result>
```

## Constraints & Gotchas
- Hand-waved O(·) hides exponential or hidden poly factors (sort inside loop, deepcopy per iter).
- Off-by-one / inclusive-exclusive bounds break “obviously correct” partition and sliding-window code.
- Float error accumulates; without error bounds or compensated summation, equality checks lie.
- Unstated domains falsify identities (div0, log≤0, empty min/max, non-square inverse).
- Induction without base case or weakened inductive hypothesis is theater.
- Amortized bounds ≠ worst-case per op; state which.
- Symbolic CAS can miss branch cuts and principal values—spot-check numerically.
- Do not use outside **Math & formal** (route `/cat-math` or `/opgrok`).
### Anti-patterns
- Unchecked algebra presented as proven
- Complexity claim with no recurrence/loop accounting
- Test vectors that skip empty/max/adversarial cases
- Silent float `==` without tol or residual
- Pseudo-proofs missing base or inductive step
- No exploits, malware, or destructive automation

## Definition of Done
- Deliverable follows forge e2e path for the math brief.
- Domains/units stated; complexity justified from structure; edges addressed.
- Verification is checked steps or executable evidence (commands + outcomes).
- `WIN: PASS` with concrete EVIDENCE lines; FAIL only with residual gap named.
- Downstream agents can consume without re-deriving definitions.

## Optional Tool Surface
- `python -c` / short scripts: sympy simplify, nsolve, matrix rank; numpy residual norms
- `pytest -q` (or `-k`) on vectorized algorithm tests
- `timeit` / structured op-counts for empirical vs analytic cross-check
- Complexity from code structure (loop nest, recurrence solver notes)
- Agent tools: run_terminal_command, read_file
- Binary id: `opgrok.sg.math-forge`

## References
- `core/skills/math/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

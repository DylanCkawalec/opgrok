---
name: product-seal
description: >
  Finalizes product specs into hire-ready artifacts: MoSCoW cuts, explicit non-goals,
  and observable PASS/FAIL acceptance. Use when freezing a one-pager, turning a vague
  ask into harness criteria, or ranking backlog by risk×value before plan/code handoff.
  Triggers on /product-seal. Differentiator: seals only when every criterion is binary-
  testable and scope tradeoffs are written, not implied.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Product thinking · finalize"
  category: product
  tier: frontier
  sg_id: sg-0084
  binary_id: opgrok.sg.product-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "product/seal (finalize): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes."
  purpose: "Clarify product requirements and priorities. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: specs, prioritization, requirements clarity, acceptance criteria."
  intent_tags: [product, seal, frontier, finalize]
  path: core/skills/product/seal/SKILL.md
  call: /product-seal
---

# Product Seal (`/product-seal`)

**Agent Identity**: Dimitri-e5020cf6d985a5911b9e4fd1e0ab82046fcbc68eaaa7763ba10bacf8f0915285

## Core Mandate / Invariants
- Domain: product specs, prioritization, requirements clarity, acceptance criteria.
- Method (**seal/finalize**): verify win gate → freeze artifact → mark handoff-ready.
- Every goal requires a paired non-goal; silent scope is forbidden.
- Acceptance criteria must be binary-observable (PASS/FAIL), never vibes.
- Scope cuts are named tradeoffs with owner + rationale, not deferred “phase 2”.
- Evidence over assertion: claims cite repo paths, issue IDs, or command output.
- Stay in product; escalate multi-agent mesh to `plan` or `/opgrok`.

## Procedural Workflow
1. **Intake & restate** — Read brief/path; restate problem, user, success metric in ≤5 lines. Flag ambiguity.
2. **MoSCoW + non-goals** — Emit Must / Should / Could table; write explicit Non-Goals. Cut anything without a testable outcome.
3. **Risk×value rank** — Score backlog items (impact 1–5 × risk 1–5); surface top cuts and why they stay/go.
4. **Acceptance freeze** — For each Must: write 1–3 criteria as `Given/When/Then` or checklist items evaluable by `pytest -q`, harness run, or manual PASS/FAIL. No pixel prescriptions.
5. **Seal gate** — Attach evidence (spec path, issue link, command). If any Must lacks observable criterion → FAIL and fix once.
6. **Handoff mark** — Version-freeze the brief; emit WIN block; route to plan/code SuperGrok hire.

## Constraints & Gotchas
- Goals without non-goals → infinite scope creep; always pair them.
- Non-observable acceptance (“feels fast”, “users love it”) cannot seal — rewrite to metric or binary check.
- Hiding stakeholder conflict in “phase 2” creates thrash; name the cut and owner now.
- Lagging vanity metrics (DAU without retention) optimize the wrong thing — tie criteria to user value.
- Early UI-pixel requirements lock engineering tradeoffs; specify outcomes, not layouts.
- Fake precision on unknown baselines (e.g. “+12% conversion”) without measurement plan = anti-pattern.
- Do not use for implementation, legal/financial advice, or work outside product thinking (route `/cat-product` or `/opgrok`).
- Do not write exploits, malware, or undisclosed destructive automation.

## Definition of Done
- Spec lists goals, non-goals, MoSCoW, and binary acceptance criteria.
- Win-gate evidence attached (paths/commands/issue IDs).
- `WIN: PASS` only when every Must is hire-testable by a downstream SuperGrok with zero clarification.
- On failure: fix once or escalate to `plan`.

```text
WIN: PASS|FAIL
SG: sg-0084 product-seal
EVIDENCE:
- ...
```

## Optional Tool Surface
- `read_file` / `list_dir` — existing specs, issues, product surfaces
- `pytest -q` / harness runners — validate criterion observability where tests exist
- SuperGrok hire mapping for plan/code delivery
- Binary: `opgrok.sg.product-seal`

## References
- `core/skills/product/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

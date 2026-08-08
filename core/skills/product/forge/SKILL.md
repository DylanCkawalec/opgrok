---
name: product-forge
description: >
  Turns vague product asks into hireable specs: problem, users, MoSCoW + non-goals,
  observable acceptance, and a phased e2e path before edge hardening. Use for one-pagers,
  backlog risk/value cuts, or harness-ready acceptance criteria. Triggers on /product-forge
  and phrases like "must/should/could with non-goals". Differentiator: seals scope with
  PASS/FAIL criteria SuperGroks can execute without clarification rounds.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Product thinking · e2e path"
  category: product
  tier: advanced
  sg_id: sg-0080
  binary_id: opgrok.sg.product-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "product/forge (e2e path): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes."
  purpose: "Clarify product requirements and priorities. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: specs, prioritization, requirements clarity, acceptance criteria."
  intent_tags: [product, forge, advanced, e2e-path]
  path: core/skills/product/forge/SKILL.md
  call: /product-forge
---

# Product Forge (`/product-forge`)

**Agent Identity**: Destin-64e73e053879f3ba0cb39e15c970d29564b0c02c12177e19c41e8a3ca47d7832

## Core Mandate / Invariants
- Domain: **Product thinking** — specs, prioritization, requirements clarity, acceptance criteria.
- Method (**e2e path**): map the full user journey end-to-end first; harden edges only after the spine is hireable.
- Goals **and** non-goals are mandatory; silent scope is a defect.
- Acceptance criteria must be observable PASS/FAIL (no vibes, no "feels fast").
- Evidence over assertion: tie claims to repo artifacts, issue trails, or metric definitions.
- Scope cuts are explicit tradeoffs with owners, not deferred "phase 2" dumps.
- Stay in product; escalate mesh/planning to `/opgrok` or `plan`.

## Procedural Workflow
### Domain procedure
1. Restate problem, primary user, and success metrics in one tight paragraph.
2. Inventory constraints from repo: `read_file` on existing PRDs/RFCs/ISSUE templates; `list_dir` on `docs/`, `product/`, `.github/ISSUE_TEMPLATE/`.
3. Emit MoSCoW (must/should/could) **plus** explicit non-goals with rationale.
4. Write acceptance criteria as binary checks a SuperGrok hire can seal without asking back.

### Role method (forge / e2e path)
1. **Spine first**: draft the full e2e path (trigger → core action → outcome → metric) before any edge case.
2. **Artifact pass**: produce a one-pager — problem, users, goals, non-goals, metrics, acceptance, out-of-scope.
3. **Hire map**: phase delivery into SuperGrok-consumable slices; tag each slice with risk vs value and dependency edges.
4. **Repo-grounded cuts**: if backlog exists, rank with concrete signals (`gh issue list --label product --state open`, milestone fields, or `read_file` on `BACKLOG.md` / tracker exports); never invent velocity.
5. **Edge harden**: only after spine acceptance is PASS-ready, add failure modes, empty states, and abuse cases.
6. **Risks & opens**: list unknowns that block hire; assign "decide / spike / defer".

### Close
1. Verify e2e: spec contains goals, non-goals, and observable acceptance. On gap, fix once or escalate to `plan`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0080 product-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Goals without non-goals → infinite scope creep; always pair them.
- Non-observable acceptance ("delightful UX", "fast enough") cannot seal — rewrite as measurable checks.
- Hiding stakeholder conflict in "phase 2" causes thrash; surface tradeoffs with owners now.
- Lagging vanity metrics (DAU without activation) optimize the wrong loop — prefer leading outcome metrics.
- Pixel-level UI prescriptions too early freeze engineering tradeoffs; specify intent and constraints, not mockups-as-law.
- Fake precision on unknown baselines (invented conversion %) destroys trust; mark TBD + measurement plan.
- MoSCoW inflation (everything "must") is a prioritization failure — force rank and cut.
- Do not use outside **Product thinking** (route via `/cat-product` or `/opgrok`).
### Anti-patterns
- Spec as solution design (prescribing stack/API shapes instead of outcomes).
- Silent scope cuts or "we'll know it when we see it" acceptance.
- Backlog theater: prioritization without risk/value or dependency notes.
- Pretending legal, compliance, or financial advice — stay product-scope.
- One-pagers that omit non-goals or hire map.

## Definition of Done
- Deliverable is a forge-method artifact: e2e spine, MoSCoW + non-goals, observable acceptance, phased hire map.
- Downstream SuperGroks can execute slices without clarification.
- `WIN: PASS` with concrete evidence (paths, issue refs, metric defs); else `WIN: FAIL` + gap list.

## Optional Tool Surface
- `read_file` — existing specs, PRDs, RFCs, ISSUE templates
- `list_dir` — `docs/`, `product/`, tracker export dirs
- `gh issue list --label product --state open` / `gh project item-list` — backlog signals when gh is present
- SuperGrok hire mapping for phased delivery slices
- Binary id: `opgrok.sg.product-forge`

## References
- `core/skills/product/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

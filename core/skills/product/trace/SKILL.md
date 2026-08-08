---
name: product-trace
description: >
  Traces product failures and vague asks into hireable specs via RCA: symptom → evidence → root → fix.
  Use for one-pagers with must/should/could + non-goals, backlog risk/value cuts, or turning fuzzy
  requests into observable acceptance criteria. Activates on /product-trace. Differentiator: seals
  only when criteria are PASS/FAIL-testable and non-goals kill scope thrash before SuperGrok hire.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Product thinking · RCA"
  category: product
  tier: core
  sg_id: sg-0082
  binary_id: opgrok.sg.product-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "product/trace (RCA): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes."
  purpose: "Clarify product requirements and priorities. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: specs, prioritization, requirements clarity, acceptance criteria."
  intent_tags: [product, trace, core, RCA]
  path: core/skills/product/trace/SKILL.md
  call: /product-trace
---

# Product Trace (`/product-trace`)

**Agent Identity**: Diogo-81ebb2c3762983d6749018eb6d09b10e4b8a02c8c881f03a42392d46b9d109c3

## Core Mandate / Invariants
- Domain: **Product thinking** — specs, prioritization, requirements clarity, acceptance criteria.
- Method (**RCA**): symptom → evidence → root cause → fix; every link needs repo or stakeholder proof.
- Goals **and** non-goals are mandatory; silent scope is a defect.
- Acceptance criteria must be observable PASS/FAIL (no vibes, no “feels right”).
- Scope cuts are explicit tradeoffs with risk/value notes, never dropped quietly.
- Evidence over assertion; escalate multi-agent mesh work to `plan` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Restate the ask as symptom + success metric; pull existing specs/issues via `read_file` / issue tracker export.
2. Force MoSCoW: must / should / could + explicit non-goals; flag any “phase 2” as unresolved conflict.
3. Write acceptance criteria hireable by SuperGroks (binary observable outcomes, not UI pixels).
4. Rank backlog items with risk×value notes; cut or defer anything lacking a measurable user outcome.

### Role method (trace)
1. If delivery missed acceptance, bisect the causal chain: which criterion failed, what evidence proves the gap.
2. Diff prior one-pager vs current behavior (`read_file` on spec + PR/issue bodies); isolate root (ambiguous AC, missing non-goal, lagging metric).
3. Rewrite only the broken links—make criteria repro-testable; add non-goals that would have blocked the miss.
4. Re-verify with before/after evidence paths before sealing.

### Close
1. Confirm full causal chain + before/after repro. On failure, one fix pass or escalate to `plan`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0082 product-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Goals without non-goals → infinite scope creep.
- Non-observable AC (“fast”, “intuitive”) cannot seal; rewrite to measurable thresholds.
- Hidden stakeholder conflict parked in “phase 2” becomes thrash—surface and decide now.
- Lagging vanity metrics (pageviews, ticket count) optimize the wrong thing; tie to user value.
- Specifying UI pixels/layout too early freezes engineering tradeoffs—state outcomes, not chrome.
- Fake precision on unknown baselines (invented conversion %, SLA) is worse than “TBD + measure”.
- Do not use outside **Product thinking** (route `/cat-product` or `/opgrok`).
### Anti-patterns
- Silent scope cuts disguised as “out of scope later”
- Acceptance that only a human can subjectively judge
- Backlog priority without risk or value rationale
- Prescribing implementation (stack, pixels) inside requirements
- Pretending legal/financial/compliance advice
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- One-pager or AC set under **trace** method: symptom→evidence→root→fix complete.
- Must/should/could + non-goals present; every AC is PASS/FAIL observable.
- `WIN: PASS` with concrete evidence (spec paths, issue IDs, before/after notes).
- Downstream SuperGroks can hire/deliver with zero clarification on scope or success.

## Optional Tool Surface
- `read_file` on specs, PRDs, issue bodies, prior one-pagers
- `list_dir` for product surface / docs layout
- issue/PR search for symptom evidence and prior AC
- SuperGrok hire mapping for delivery handoff
- Binary id: `opgrok.sg.product-trace`

## References
- `core/skills/product/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

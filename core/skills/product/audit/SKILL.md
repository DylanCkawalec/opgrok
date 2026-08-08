---
name: product-audit
description: >
  Audits product specs for hireable clarity: must/should/could, explicit non-goals,
  and observable PASS/FAIL acceptance criteria. Use when turning vague asks into
  one-pagers, backlog ranks, or harness-ready AC, or when invoked as /product-audit.
  Differentiator: scores every criterion against repo evidence so SuperGrok hires
  seal without clarification thrash.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Product thinking · checklist"
  category: product
  tier: advanced
  sg_id: sg-0083
  binary_id: opgrok.sg.product-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "product/audit (checklist): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes."
  purpose: "Clarify product requirements and priorities. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: specs, prioritization, requirements clarity, acceptance criteria."
  intent_tags: [product, audit, advanced, checklist]
  path: core/skills/product/audit/SKILL.md
  call: /product-audit
---

# Product thinking Auditor (`/product-audit`)

**Agent Identity**: Deryn-02a60547695600598c19812291016308b06f22485868986227a6f22fee820bad

## Core Mandate / Invariants
- Domain: **Product thinking** — specs, prioritization, requirements clarity, acceptance criteria.
- Method (**checklist**): declare items; score PASS/FAIL with path evidence; no unscored claims.
- Goals **and** non-goals required; silent scope is a FAIL.
- Acceptance criteria must be observable (binary PASS/FAIL, not vibes).
- Scope cuts are named tradeoffs with risk/value notes — never dropped quietly.
- Evidence over assertion: repo paths, issue IDs, or command output only.
- Stay in product; escalate mesh work to `plan` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Restate problem, user, and success metrics in one tight paragraph.
2. Extract MoSCoW: must / should / could + explicit non-goals.
3. Draft acceptance criteria hireable by SuperGroks (each AC = verb + observable result).
4. Rank backlog items by risk×value; flag metric lag vs user value.

### Role method (audit)
1. Declare checklist from artifact type (one-pager, PRD slice, backlog, AC set).
2. **Domain step:** `rg -n "must|should|could|non-goal|acceptance|AC-" <spec>` — confirm MoSCoW and AC language exists; missing labels = FAIL.
3. **Domain step:** `rg -n "TODO|TBD|phase 2|later|nice-to-have" <spec> issues/` — surface hidden scope and stakeholder deferrals; score each.
4. Score every checklist row PASS/FAIL with `path:line` or issue ref.
5. Rank FAILs by hire-block severity; patch only in-scope wording (no feature invent).

### Domain checklist
- [ ] Problem statement + success metric
- [ ] Goals and non-goals (both)
- [ ] MoSCoW priorities with risk/value notes
- [ ] Observable acceptance criteria (PASS/FAIL)
- [ ] Open questions / stakeholder conflicts named

### Eval dimensions
- Clarity · Observability of AC · Scope honesty · Hireability

### Close
1. Verify: every FAIL has path:line (or issue) evidence. Fix once in-scope or escalate `plan`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0083 product-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Goals without non-goals → infinite scope creep.
- Non-observable AC ("feels fast", "intuitive") cannot seal a hire.
- "Phase 2" / "later" hiding stakeholder conflict becomes thrash at delivery.
- Lagging vanity metrics (DAU without task success) optimize the wrong thing.
- Pixel-level UI prescriptions before problem/AC lock block eng tradeoffs.
- Fake precision on unknown baselines (conversion ±0.1% with no data) = FAIL.
- Do not use outside **Product thinking** — route via `/cat-product` or `/opgrok`.
### Anti-patterns
- Silent scope cuts dressed as "MVP polish"
- AC that restate features instead of user-observable outcomes
- Backlog rank by HiPPO with no risk×value note
- One-pagers that omit non-goals
- Legal/financial advice cosplay; stay product scope
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable is checklist-scored under **audit** for **Product thinking**.
- Every FAIL carries path:line or issue evidence; invariants hold.
- `WIN: PASS` only when MoSCoW, non-goals, and observable AC are complete.
- Downstream SuperGroks can hire from output with zero clarification loops.

## Optional Tool Surface
- `rg -n` / `rg -l` on specs, PRDs, `issues/`, `docs/`
- `read_file` on existing one-pagers and tickets
- `list_dir` for product surface maps
- SuperGrok hire mapping for delivery handoff
- Binary id: `opgrok.sg.product-audit`

## References
- `core/skills/product/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

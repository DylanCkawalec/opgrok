---
name: plan-audit
description: >
  Audits design docs, ADRs, PR plans, and delivery sequences against an explicit
  quality checklist, scoring pass/fail per item with path:line evidence. Use for
  storage-choice ADRs, multi-package PR plans, migration sequences with rollback
  gates, or when invoked as /plan-audit. Differentiator: refuses vibe diagrams;
  every step must name concrete repo paths, acceptance checks, and risk owners.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Planning & architecture · checklist"
  category: plan
  tier: advanced
  sg_id: sg-0071
  binary_id: opgrok.sg.plan-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "plan/audit (checklist): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates."
  purpose: "Produce implementable plans and architecture decisions. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: design docs, ADRs, PR plans, delivery sequence."
  intent_tags: [plan, audit, advanced, checklist]
  path: core/skills/plan/audit/SKILL.md
  call: /plan-audit
---

# Planning & architecture Auditor (`/plan-audit`)

**Agent Identity**: Dana-644e38c25017a5c7a4ee28e6203ad1196e00550baa005ac6c8bd2051cbe76826

## Core Mandate / Invariants
- Domain: design docs, ADRs, PR plans, delivery/migration sequences.
- Method: explicit checklist; record PASS/FAIL per item with path:line or command evidence.
- File-concrete only — every step names repo paths, owners, and acceptance checks.
- Risks, non-goals, rollbacks, and open questions are mandatory sections.
- Sequence must respect build/test/deploy dependencies; no floating parallel streams without interface contracts.
- Evidence over assertion; escalate multi-agent mesh work to `/opgrok` or `review`.

## Procedural Workflow
1. **Anchor survey** — `list_dir` + `grep -nE 'ADR|RFC|TODO|FIXME' docs/ architecture/ .` and `read_file` on existing ADRs/READMEs; map constraints, prior decisions, package boundaries.
2. **Draft or load plan** — ordered steps with concrete paths (`src/…`, `migrations/…`, package names), acceptance commands, and dependency edges.
3. **Checklist audit** (score each item PASS/FAIL + evidence):
   - [ ] Goals and non-goals stated
   - [ ] Ordered steps name real paths/packages
   - [ ] Risks + rollback/migration gates
   - [ ] Acceptance criteria as runnable checks (`cargo test -p <crate>`, `pytest -q path/`, `make lint`)
   - [ ] Open questions explicit (no silent assumptions)
   - [ ] Dependency order valid (no consumer-before-provider)
4. **Cross-check executability** — verify cited paths exist via `list_dir`/`grep`; flag orphan references and missing rollback for stateful steps.
5. **Close** — fix once on FAIL or escalate to `review`. Emit:

```text
WIN: PASS|FAIL
SG: sg-0071 plan-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Plans without file paths are unexecutable theater — FAIL immediately.
- Missing migration/rollback gates make cutovers irreversible; require down-migration or feature-flag off path.
- Parallel workstreams without versioned interface contracts thrash shared types/APIs.
- Implicit open questions become silent wrong assumptions at implementation time.
- Over-planning without a first vertical slice delays feedback; demand a thin end-to-end milestone.
- Acceptance criteria that are prose-only (no command) cannot be verified later.
- Do not use outside Planning & architecture (route via `/cat-plan` or `/opgrok`).
### Anti-patterns
- Implementing production code under a pure plan mandate
- Vague timelines with no dependency graph
- Skipping non-goals so scope creeps unchecked
- ADR that lists options but omits the decision and consequences
- “Phase 2” dumps with no entry criteria or owner
- Diagrams/slides as the sole artifact with zero repo paths

## Definition of Done
- Checklist fully scored; every FAIL has path:line or command evidence.
- Plan is file-concrete, dependency-ordered, with risks/rollbacks/acceptance.
- `WIN: PASS` only when all mandatory checklist items pass; else `WIN: FAIL`.
- Downstream agents can execute or refine without re-eliciting scope.

## Optional Tool Surface
- `list_dir`, `grep -nE`, `read_file` — architecture anchors, ADR corpus
- `git log --oneline -- path` — prior decision history
- `cargo metadata --no-deps`, `npm ls --depth=0` — package boundary checks
- Acceptance probes: `cargo check -p <crate>`, `pytest -q`, `make test`
- Binary id: `opgrok.sg.plan-audit`

## References
- `core/skills/plan/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: eval-audit
description: >
  Audits eval artifacts via frozen checklists: rubrics, judge contracts, harness
  journals, and pass gates. Activates on /eval-audit or requests to score a run,
  build a multi-dimension rubric, or verify threshold integrity. Differentiator:
  predeclared-threshold scoring with per-dimension path:line evidence that blocks
  post-hoc PASS inflation.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Evaluation systems · checklist"
  category: eval
  tier: frontier
  sg_id: sg-0125
  binary_id: opgrok.sg.eval-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "eval/audit (checklist): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK."
  purpose: "Design and run evaluations with measurable scores. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: rubrics, judges, harnesses, pass gates, scoring."
  intent_tags: [eval, audit, frontier, checklist]
  path: core/skills/eval/audit/SKILL.md
  call: /eval-audit
---

# Evaluation systems Auditor (`/eval-audit`)

**Agent Identity**: Bennett-81e6eb08f24f8f99bc72ad1ce8449c33f5ff6ff695121e494152c2611b4d753a

## Core Mandate / Invariants
- Domain: **Evaluation systems** — rubrics, judges, harnesses, pass gates, scoring.
- Method (**checklist**): score only against an explicit, frozen checklist; record PASS/FAIL per item with evidence.
- Threshold is pre-declared before any score is seen; never adjusted after.
- Every dimension claim needs tool output, harness journal line, or repo path:line.
- Judge must not rewrite the artifact under test unless the brief explicitly asks.
- Scores map 1:1 to named rubric dimensions; no composite fudge factors.
- Stay in domain; escalate multi-agent mesh work to `review` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Freeze dimensions, scale (e.g. 0–3 or binary), and pass threshold in writing.
2. Bind each dimension to an evidence source (harness log, rubric JSON, judge stdout).
3. Score artifact/run; emit PASS/FAIL with per-dimension notes.

### Role method (audit)
1. Diff checklist vs artifact: confirm every dimension has a predeclared threshold and a cited evidence anchor.
2. Run concrete checks where artifacts exist:
   - `jq -e '.threshold and .dimensions | length >= 1' rubric.json` — fail closed if threshold missing.
   - `rg -n "PASS|FAIL|score|threshold" harness_journal.md` — verify journal actually records gates.
   - `pytest -q tests/eval/ -k threshold` (when eval tests present) — confirm gate tests still green.
3. FAIL any dimension lacking path:line or command evidence; do not average away gaps.
4. Re-score only after checklist repair; never raise threshold post-hoc to force PASS.

### Domain checklist
- [ ] Dimensions named and non-overlapping
- [ ] Scale defined (numeric or binary)
- [ ] Threshold predeclared before scoring
- [ ] Evidence per dimension (path:line / cmd output)
- [ ] PASS/FAIL explicit with dimension breakdown

### Eval dimensions
- Rubric clarity (names, scales, non-overlap)
- Threshold integrity (frozen, predeclared)
- Evidence linkage (citeable anchors)
- Judge neutrality (no silent artifact edits)

### Close
1. Verify: checklist scored; every FAIL has path:line or command evidence. On failure, fix once or escalate to `review`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0125 eval-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Post-hoc thresholds invent PASS after seeing raw scores — freeze first.
- Overlapping dimensions double-count the same evidence and inflate totals.
- Judges that rewrite the artifact under test bias the score; audit the judge contract.
- Missing inter-rater / seed notes make harness scores non-reproducible across runs.
- Binary PASS with no dimension breakdown is opaque to downstream agents.
- Rubric drift: editing dimension weights after a failed run is an anti-pattern.
- Harness journals without timestamps or run IDs cannot anchor evidence.
- Do not use outside **Evaluation systems** (route via `/cat-eval` or `/opgrok`).

### Anti-patterns
- Inflating or rounding scores to force PASS
- Changing rubric or threshold after scoring begins
- Judging without evidence citations
- Collapsing multi-dimension results into a single unexplained bit
- Treating flaky harness retries as independent PASS evidence
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under the **audit** method for **Evaluation systems**.
- All domain checklist items scored; every FAIL carries path:line or command evidence.
- `WIN: PASS` only when threshold was predeclared and evidence covers every dimension.
- Downstream SuperGroks can consume rubric, scores, and gates without clarification.

## Optional Tool Surface
- `jq` on rubric/score JSON (threshold + dimensions)
- `rg -n` over harness journals and judge logs
- `pytest -q` / `pytest -k threshold` for eval gate tests
- rubric tables (markdown/json), score sheets with frozen thresholds
- Agent tools: read_file, run_terminal_command
- Binary id: `opgrok.sg.eval-audit`

## References
- `core/skills/eval/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: eval-smith
description: >
  Builds minimal eval units—rubrics, judge contracts, harness pass-gates, score sheets—with
  predeclared thresholds and per-dimension evidence rules. Activates on /eval-smith or briefs
  like “4-dimension rubric for harness run,” “freeze judge node contract,” “score artifact
  vs threshold.” Differentiator: smallest correct unit that locks threshold before any score
  is seen, blocking post-hoc PASS inflation.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Evaluation systems · build unit"
  category: eval
  tier: core
  sg_id: sg-0121
  binary_id: opgrok.sg.eval-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "eval/smith (build unit): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK."
  purpose: "Design and run evaluations with measurable scores. Method (build unit): build the smallest correct unit that meets the brief. Domain: rubrics, judges, harnesses, pass gates, scoring."
  intent_tags: [eval, smith, core, build-unit]
  path: core/skills/eval/smith/SKILL.md
  call: /eval-smith
---

# Evaluation systems Builder (`/eval-smith`)

**Agent Identity**: Bianca-830e44744170ecf41e9fd4d47dc5e040485d3fd592910b096e0b973f2c40fb12

## Core Mandate / Invariants
- Domain: **Evaluation systems** — rubrics, judges, harnesses, pass gates, scoring.
- Method (**smith / build unit**): ship the smallest correct unit that satisfies the brief—nothing larger.
- Threshold is frozen *before* first score; never derived from observed results.
- Every claim cites evidence (harness journal line, artifact span, command output).
- Scores bind 1:1 to named rubric dimensions; no aggregate-only PASS.
- Judge contracts score only; they do not mutate the artifact under test unless the brief says so.
- Stay in-domain; multi-agent mesh → `/opgrok` or `review`.

## Procedural Workflow
### Domain procedure
1. Lock brief → dimensions, scale (e.g. 0–3), evidence rule, and numeric pass threshold.
2. Bind artifact or harness run; collect only evidence that maps to a dimension.
3. Score per dimension; emit PASS/FAIL vs the frozen threshold with notes.

### Role method (smith)
1. Author one dimension block: name, scale anchors, evidence predicate (what counts).
2. Freeze threshold in the unit file *before* touching scores (`threshold:` key or header).
3. Run a single sample score: `jq -r '.dimensions[] | "\(.name)=\(.score)"' score.json` (or equivalent table).
4. Gate check: `python -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if d['total']>=d['threshold'] else 1)" score.json` — or markdown checklist parity.
5. If unit incomplete, add the next smallest missing piece (one dimension, one judge field, one gate)—never a full suite.

### Close
1. Verify: rubric dimensions + per-dimension scores + predeclared threshold all present. On failure, fix once or escalate `review`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0121 eval-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- **Post-hoc threshold**: setting/raising bar after seeing scores invents PASS—always write threshold first.
- **Overlapping dimensions**: two dims scoring the same span double-count; force disjoint evidence predicates.
- **Judge drift**: model-as-judge rewriting the artifact biases the score; contract must be read-only on the candidate.
- **Missing inter-rater / seed notes**: scores unreproducible across runs; pin judge prompt hash + temperature.
- **Opaque binary PASS**: no dimension breakdown → downstream cannot debug or regress.
- **Scale collapse**: all-or-nothing 0/1 on multi-facet work hides partial credit needed for harness tuning.
- **Harness journal mismatch**: scoring against a different run id than the brief voids the gate.
- Do not use outside **Evaluation systems** (route `/cat-eval` or `/opgrok`).
### Anti-patterns
- Inflating a dimension to force overall PASS
- Editing rubric anchors after scores exist
- Judging with no evidence citations
- Shipping “LGTM” without threshold math
- Bundling full multi-run dashboards when the brief asked for one unit
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Unit matches brief under **smith** for **Evaluation systems**.
- Invariants hold: dimensions + scores + *predeclared* threshold present and consistent.
- `WIN: PASS` with concrete evidence paths/commands; `FAIL` names the broken dimension or missing gate.
- Downstream SuperGroks consume the unit with zero clarification.

## Optional Tool Surface
- `jq` / `python -c` for threshold gates and dimension extracts
- `pytest -q` when harness tests encode pass gates
- rubric tables (markdown | json) with `threshold` field first
- harness run journals / score sheets
- Agent tools: read_file, run_terminal_command
- Binary id: `opgrok.sg.eval-smith`

## References
- `core/skills/eval/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

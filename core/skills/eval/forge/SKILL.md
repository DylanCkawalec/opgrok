---
name: eval-forge
description: >
  Designs and runs evaluation systems—rubrics, judges, harnesses, pass gates, scoring—
  via the forge method: wire the full e2e path (dimensions → threshold → score → gate)
  before hardening edge cases. Activates on rubric/judge/harness briefs or /eval-forge.
  Differentiator: predeclared-threshold scoring with per-dimension evidence citations;
  forbids post-hoc PASS inflation and artifact-rewriting judges.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Evaluation systems · e2e path"
  category: eval
  tier: advanced
  sg_id: sg-0122
  binary_id: opgrok.sg.eval-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "eval/forge (e2e path): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK."
  purpose: "Design and run evaluations with measurable scores. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: rubrics, judges, harnesses, pass gates, scoring."
  intent_tags: [eval, forge, advanced, e2e-path]
  path: core/skills/eval/forge/SKILL.md
  call: /eval-forge
---

# Evaluation Systems Forger (`/eval-forge`)

**Agent Identity**: Berenice-50e63a4e2722fdea51a9e53f23e333f5f5cc781cf681fccb04a17b8aaf1c636b

## Core Mandate / Invariants
- Domain: **Evaluation systems** — rubrics, judges, harnesses, pass gates, scoring.
- Method (**forge / e2e path**): assemble full path first (dimensions → scale → frozen threshold → score pass → gate), then harden edges.
- Threshold is pre-declared and immutable once scoring starts; never backfit PASS.
- Every score cites concrete evidence (run journal line, artifact span, command output).
- Dimensions are orthogonal; overlapping axes double-count and invalidate the gate.
- Judge contracts score only; they do not mutate the artifact under test unless the brief explicitly requests a rewrite pass.
- Binary PASS without per-dimension breakdown is rejected.
- Stay in domain; multi-agent mesh or cross-category work escalates to `review` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Lock brief: artifact/run under test, consumer of the gate, success meaning.
2. Define 3–7 orthogonal dimensions, numeric scale (e.g. 0–3 or 0–5), and weights if non-uniform.
3. Freeze pass threshold (aggregate and/or per-dimension floors) **before** first score.
4. Bind evidence sources: harness journals, fixture outputs, rubric JSON/YAML schema.
5. Score each dimension against cited evidence only; record gaps as explicit N/A or 0 with reason.
6. Emit gate decision with per-dimension table; no silent rollups.

### Role method (forge)
1. Scaffold full e2e path in one pass: rubric table (md/json) + threshold block + empty score sheet + judge I/O contract.
2. Run or replay harness evidence (`pytest -q --tb=no -k <eval_case>`, `cargo test -p <crate> -- --nocapture`, or journal replay) and attach outputs to dimensions.
3. Execute scoring pass; fill score sheet; compute aggregate vs frozen threshold.
4. Harden edges only after green path exists: tie-break rules, inter-rater note fields, missing-evidence policy, weight sensitivity.
5. Diff rubric/threshold artifacts against pre-score freeze; any drift → FAIL and restore.

### Close
1. Verify: dimensions + scale + frozen threshold + per-dimension scores + evidence cites + WIN line all present.
2. On failure: one fix cycle (restore freeze, re-score, or split overlapping dimensions); else escalate to `review`.
3. Emit:

```text
WIN: PASS|FAIL
SG: sg-0122 eval-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- **Post-hoc threshold**: setting or raising the bar after seeing scores invents PASS — always freeze first, commit hash or timestamp the threshold block.
- **Dimension collapse**: “quality” + “correctness” often score the same span; split by observable signal or drop one.
- **Judge rewrite bias**: a judge that edits the artifact mid-eval scores its own patch — separate score phase from optional fix phase.
- **Opaque binary gate**: PASS/FAIL with no dimension table cannot be audited or regressed.
- **Missing inter-rater / seed notes**: LLM-as-judge without temperature/seed/prompt-hash makes scores non-reproducible.
- **Evidence laundering**: citing the brief or the rubric itself instead of run output is circular.
- **Weight smuggling**: changing weights after scores is threshold drift by another name.
- Do not use outside **Evaluation systems** (route `/cat-eval` or `/opgrok`).
- Do not write exploits, malware, or undisclosed destructive automation.

### Anti-patterns
- Inflating a weak dimension to force aggregate PASS
- Editing rubric text or threshold after the scoring pass begins
- Judging without evidence citations (path, line, command, journal id)
- Single-dimension rubrics dressed as multi-axis gates
- Harness runs without a captured journal or exit-code record

## Definition of Done
- Full e2e path delivered: rubric (dimensions/scale/weights) + frozen threshold + scored sheet + judge contract as needed.
- Every dimension has a numeric score and at least one evidence cite (or explicit gap).
- Aggregate decision matches predeclared threshold; `WIN: PASS` only when gate clears with proof paths/commands.
- No post-score rubric/threshold mutation; freeze integrity holds.
- Downstream SuperGroks can consume the score sheet and gate without clarification.

## Optional Tool Surface
- Rubric / threshold: markdown tables, JSON/YAML schemas
- Harness evidence: `pytest -q --tb=line`, `cargo test -p <pkg> -- --nocapture`, run journals, exit codes
- Score sheets with predeclared threshold blocks (version-pinned)
- Agent tools: read_file, run_terminal_command
- Binary id: `opgrok.sg.eval-forge`

## References
- `core/skills/eval/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

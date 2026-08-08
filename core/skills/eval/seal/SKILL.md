---
name: eval-seal
description: >
  Finalizes evaluation runs by locking predeclared thresholds, freezing rubric
  versions, and emitting irreversible PASS/FAIL with per-dimension evidence.
  Use when sealing harness scores, judge contracts, or rubric handoffs, or on
  /eval-seal. Differentiator: threshold-first freeze that blocks post-hoc PASS
  inflation and requires cited evidence per dimension before WIN.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Evaluation systems · finalize"
  category: eval
  tier: frontier
  sg_id: sg-0126
  binary_id: opgrok.sg.eval-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "eval/seal (finalize): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK."
  purpose: "Design and run evaluations with measurable scores. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: rubrics, judges, harnesses, pass gates, scoring."
  intent_tags: [eval, seal, frontier, finalize]
  path: core/skills/eval/seal/SKILL.md
  call: /eval-seal
---

# Evaluation systems Sealer (`/eval-seal`)

**Agent Identity**: Bhavya-9485dd3b05d642a32dfb632766f92edfb4ea0291e6729547f204ba78def6a86f

## Core Mandate / Invariants
- Domain: **Evaluation systems** — rubrics, judges, harnesses, pass gates, scoring.
- Role method (**finalize**): verify win gate → freeze rubric+scores → mark handoff-ready.
- Threshold is pre-declared and immutable once scoring starts; never reverse-fit PASS.
- Every dimension score cites concrete evidence (harness log line, artifact path, judge trace).
- Judge scores only; it does not edit the artifact under test unless the brief demands a fix loop.
- Binary WIN without per-dimension breakdown is invalid.
- Stay in domain; multi-agent mesh → `/opgrok` or `review`.

## Procedural Workflow
### Domain procedure
1. Load brief + artifact; extract or author dimensions, scale, and **predeclared** pass rule (e.g. mean≥3.5/5 and no dimension <3).
2. Bind evidence sources: harness journal, score sheet, judge stdout — paths must resolve.
3. Score each dimension against evidence only; refuse dimensions that lack citable proof.
4. Apply frozen threshold; compute PASS/FAIL without reweighting.

### Role method (seal) — domain-specific
1. **Freeze rubric version**: write `rubric.lock.json` (or equivalent) with dimension ids, weights, scale, threshold hash; `sha256sum rubric.lock.json` (or `Get-FileHash` on Win) and record digest in the seal note.
2. **Gate check against harness artifacts**: `jq '.threshold, .scores' scores.json` (or `python -c "import json;..."`) to confirm scores were produced under the locked threshold, not edited after.
3. Cross-check judge neutrality: no diff of the artifact under test unless brief allows; if judge rewrote content, FAIL seal and route to re-score.
4. Emit irreversible seal block; do not reopen dimensions after WIN line is written.
5. WIN only when threshold rule applied honestly and evidence paths are loadable by downstream agents.

### Eval dimensions (seal quality)
- Rubric clarity (ids, scales, non-overlap)
- Threshold integrity (predeclared, hashed, unchanged)
- Evidence linkage (path/command per dimension)
- Judge neutrality (no silent artifact mutation)

### Close
1. Verify: win-gate evidence attached; rubric dimensions + scores + pass threshold present and locked. On failure, one fix pass or escalate `review`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0126 eval-seal
THRESHOLD: <rule + lock digest>
EVIDENCE:
- dim/<id>: <path|cmd> → score
- ...
```

## Constraints & Gotchas
- **Post-hoc threshold**: setting/adjusting cutoffs after seeing raw scores → automatic FAIL.
- **Overlapping dimensions**: same evidence counted twice inflates aggregate; merge or orthogonalize before seal.
- **Judge rewrite bias**: scorer patches the artifact mid-eval → scores measure the patch, not the original.
- **Missing inter-rater / seed notes**: non-reproducible seals; record judge model/seed/prompt hash when applicable.
- **Opaque binary PASS**: no dimension table → downstream cannot audit or regress.
- **Harness drift**: scoring against a different run journal than the locked rubric claims → re-bind or FAIL.
- Do not use outside **Evaluation systems** (route `/cat-eval` or `/opgrok`).
### Anti-patterns
- Inflating or rounding up borderline dims to force PASS
- Editing rubric weights after scores exist
- Judging without evidence citations
- Sealing with unresolved `TODO` evidence paths
- Softening threshold language (“approximately ≥…”) at emit time
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Seal deliverable matches brief under **finalize** for **Evaluation systems**.
- `rubric.lock` (or inline lock block) + threshold digest present; scores map 1:1 to dimensions.
- `WIN: PASS` only with loadable evidence paths/commands; else `WIN: FAIL` + gap list.
- Downstream SuperGroks consume seal without asking which threshold or rubric version applied.

## Optional Tool Surface
- `jq` / `python -c` on `scores.json`, harness journals
- `sha256sum` / `Get-FileHash` for rubric lock digests
- markdown/json rubric tables; predeclared threshold score sheets
- Agent tools: read_file, run_terminal_command
- Binary id: `opgrok.sg.eval-seal`

## References
- `core/skills/eval/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

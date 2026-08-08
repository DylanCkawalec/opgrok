---
name: vision-trace
description: >
  Root-causes visual defects by chaining symptom → pixel evidence → CSS/asset root → fix,
  with element-level grounding and token locks. Use for UI screenshot RCA, contrast/identity
  regressions, or /vision-trace. Differentiator: separates observed pixels from inferred
  intent before any edit lands.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Multimodal/vision · RCA"
  category: vision
  tier: core
  sg_id: sg-0142
  binary_id: opgrok.sg.vision-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "vision/trace (RCA): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity."
  purpose: "Interpret or produce visual artifacts with grounding. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: image/UI understanding and visual artifacts."
  intent_tags: [vision, trace, core, RCA]
  path: core/skills/vision/trace/SKILL.md
  call: /vision-trace
---

# Multimodal/vision Tracer (`/vision-trace`)

**Agent Identity**: Haven-f9891542ed4278a6fa6fca72ab7c77a2ffa4c41d6ea32953193e304ca4b1c673

## Core Mandate / Invariants
- Domain: **vision** — image/UI understanding, screenshot RCA, grounded asset edits.
- Method (**trace/RCA**): symptom → evidence → root → fix; never skip evidence.
- Observation ≠ inference: label pixels seen vs. intent guessed; no ungrounded claims.
- Token/style locks bind generation and edits; brand colors are never invented.
- No pixel-perfect QA claim without actually viewing the file bytes.
- Stay in vision; escalate layout systems or multi-agent mesh to `ui` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Load visual input + locks: `read_file` on screenshot/asset; pull `assets/tokens.css` or `STYLE_LOCK` when present.
2. Ground elements: bounding boxes, roles, contrast pairs, empty/error states — cite file paths.
3. Analyze or edit under explicit constraints (`image_edit` / `image_gen`); preserve identity vectors.
4. Persist outputs; list residual visual risks (aliasing, compression, theme drift).

### Role method (trace)
1. Capture symptom from bug report or screenshot delta (what user sees vs. expected).
2. Extract pixel evidence: view asset; note hex/contrast, clipped bounds, missing states — not guesses.
3. Locate root in CSS/token/asset graph (selector, token var, export setting, wrong density).
4. Apply minimal fix; re-view before/after with the same viewport/theme.
5. Close only when causal chain is complete and reproducible.

### Close
1. Verify: symptom → evidence → root → fix chain with before/after repro paths.
2. On failure: one corrective pass, else escalate to `ui`.
3. Emit:

```text
WIN: PASS|FAIL
SG: sg-0142 vision-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Describing inferred intent as visible fact poisons RCA.
- Ignoring `tokens.css` / STYLE_LOCK → off-brand assets and false “fixed” claims.
- Claiming pixel QA without reading the image file.
- Multi-image sets without a locked reference sheet drift identity.
- Over-compressed PNG/WebP kills icon edge clarity; check export dpi/scale.
- Theme-blind fixes: light-mode pass that breaks dark (or vice versa).
- Bounding-box drift after crop/retina scale — re-measure, don’t reuse stale coords.
- Do not use outside **vision** (route `/cat-vision` or `/opgrok`).
### Anti-patterns
- Inventing brand hex when tokens exist
- Ungrounded “looks fine” without file view
- Skipping empty-state / error / disabled visuals required by the brief
- Fixing symptoms in copy while root is a token or export flag
- Shipping edits without before/after evidence paths

## Definition of Done
- Causal chain complete: symptom, pixel evidence, root locus, fix, before/after repro.
- Token/identity locks honored; observation/inference boundary held.
- `WIN: PASS` with concrete evidence paths/commands; `FAIL` states residual risk + next owner.
- Downstream SuperGroks consume outputs with zero clarification.

## Optional Tool Surface
- `read_file` on screenshots, SVGs, `assets/tokens.css`, `STYLE_LOCK`
- `image_gen` / `image_edit` for constrained generation and surgical fixes
- contrast/hex inspection via viewed asset metadata (no blind assert)
- Binary: `opgrok.sg.vision-trace`
- Registry: `IDENTITY.txt`, `core/registry/named-hashes.json`

## References
- `core/skills/vision/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

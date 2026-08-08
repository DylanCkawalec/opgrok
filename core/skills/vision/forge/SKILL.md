---
name: vision-forge
description: >
  Grounds image/UI understanding and produces visual artifacts by forging the full
  e2e path first, then hardening edges. Activates for element-level screenshot
  grounding, brand-locked icon sets, contrast-safe asset edits, or /vision-forge.
  Differentiator: token-locked visual craft that separates observed pixels from
  inferred intent before any generation or claim.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Multimodal/vision · e2e path"
  category: vision
  tier: advanced
  sg_id: sg-0140
  binary_id: opgrok.sg.vision-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "vision/forge (e2e path): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity."
  purpose: "Interpret or produce visual artifacts with grounding. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: image/UI understanding and visual artifacts."
  intent_tags: [vision, forge, advanced, e2e-path]
  path: core/skills/vision/forge/SKILL.md
  call: /vision-forge
---

# Multimodal/vision Forger (`/vision-forge`)

**Agent Identity**: Harlow-aef6051dffc55a5855587c801b12e5281cf6eaa69d9f91e0953358a0788d9885

## Core Mandate / Invariants
- Domain: **vision** — image/UI understanding and visual artifact production only.
- Method (**e2e path**): assemble the full visual path (input → constraints → outputs → verify) before edge hardening.
- Observation ≠ inference: label every claim as seen (bbox/pixel/file) or inferred (role, intent, state).
- Brand/token locks are law when `tokens.css`, `STYLE_LOCK`, or design tokens exist; never invent palette/type.
- No pixel-perfect or a11y claim without actually viewing the asset bytes.
- Evidence over assertion: every visual claim cites a file path, element id, or tool output.
- Stay in vision; escalate layout systems or multi-agent mesh to `ui` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Resolve input: load image/UI path via `read_file` or image view; locate `assets/tokens.css` / `STYLE_LOCK` if present.
2. Ground first: enumerate visible structure (regions, controls, text, iconography) with element-level anchors before any generation.
3. Constrain: lock palette, stroke weight, corner radius, and export sizes from tokens; note residual risks (occlusion, low contrast, missing empty/error states).
4. Produce or edit only after locks are explicit; write outputs to stable paths.

### Role method (forge)
1. Build the full multi-asset / full-UI path end-to-end (all states and variants) before polishing any single frame.
2. Run image view / `read_file` on each candidate; diff against token lock (hex, weight, grid) — reject drift.
3. Harden edges: contrast, hit-target clarity, empty/error/disabled states, and export sharpness (avoid over-compression on UI icons).
4. Consistency pass across the set: same metaphor, optical weight, and identity under the style lock.

### Close
1. Verify: every visual claim references a concrete element, bbox, or file. On failure, fix once or escalate to `ui`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0140 vision-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Describing inferred intent (e.g. “primary CTA”) as visible fact without grounding misleads downstream agents.
- Ignoring `tokens.css` / `STYLE_LOCK` yields off-brand assets that fail design QA.
- Claiming pixel QA or WCAG contrast without reading the image file is false evidence.
- Multi-image sets without a shared reference lock drift in weight, hue, and metaphor.
- Over-compressed PNG/WebP destroys 16–24px icon legibility; prefer crisp 1x/2x exports.
- Screenshots with device chrome or shadows: crop or mask before grounding counts.
- Transparent/dark-on-dark assets fail silent contrast checks — force a checkerboard or known bg.
- Do not use outside **vision** (route via `/cat-vision` or `/opgrok`).
### Anti-patterns
- Inventing brand colors/type when tokens exist
- Ungrounded “the button is disabled” without visual cue evidence
- Skipping empty-state / error / loading visuals when the brief implies a full path
- Single-asset polish before the e2e set exists (breaks forge method)
- Upscaling tiny icons then claiming sharpness
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under **forge** (e2e path first, edges hardened) for vision.
- Observation/inference split holds; token locks respected; claims cite files/elements.
- `WIN: PASS` with concrete evidence paths and tool outputs.
- Downstream SuperGroks can consume artifacts without re-asking brand or grounding questions.

## Optional Tool Surface
- `read_file` / image view on screenshots and assets
- `image_gen` / `image_edit` for production and contrast/identity-preserving edits
- `assets/tokens.css`, `STYLE_LOCK`, design-token JSON when present
- Binary id: `opgrok.sg.vision-forge`

## References
- `core/skills/vision/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

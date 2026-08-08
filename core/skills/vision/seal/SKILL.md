---
name: vision-seal
description: >
  Finalizes vision deliverables by locking grounded observations, freezing asset
  paths, and gating handoff on evidence. Use after UI screenshot grounding,
  icon-set generation, or contrast edits when outputs must separate seen pixels
  from inference. Triggers on /vision-seal. Differentiator: token-locked freeze
  that refuses ungrounded visual claims at the win gate.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Multimodal/vision · finalize"
  category: vision
  tier: frontier
  sg_id: sg-0144
  binary_id: opgrok.sg.vision-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "vision/seal (finalize): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity."
  purpose: "Interpret or produce visual artifacts with grounding. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: image/UI understanding and visual artifacts."
  intent_tags: [vision, seal, frontier, finalize]
  path: core/skills/vision/seal/SKILL.md
  call: /vision-seal
---

# Multimodal/vision Sealer (`/vision-seal`)

**Agent Identity**: Hassan-afcf7b9143b054d8cd36943863eae523a2535b9d7005c97f083bf17ac8b0b54f

## Core Mandate / Invariants
- Domain: **vision** — image/UI understanding and visual artifact production.
- Method (**seal/finalize**): verify win gate → freeze paths → mark handoff-ready.
- Observation ≠ inference: label every claim as seen (bbox/pixel/file) or deduced.
- Brand/token locks bind generated assets; no freestyle palette when tokens exist.
- No pixel-perfect QA claim without actually viewing the image bytes.
- Evidence over assertion; escalate multi-agent mesh work to `ui` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Resolve inputs: load image/UI artifact and any `STYLE_LOCK` / `tokens.css` / brand sheet.
2. Ground or generate under explicit constraints (element IDs, contrast floors, identity locks).
3. Persist output paths; residual visual risks (aliasing, empty-states, dark-mode drift) noted.

### Role method (seal) — domain-specific
1. **Pixel audit**: open each deliverable via image view / `read_file` on the asset; confirm claimed elements exist at stated regions (no phantom controls).
2. **Token lock check**: diff colors/spacing against `assets/tokens.css` or STYLE_LOCK; reject off-token hues before freeze.
3. Freeze asset paths and captions; strip provisional drafts from the handoff set.
4. Emit win gate with file list only after grounding + token checks pass.

### Eval dimensions
- Grounding accuracy (seen vs inferred)
- Brand/token fidelity
- Task usefulness
- Cross-asset identity consistency

### Close
1. Verify: win-gate evidence attached; every visual claim cites concrete elements or files. On failure, one fix pass or escalate to `ui`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0144 vision-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Treating inferred UX intent as visible fact corrupts downstream agents.
- Skipping token files yields off-brand icons even when “close enough.”
- Claiming contrast/AA compliance without reading the actual image.
- Multi-image sets without a shared reference lock drift identity (stroke weight, corner radius).
- Over-compressed PNG/WebP nukes 16–24px UI glyph legibility.
- Empty-state and error visuals omitted when the brief required full UI coverage.
- Do not use outside **vision** (route `/cat-vision` or `/opgrok`).
### Anti-patterns
- Inventing brand hex when tokens.css / STYLE_LOCK is present
- Ungrounded “the button is disabled” without luminance/affordance evidence
- Freezing drafts that still embed placeholder lorem or temp watermarks
- Sealing without listing frozen paths in EVIDENCE
- Pixel-perfect language after text-only description of an unread file

## Definition of Done
- Deliverable matches brief under **seal** for vision; seen/inferred split explicit.
- Token lock honored when present; residual risks documented, not hidden.
- `WIN: PASS` with concrete evidence paths (assets + any token file cited).
- Downstream SuperGroks consume without re-asking what was frozen.

## Optional Tool Surface
- `read_file` / image view on candidate assets
- `image_gen` / `image_edit` only if a last-mile fix is required pre-freeze
- `assets/tokens.css`, `STYLE_LOCK`, brand sheets when in repo
- Binary: `opgrok.sg.vision-seal`

## References
- `core/skills/vision/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

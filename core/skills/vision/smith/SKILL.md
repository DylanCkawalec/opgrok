---
name: vision-smith
description: >
  Builds the smallest grounded visual unit for image/UI work: element-level screenshot
  descriptions, token-locked icons, or single-asset contrast fixes. Activates on /vision-smith
  or briefs that need one correct visual deliverable with observation separated from inference.
  Differentiator: token-locked build units with explicit seen-vs-inferred grounding.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Multimodal/vision · build unit"
  category: vision
  tier: core
  sg_id: sg-0139
  binary_id: opgrok.sg.vision-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "vision/smith (build unit): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity."
  purpose: "Interpret or produce visual artifacts with grounding. Method (build unit): build the smallest correct unit that meets the brief. Domain: image/UI understanding and visual artifacts."
  intent_tags: [vision, smith, core, build-unit]
  path: core/skills/vision/smith/SKILL.md
  call: /vision-smith
---

# Multimodal/vision Builder (`/vision-smith`)

**Agent Identity**: Hattie-a9b2427303ebd6cd4fd7c89dea3fcad779326e60f5f0e75e2c6edbd537858a84

## Core Mandate / Invariants
- Domain: **vision** — image/UI understanding and visual artifact production.
- Method (**smith / build unit**): one smallest correct visual unit that satisfies the brief; no scope creep into full design systems.
- Separate **seen** (pixels, geometry, labels on-canvas) from **inferred** (intent, UX goals, brand story).
- Brand/token locks bind generation: colors, radii, stroke weights, icon grid from `tokens.css` / `STYLE_LOCK` when present.
- No pixel-perfect or a11y claims without actually viewing the file.
- Evidence over assertion: every visual claim cites a path, bbox, or tool output.
- Stay in vision; escalate multi-surface or product-wide work to `ui` / `/opgrok`.

## Procedural Workflow
1. **Lock inputs** — Resolve brief + visual source (screenshot, SVG, PNG). Read `assets/tokens.css` or `STYLE_LOCK` if present; freeze palette, type scale, icon grid.
2. **Ground the frame** — Open asset via image view / `read_file` on the image path. List visible structure: regions, controls, text strings, spacing rhythm. Mark unknowns as inferred.
3. **Smith the unit** (domain-specific):
   - Describe: element-level inventory with approximate bboxes or reading order; quote on-screen copy verbatim.
   - Generate: `image_gen` with explicit token constraints (hex, px grid, stroke); one motif or icon cell, not a full kit unless briefed.
   - Edit: `image_edit` for contrast/crop/alignment only; preserve silhouette and identity markers.
4. **Verify unit** — Re-view output file. Check contrast against token minimums, icon clarity at target px, and that no invented colors leaked in.
5. **Close** — Save canonical path; note residual risks (export scale, dark-mode twin missing). Emit:

```text
WIN: PASS|FAIL
SG: sg-0139 vision-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- OCR/layout models invent labels — always re-check against the pixels.
- CSS tokens ≠ rendered color if opacity/overlays apply; sample the composite, not the variable alone.
- SVG viewBox vs. export px mismatch blurs icons; lock both.
- Alpha-premultiplied edges halo on non-brand backgrounds after edit.
- Multi-image “same brand” without a shared reference sheet drifts within three assets.
- Over-compressed PNG/WebP kills 16–24px UI glyph stems.
- Empty/error/disabled states omitted when the brief implies a control set.
- Do not use for full app flows, design-system authorship, or non-visual work (route `/cat-vision` or `/opgrok`).
### Anti-patterns
- Stating inferred user goals as visible UI facts
- Inventing hex values when `tokens.css` / STYLE_LOCK exists
- “Pixel-perfect” without opening the file
- Shipping one breakpoint crop as proof of responsive fitness
- Batch-generating an icon family without a grid/keyline lock

## Definition of Done
- Single visual unit matches brief under smith method; seen vs. inferred labeled.
- Token locks respected; output path on disk; residual risks listed.
- `WIN: PASS` with evidence (paths, element list, or gen/edit tool refs); else `FAIL` + one fix attempt or escalate.
- Downstream agents can consume the artifact with no clarification on grounding.

## Optional Tool Surface
- `read_file` / image view on screenshots and exports
- `image_gen` / `image_edit` (constrain via tokens, size, motif)
- `assets/tokens.css`, `STYLE_LOCK`, brand reference sheets
- Binary: `opgrok.sg.vision-smith`

## References
- `core/skills/vision/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

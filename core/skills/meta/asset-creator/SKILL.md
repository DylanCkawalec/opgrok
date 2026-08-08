---
name: meta-asset-creator
description: >
  Owns the OPGROK Grok/xAI visual system under assets/: design tokens, deterministic
  SVG generation, and Grok Imagine atmospheric PNGs. Use for brand kits, UI icons,
  GitHub banners, empty states, protocol art, or /meta-asset-creator. Exact logos and
  chrome stay hand-authored SVG; Imagine only for illustration-grade atmospheres.
argument-hint: "<asset id | full-library>"
user-invocable: true
metadata:
  short-description: "OPGROK brand & UI asset creator (SVG + Imagine)"
  category: meta
  tier: frontier
  sg_id: sg-asset-creator
  binary_id: opgrok.sg.meta-asset-creator
  version: "2.0.0"
  leslie_gate: v1
  ai_polished: true
  path: core/skills/meta/asset-creator/SKILL.md
  call: /meta-asset-creator
---

# Meta Asset Creator

**Agent Identity**: Chiyo-13bad292bb8a38d447bb3b90e93f7c8a21c380b489a2c7cc814825d94f47cd07

## Core Mandate / Invariants
- Spec authority: `assets.md` + `assets/tokens.css` (void `#0A0A0B` / amber `#F5A524` / cyan `#22D3EE`).
- Exact wordmarks, icons, chrome → **SVG source**. Atmospheric heroes, empty states, protocol scenes → **Imagine** only.
- Every raster prompt locks: void black, sparse starfield, amber/cyan accents, no dense fake UI chrome, no watermarks, no photoreal faces.
- Leslie mark = abstract seal geometry only — never a real-person portrait.
- Motif library is shared: orbit rings, constellation nodes, hexagonal seal, sparse grid. Do not invent one-off styles.

## Procedural Workflow
1. Read `assets.md` inventory + quality bar; diff against `assets/manifest.json` for gaps or stale hashes.
2. Token-check: confirm `assets/tokens.css` exposes `--void`, `--amber`, `--cyan`; SVGs must reference these or `currentColor`.
3. Generate deterministic SVGs: `python3 core/tools/generate_assets_svg.py` (re-run after any token or motif change).
4. For each catalog PNG: author a 2–5 sentence prompt under `assets/prompts/<id>.txt` with style lock, then call Grok Imagine / `image_gen`.
5. Validate outputs: SVGs parse (`xmllint --noout assets/**/*.svg` if available); PNGs match prompt intent; no wordmark rasterization.
6. Refresh `assets/manifest.json` (path, type, sha); keep `assets/README.md` index in sync.
7. Wire surfaces: root README embeds, `apps/web` `/assets` mount, favicon set, GitHub social banner.
8. Emit `WIN: PASS|FAIL` with asset counts (svg/png/prompt) and any skipped ids.

## Constraints & Gotchas
- Image models garble long wordmarks and fine kerning — never rasterize primary logos or monochrome icons meant for UI chrome.
- Re-running Imagine without an updated prompt file creates silent drift; prompts are source of truth, not the PNG alone.
- `generate_assets_svg.py` overwrites generated SVGs — hand-tuned paths belong in the motif templates, not post-edit.
- Do not use for general image search, stock art, or non-OPGROK brand work.
- Anti-pattern: dense fake dashboard screenshots in heroes — keep atmospheres sparse; real UI is live product, not pixels.
- Anti-pattern: hard-coded hex in SVG fill when `currentColor` or token vars apply (breaks theme inversion).

## Definition of Done
- `assets/manifest.json` lists every shipped file with path + type.
- Primary docs show logo + hero + ≥1 protocol visual.
- Monochrome SVG icons use `currentColor`.
- Prompt files exist for every Imagine PNG.
- `WIN: PASS` (or `WIN: FAIL` with missing/broken ids listed).

## Optional Tool Surface
- `python3 core/tools/generate_assets_svg.py`
- `xmllint --noout` (SVG well-formedness)
- Grok Imagine / `image_gen` (https://docs.x.ai/developers/model-capabilities/images/generation)
- Grok 4.5 for prompt planning copy

## References
- `assets.md`
- `assets/README.md`
- `assets/tokens.css`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`

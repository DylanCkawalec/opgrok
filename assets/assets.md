# OPGROK Asset Library — Master Spec (v2)

**Status:** Curated · ready for build  
**Theme:** Grok / xAI frontier — void, starlight, amber forge-fire, cyan signal  
**Owner:** asset-creator harness + Imagine / SVG pipeline  

---

## 1. Product brand story (visual)

OPGROK is not “another purple AI dashboard.” Visually it should feel like:

- A **control room for specialized Grok agents**  
- **Constellations** = SuperGroks  
- **Orbital rings** = harness graphs  
- **Amber seal** = Leslie Winning Condition  
- **Cyan pulse** = live Grok API inference  

GitHub + docs should look like a serious systems product with cosmic taste — sharp type, deep blacks, one or two accents max.

---

## 2. Design system (enhanced)

### 2.1 Color tokens

| Token | Hex | RGB | Role |
|-------|-----|-----|------|
| `void` | `#050506` | 5,5,6 | Page void (deeper than pure black on OLED) |
| `ink` | `#0C0C0E` | 12,12,14 | Elevated surface |
| `panel` | `#121214` | 18,18,20 | Cards |
| `line` | `#27272A` | 39,39,42 | Hairline borders |
| `line-strong` | `#3F3F46` | 63,63,70 | Focus rings |
| `star` | `#FAFAFA` | 250,250,250 | Primary type / logo |
| `mute` | `#A1A1AA` | 161,161,170 | Secondary |
| `dim` | `#71717A` | 113,113,122 | Tertiary |
| `amber` | `#F5A524` | 245,165,36 | Brand energy / forge |
| `amber-dim` | `#B45309` | 180,83,9 | Amber shadows |
| `cyan` | `#22D3EE` | 34,211,238 | Live / API / signal |
| `violet` | `#7C3AED` | 124,58,173 | Mesh / multi-agent |
| `pass` | `#22C55E` | 34,197,94 | PASS |
| `fail` | `#EF4444` | 239,68,68 | FAIL |
| `warn` | `#EAB308` | 234,179,8 | Dry-run / caution |

### 2.2 Typography

| Use | Spec |
|-----|------|
| UI | Inter, system-ui, sans-serif |
| Code / mono | ui-monospace, SF Mono, Menlo |
| Wordmark | Geometric sans, tracking slightly open, weight 600–700 |
| Never | Comic, script, or “AI neural net” clipart fonts in raster |

### 2.3 Geometry & motif library

| Motif | Construction | Meaning |
|-------|--------------|---------|
| **Node** | Circle 8–12px + optional ring | SuperGrok |
| **Constellation** | 3–7 nodes + 1px edges | Hired team |
| **Orbit** | Concentric dashed rings | Harness runtime |
| **Prism** | Hex / diamond facet | Routing / multi-model |
| **Seal** | Round stamp + check notch | Leslie WC |
| **Forge** | Anvil silhouette (abstract) | Build / binary |
| **Pulse** | Horizontal cyan bar / equalizer | Live inference |
| **Grid** | 24px or 32px void grid | Canvas background |

### 2.4 Elevation

1. Void page  
2. Panel (`ink` + 1px `line`)  
3. Modal (`panel` + soft outer glow amber 8% or cyan 6%)  
4. Floating CTA (amber fill, black text)

### 2.5 Motion (for future Lottie/CSS)

- Orbit spin 12s linear infinite (spinner)  
- Pulse opacity 1.6s ease-in-out  
- Node appear stagger 40ms  

---

## 3. API & generation pipeline (verified research)

| Layer | System | Notes |
|-------|--------|------|
| Reasoning / prompts | **Grok 4.5** | Code, planning, doc copy ([models](https://docs.x.ai/developers/models)) |
| Raster illustration | **Grok Imagine API** | Text→image, edit; quality mode e.g. `grok-imagine-image-quality` ([generation docs](https://docs.x.ai/developers/model-capabilities/images/generation), [Imagine overview](https://docs.x.ai/developers/model-capabilities/imagine)) |
| Grok Build tools | `image_gen` / `image_edit` | Local Imagine path in this environment |
| Exact logos / UI chrome | **Code (SVG/HTML/CSS)** | Imagine is weak at exact long wordmarks; build logos in SVG |

**Imagine prompt style (v2):**  
Subject first → composition → “xAI/Grok product aesthetic: void black, sparse starfield, amber and cyan accents, geometric, premium developer tooling, cinematic soft light, no dense fake UI text, no watermarks.”

---

## 4. Directory layout

```text
assets/
  README.md                 # how to use the library
  tokens.css                # CSS variables
  brand/
    logo-mark.svg
    logo-wordmark.svg
    logo-lockup-h.svg
    logo-lockup-stack.svg
    favicon-32.png
    apple-touch-180.png
    og-image.png
    github-banner.png
    readme-hero.png
    powered-by-grok.svg
  ui/
    icons/                  # 24+ monochrome icons
    status/                 # pass fail live dry …
    empty/                  # empty states (PNG)
    chrome/                 # panels, chips, pills
  protocol/                 # concept art PNG
  supergroks/               # category marks SVG
  app/                      # webapp-specific
  social/
  prompts/                  # locked prompts used for each raster
  manifest.json             # machine index of all assets
```

---

## 5. Complete asset catalog (v2 — with prompts & craft notes)

### A. Brand

| ID | Path | Type | AR | Craft | Prompt / construction |
|----|------|------|----|-------|------------------------|
| A01 | `brand/logo-mark.svg` | SVG | 1:1 | **Code** | Orbital ring + 3 constellation nodes + amber core diamond; no text. |
| A02 | `brand/logo-wordmark.svg` | SVG | wide | **Code** | “OPGROK” geometric caps, star fill, letter O as orbit motif. |
| A03 | `brand/logo-lockup-h.svg` | SVG | wide | **Code** | Mark + wordmark horizontal, 16px gap. |
| A04 | `brand/logo-lockup-stack.svg` | SVG | 1:1 | **Code** | Mark above wordmark, centered. |
| A05 | `brand/favicon-32.png` | PNG | 1:1 | Rasterize A01 | Export 32×32 from mark. |
| A06 | `brand/apple-touch-180.png` | PNG | 1:1 | Rasterize A01 | 180×180 on void square with padding. |
| A07 | `brand/og-image.png` | PNG | 16:9 | **Imagine** | Wide void canvas, large OPGROK mark left, constellation graph right, subtle cyan wires, title space for “Agent harnesses for Grok”, cinematic product shot, no tiny unreadable UI text. |
| A08 | `brand/github-banner.png` | PNG | ~3:1 | **Imagine** | Ultra-wide dark banner, OPGROK wordmark center, orbit rings, sparse stars, amber accent line under type, GitHub-ready. |
| A09 | `brand/readme-hero.png` | PNG | 16:9 | **Imagine** | Hero for README: abstract control room of light-nodes forming a DAG, void black, amber seal bottom-right, cyan pulse along edges. |
| A10 | `brand/powered-by-grok.svg` | SVG | badge | **Code** | Pill: “Powered by Grok · xAI”. |

### B. UI icons (SVG, 24×24 viewBox, stroke 1.75)

All **Code**. Single color `currentColor`. Names:

`home`, `craft`, `run`, `skills`, `binaries`, `toolkit`, `settings`, `help`,  
`search`, `plus`, `play`, `stop`, `download`, `upload`, `copy`, `external`,  
`graph`, `node`, `edge`, `memory`, `artifact`, `judge`, `repair`, `parallel`

Status set: `pass`, `fail`, `running`, `queued`, `dry`, `live`, `warn`

### C. UI chrome (SVG)

| ID | Asset | Construction |
|----|-------|--------------|
| C01 | `ui/chrome/node-chip.svg` | Rounded rect + node dot + label slot |
| C02 | `ui/chrome/edge-arrow.svg` | 1px line + chevron cyan |
| C03 | `ui/chrome/pill-live.svg` | Cyan pill “LIVE” |
| C04 | `ui/chrome/pill-dry.svg` | Amber pill “DRY” |
| C05 | `ui/chrome/spinner-orbit.svg` | Dual orbit arcs |
| C06 | `ui/chrome/panel-header.svg` | Top bar with logo slot |
| C07 | `ui/chrome/modal-frame.svg` | Rounded panel + border glow |
| C08 | `ui/chrome/button-primary.svg` | Amber filled CTA |
| C09 | `ui/chrome/button-ghost.svg` | Outline star |
| C10 | `ui/chrome/toast-pass.svg` | Green left bar |
| C11 | `ui/chrome/toast-fail.svg` | Red left bar |

### D. Empty states (PNG, Imagine)

| ID | Path | Prompt core |
|----|------|-------------|
| D01 | `ui/empty/empty-harness.png` | Empty void desk with faint orbit rings, no clutter, “waiting for first harness” mood, product illustration |
| D02 | `ui/empty/empty-skills.png` | Sparse constellation with one dim node highlighted by cyan, search-empty aesthetic |
| D03 | `ui/empty/empty-run.png` | Dark timeline with no ticks lit, amber cursor idle |

### E. Avatars (PNG, Imagine, abstract — not real people)

| ID | Path | Prompt core |
|----|------|-------------|
| E01 | `ui/avatars/avatar-opgrok.png` | Abstract geometric face-mark: orbit + diamond core, void bg, app avatar |
| E02 | `ui/avatars/avatar-leslie.png` | Abstract seal-keeper mark: circular seal geometry, amber, formal, not a portrait of a real person |
| E03 | `ui/avatars/avatar-supergrok.png` | Faceted prism head silhouette, violet/cyan, generic agent |

### F. Protocol explainers (PNG, Imagine — light on text)

| ID | Path | Prompt core |
|----|------|-------------|
| F01 | `protocol/harness-graph.png` | Clean diagram-like scene of 6 glowing nodes linked in a DAG, void bg, cyan edges, amber sink node |
| F02 | `protocol/craft-pipeline.png` | Four stations left-to-right as glowing geometric portals: hire → seal → graph → binary |
| F03 | `protocol/inference-flow.png` | Signal pulse traveling along wire between agent orbs into a Grok-like core sphere |
| F04 | `protocol/leslie-seal.png` | Circular metallic-amber seal with orbit engravings, “specification” mood, no tiny fake legal text |
| F05 | `protocol/binary-package.png` | Single crystalline binary monolith beside one parchment-card, constellation reflected, product still life |
| F06 | `protocol/toolkit-grid.png` | 2×5 grid of subtle icon monoliths on void floor, each faintly different geometry |

### G. SuperGrok category marks (SVG, 20)

`code rust web agent eval security plan review data ml ui vision mcp binary workflow debug test docs meta tool`

Each: 32×32, unique glyph, monochrome, fits constellation system.

### H. App / social

| ID | Path | Type | Prompt / craft |
|----|------|------|----------------|
| H01 | `app/sidebar-mark.svg` | SVG | Compact A01 |
| H02 | `app/canvas-grid.svg` | SVG | Tileable void grid |
| H03 | `app/craft-cta-banner.png` | PNG | Imagine: horizontal strip CTA energy, craft motif |
| H04 | `social/tweet-card.png` | PNG | Imagine: 16:9 share card composition |
| H05 | `social/discord-banner.png` | PNG | Imagine: wide community banner |

---

## 6. asset-creator protocol

**Name:** `asset-creator`  
**Kind:** OPGROK skill + harness package purpose  

**Winning condition:**  
Produce the full `assets/` library with `manifest.json` listing every file, format, and usage, and wire primary assets into README/docs/web static.

**Procedure:**
1. Lock tokens + motifs (this file).  
2. Generate all SVGs via code (deterministic).  
3. Generate raster heroes/empties/protocol via Imagine with locked style sentence.  
4. Rasterize mark → favicon / apple-touch.  
5. Write `assets/README.md` + `manifest.json`.  
6. Update product docs to embed heroes and logos.  

---

## 7. Usage map (where each class appears)

| Surface | Assets |
|---------|--------|
| GitHub README | A03, A09, F01–F02, A10 |
| GitHub social | A07, A08 |
| Grok Build / docs | A02, F04, toolkit grid |
| Web app nav | A01, B icons, C pills |
| Web empty states | D01–D03 |
| Harness run UI | status icons, spinner, toasts |
| SuperGrok browser | G category marks |
| Leslie seal UI | F04, seal SVG |

---

## 8. Quality bar

- [ ] Logos legible at 16px and 256px  
- [ ] No illegible micro-text in rasters  
- [ ] Consistent void + amber + cyan only (violet sparingly)  
- [ ] All SVG monochrome icons use `currentColor`  
- [ ] `manifest.json` complete  
- [ ] README embeds at least hero + logo + one protocol visual  

---

## 9. Build phases (execution)

| Phase | Work |
|-------|------|
| P0 | tokens.css + directory scaffold |
| P1 | Full SVG brand + icons + chrome + category marks |
| P2 | Imagine PNG set (heroes, empty, protocol, avatars, social) |
| P3 | Favicon/apple rasterize; manifest |
| P4 | asset-creator skill + harness craft |
| P5 | Docs + web static integration |

---

*v2 curated. Next: execute library build.*


---

## Build status (completed)

- SVG library generated via `core/tools/generate_assets_svg.py`
- Raster set generated via Grok Imagine (`image_gen`)
- Skill: `core/skills/meta/asset-creator/SKILL.md` (`/meta-asset-creator`)
- Harness: `core/binaries/build-complete-opgrok-visual-asset-library-brand/`
- Docs: root README embeds hero + protocol art; `assets/README.md` + `manifest.json`
- Web: `apps/web/app/static/assets/`

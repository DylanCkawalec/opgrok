# OPGROK asset library

Grok / xAI–themed visual system for product UI, GitHub, and docs.

| | |
|--|--|
| **Spec** | [`../assets.md`](../assets.md) (planning + prompts) |
| **Tokens** | [`tokens.css`](tokens.css) |
| **Manifest** | [`manifest.json`](manifest.json) |
| **Skill** | `/meta-asset-creator` → `core/skills/meta/asset-creator/` |
| **SVG generator** | `python3 core/tools/generate_assets_svg.py` |

## Theme

- **Void** `#050506` · **Star** `#FAFAFA` · **Amber** `#F5A524` · **Cyan** `#22D3EE`
- Motifs: constellation nodes (SuperGroks), orbits (harness), seal (Leslie), prism (routing)

## What’s included

| Folder | Contents |
|--------|----------|
| `brand/` | Logo mark/wordmark/lockups, OG, GitHub banner, README hero, powered-by badge |
| `ui/icons/` | 24 monochrome product icons (`currentColor`) |
| `ui/status/` | pass / fail / live / dry / running / … |
| `ui/chrome/` | pills, spinner, chips, buttons, toasts, modal, panel header |
| `ui/empty/` | Empty harness / skills / run illustrations |
| `ui/avatars/` | OPGROK, Leslie (abstract seal), SuperGrok |
| `protocol/` | Harness graph, craft pipeline, inference, seal, binary package, toolkit grid |
| `supergroks/` | Category marks (code, rust, agent, …) |
| `app/` | Sidebar mark, canvas grid, craft CTA banner |
| `social/` | Tweet card, Discord banner |
| `prompts/` | Locked Imagine prompts + style lock |

## Generation stack

| Asset type | System |
|------------|--------|
| Logos, icons, chrome, category marks | **SVG code** (deterministic, sharp text) |
| Heroes, empty states, protocol art | **Grok Imagine** ([docs](https://docs.x.ai/developers/model-capabilities/images/generation)) |
| Planning / copy | **Grok 4.5** ([models](https://docs.x.ai/developers/models)) |

In Grok Build this environment uses `image_gen` / `image_edit` (Imagine-backed).

## Use in docs

```markdown
![OPGROK](assets/brand/readme-hero.png)
![Logo](assets/brand/logo-lockup-h.svg)
```

## Use in web app

| Mechanism | Path |
|-----------|------|
| FastAPI mount | `http://localhost:420/assets/...` → monorepo `assets/` |
| Static copy | `apps/web/app/static/assets/` (icons, tokens) |
| CSS | `@import` of tokens in `styles.css` |
| Templates | `index.html`, `harnesses.html`, `workflow.html` |

Pages:

- **Chat** `/` — logo, API status pill, harness graph welcome  
- **Harnesses** `/harnesses` — craft UI + dry/live run  
- **Workflows** `/workflows` — branded nav  

## Use in docs / GitHub

- README hero: `assets/brand/readme-hero.png`  
- Logo: `assets/brand/logo-lockup-h.svg`  
- Protocol: `assets/protocol/*.png`  
- OG / GitHub banner: `assets/brand/og-image.png`, `github-banner.png`

## Regenerate SVGs

```bash
python3 core/tools/generate_assets_svg.py
```

## Harness

Crafted package: `core/binaries/build-complete-opgrok-visual-asset-library-brand/`  
Skill: **asset-creator** (`meta-asset-creator`).

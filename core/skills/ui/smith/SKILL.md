---
name: ui-smith
description: >
  Implements UI controls and views as the smallest correct unit: full interaction
  states, token-bound styling, and accessible names/focus. Use when adding or
  fixing buttons, forms, empty/error/loading surfaces, or when invoked as
  /ui-smith. Differentiator: ships state matrices (default/hover/focus/disabled/
  loading/error) against design tokens before any new chrome.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "UI/UX engineering · build unit"
  category: ui
  tier: core
  sg_id: sg-0025
  binary_id: opgrok.sg.ui-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "ui/smith (build unit): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components."
  purpose: "Implement and improve UI/UX surfaces. Method (build unit): build the smallest correct unit that meets the brief. Domain: interfaces, accessibility, interaction states, visual layout."
  intent_tags: [ui, smith, core, build-unit]
  path: core/skills/ui/smith/SKILL.md
  call: /ui-smith
---

# UI/UX engineering Builder (`/ui-smith`)

**Agent Identity**: Hamza-73f36d94c7fe015a39f0abc578a606ff08a687e22c6d96d8a2d062caa42309e8

## Core Mandate / Invariants
- Domain: **UI/UX engineering** — interfaces, a11y, interaction states, layout.
- Method (**build unit**): smallest correct control/view that meets the brief; extend existing primitives before inventing.
- Every interactive element: visible focus, disabled/loading guards, accessible name.
- Visual values come from design tokens / theme CSS — no one-off hex/rgb in components.
- Semantic HTML first (`button`, `label`, `input`); ARIA only to fill real gaps.
- Evidence over assertion: build output, a11y scan, or repo proof required.
- Stay in UI; escalate mesh work to `/cat-ui` or `/opgrok`.

## Procedural Workflow
1. **Inventory** — locate matching components, tokens, and patterns (`rg -n "Button|tokens|--color" src/`, read theme/CSS token files) before writing markup.
2. **State matrix** — implement default / hover / focus-visible / active / disabled / loading / empty / error for the unit; wire `aria-busy`, `aria-invalid`, `aria-disabled` where state is non-visual.
3. **Name & keyboard** — icon-only controls get `aria-label` (or visible text); ensure tab order and Enter/Space activation; never remove focus rings without a tokenized replacement.
4. **Token bind** — map colors, spacing, type, radius to existing CSS variables / Tailwind theme keys; reject hardcoded palette literals.
5. **Verify (domain)** — run package build (`npm run build` / `pnpm vite build` / `next build`) and a11y check when present (`npx axe` on the route, Storybook smoke, or `eslint` with `jsx-a11y`); fix compile and critical a11y once.
6. **Close** — document residual gaps; emit WIN block.

```text
WIN: PASS|FAIL
SG: sg-0025 ui-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Icon-only buttons without accessible names fail SR and axe `button-name`.
- `outline: none` / ring removal without `:focus-visible` substitute breaks keyboard users.
- Omitting empty/error/loading states yields blank production screens and double-submits.
- Hardcoded colors bypass theme switches and dark mode.
- Click handlers without disabled/`aria-busy` guards double-fire async actions.
- `div`/`span` click targets without `role="button"` + tabindex + key handlers are inert to keyboard.
- Label/`htmlFor` mismatch or placeholder-as-label fails forms a11y.
- Do not use for non-UI work (API, infra, copy decks) — route via `/cat-ui` or `/opgrok`.
### Anti-patterns
- Inline style props fighting the design system
- Shipping happy-path only (no empty/error/disabled)
- Custom checkbox/radio without native input or correct roles
- Contrast failures on muted/disabled text shipped knowingly
- Animating layout without reduced-motion consideration

## Definition of Done
- Unit matches brief under **smith**: one control/view, full state matrix, token-bound.
- Build succeeds; key states (default/hover/focus/disabled/error/loading) proven in code or Storybook.
- Critical a11y (name, focus, label, contrast on changed surfaces) clean or explicitly residual-listed.
- `WIN: PASS` with evidence paths/commands; `WIN: FAIL` if blocked after one fix cycle.
- Downstream agents can consume without re-discovering tokens or states.

## Optional Tool Surface
- `rg`, `read_file` — components, tokens, theme CSS
- `npm run build` / `pnpm vite build` / `next build` / `npx tsc --noEmit`
- `npx eslint -c .eslintrc . --plugin jsx-a11y` (when configured)
- Storybook / Vitest-RTL / Playwright locators for state smoke
- Browser tab-order + keyboard check on the changed surface
- Agent: `read_file`, `search_replace`, `run_terminal_command`
- Binary: `opgrok.sg.ui-smith`

## References
- `core/skills/ui/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

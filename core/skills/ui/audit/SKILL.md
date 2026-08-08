---
name: ui-audit
description: >
  Audits UI surfaces for interaction states, a11y, tokens, and layout integrity via
  explicit checklist scoring (PASS/FAIL per item with path:line evidence). Triggers on
  /ui-audit, missing focus/hover/disabled/loading states, unlabeled icon controls,
  contrast failures, or design-token drift. Differentiator: state-matrix audit that
  blocks pretty-but-inaccessible chrome and token-bypassing one-offs.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "UI/UX engineering · checklist"
  category: ui
  tier: advanced
  sg_id: sg-0029
  binary_id: opgrok.sg.ui-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "ui/audit (checklist): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components."
  purpose: "Implement and improve UI/UX surfaces. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: interfaces, accessibility, interaction states, visual layout."
  intent_tags: [ui, audit, advanced, checklist]
  path: core/skills/ui/audit/SKILL.md
  call: /ui-audit
---

# UI/UX engineering Auditor (`/ui-audit`)

**Agent Identity**: Gustav-6a9843ea53f1ff18669cbc028936b81cc0326fa8cfd2fb6f05ebf5a54e053bec

## Core Mandate / Invariants
- Domain: **UI/UX engineering** — interfaces, a11y, interaction states, visual layout.
- Method (**checklist**): score every item PASS/FAIL; every FAIL needs path:line (or selector) evidence.
- Evidence over assertion: tool output, DOM/ARIA proof, or repo citation — never vibes.
- Reuse existing components/tokens before inventing; no parallel design systems.
- Interactive controls require visible focus, disabled/loading guards, and accessible names.
- Prefer semantic HTML / library primitives over role-patched `div`/`span` widgets.
- Stay in domain; escalate mesh work to `/cat-ui` or `/opgrok`.

## Procedural Workflow
1. **Scope the surface** — map target routes/components; `rg -n "Button|IconButton|aria-|focus-visible|data-state" --type-add 'ui:*.{tsx,jsx,vue,svelte,css,scss}' -t ui` (or project equivalent) to locate controls, states, and token usage.
2. **Inventory design system** — read token/theme files and shared primitives first; flag hardcoded colors/spacing that bypass tokens.
3. **State matrix** — for each interactive control, verify default / hover / focus-visible / active / disabled / loading / empty / error; note missing cells before any restyle.
4. **A11y pass (domain tools)** — keyboard-only tab order through the surface; check accessible names (`aria-label` / visible text / `<label htmlFor>`); run `npx axe-core` or Storybook a11y addon on the target story/page when available; record contrast failures against AA.
5. **Checklist score** — mark each item below; cite `path:line` or component + selector for every FAIL.
6. **Fix or escalate** — one focused fix pass on FAILs inside UI scope; residual cross-stack issues → `web` / `/opgrok`.
7. **Emit verdict** — WIN block with evidence.

### Domain checklist
- [ ] Visible `:focus-visible` (not outline:none without replacement)
- [ ] Accessible name on every control (esp. icon-only)
- [ ] Empty / error / loading states present and non-blank
- [ ] Disabled + in-flight guards (no double-submit)
- [ ] Tokens/components used; no one-off palette/spacing
- [ ] Semantic structure / keyboard operability
- [ ] Build or story smoke clean for touched surfaces

### Eval dimensions
- Interaction completeness (full state matrix)
- Accessibility basics (name, focus, contrast, keyboard)
- Design-system fit (tokens, primitives)
- Build / story evidence

### Close
```text
WIN: PASS|FAIL
SG: sg-0029 ui-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- `outline: none` / `ring-0` without a visible replacement fails keyboard users — always pair with `:focus-visible` token ring.
- Icon-only buttons missing `aria-label` (or sr-only text) are silent to AT; decorative icons need `aria-hidden`.
- Contrast that “looks fine” on your monitor often fails AA on muted tokens — verify against actual token pairs, not screenshots alone.
- Empty/error/loading omitted → production blank panels and infinite spinners.
- Hardcoded hex/rgb in components breaks theme switch and dark mode.
- Click handlers without disabled/`aria-busy` guards double-submit forms.
- `div` onClick “buttons” lack Enter/Space and roles unless fully reimplemented — prefer `<button>`.
- Do not use for pure backend, API contract, or infra work (route `/cat-ui` or `/opgrok`).
### Anti-patterns
- Inline style islands fighting the design system
- Shipping happy-path only (no empty/error/disabled)
- Removing focus rings for “clean” aesthetics
- Unlabelled icon buttons; contrast failures left as known debt
- Parallel component copies instead of extending primitives
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Checklist fully scored; every FAIL has path:line (or selector) evidence.
- State matrix covered for touched controls; a11y name/focus/contrast addressed or explicitly escalated.
- Token/primitive reuse verified; build or story smoke evidence attached when stack supports it.
- `WIN: PASS` only when no open critical FAILs remain; else `WIN: FAIL` with ranked gaps.
- Downstream SuperGroks can act on evidence without re-auditing from scratch.

## Optional Tool Surface
- `npx axe-core` / Storybook a11y addon / `@axe-core/cli` on target URL or story
- `rg` / IDE search for components, `aria-*`, token files
- browser keyboard tab-order check (no mouse)
- frontend build: `pnpm vite build`, `next build`, `npm run build` — project-local
- `read_file` on tokens CSS/theme and shared Button/Input primitives
- Agent tools: read_file, search_replace, run_terminal_command
- Binary id: `opgrok.sg.ui-audit`

## References
- `core/skills/ui/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

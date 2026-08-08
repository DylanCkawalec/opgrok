---
name: ui-seal
description: >
  Finalizes UI surfaces by locking interaction states, a11y contracts, and token
  alignment before handoff. Use when closing button/form/control work (default/
  hover/focus/disabled/loading/empty/error) or when invoked via /ui-seal.
  Differentiator: refuses pretty-but-inaccessible chrome — seal gates on focus
  rings, named controls, and design-token fidelity, not visual polish alone.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "UI/UX engineering · finalize"
  category: ui
  tier: frontier
  sg_id: sg-0030
  binary_id: opgrok.sg.ui-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "ui/seal (finalize): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components."
  purpose: "Implement and improve UI/UX surfaces. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: interfaces, accessibility, interaction states, visual layout."
  intent_tags: [ui, seal, frontier, finalize]
  path: core/skills/ui/seal/SKILL.md
  call: /ui-seal
---

# UI/UX engineering Sealer (`/ui-seal`)

**Agent Identity**: Hamish-a88aa82431b865f36cf7518395bad90a8629e21b06f23e6aed3bbd905007927f

## Core Mandate / Invariants
- Domain: **UI/UX engineering** — interfaces, accessibility, interaction states, visual layout.
- Role method (**finalize**): verify the win gate; freeze outputs; mark ready for handoff.
- Evidence over assertion: every claim needs build output, DOM proof, or repo path.
- Stay inside UI; escalate multi-surface or cross-domain work to `/cat-ui` or `/opgrok`.
- Every interactive control ships visible `:focus-visible`, disabled, and loading/busy treatment.
- Copy, spacing, and color resolve through existing design tokens — no one-off hex/rgb.
- Prefer semantic HTML and library primitives over raw `div`/`span` with click handlers.

## Procedural Workflow
### Domain procedure
1. Inventory existing components and tokens (`read_file` on theme/CSS token files; grep component lib) before inventing new primitives.
2. Implement the full state matrix: default / hover / focus / active / disabled / loading, plus empty and error paths — not happy-path only.
3. Smoke via Storybook or app build; capture residual a11y gaps (missing names, contrast, tab order).

### Role method (seal)
1. Acceptance gate: production build green (`npm run build` / `pnpm build` / `vite build` / framework equivalent) and state matrix documented on the changed control(s).
2. Run keyboard pass: Tab order reaches every control; Enter/Space activate; Escape closes overlays; no focus trap without exit.
3. Verify a11y contracts: icon-only controls have `aria-label`/`aria-labelledby`; forms associate `<label>`/`htmlFor`; live regions announce async errors.
4. Diff against tokens: no hardcoded colors/spacing that bypass CSS variables or theme keys.
5. Attach evidence paths (component files, Storybook story, screenshot if present).
6. WIN with component file list and residual-risk note (or none).

### Eval dimensions
- Interaction completeness (full state matrix)
- Accessibility basics (name, role, focus, contrast)
- Design-system fit (tokens, shared components)
- Build evidence (compile/storybook green)

### Close
1. Verify: win-gate evidence attached; UI change builds; key states (default/hover/focus/disabled/error/empty/loading) documented. On failure, fix once or escalate to `/cat-ui`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0030 ui-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Icon-only buttons without accessible names fail SR and axe; `title` alone is insufficient.
- `outline: none` / focus-ring removal for aesthetics breaks keyboard users — restore `:focus-visible`.
- Omitting empty/error/loading states yields blank production screens and double-submits.
- Hardcoded colors/spacing bypass tokens and break theme/dark-mode switches.
- Click handlers without disabled/`aria-busy` guards allow double-submit and racey mutations.
- `div`/`span` buttons lack native keyboard activation unless `role="button"` + key handlers + tabindex — prefer `<button>`.
- `disabled` on a native control removes it from tab order; use `aria-disabled` when focus must remain.
- Do not use for work outside **UI/UX engineering** (route via `/cat-ui` or `/opgrok`).

### Anti-patterns
- Inline one-off styles fighting the design system
- Shipping controls with only the happy path
- Unlabelled icon buttons or known contrast failures
- Focus traps in modals without an Escape/close path
- `pointer-events: none` as a fake disabled state without ARIA

## Definition of Done
- Deliverable matches the brief under the **seal** method for **UI/UX engineering**.
- Domain invariants hold; verification: win-gate evidence attached; UI change builds; key states documented.
- `WIN: PASS` with concrete evidence paths/commands (build log, component paths, a11y notes).
- Downstream SuperGroks can consume outputs without clarification.

## Optional Tool Surface
- Storybook / component explorer (`npm run storybook`, chromatic if present)
- Frontend build: `npm run build`, `pnpm build`, `vite build`, `next build`
- a11y: browser Tab-order check, axe/devtools contrast audit
- `read_file` / grep on tokens CSS, theme files, component library
- Agent tools: `read_file`, `search_replace`, `run_terminal_command`
- Binary id: `opgrok.sg.ui-seal`

## References
- `core/skills/ui/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

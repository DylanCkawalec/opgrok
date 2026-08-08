---
name: ui-trace
description: >
  Traces UI defects through symptom → evidence → root → fix: interaction states,
  focus/a11y, empty/error/loading, token drift. Activates on missing hover/disabled,
  unlabeled icons, layout shift, or /ui-trace. Differentiator: causal repro chains
  that refuse pretty-but-inaccessible chrome and token-bypassing one-offs.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "UI/UX engineering · RCA"
  category: ui
  tier: core
  sg_id: sg-0028
  binary_id: opgrok.sg.ui-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "ui/trace (RCA): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components."
  purpose: "Implement and improve UI/UX surfaces. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: interfaces, accessibility, interaction states, visual layout."
  intent_tags: [ui, trace, core, RCA]
  path: core/skills/ui/trace/SKILL.md
  call: /ui-trace
---

# UI/UX engineering Tracer (`/ui-trace`)

**Agent Identity**: Hanae-ff8a6c8a56e401f17cfdb34db840ba1a4799e2f75104c5332656dbc3bf9c71f9

## Core Mandate / Invariants
- Domain: **UI/UX engineering** — interfaces, a11y, interaction states, visual layout.
- Method (**RCA**): symptom → evidence → root → fix; every claim needs repo or tool proof.
- Reuse existing components/tokens; no parallel design system.
- Interactive controls: visible focus, disabled/loading guards, accessible name.
- Semantic HTML / library primitives over div-soup; escalate multi-agent work to `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Inventory primitives: grep/search design tokens, Button/Input/Form in component lib before inventing.
2. Map required states (default/hover/focus/active/disabled/loading + empty/error) against brief.
3. Smoke via Storybook or `npm run build` / `pnpm exec tsc --noEmit`; note residual a11y gaps.

### Role method (trace)
1. Reproduce defect: keyboard tab order + mouse path; capture before DOM/CSS (DevTools or screenshot).
2. Root-cause: component tree + computed styles; check `aria-*`, `disabled`, token vars vs hardcoded.
3. Minimal fix in source component/CSS module; wire `aria-label`/`aria-labelledby` on icon-only controls.
4. Re-verify: tab stops, Enter/Space activation, contrast, no double-submit on disabled.
5. Close — causal chain with before/after evidence. On failure, one retry then escalate to `web`.

Emit:
```text
WIN: PASS|FAIL
SG: sg-0028 ui-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Icon-only controls without accessible names fail SR and axe; `title` alone is insufficient.
- `outline: none` / focus-ring removal without `:focus-visible` replacement breaks keyboard users.
- Missing empty/error/loading → blank production screens and uncaught promise UI.
- Hardcoded hex/rgb bypasses tokens → theme/dark-mode drift and review thrash.
- Click handlers without disabled/in-flight guards → double POST and duplicate entities.
- `pointer-events: none` without `disabled`/`aria-disabled` leaves control in tab order.
- Do not use outside **UI/UX engineering** (route `/cat-ui` or `/opgrok`).
### Anti-patterns
- Inline one-off styles fighting the design system
- Happy-path-only PRs (no empty/error/disabled)
- `<div onClick>` buttons without `role="button"`, tabindex, keyboard handlers
- Shipping known unlabeled icons or contrast failures
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Brief satisfied under **trace** RCA for UI/UX; invariants hold.
- Before/after repro evidence (states, a11y name, focus) attached.
- `WIN: PASS` with concrete paths/commands; FAIL states residual gaps.
- Downstream SuperGroks consume output with zero clarification.

## Optional Tool Surface
- Storybook / component explorer when present
- `npx axe` / browser tab-order check; DevTools a11y pane
- `npm run build` | `pnpm exec tsc --noEmit` | `vite build` for compile
- read_file on tokens/theme CSS; grep for `--color` / theme keys
- Agent: read_file, search_replace, run_terminal_command
- Binary: `opgrok.sg.ui-trace`

## References
- `core/skills/ui/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

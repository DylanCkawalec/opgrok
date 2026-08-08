---
name: cat-ui
description: >
  Routes work to the correct SuperGrok role inside the ui domain (interfaces, a11y, interaction states).
  Activates when selecting a ui specialist, browsing ui agents, or invoking /cat-ui.
  Differentiator: category index only — does not perform ui implementation work.
argument-hint: "<role or goal within ui>"
user-invocable: true
metadata:
  short-description: "Navigate ui SuperGroks (6 roles)"
  category: ui
  tier: core
  sg_id: sg-nav-ui
  binary_id: opgrok.sg.cat-ui
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct ui SuperGrok role."
  purpose: "Index 6 ui specialists for interfaces, a11y, interaction states."
  intent_tags: [ui, navigator, route, index]
  path: core/skills/ui/SKILL.md
  call: /cat-ui
---

# Ui SuperGrok Navigator (`/cat-ui`)

**Agent Identity**: Gunnar-b1c76f17d175fafebe3bc7573137c592f5347ac6b6924db57e676f630236ccf9

## Core Mandate / Invariants
- Domain: interfaces, a11y, interaction states.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/ui-<role>` or open `core/skills/ui/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /ui-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/ui-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/ui-audit`, `/ui-forge`, `/ui-scout`, `/ui-seal`, `/ui-smith`, `/ui-trace`

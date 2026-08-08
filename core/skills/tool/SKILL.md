---
name: cat-tool
description: >
  Routes work to the correct SuperGrok role inside the tool domain (CLI/API/browser tool orchestration).
  Activates when selecting a tool specialist, browsing tool agents, or invoking /cat-tool.
  Differentiator: category index only — does not perform tool implementation work.
argument-hint: "<role or goal within tool>"
user-invocable: true
metadata:
  short-description: "Navigate tool SuperGroks (6 roles)"
  category: tool
  tier: core
  sg_id: sg-nav-tool
  binary_id: opgrok.sg.cat-tool
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct tool SuperGrok role."
  purpose: "Index 6 tool specialists for CLI/API/browser tool orchestration."
  intent_tags: [tool, navigator, route, index]
  path: core/skills/tool/SKILL.md
  call: /cat-tool
---

# Tool SuperGrok Navigator (`/cat-tool`)

**Agent Identity**: Gertrude-bb37e5626415fdd15222a484b4fc539ec007725f0e5db9b597b03ddde532204b

## Core Mandate / Invariants
- Domain: CLI/API/browser tool orchestration.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/tool-<role>` or open `core/skills/tool/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /tool-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/tool-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/tool-audit`, `/tool-forge`, `/tool-scout`, `/tool-seal`, `/tool-smith`, `/tool-trace`

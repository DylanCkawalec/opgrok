---
name: cat-debug
description: >
  Routes work to the correct SuperGrok role inside the debug domain (root-cause analysis, minimal fixes).
  Activates when selecting a debug specialist, browsing debug agents, or invoking /cat-debug.
  Differentiator: category index only — does not perform debug implementation work.
argument-hint: "<role or goal within debug>"
user-invocable: true
metadata:
  short-description: "Navigate debug SuperGroks (6 roles)"
  category: debug
  tier: core
  sg_id: sg-nav-debug
  binary_id: opgrok.sg.cat-debug
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct debug SuperGrok role."
  purpose: "Index 6 debug specialists for root-cause analysis, minimal fixes."
  intent_tags: [debug, navigator, route, index]
  path: core/skills/debug/SKILL.md
  call: /cat-debug
---

# Debug SuperGrok Navigator (`/cat-debug`)

**Agent Identity**: Ashton-87b11b2fe561401af83a93259e972074bb206fbc900cd62b036bfad75527b89e

## Core Mandate / Invariants
- Domain: root-cause analysis, minimal fixes.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/debug-<role>` or open `core/skills/debug/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /debug-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/debug-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/debug-audit`, `/debug-forge`, `/debug-scout`, `/debug-seal`, `/debug-smith`, `/debug-trace`

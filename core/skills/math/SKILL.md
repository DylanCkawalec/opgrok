---
name: cat-math
description: >
  Routes work to the correct SuperGrok role inside the math domain (algorithms, numerics, formal reasoning).
  Activates when selecting a math specialist, browsing math agents, or invoking /cat-math.
  Differentiator: category index only — does not perform math implementation work.
argument-hint: "<role or goal within math>"
user-invocable: true
metadata:
  short-description: "Navigate math SuperGroks (6 roles)"
  category: math
  tier: core
  sg_id: sg-nav-math
  binary_id: opgrok.sg.cat-math
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct math SuperGrok role."
  purpose: "Index 6 math specialists for algorithms, numerics, formal reasoning."
  intent_tags: [math, navigator, route, index]
  path: core/skills/math/SKILL.md
  call: /cat-math
---

# Math SuperGrok Navigator (`/cat-math`)

**Agent Identity**: Carmelo-c8f6228600e5f744db02cd5fe3742cbb3f7abc643cfb7bffdc9aadfee81a1037

## Core Mandate / Invariants
- Domain: algorithms, numerics, formal reasoning.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/math-<role>` or open `core/skills/math/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /math-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/math-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/math-audit`, `/math-forge`, `/math-scout`, `/math-seal`, `/math-smith`, `/math-trace`

---
name: cat-python
description: >
  Routes work to the correct SuperGrok role inside the python domain (Python packages, typing, async).
  Activates when selecting a python specialist, browsing python agents, or invoking /cat-python.
  Differentiator: category index only — does not perform python implementation work.
argument-hint: "<role or goal within python>"
user-invocable: true
metadata:
  short-description: "Navigate python SuperGroks (6 roles)"
  category: python
  tier: core
  sg_id: sg-nav-python
  binary_id: opgrok.sg.cat-python
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct python SuperGrok role."
  purpose: "Index 6 python specialists for Python packages, typing, async."
  intent_tags: [python, navigator, route, index]
  path: core/skills/python/SKILL.md
  call: /cat-python
---

# Python SuperGrok Navigator (`/cat-python`)

**Agent Identity**: Draco-7a29444cc570940b31d9f7b041271a3215e98f93dcc68066428860ea18604e27

## Core Mandate / Invariants
- Domain: Python packages, typing, async.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/python-<role>` or open `core/skills/python/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /python-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/python-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/python-audit`, `/python-forge`, `/python-scout`, `/python-seal`, `/python-smith`, `/python-trace`

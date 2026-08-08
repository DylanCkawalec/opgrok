---
name: cat-code
description: >
  Routes work to the correct SuperGrok role inside the code domain (application code, modules, refactors).
  Activates when selecting a code specialist, browsing code agents, or invoking /cat-code.
  Differentiator: category index only — does not perform code implementation work.
argument-hint: "<role or goal within code>"
user-invocable: true
metadata:
  short-description: "Navigate code SuperGroks (6 roles)"
  category: code
  tier: core
  sg_id: sg-nav-code
  binary_id: opgrok.sg.cat-code
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct code SuperGrok role."
  purpose: "Index 6 code specialists for application code, modules, refactors."
  intent_tags: [code, navigator, route, index]
  path: core/skills/code/SKILL.md
  call: /cat-code
---

# Code SuperGrok Navigator (`/cat-code`)

**Agent Identity**: Almudena-19dddc82c09f03bff3b7019171826eb78110f5ddd0914f9eb8b4ad86d83c1c65

## Core Mandate / Invariants
- Domain: application code, modules, refactors.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/code-<role>` or open `core/skills/code/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /code-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/code-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/code-audit`, `/code-forge`, `/code-scout`, `/code-seal`, `/code-smith`, `/code-trace`

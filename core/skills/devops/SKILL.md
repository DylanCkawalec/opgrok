---
name: cat-devops
description: >
  Routes work to the correct SuperGrok role inside the devops domain (CI/CD, containers, deploy).
  Activates when selecting a devops specialist, browsing devops agents, or invoking /cat-devops.
  Differentiator: category index only — does not perform devops implementation work.
argument-hint: "<role or goal within devops>"
user-invocable: true
metadata:
  short-description: "Navigate devops SuperGroks (6 roles)"
  category: devops
  tier: core
  sg_id: sg-nav-devops
  binary_id: opgrok.sg.cat-devops
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct devops SuperGrok role."
  purpose: "Index 6 devops specialists for CI/CD, containers, deploy."
  intent_tags: [devops, navigator, route, index]
  path: core/skills/devops/SKILL.md
  call: /cat-devops
---

# Devops SuperGrok Navigator (`/cat-devops`)

**Agent Identity**: Aurelio-d2f5e85041dfac53756b633679b54f593215e096754af15b0533b9b9a5482b17

## Core Mandate / Invariants
- Domain: CI/CD, containers, deploy.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/devops-<role>` or open `core/skills/devops/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /devops-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/devops-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/devops-audit`, `/devops-forge`, `/devops-scout`, `/devops-seal`, `/devops-smith`, `/devops-trace`

---
name: cat-docs
description: >
  Routes work to the correct SuperGrok role inside the docs domain (README, API docs, runbooks).
  Activates when selecting a docs specialist, browsing docs agents, or invoking /cat-docs.
  Differentiator: category index only — does not perform docs implementation work.
argument-hint: "<role or goal within docs>"
user-invocable: true
metadata:
  short-description: "Navigate docs SuperGroks (6 roles)"
  category: docs
  tier: core
  sg_id: sg-nav-docs
  binary_id: opgrok.sg.cat-docs
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct docs SuperGrok role."
  purpose: "Index 6 docs specialists for README, API docs, runbooks."
  intent_tags: [docs, navigator, route, index]
  path: core/skills/docs/SKILL.md
  call: /cat-docs
---

# Docs SuperGrok Navigator (`/cat-docs`)

**Agent Identity**: Bahar-0ea8d09e70842686cb22c290584771a80f24669d427969063f69d396f1a1de80

## Core Mandate / Invariants
- Domain: README, API docs, runbooks.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/docs-<role>` or open `core/skills/docs/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /docs-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/docs-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/docs-audit`, `/docs-forge`, `/docs-scout`, `/docs-seal`, `/docs-smith`, `/docs-trace`

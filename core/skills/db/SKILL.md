---
name: cat-db
description: >
  Routes work to the correct SuperGrok role inside the db domain (SQL, migrations, query performance).
  Activates when selecting a db specialist, browsing db agents, or invoking /cat-db.
  Differentiator: category index only — does not perform db implementation work.
argument-hint: "<role or goal within db>"
user-invocable: true
metadata:
  short-description: "Navigate db SuperGroks (6 roles)"
  category: db
  tier: core
  sg_id: sg-nav-db
  binary_id: opgrok.sg.cat-db
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct db SuperGrok role."
  purpose: "Index 6 db specialists for SQL, migrations, query performance."
  intent_tags: [db, navigator, route, index]
  path: core/skills/db/SKILL.md
  call: /cat-db
---

# Db SuperGrok Navigator (`/cat-db`)

**Agent Identity**: Arista-724739308f74e9df878acfde6b4a1341a41f02ace7f3c1763b15063d1488a67c

## Core Mandate / Invariants
- Domain: SQL, migrations, query performance.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/db-<role>` or open `core/skills/db/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /db-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/db-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/db-audit`, `/db-forge`, `/db-scout`, `/db-seal`, `/db-smith`, `/db-trace`

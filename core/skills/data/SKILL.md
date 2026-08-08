---
name: cat-data
description: >
  Routes work to the correct SuperGrok role inside the data domain (pipelines, ETL, schemas).
  Activates when selecting a data specialist, browsing data agents, or invoking /cat-data.
  Differentiator: category index only — does not perform data implementation work.
argument-hint: "<role or goal within data>"
user-invocable: true
metadata:
  short-description: "Navigate data SuperGroks (6 roles)"
  category: data
  tier: core
  sg_id: sg-nav-data
  binary_id: opgrok.sg.cat-data
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct data SuperGrok role."
  purpose: "Index 6 data specialists for pipelines, ETL, schemas."
  intent_tags: [data, navigator, route, index]
  path: core/skills/data/SKILL.md
  call: /cat-data
---

# Data SuperGrok Navigator (`/cat-data`)

**Agent Identity**: Antonia-10516b2f7727574c1254d30c9215976321b238e1c0605ba995fede76b4b2269a

## Core Mandate / Invariants
- Domain: pipelines, ETL, schemas.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/data-<role>` or open `core/skills/data/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /data-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/data-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/data-audit`, `/data-forge`, `/data-scout`, `/data-seal`, `/data-smith`, `/data-trace`

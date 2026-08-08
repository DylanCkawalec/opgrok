---
name: cat-meta
description: >
  Routes work to the correct SuperGrok role inside the meta domain (skill authoring, registry, asset systems).
  Activates when selecting a meta specialist, browsing meta agents, or invoking /cat-meta.
  Differentiator: category index only — does not perform meta implementation work.
argument-hint: "<role or goal within meta>"
user-invocable: true
metadata:
  short-description: "Navigate meta SuperGroks (6 roles)"
  category: meta
  tier: core
  sg_id: sg-nav-meta
  binary_id: opgrok.sg.cat-meta
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct meta SuperGrok role."
  purpose: "Index 6 meta specialists for skill authoring, registry, asset systems."
  intent_tags: [meta, navigator, route, index]
  path: core/skills/meta/SKILL.md
  call: /cat-meta
---

# Meta SuperGrok Navigator (`/cat-meta`)

**Agent Identity**: Cheryl-9e6e2768b447a1401155b7de97b3333a65d606de095269b23e978ba4ecb3ff41

## Core Mandate / Invariants
- Domain: skill authoring, registry, asset systems.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/meta-<role>` or open `core/skills/meta/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /meta-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/meta-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/meta-audit`, `/meta-forge`, `/meta-scout`, `/meta-seal`, `/meta-smith`, `/meta-trace`

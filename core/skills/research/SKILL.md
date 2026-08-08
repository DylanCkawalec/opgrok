---
name: cat-research
description: >
  Routes work to the correct SuperGrok role inside the research domain (multi-source grounded research).
  Activates when selecting a research specialist, browsing research agents, or invoking /cat-research.
  Differentiator: category index only — does not perform research implementation work.
argument-hint: "<role or goal within research>"
user-invocable: true
metadata:
  short-description: "Navigate research SuperGroks (6 roles)"
  category: research
  tier: core
  sg_id: sg-nav-research
  binary_id: opgrok.sg.cat-research
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct research SuperGrok role."
  purpose: "Index 6 research specialists for multi-source grounded research."
  intent_tags: [research, navigator, route, index]
  path: core/skills/research/SKILL.md
  call: /cat-research
---

# Research SuperGrok Navigator (`/cat-research`)

**Agent Identity**: Edina-93a4d031b9b13e7654dc1dc422fe1db1030eb98402d4d22a8430dc8d84758cb7

## Core Mandate / Invariants
- Domain: multi-source grounded research.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/research-<role>` or open `core/skills/research/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /research-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/research-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/research-audit`, `/research-forge`, `/research-scout`, `/research-seal`, `/research-smith`, `/research-trace`

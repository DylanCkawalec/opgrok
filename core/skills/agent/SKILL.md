---
name: cat-agent
description: >
  Routes work to the correct SuperGrok role inside the agent domain (multi-agent routing and mesh).
  Activates when selecting a agent specialist, browsing agent agents, or invoking /cat-agent.
  Differentiator: category index only — does not perform agent implementation work.
argument-hint: "<role or goal within agent>"
user-invocable: true
metadata:
  short-description: "Navigate agent SuperGroks (6 roles)"
  category: agent
  tier: core
  sg_id: sg-nav-agent
  binary_id: opgrok.sg.cat-agent
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct agent SuperGrok role."
  purpose: "Index 6 agent specialists for multi-agent routing and mesh."
  intent_tags: [agent, navigator, route, index]
  path: core/skills/agent/SKILL.md
  call: /cat-agent
---

# Agent SuperGrok Navigator (`/cat-agent`)

**Agent Identity**: Aaliyah-1cee01187ff4924654ad4a994caecdf7fbcae3e8c4f3ab789b269741a4c9372e

## Core Mandate / Invariants
- Domain: multi-agent routing and mesh.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/agent-<role>` or open `core/skills/agent/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /agent-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/agent-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/agent-audit`, `/agent-forge`, `/agent-scout`, `/agent-seal`, `/agent-smith`, `/agent-trace`

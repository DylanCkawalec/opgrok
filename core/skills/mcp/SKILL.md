---
name: cat-mcp
description: >
  Routes work to the correct SuperGrok role inside the mcp domain (MCP servers, schemas, discovery).
  Activates when selecting a mcp specialist, browsing mcp agents, or invoking /cat-mcp.
  Differentiator: category index only — does not perform mcp implementation work.
argument-hint: "<role or goal within mcp>"
user-invocable: true
metadata:
  short-description: "Navigate mcp SuperGroks (6 roles)"
  category: mcp
  tier: core
  sg_id: sg-nav-mcp
  binary_id: opgrok.sg.cat-mcp
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct mcp SuperGrok role."
  purpose: "Index 6 mcp specialists for MCP servers, schemas, discovery."
  intent_tags: [mcp, navigator, route, index]
  path: core/skills/mcp/SKILL.md
  call: /cat-mcp
---

# Mcp SuperGrok Navigator (`/cat-mcp`)

**Agent Identity**: Celeste-7f6f2b9f219218b2844c80c895daa86522e13c35ef7bb261f8e503d017fff0e1

## Core Mandate / Invariants
- Domain: MCP servers, schemas, discovery.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/mcp-<role>` or open `core/skills/mcp/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /mcp-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/mcp-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/mcp-audit`, `/mcp-forge`, `/mcp-scout`, `/mcp-seal`, `/mcp-smith`, `/mcp-trace`

---
name: cat-vision
description: >
  Routes work to the correct SuperGrok role inside the vision domain (image/UI multimodal understanding).
  Activates when selecting a vision specialist, browsing vision agents, or invoking /cat-vision.
  Differentiator: category index only — does not perform vision implementation work.
argument-hint: "<role or goal within vision>"
user-invocable: true
metadata:
  short-description: "Navigate vision SuperGroks (6 roles)"
  category: vision
  tier: core
  sg_id: sg-nav-vision
  binary_id: opgrok.sg.cat-vision
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct vision SuperGrok role."
  purpose: "Index 6 vision specialists for image/UI multimodal understanding."
  intent_tags: [vision, navigator, route, index]
  path: core/skills/vision/SKILL.md
  call: /cat-vision
---

# Vision SuperGrok Navigator (`/cat-vision`)

**Agent Identity**: Hannah-8bcb2bacac34d05d1e42659d0f637a33745e6b996eb6d5b54223e89ad32f2b8c

## Core Mandate / Invariants
- Domain: image/UI multimodal understanding.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/vision-<role>` or open `core/skills/vision/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /vision-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/vision-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/vision-audit`, `/vision-forge`, `/vision-scout`, `/vision-seal`, `/vision-smith`, `/vision-trace`

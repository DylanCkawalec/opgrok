---
name: cat-binary
description: >
  Routes work to the correct SuperGrok role inside the binary domain (native binaries, packaging, FFI).
  Activates when selecting a binary specialist, browsing binary agents, or invoking /cat-binary.
  Differentiator: category index only — does not perform binary implementation work.
argument-hint: "<role or goal within binary>"
user-invocable: true
metadata:
  short-description: "Navigate binary SuperGroks (6 roles)"
  category: binary
  tier: core
  sg_id: sg-nav-binary
  binary_id: opgrok.sg.cat-binary
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct binary SuperGrok role."
  purpose: "Index 6 binary specialists for native binaries, packaging, FFI."
  intent_tags: [binary, navigator, route, index]
  path: core/skills/binary/SKILL.md
  call: /cat-binary
---

# Binary SuperGrok Navigator (`/cat-binary`)

**Agent Identity**: Aileen-48a918231603b068d9ff1783d675b4fdcfe03c0913d921714026628cde51f8a7

## Core Mandate / Invariants
- Domain: native binaries, packaging, FFI.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/binary-<role>` or open `core/skills/binary/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /binary-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/binary-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/binary-audit`, `/binary-forge`, `/binary-scout`, `/binary-seal`, `/binary-smith`, `/binary-trace`

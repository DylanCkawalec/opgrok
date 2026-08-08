---
name: cat-security
description: >
  Routes work to the correct SuperGrok role inside the security domain (threat models, defensive audits).
  Activates when selecting a security specialist, browsing security agents, or invoking /cat-security.
  Differentiator: category index only — does not perform security implementation work.
argument-hint: "<role or goal within security>"
user-invocable: true
metadata:
  short-description: "Navigate security SuperGroks (6 roles)"
  category: security
  tier: core
  sg_id: sg-nav-security
  binary_id: opgrok.sg.cat-security
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct security SuperGrok role."
  purpose: "Index 6 security specialists for threat models, defensive audits."
  intent_tags: [security, navigator, route, index]
  path: core/skills/security/SKILL.md
  call: /cat-security
---

# Security SuperGrok Navigator (`/cat-security`)

**Agent Identity**: Faisal-1255038b1c0d114fda8a063d4ed50c9ba708d8d701e77359b7f2564da4ed18d9

## Core Mandate / Invariants
- Domain: threat models, defensive audits.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/security-<role>` or open `core/skills/security/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /security-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/security-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/security-audit`, `/security-forge`, `/security-scout`, `/security-seal`, `/security-smith`, `/security-trace`

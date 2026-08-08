---
name: cat-plan
description: >
  Routes work to the correct SuperGrok role inside the plan domain (design docs, ADRs, PR plans).
  Activates when selecting a plan specialist, browsing plan agents, or invoking /cat-plan.
  Differentiator: category index only — does not perform plan implementation work.
argument-hint: "<role or goal within plan>"
user-invocable: true
metadata:
  short-description: "Navigate plan SuperGroks (6 roles)"
  category: plan
  tier: core
  sg_id: sg-nav-plan
  binary_id: opgrok.sg.cat-plan
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct plan SuperGrok role."
  purpose: "Index 6 plan specialists for design docs, ADRs, PR plans."
  intent_tags: [plan, navigator, route, index]
  path: core/skills/plan/SKILL.md
  call: /cat-plan
---

# Plan SuperGrok Navigator (`/cat-plan`)

**Agent Identity**: Damien-ebefbc92c3c752964182e6f9774c181998030a44a6d490026fde611dc64fcf1e

## Core Mandate / Invariants
- Domain: design docs, ADRs, PR plans.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/plan-<role>` or open `core/skills/plan/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /plan-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/plan-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/plan-audit`, `/plan-forge`, `/plan-scout`, `/plan-seal`, `/plan-smith`, `/plan-trace`

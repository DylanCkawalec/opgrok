---
name: cat-eval
description: >
  Routes work to the correct SuperGrok role inside the eval domain (rubrics, judges, harnesses).
  Activates when selecting a eval specialist, browsing eval agents, or invoking /cat-eval.
  Differentiator: category index only — does not perform eval implementation work.
argument-hint: "<role or goal within eval>"
user-invocable: true
metadata:
  short-description: "Navigate eval SuperGroks (6 roles)"
  category: eval
  tier: core
  sg_id: sg-nav-eval
  binary_id: opgrok.sg.cat-eval
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct eval SuperGrok role."
  purpose: "Index 6 eval specialists for rubrics, judges, harnesses."
  intent_tags: [eval, navigator, route, index]
  path: core/skills/eval/SKILL.md
  call: /cat-eval
---

# Eval SuperGrok Navigator (`/cat-eval`)

**Agent Identity**: Benedict-086cc36e0cdb08c767912c8b424c44f16cb43eaff785d485c45ae27bef49cb68

## Core Mandate / Invariants
- Domain: rubrics, judges, harnesses.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/eval-<role>` or open `core/skills/eval/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /eval-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/eval-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/eval-audit`, `/eval-forge`, `/eval-scout`, `/eval-seal`, `/eval-smith`, `/eval-trace`

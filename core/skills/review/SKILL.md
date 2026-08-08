---
name: cat-review
description: >
  Routes work to the correct SuperGrok role inside the review domain (code and design review).
  Activates when selecting a review specialist, browsing review agents, or invoking /cat-review.
  Differentiator: category index only — does not perform review implementation work.
argument-hint: "<role or goal within review>"
user-invocable: true
metadata:
  short-description: "Navigate review SuperGroks (6 roles)"
  category: review
  tier: core
  sg_id: sg-nav-review
  binary_id: opgrok.sg.cat-review
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct review SuperGrok role."
  purpose: "Index 6 review specialists for code and design review."
  intent_tags: [review, navigator, route, index]
  path: core/skills/review/SKILL.md
  call: /cat-review
---

# Review SuperGrok Navigator (`/cat-review`)

**Agent Identity**: Eliana-f1a026be79240e61b15b88437bbcd937eb59ab7c39821a8f637e11bc33720f92

## Core Mandate / Invariants
- Domain: code and design review.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/review-<role>` or open `core/skills/review/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /review-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/review-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/review-audit`, `/review-forge`, `/review-scout`, `/review-seal`, `/review-smith`, `/review-trace`

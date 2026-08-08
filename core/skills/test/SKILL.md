---
name: cat-test
description: >
  Routes work to the correct SuperGrok role inside the test domain (unit/integration/e2e tests).
  Activates when selecting a test specialist, browsing test agents, or invoking /cat-test.
  Differentiator: category index only — does not perform test implementation work.
argument-hint: "<role or goal within test>"
user-invocable: true
metadata:
  short-description: "Navigate test SuperGroks (6 roles)"
  category: test
  tier: core
  sg_id: sg-nav-test
  binary_id: opgrok.sg.cat-test
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct test SuperGrok role."
  purpose: "Index 6 test specialists for unit/integration/e2e tests."
  intent_tags: [test, navigator, route, index]
  path: core/skills/test/SKILL.md
  call: /cat-test
---

# Test SuperGrok Navigator (`/cat-test`)

**Agent Identity**: Galit-b5fc2c7d534d5d670df350ab95276ca86dbbaca7229ceebd9d8f432e97c5f354

## Core Mandate / Invariants
- Domain: unit/integration/e2e tests.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/test-<role>` or open `core/skills/test/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /test-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/test-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/test-audit`, `/test-forge`, `/test-scout`, `/test-seal`, `/test-smith`, `/test-trace`

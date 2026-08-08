---
name: cat-product
description: >
  Routes work to the correct SuperGrok role inside the product domain (specs, prioritization, requirements).
  Activates when selecting a product specialist, browsing product agents, or invoking /cat-product.
  Differentiator: category index only — does not perform product implementation work.
argument-hint: "<role or goal within product>"
user-invocable: true
metadata:
  short-description: "Navigate product SuperGroks (6 roles)"
  category: product
  tier: core
  sg_id: sg-nav-product
  binary_id: opgrok.sg.cat-product
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct product SuperGrok role."
  purpose: "Index 6 product specialists for specs, prioritization, requirements."
  intent_tags: [product, navigator, route, index]
  path: core/skills/product/SKILL.md
  call: /cat-product
---

# Product SuperGrok Navigator (`/cat-product`)

**Agent Identity**: Dennis-9ee80812d9e060ed12cf8ad16f2b622e46a95805e95bacbf2155e9f5f9e32e83

## Core Mandate / Invariants
- Domain: specs, prioritization, requirements.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/product-<role>` or open `core/skills/product/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /product-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/product-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/product-audit`, `/product-forge`, `/product-scout`, `/product-seal`, `/product-smith`, `/product-trace`

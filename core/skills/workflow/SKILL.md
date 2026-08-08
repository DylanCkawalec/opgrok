---
name: cat-workflow
description: >
  Routes work to the correct SuperGrok role inside the workflow domain (n8n/DAG/pipeline automation).
  Activates when selecting a workflow specialist, browsing workflow agents, or invoking /cat-workflow.
  Differentiator: category index only — does not perform workflow implementation work.
argument-hint: "<role or goal within workflow>"
user-invocable: true
metadata:
  short-description: "Navigate workflow SuperGroks (6 roles)"
  category: workflow
  tier: core
  sg_id: sg-nav-workflow
  binary_id: opgrok.sg.cat-workflow
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct workflow SuperGrok role."
  purpose: "Index 6 workflow specialists for n8n/DAG/pipeline automation."
  intent_tags: [workflow, navigator, route, index]
  path: core/skills/workflow/SKILL.md
  call: /cat-workflow
---

# Workflow SuperGrok Navigator (`/cat-workflow`)

**Agent Identity**: Herbert-de1945dd95fc7cdf02227c62fd773420a6bfc798cbee301aa168e3ce3c80a896

## Core Mandate / Invariants
- Domain: n8n/DAG/pipeline automation.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/workflow-<role>` or open `core/skills/workflow/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /workflow-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/workflow-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/workflow-audit`, `/workflow-forge`, `/workflow-scout`, `/workflow-seal`, `/workflow-smith`, `/workflow-trace`

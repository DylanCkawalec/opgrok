---
name: cat-rust
description: >
  Routes work to the correct SuperGrok role inside the rust domain (Rust crates, ownership, cargo).
  Activates when selecting a rust specialist, browsing rust agents, or invoking /cat-rust.
  Differentiator: category index only — does not perform rust implementation work.
argument-hint: "<role or goal within rust>"
user-invocable: true
metadata:
  short-description: "Navigate rust SuperGroks (6 roles)"
  category: rust
  tier: core
  sg_id: sg-nav-rust
  binary_id: opgrok.sg.cat-rust
  version: "2.0.0"
  leslie_gate: v1
  kind: navigator
  intent: "Route work to the correct rust SuperGrok role."
  purpose: "Index 6 rust specialists for Rust crates, ownership, cargo."
  intent_tags: [rust, navigator, route, index]
  path: core/skills/rust/SKILL.md
  call: /cat-rust
---

# Rust SuperGrok Navigator (`/cat-rust`)

**Agent Identity**: Elsie-03025d6e590d8994b30049efc339057275c063b82cd47a13ee49802bbcf0d420

## Core Mandate / Invariants
- Domain: Rust crates, ownership, cargo.
- This skill selects a specialist; it does not implement the domain work.
- Prefer a single primary SuperGrok; secondary agents only for mesh handoff via `/opgrok`.

## Procedural Workflow
1. Parse the goal into a role method (build, review, map, harden, document, integrate, …).
2. Map method → role among: audit, forge, scout, seal, smith, trace.
3. Invoke `/rust-<role>` or open `core/skills/rust/<role>/SKILL.md`.
4. If multi-agent composition is required, escalate to `/opgrok`.
5. Emit: `SELECTED: /rust-<role>` with a one-line justification.

## Constraints & Gotchas
- Do not perform heavy implementation under this navigator.
- Do not invent roles outside the catalog.
- Ambiguous goals: choose the highest-risk path role (anvil/crux) or scout first.

## Definition of Done
- One primary call path named (`/rust-<role>`).
- Intent/purpose of that skill fits the goal.
- Optional secondaries listed only if mesh is required.

## Optional Tool Surface
- Registry: `core/skills/_framework/REGISTRY.json`
- MCP catalog: `core/skills/_framework/MCP_CATALOG.json`

## References
- `core/skills/_framework/NAVIGATION.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- Roles: `/rust-audit`, `/rust-forge`, `/rust-scout`, `/rust-seal`, `/rust-smith`, `/rust-trace`

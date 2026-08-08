---
name: agent-audit
description: >
  Audits multi-agent SuperGrok meshes against an explicit hire/graph/WC checklist,
  scoring PASS/FAIL with path evidence and Name-Hash peer resolution. Use when
  composing harnesses, thrifting context packs, validating I/O contracts, sealing
  Leslie WC, or invoking /agent-audit. Differentiator: checklist gate that rejects
  bulk body dumps and unbounded spawns before any live mesh run.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Agent orchestration · checklist"
  category: agent
  tier: frontier
  sg_id: sg-0101
  binary_id: opgrok.sg.agent-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "agent/audit (checklist): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run."
  purpose: "Plan and run multi-agent SuperGrok compositions. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift."
  intent_tags: [agent, audit, frontier, checklist]
  path: core/skills/agent/audit/SKILL.md
  call: /agent-audit
---

# /agent-audit — Agent Mesh Checklist Auditor

**Agent Identity**: Abbas-5b4f91486f937d65db48f71b19b56edb3032491a00d618d7a9570eb063a7e0fd

## Core Mandate / Invariants
- Domain: **Agent orchestration** — multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- Method: **checklist** — declare items, score PASS/FAIL with path:line or command evidence, rank failures.
- Resolve peers by Name-Hash / token / path only; never embed full skill bodies.
- Hire thrift: ≤12 specialists; each node has explicit IPO + win criteria.
- Leslie WC must be present or planned before harness is treated complete.
- Evidence over assertion; dry-run before live spawn.
- Stay in domain; escalate mesh-wide orchestration to `leslie` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Parse goal → role set, dependency edges, I/O contracts.
2. Resolve SuperGrok tokens via `core/registry/named-hashes.json` + `core/skills/_framework/REGISTRY.json`; prefer identity tokens over paths.
3. Draft mesh / harness; mark dry-run vs live; note context budget.

### Role method (audit)
1. Declare checklist scoped to this mesh (hire thrift, graph I/O, WC, identity tokens, dry-run path, context cost).
2. Run `python3 core/tools/craft_harness.py` (or inspect existing harness artifact) and verify node list ≤12 with IPO fields populated.
3. Execute `python3 core/tools/run_harness.py --dry-run` when a runnable plan exists; treat silence as dry-run success, not API failure.
4. Score every checklist item PASS/FAIL with evidence (`path:line`, registry key, or command output). Rank FAILs; patch only in-scope defensive fixes.
5. Confirm Leslie WC block exists or is explicitly scheduled before any live spawn.

### Domain checklist
- [ ] Hire list thrifty (≤12)
- [ ] Graph edges + I/O contracts explicit
- [ ] WC present or planned
- [ ] Identity tokens preferred over body dumps
- [ ] Dry-run path known / exercised
- [ ] Context pack excludes full skill bodies

### Eval dimensions
- Hire thrift
- Graph clarity
- WC readiness
- Context cost

### Close
1. Verify: every FAIL has path:line or command evidence. Fix once in scope or escalate to `leslie`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0101 agent-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Unbounded hires explode context and cost; hard-cap ≤12.
- Missing Leslie WC leaves harness unsealed — never mark complete without it.
- Loading full skill bodies instead of Name-Hash tokens wastes the context budget.
- Graphs without I/O contracts deadlock or thrash under spawn.
- Dry-run silence ≠ API failure; only non-zero exit or explicit error is FAIL.
- Identity drift: registry token mismatch vs on-disk skill → re-resolve before hire.
- Do not use outside **Agent orchestration** (route via `/cat-agent` or `/opgrok`).
### Anti-patterns
- Spawning unbounded agents / agent spam
- Skipping Winning Condition
- Embedding all skill bodies in one prompt
- Treating dry-run quiet as broken tooling
- Hiring by free-text name without Name-Hash lookup
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Checklist fully scored; every FAIL has concrete evidence.
- Hire list ≤12, graph I/O clear, WC present/planned, tokens not bodies.
- `WIN: PASS` with evidence paths/commands; downstream SuperGroks can consume without clarification.
- On residual FAIL: one fix attempt or explicit escalate — no silent ship.

## Optional Tool Surface
- `python3 core/tools/craft_harness.py`
- `python3 core/tools/run_harness.py --dry-run`
- `core/registry/named-hashes.json` + IdentityIndex
- `core/skills/_framework/REGISTRY.json`
- Agent runtime: `spawn_subagent`, `read_file`, `todo_write`
- Binary id: `opgrok.sg.agent-audit`

## References
- `core/skills/agent/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

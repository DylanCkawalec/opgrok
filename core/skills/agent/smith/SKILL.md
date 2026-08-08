---
name: agent-smith
description: >
  Builds the smallest SuperGrok mesh unit that satisfies a multi-agent brief: role graph,
  Name-Hash hires, IPO contracts, and thrift context packs. Use when composing harnesses,
  routing goals to category roles, packing mesh context, sealing a WC gate, or invoking
  /agent-smith. Differentiator: resolves peers by Name-Hash and Leslie WC — never bulk
  skill-body dumps.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Agent orchestration · build unit"
  category: agent
  tier: core
  sg_id: sg-0097
  binary_id: opgrok.sg.agent-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "agent/smith (build unit): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run."
  purpose: "Plan and run multi-agent SuperGrok compositions. Method (build unit): build the smallest correct unit that meets the brief. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift."
  intent_tags: [agent, smith, core, build-unit]
  path: core/skills/agent/smith/SKILL.md
  call: /agent-smith
---

# /agent-smith — Agent Mesh Unit Builder

**Agent Identity**: Agata-d13fac51e4b987682edd33a899691622f51ce55d44c71572e31bfa477b70eee3

## Core Mandate / Invariants
- Domain: **Agent orchestration** — multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- Method (**build unit**): ship the smallest correct node/harness that meets the brief — nothing more.
- Resolve peers by **Name-Hash / token / path** only; never embed full skill bodies.
- Every node carries explicit IPO (inputs → process → outputs) and a measurable win criterion.
- Hire the fewest specialists that cover the dependency cut; thrift context packs.
- Leslie WC gate seals the harness before it is treated complete.
- Evidence over assertion: registry hits, dry-run logs, or artifact paths only.

## Procedural Workflow
### Domain procedure
1. Parse brief into goal, roles, and hard dependencies; drop nice-to-haves.
2. Query `core/skills/_framework/REGISTRY.json` + `core/registry/named-hashes.json` for candidate SuperGrok tokens; reject unregistered names.
3. Sketch directed graph (order, fan-in/out); mark dry-run vs live edges.
4. Emit mesh plan or invoke `core/tools/craft_harness.py` with the contracted node set.

### Role method (smith)
1. Define **one** node contract: IPO fields + win criterion + max context budget.
2. Resolve exactly one SuperGrok via Name-Hash (`IdentityIndex` / `named-hashes.json`); record `sg_id` + path.
3. Run `core/tools/run_harness.py --dry-run` on the unit; confirm I/O wiring and no silent no-op.
4. If dry-run fails contract, fix the single node once; else escalate to `leslie` — do not widen the hire set.

### Close
1. Verify: mesh plan lists agents, topological order, and I/O contracts; WC present.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0097 agent-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Over-hiring SuperGroks explodes context window and token cost; default to 1–3 nodes for a smith unit.
- Missing Leslie WC leaves harnesses unsealed and non-composable downstream.
- Loading full skill bodies instead of tokens/paths wastes the thrift budget.
- Graphs without I/O contracts deadlock, thrash, or silently drop outputs.
- Dry-run silence ≠ API failure — inspect harness log before retry/live.
- Name collisions across categories: always pin `sg_id` + path, not display name alone.
- Do not use for work outside **Agent orchestration** (route via `/cat-agent` or `/opgrok`).
### Anti-patterns
- Spawning unbounded or speculative agents “just in case”
- Skipping the Winning Condition / Leslie WC gate
- Embedding dozens of skill bodies in one prompt
- Treating dry-run no-output as success without contract check
- Widening the mesh on first failure instead of fixing the unit
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Unit matches the brief under **smith** (smallest correct mesh fragment).
- Plan enumerates agents, order, IPO contracts, and WC; registry tokens resolve.
- `run_harness.py --dry-run` (or equivalent evidence) supports the contracts.
- `WIN: PASS` with concrete paths/commands; downstream SuperGroks consume outputs with zero clarification.

## Optional Tool Surface
- `core/tools/craft_harness.py`
- `core/tools/run_harness.py --dry-run`
- `core/registry/named-hashes.json` + IdentityIndex
- `core/skills/_framework/REGISTRY.json`
- Agent runtime: `spawn_subagent`, `read_file`, `todo_write`
- Binary id: `opgrok.sg.agent-smith`

## References
- `core/skills/agent/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

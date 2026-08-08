---
name: agent-seal
description: >
  Finalizes multi-agent SuperGrok meshes: verifies Leslie WC, freezes harness
  artifacts, resolves peers by Name-Hash, and marks handoff-ready. Use when
  sealing a composed harness, closing a mesh run, checking win-gate evidence,
  thrifting context packs before handoff, or invoking /agent-seal.
  Differentiator: Name-Hash peer freeze plus Leslie WC gate — not live re-hire.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Agent orchestration · finalize"
  category: agent
  tier: frontier
  sg_id: sg-0102
  binary_id: opgrok.sg.agent-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "agent/seal (finalize): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run."
  purpose: "Plan and run multi-agent SuperGrok compositions. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift."
  intent_tags: [agent, seal, frontier, finalize]
  path: core/skills/agent/seal/SKILL.md
  call: /agent-seal
---

# /agent-seal — Agent Mesh Finalizer

**Agent Identity**: Afua-afa8a6dc73944430881fae71659e53c1fbb907567ff104c5ad3a3c91a79ede22

## Core Mandate / Invariants
- Domain: **Agent orchestration** — mesh plans, SuperGrok composition, routing, context thrift.
- Method (**finalize**): verify win gate → freeze outputs → mark handoff-ready.
- Evidence over assertion: every claim needs tool output, harness path, or registry proof.
- Hire thrift: few specialists; tokens/paths only — never bulk skill bodies.
- Each node carries explicit IPO + falsifiable WC before seal.
- Leslie WC must pass before harness is treated complete.
- Resolve peers via Name-Hash (`named-hashes.json` / IdentityIndex), not re-spawn.

## Procedural Workflow
### Domain procedure
1. Read brief/artifact; confirm mesh graph (agents, order, I/O contracts) is closed.
2. Resolve SuperGrok peers by token/path from `core/registry/named-hashes.json` and `core/skills/_framework/REGISTRY.json` — no full-body loads.
3. Run `python3 core/tools/run_harness.py --dry-run` on the package; treat silence as dry-run success, not API failure.
4. Diff live vs frozen paths; reject any node still hiring or missing WC.

### Role method (seal)
1. Freeze harness package paths; lock agent order and I/O contracts in the plan artifact.
2. Verify Leslie WC is falsifiable and attached (criteria + evidence pointers).
3. Confirm Name-Hash identities match registry; drop any unresolved or duplicate hire.
4. Emit seal record only when dry-run (or live evidence) supports the WC.

### Eval dimensions
- Hire thrift (node count vs goal)
- Graph clarity (order + I/O)
- WC readiness (falsifiable + evidenced)
- Context cost (tokens/paths only)

### Close
1. Verify: WC evidence attached; mesh plan lists agents, order, I/O contracts. On failure, fix once or escalate to `leslie`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0102 agent-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Over-hire explodes context and cost; seal must refuse unbounded graphs.
- Missing Leslie WC → harness stays unsealed; do not hand off.
- Loading full skill bodies instead of tokens wastes the thrift budget.
- Graphs without I/O contracts deadlock or thrash under spawn.
- Dry-run silence ≠ API failure; check exit code and package paths.
- Re-hiring at seal time invalidates freeze; resolve by Name-Hash only.
- Do not use outside **Agent orchestration** (route `/cat-agent` or `/opgrok`).
### Anti-patterns
- Spawning unbounded agents at finalize
- Skipping Winning Condition / Leslie gate
- Embedding all skill bodies in one prompt
- Re-running craft instead of freezing paths
- Treating dry-run quiet as hard failure
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches brief under **seal** for **Agent orchestration**.
- Win-gate evidence attached; mesh plan lists agents, order, I/O contracts.
- Peers frozen by Name-Hash; no pending hires.
- `WIN: PASS` with concrete evidence paths/commands (`run_harness.py --dry-run`, plan artifact).
- Downstream SuperGroks consume outputs with zero clarification.

## Optional Tool Surface
- `python3 core/tools/craft_harness.py`
- `python3 core/tools/run_harness.py --dry-run`
- `core/registry/named-hashes.json` + IdentityIndex
- `core/skills/_framework/REGISTRY.json`
- Agent tools: `spawn_subagent`, `read_file`, `todo_write`
- Binary id: `opgrok.sg.agent-seal`

## References
- `core/skills/agent/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

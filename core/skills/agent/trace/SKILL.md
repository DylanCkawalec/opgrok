---
name: agent-trace
description: >
  Traces multi-agent SuperGrok failures via RCA: symptom → evidence → root → fix across mesh plans,
  routing graphs, and thrift context packs. Use when a harness node stalls, peers thrash on missing
  I/O contracts, Name-Hash resolution fails, dry-run silence confuses live status, or the user runs
  /agent-trace. Differentiator: resolves peers by Name-Hash and Leslie WC gate, never bulk skill dumps.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Agent orchestration · RCA"
  category: agent
  tier: frontier
  sg_id: sg-0100
  binary_id: opgrok.sg.agent-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "agent/trace (RCA): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run."
  purpose: "Plan and run multi-agent SuperGrok compositions. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift."
  intent_tags: [agent, trace, frontier, RCA]
  path: core/skills/agent/trace/SKILL.md
  call: /agent-trace
---

# /agent-trace — Agent Mesh RCA Tracer

**Agent Identity**: Agustin-27533c4e39ff9d3c9a4311e5b7ea8fad2bfc1780d343ce72f73188352b9799e2

## Core Mandate / Invariants
- Domain: **Agent orchestration** — multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- Method (**RCA**): symptom → evidence → root → fix; every claim needs journal, ledger, or tool proof.
- Hire few specialists; thrift context; resolve peers by Name-Hash/token/path only — never embed full skill bodies.
- Each node declares IPO (inputs/process/outputs) and explicit win criteria before live run.
- Leslie WC gate seals the harness; unsealed graphs are incomplete.
- Stay in domain; escalate mesh-wide policy to `leslie` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Parse goal into role tokens, edges, and I/O contracts; reject unbounded fan-out.
2. Resolve SuperGrok paths via `core/registry/named-hashes.json` + `core/skills/_framework/REGISTRY.json`; build graph with thrift context packs only.
3. Emit mesh plan; prefer `python3 core/tools/craft_harness.py` then `python3 core/tools/run_harness.py --dry-run` before live.

### Role method (trace / RCA)
1. Capture **symptom** from harness journal/ledger (failed node id, exit, missing artifact).
2. Gather **evidence**: re-run `python3 core/tools/run_harness.py --dry-run` on the suspect subgraph; diff Name-Hash hits vs expected tokens; inspect IPO contract gaps.
3. Name **root**: wrong peer token, missing WC, context bloat, or silent dry-run misread as API death.
4. Apply **fix**: retarget edge or skill path, shrink hire set, restore I/O contract; single re-dry-run to confirm.
5. If causal chain still open after one fix cycle, escalate to `leslie` with evidence bundle.

### Close
1. Verify: full symptom→fix chain with before/after repro. Emit:

```text
WIN: PASS|FAIL
SG: sg-0100 agent-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Over-hire explodes context/cost; default to minimal specialist set.
- Missing Leslie WC leaves harnesses unsealed and non-consumable downstream.
- Loading full skill bodies instead of tokens thrash the context window.
- Graphs without I/O contracts deadlock or ping-pong.
- Dry-run silence ≠ API failure — check harness exit and ledger before retry storms.
- Name-Hash mismatch silently routes to the wrong peer; always verify against `named-hashes.json`.
- Do not use outside **Agent orchestration** (route via `/cat-agent` or `/opgrok`).
### Anti-patterns
- Spawning unbounded agents / agent spam
- Skipping Winning Condition or IPO contracts
- Embedding all skill bodies in one prompt
- Treating dry-run quiet as live success
- Re-tracing the whole mesh when one node’s journal already pins the root
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- RCA chain complete: symptom, evidence paths/commands, root, fix — with before/after repro.
- Mesh plan or harness delta is thrift-safe; peers resolve by Name-Hash; Leslie WC addressed or explicitly escalated.
- `WIN: PASS` with concrete evidence; downstream SuperGroks consume outputs without clarification.
- `WIN: FAIL` only with pinned root + next owner (`leslie` / specific peer).

## Optional Tool Surface
- `python3 core/tools/craft_harness.py`
- `python3 core/tools/run_harness.py --dry-run`
- `core/registry/named-hashes.json` + IdentityIndex
- `core/skills/_framework/REGISTRY.json`
- Agent tools: `spawn_subagent`, `read_file`, `todo_write`
- Binary id: `opgrok.sg.agent-trace`

## References
- `core/skills/agent/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

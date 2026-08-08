---
name: agent-scout
description: >
  Maps multi-agent SuperGrok meshes before any hire: resolves peers by Name-Hash,
  drafts thrift context packs, and gates composition on Leslie WC. Use when composing
  N-node harnesses, routing goals to category roles with I/O contracts, estimating
  mesh context cost, or invoking /agent-scout. Differentiator: registry-first map that
  cuts hires by token cost before forge, never bulk-loads skill bodies.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Agent orchestration · map"
  category: agent
  tier: frontier
  sg_id: sg-0099
  binary_id: opgrok.sg.agent-scout
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "agent/scout (map): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run."
  purpose: "Plan and run multi-agent SuperGrok compositions. Method (map): map structure and constraints before committing to edits. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift."
  intent_tags: [agent, scout, frontier, map]
  path: core/skills/agent/scout/SKILL.md
  call: /agent-scout
---

# /agent-scout — Agent orchestration Scout

**Agent Identity**: Adriana-9d5801538d19dcbb13ecef67b2ae35dcbdbed2f8f0f39cfe819a437499dcd66d

## Core Mandate / Invariants
- Domain: **Agent orchestration** — multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- Method (**map**): structure, constraints, and cost before any edit or spawn.
- Resolve peers by Name-Hash / token path only; never embed full skill bodies.
- Hire the minimum specialist set; each node needs explicit IPO + win criteria.
- Evidence over assertion: registry hits, harness dry-run output, or repo paths.
- Leslie WC seals the harness; unsealed graphs are not done.
- Escalate mesh-wide policy or cross-category conflicts to `leslie` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Parse goal → roles, deps, hard constraints (latency, budget, sealed WC).
2. Query `core/skills/_framework/REGISTRY.json` and `core/registry/named-hashes.json`; bind tokens/paths, not bodies.
3. Draft mesh graph with per-node I/O contracts; mark dry-run vs live.
4. Run `python3 core/tools/craft_harness.py` (plan) then `python3 core/tools/run_harness.py --dry-run` to validate wiring silence vs failure.

### Role method (scout)
1. Map goal phrases to category roles; list candidate SG tokens from IdentityIndex / named-hashes.
2. Estimate context cost per hire (token footprint of path + expected artifacts); drop redundant peers until thrift budget holds.
3. Emit scout map: entrypoints, constraints, ordered hire list, next recommended `/agent-forge` (or sibling) with I/O contract stubs.
4. If dry-run shows contract gaps or unresolved hashes, fix map once; else escalate.

### Close
1. Verify map completeness: entrypoints, constraints, next hire named, WC stub present.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0099 agent-scout
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Over-hire explodes context; prefer 3–6 tight nodes over sprawling meshes.
- Missing Leslie WC → harness never seals; downstream treats it as draft forever.
- Loading full SKILL.md bodies instead of tokens burns the thrift budget immediately.
- Graphs without I/O contracts deadlock, thrash, or silent-skip edges.
- `run_harness.py --dry-run` silence ≠ API failure; check exit code and plan diff.
- Stale Name-Hash after registry churn → wrong peer; re-resolve before spawn.
- Do not use outside **Agent orchestration** (route via `/cat-agent` or `/opgrok`).
### Anti-patterns
- Unbounded `spawn_subagent` fan-out
- Skipping Winning Condition / Leslie gate
- Embedding “all skills” dumps in one prompt
- Forging before scout map exists
- Treating dry-run no-op as success without contract checks
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Scout map names entrypoints, constraints, thrift hire list, and next forge target.
- Domain invariants hold; peers resolve by token/hash only.
- `WIN: PASS` with evidence: registry paths, `craft_harness.py` / `run_harness.py --dry-run` output, WC stub.
- Downstream SuperGroks consume the map without clarification.

## Optional Tool Surface
- `python3 core/tools/craft_harness.py`
- `python3 core/tools/run_harness.py --dry-run`
- `core/registry/named-hashes.json` + IdentityIndex
- `core/skills/_framework/REGISTRY.json`
- Agent tools: `spawn_subagent`, `read_file`, `todo_write`
- Binary id: `opgrok.sg.agent-scout`

## References
- `core/skills/agent/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

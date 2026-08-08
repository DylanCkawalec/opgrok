---
name: meta-trace
description: >
  Root-causes SuperGrok catalog, registry, and skill-hygiene failures via symptom→evidence→root→fix chains.
  Activates on broken validate gates, stale identities after bulk SKILL.md edits, registry drift post-category add,
  or /meta-trace. Differentiator: forces generate→rebuild→identity→validate loop with Leslie Gate as hard stop.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Meta & catalog ops · RCA"
  category: meta
  tier: frontier
  sg_id: sg-0148
  binary_id: opgrok.sg.meta-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "meta/trace (RCA): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category."
  purpose: "Maintain SuperGrok skills, registry, and program hygiene. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: skill authoring, registry, SuperGrok program hygiene, assets."
  intent_tags: [meta, trace, frontier, RCA]
  path: core/skills/meta/trace/SKILL.md
  call: /meta-trace
---

# Meta & catalog ops Tracer (`/meta-trace`)

**Agent Identity**: Clark-d1c3d6b8785089cdea2ed87d9571af131728d44e8997b94330ecd71021afe4ff

## Core Mandate / Invariants
- Domain: skill authoring, registry, catalog hygiene, SuperGrok program assets — nothing else.
- Method is RCA only: symptom → evidence → root → fix; no speculative rewrites.
- Generator/registry scripts are source of truth; hand-mass-edits are drift.
- Every catalog mutation re-runs full loop: generate → rebuild → identity → validate.
- No skill ships without unique third-person description + observable Definition of Done.
- Leslie Gate is non-optional; framework law seals defer to `leslie`.
- Evidence over assertion: every claim cites tool output or repo path.

## Procedural Workflow
### Domain procedure
1. Pin the failing surface: gate log, registry count mismatch, missing identity hash, or navigator/role desync.
2. Diff against generator outputs — never invent SKILL.md bodies by hand when `generate_supergroks.py` owns the shape.
3. Apply the smallest registry/skill/catalog fix that restores the causal chain.
4. Re-run gates; capture PASS/FAIL with command evidence.

### Role method (trace)
1. From gate failure, bisect: `python3 core/tools/validate_supergroks.py 2>&1 | tail -80` — isolate first failing assertion/script.
2. Trace root: compare `core/registry/named-hashes.json` vs on-disk SKILL.md; check category folder ↔ navigator parity.
3. Fix at source (generator input, registry entry, or single SKILL.md), not symptoms downstream.
4. Rebind: `python3 core/tools/assign_agent_identities.py` after any SKILL.md edit; never skip.
5. Close loop: `python3 core/tools/generate_supergroks.py && python3 core/tools/rebuild_skill_registry.py && python3 core/tools/validate_supergroks.py`.
6. On second failure, escalate to `leslie` with the causal chain attached — do not thrash.

### Close
1. Verify: before/after repro evidence completes the chain (failing cmd → root path → fix → green gate).
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0148 meta-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Hand-editing dozens of skills while generator is SoT → silent drift; validators lag one commit.
- Skipping `assign_agent_identities.py` after SKILL.md edits → identity seal breaks; Leslie Gate rejects.
- Legacy registry count assumptions (e.g. hardcoded 1000) false-fail validators after category adds.
- Navigators (`core/skills/<cat>/SKILL.md`) out of sync with role folders → misrouting across 20+ peers.
- `enhance_skills.py` without post-run validate + Leslie re-check ships invalid L2 bodies.
- Stale `.bak` forests from partial generator runs pollute greps and registry rebuilds.
- Description collisions across skills defeat routing; uniqueness is load-bearing.
- Do not use outside **Meta & catalog ops** — route via `/cat-meta` or `/opgrok`.
### Anti-patterns
- Manual mass search-replace across `core/skills/**/SKILL.md` bypassing generator
- Committing registry JSON without `rebuild_skill_registry.py` + validate
- Leaving orphan identity hashes after skill renames/deletes
- Treating WIN: PASS as ceremonial (must cite concrete cmds/paths)
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Causal chain complete: symptom, evidence artifact, root cause path, fix, re-gate result.
- generate → rebuild → identity → validate all green; Leslie Gate satisfied when in scope.
- `WIN: PASS` with concrete evidence (commands, paths, before/after snippets).
- Downstream SuperGroks consume catalog/registry outputs with zero clarification.

## Optional Tool Surface
- `python3 core/tools/generate_supergroks.py`
- `python3 core/tools/rebuild_skill_registry.py`
- `python3 core/tools/assign_agent_identities.py`
- `python3 core/tools/validate_supergroks.py`
- `python3 core/tools/enhance_skills.py`
- `python3 core/tools/domain_enrichment.py`
- Agent: read_file, run_terminal_command, search_replace
- Binary: `opgrok.sg.meta-trace`
- Seals: `IDENTITY.txt`, `core/registry/named-hashes.json`

## References
- `core/skills/meta/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

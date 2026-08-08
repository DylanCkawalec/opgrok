---
name: meta-seal
description: >
  Finalizes SuperGrok catalog and registry work: runs the Leslie win gate, freezes
  generator outputs, and marks artifacts handoff-ready. Use after role edits,
  category adds, bulk skill changes, or /meta-seal. Differentiator: enforce
  generate→rebuild→identity→validate as a single atomic seal; refuse WIN if any
  gate is skipped or identity hashes drift.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Meta & catalog ops · finalize"
  category: meta
  tier: frontier
  sg_id: sg-0150
  binary_id: opgrok.sg.meta-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "meta/seal (finalize): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category."
  purpose: "Maintain SuperGrok skills, registry, and program hygiene. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: skill authoring, registry, SuperGrok program hygiene, assets."
  intent_tags: [meta, seal, frontier, finalize]
  path: core/skills/meta/seal/SKILL.md
  call: /meta-seal
---

# Meta & catalog ops Sealer (`/meta-seal`)

**Agent Identity**: Clara-6413b3494b29d9fee6a584e6cb710837f6c3a800c7e4a13c1efc0c9370b22b5f

## Core Mandate / Invariants
- Domain: **Meta & catalog ops** — skill authoring, registry, SuperGrok program hygiene, assets.
- Method (**finalize**): verify Leslie win gate → freeze generator outputs → mark handoff-ready.
- Generator is source of truth; hand-edits to mass SKILL.md sets are drift until regenerate.
- Every catalog-touching change must complete: `generate_supergroks` → `rebuild_skill_registry` → `assign_agent_identities` → `validate_supergroks`.
- No skill ships without unique third-person description and observable Definition of Done.
- Evidence over assertion: PASS requires command output or repo proof paths.
- Framework WC seals defer to Leslie; escalate mesh/orchestration to `/opgrok` or `leslie`.

## Procedural Workflow
### Domain procedure
1. Scope the seal target: role folder, category add, registry row, or bulk SKILL.md delta.
2. Diff against generator inputs; prefer minimal patch to templates/enrichment tables over per-file edits.
3. If catalog shape changed, run full loop before any WIN claim.

### Role method (seal)
1. Attach green evidence from prior gates (or re-run them).
2. **Domain step:** `python3 core/tools/generate_supergroks.py` then `python3 core/tools/rebuild_skill_registry.py` — confirm registry counts match role folders (no legacy 1000 assumption).
3. **Domain step:** `python3 core/tools/assign_agent_identities.py` then `python3 core/tools/validate_supergroks.py` — require identity rehash after any SKILL.md body change; fail closed on hash drift.
4. Freeze outputs: no further skill body edits post-validate without re-loop.
5. WIN only when validate + identity verify are both green and evidence paths are listed.

### Eval dimensions
- Catalog integrity (folder ↔ registry ↔ navigator)
- Gate compliance (full loop, not partial)
- Identity integrity (`IDENTITY.txt` / `named-hashes.json`)
- Doc accuracy (descriptions route; DoD observable)

### Close
1. Verify: win-gate evidence attached; `validate_supergroks.py` and identity gate pass on catalog changes. On failure, one fix cycle or escalate to `leslie`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0150 meta-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Hand-editing dozens/hundreds of skills when generator owns content → silent drift and false green.
- Skipping `assign_agent_identities.py` after SKILL.md edits → identity gate fails downstream.
- Stale registry count assumptions (legacy 1000) break validators after category adds.
- Navigators (`core/skills/<cat>/SKILL.md`) out of sync with role folders → misrouting.
- `enhance_skills.py` without Leslie Gate re-check ships invalid frontier skills.
- `.bak` forests from partial regenerations confuse diffs; clean or ignore deliberately.
- Do not use outside **Meta & catalog ops** (route via `/cat-meta` or `/opgrok`).
### Anti-patterns
- Manual mass search-replace across `core/skills/**` bypassing generator
- Committing registry/SKILL changes without `validate_supergroks.py` green
- Claiming WIN on generate-only (missing rebuild/identity/validate)
- Rebinding identities only for touched files when bulk edit requires full rehash
- Leaving orphan categories in registry after folder deletes
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Seal brief satisfied under **finalize** for Meta & catalog ops.
- Full generate→rebuild→identity→validate loop green when catalog touched.
- `WIN: PASS` with concrete evidence (commands + paths); else `WIN: FAIL` + residual gaps.
- Downstream SuperGroks consume outputs with no clarification on routing or identity.

## Optional Tool Surface
- `python3 core/tools/generate_supergroks.py`
- `python3 core/tools/rebuild_skill_registry.py`
- `python3 core/tools/assign_agent_identities.py`
- `python3 core/tools/validate_supergroks.py`
- `python3 core/tools/enhance_skills.py`
- Agent tools: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.meta-seal`
- Identity: `IDENTITY.txt` / `core/registry/named-hashes.json`

## References
- `core/skills/meta/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

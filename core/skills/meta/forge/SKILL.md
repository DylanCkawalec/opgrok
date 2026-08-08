---
name: meta-forge
description: >
  Authors and hardens SuperGrok skills, registry, and catalog hygiene via the forge method:
  full generate→rebuild→identity→validate path before edge fixes. Activates on catalog drift,
  role/SKILL.md bulk edits, registry rebinds, or /meta-forge. Differentiator: treats Leslie Gate
  and identity rehash as mandatory seals—never optional post-edit checks.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Meta & catalog ops · e2e path"
  category: meta
  tier: advanced
  sg_id: sg-0146
  binary_id: opgrok.sg.meta-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "meta/forge (e2e path): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category."
  purpose: "Maintain SuperGrok skills, registry, and program hygiene. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: skill authoring, registry, SuperGrok program hygiene, assets."
  intent_tags: [meta, forge, advanced, e2e-path]
  path: core/skills/meta/forge/SKILL.md
  call: /meta-forge
---

# Meta & catalog ops Forger (`/meta-forge`)

**Agent Identity**: Christian-a6fb369addfc41edaf7e841d65df7c8774fd4a6e6283dce1546847c03fba991c

## Core Mandate / Invariants
- Domain: skill authoring, registry, SuperGrok program hygiene, assets—nothing outside meta catalog ops.
- Forge method: build the full e2e path (generate → rebuild → identity → validate) first; harden edges only after green gates.
- Generator and registry are source of truth; hand-edits are patches, not bulk strategy.
- Every skill ships unique third-person description + observable Definition of Done.
- Catalog/SKILL.md changes always re-run identity rehash and Leslie Gate; no seal, no ship.
- Evidence over assertion: PASS requires command output or repo proof paths.
- Escalate multi-agent mesh or cross-category work to `leslie` / `/opgrok`.

## Procedural Workflow
1. Scope the meta target: new/changed role, category add, registry drift, bulk SKILL.md edit, or navigator desync.
2. Prefer generator path over manual mass edit—touch source templates/enrichment tables, not 150 leaf files.
3. **Forge pipeline (mandatory order):**
   - `python3 core/tools/generate_supergroks.py` (or scoped equivalent) to materialize skills from source.
   - `python3 core/tools/rebuild_skill_registry.py` so counts, paths, and call map match disk.
   - `python3 core/tools/assign_agent_identities.py` to rebind hashes after any SKILL.md body change.
   - `python3 core/tools/validate_supergroks.py` — require clean exit; capture failures as evidence.
4. If enhance pass needed: `python3 core/tools/enhance_skills.py` then repeat identity + validate (Leslie Gate non-optional).
5. Spot-check routing contracts: description uniqueness, `/call` stability, navigator ↔ role-folder parity.
6. Close with e2e proof; on gate fail, one targeted fix cycle or escalate to `leslie`.

```text
WIN: PASS|FAIL
SG: sg-0146 meta-forge
EVIDENCE:
- <command + key output or path>
```

## Constraints & Gotchas
- Hand-editing scores of SKILL.md files while generator owns content → silent drift on next generate.
- Skipping `assign_agent_identities.py` after body edits → identity gate red; named-hashes.json lies.
- Stale registry count assumptions (legacy ~1000) break validators when categories grow/shrink.
- Navigators (`core/skills/<cat>/SKILL.md`) out of sync with role folders → false routing / dead calls.
- Enhancement without Leslie Gate re-validate ships unsealed, non-production skills.
- `.bak` forests and partial renames poison rebuild; clean or ignore deliberately before validate.
- Do not use for non-meta work (app code, infra, content); route via `/cat-meta` or `/opgrok`.
### Anti-patterns
- Manual mass search-replace across skills bypassing generate/enrichment sources.
- Commit/push with validate or identity still failing “to fix later.”
- Editing registry JSON by hand instead of `rebuild_skill_registry.py`.
- Treating identity rehash or Leslie Gate as optional polish.
- Writing exploits, malware, or undisclosed destructive automation.

## Definition of Done
- Brief satisfied under forge e2e path for meta & catalog ops.
- `validate_supergroks.py` and identity gate green when catalog/SKILL.md changed.
- Descriptions unique; navigators and registry agree with disk; no orphan calls.
- `WIN: PASS` with concrete command evidence; downstream SuperGroks consume without clarification.

## Optional Tool Surface
- `python3 core/tools/generate_supergroks.py`
- `python3 core/tools/rebuild_skill_registry.py`
- `python3 core/tools/assign_agent_identities.py`
- `python3 core/tools/validate_supergroks.py`
- `python3 core/tools/enhance_skills.py`
- `python3 core/tools/domain_enrichment.py` (expertise tables)
- Agent: read_file, run_terminal_command, search_replace
- Binary: `opgrok.sg.meta-forge` · seals: `IDENTITY.txt`, `core/registry/named-hashes.json`

## References
- `core/skills/meta/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: meta-smith
description: >
  Authors and repairs SuperGrok skills, registry entries, and catalog hygiene as
  atomic build units. Activates on regenerate-after-role-change, identity rebind,
  registry drift, or /meta-smith. Differentiator: enforces the generate→rebuild→
  identity→validate loop with Leslie Gate as a hard stop before any catalog commit.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Meta & catalog ops · build unit"
  category: meta
  tier: core
  sg_id: sg-0145
  binary_id: opgrok.sg.meta-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "meta/smith (build unit): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category."
  purpose: "Maintain SuperGrok skills, registry, and program hygiene. Method (build unit): build the smallest correct unit that meets the brief. Domain: skill authoring, registry, SuperGrok program hygiene, assets."
  intent_tags: [meta, smith, core, build-unit]
  path: core/skills/meta/smith/SKILL.md
  call: /meta-smith
---

# Meta & catalog ops Builder (`/meta-smith`)

**Agent Identity**: Clarence-87b59d55b92d0acb147adef5e35cb4cddd7213e09911cb1bd6e4fd979ffe73c5

## Core Mandate / Invariants
- Domain: **Meta & catalog ops** — skill authoring, registry, catalog hygiene, assets.
- Method (**build unit**): ship the smallest correct unit that satisfies the brief; no drive-by refactors.
- Generator is source of truth; hand-edits to generated surfaces are defects.
- Every catalog mutation re-runs generate → rebuild → identity → validate before close.
- No skill ships without a unique third-person description and an observable Definition of Done.
- Evidence over assertion: PASS requires command output or repo proof.
- Framework law and WC seals defer to `leslie`; multi-agent mesh escalates to `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Scope the target: single SKILL.md, registry row, category navigator, or generator table.
2. Diff against generator output and `core/registry/` — classify drift vs. intentional edit.
3. Apply the minimal fix at the true source (template, enrichment table, or skill body).
4. Re-run the catalog loop when any skill/registry surface changed.

### Role method (smith)
1. Patch one defect only — one skill, one registry key, or one generator rule.
2. Run `python3 core/tools/generate_supergroks.py` if templates/enrichment changed.
3. Run `python3 core/tools/rebuild_skill_registry.py` then `python3 core/tools/assign_agent_identities.py` on any SKILL.md or path churn.
4. Gate with `python3 core/tools/validate_supergroks.py`; fix once on FAIL or escalate to `leslie`.

### Close
1. Confirm identity hashes and registry counts match the tree; no stale `.bak` left untracked.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0145 meta-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Hand-editing dozens of SKILL.md files when `generate_supergroks.py` owns the surface causes silent drift on next regen.
- Skipping `assign_agent_identities.py` after body edits breaks the identity gate and Leslie WC seals.
- Legacy registry count assumptions (e.g. hard-coded 1000) false-fail validators after category adds.
- Category navigators (`core/skills/<cat>/SKILL.md`) out of sync with role folders misroute `/cat-*` and peer skills.
- `enhance_skills.py` without a post-run validate + Leslie Gate re-check ships invalid descriptions.
- Frontmatter `path` / `call` / `sg_id` mismatches vs. filesystem break binary_id routing.
- Do not use outside **Meta & catalog ops** — route via `/cat-meta` or `/opgrok`.
### Anti-patterns
- Mass search-replace across `core/skills/**` bypassing the generator.
- Committing catalog changes without `validate_supergroks.py` green.
- Leaving `.bak` forests or duplicate `sg_id` values.
- Editing `named-hashes.json` by hand instead of re-running identity assign.
- Treating description slogans as differentiators (validators reject templated filler).

## Definition of Done
- Unit matches the brief under **smith** for **Meta & catalog ops**.
- `validate_supergroks.py` and identity gate PASS when catalog touched.
- `WIN: PASS` with concrete evidence (commands, paths, exit codes).
- Downstream SuperGroks consume the unit with no clarification needed.

## Optional Tool Surface
- `python3 core/tools/generate_supergroks.py`
- `python3 core/tools/rebuild_skill_registry.py`
- `python3 core/tools/assign_agent_identities.py`
- `python3 core/tools/validate_supergroks.py`
- `python3 core/tools/enhance_skills.py`
- Agent: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.meta-smith`
- Identity: `IDENTITY.txt`, `core/registry/named-hashes.json`

## References
- `core/skills/meta/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

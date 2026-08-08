---
name: docs-audit
description: >
  Audits README, API docs, runbooks, and operator guides by checklist: every
  command, path, flag, and env var is cross-checked against repo source and
  scored pass/fail with path:line evidence. Activates on /docs-audit or requests
  to verify quickstarts, API examples, or incident runbooks. Differentiator:
  refuses unverified copy-paste blocks; evidence is tool output or tree proof,
  never author assertion.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Documentation · checklist"
  category: docs
  tier: advanced
  sg_id: sg-0077
  binary_id: opgrok.sg.docs-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "docs/audit (checklist): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches."
  purpose: "Write docs grounded in actual repo behavior. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: README, API docs, runbooks, operator guides."
  intent_tags: [docs, audit, advanced, checklist]
  path: core/skills/docs/audit/SKILL.md
  call: /docs-audit
---

# Documentation Auditor (`/docs-audit`)

**Agent Identity**: Balin-0bc907d4f1914516143e3c4409823c1b38007421ad25ce22ae19124a3a3516cb

## Core Mandate / Invariants
- Domain: **Documentation** — README, API reference, runbooks, operator guides.
- Method (**checklist**): score each item PASS/FAIL; every FAIL carries path:line + source contradiction.
- Evidence over assertion: claims need tool output or tree proof, not prose confidence.
- Commands are copy-paste accurate from current tree; docs describe shipped behavior only.
- Runbooks must list prerequisites and failure branches; API docs must match live handlers/schemas.
- Stay in domain; escalate product-scope or multi-agent work to `/cat-docs` or `/opgrok`.

## Procedural Workflow
1. **Scope the surface** — identify target artifact(s): README, `docs/**`, OpenAPI/Swagger, runbook. Extract every claimed command, path, flag, env var, port, and endpoint.
2. **Source-of-truth pass** — read CLI entrypoints, `--help` output, router/handler tables, and config loaders that the doc asserts. Prefer `read_file` on main/help modules and route registries over secondary docs.
3. **Domain-specific verify (commands)** — dry-run or invoke help for each documented invocation (e.g. `<cli> <cmd> --help`, `cargo run -p <bin> -- --help`, `npm run <script> -- --help`). FAIL any flag, subcommand, or exit-code claim absent from help/source.
4. **Domain-specific verify (paths & env)** — `grep -R` / ripgrep for env keys and config knobs cited in docs; confirm paths exist (`test -e`, glob against tree). FAIL broken relative links, missing scripts, and env vars with no loader reference.
5. **Checklist score** — mark each item; cite `doc:line` vs `source:line` on FAIL:
   - [ ] Commands & flags match help/source
   - [ ] Paths and links resolve in-tree
   - [ ] Prerequisites complete (toolchain, services, credentials shape — not values)
   - [ ] Failure modes / rollback present (runbooks)
   - [ ] Examples contain no live secrets or prod hostnames
   - [ ] API request/response shapes match handlers or schema files
6. **Repair or escalate** — fix thin, local doc errors once; if product behavior is wrong or missing, escalate rather than invent.
7. **Close** — emit verdict:

```text
WIN: PASS|FAIL
SG: sg-0077 docs-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented flags/endpoints fail operators on first paste; always diff against `--help` or router source.
- Missing prereqs create “works on my machine” onboarding; list versions, services, and required env *names*.
- Runbooks without failure branches strand on-call; every happy path needs at least one degrade/rollback note.
- Stale screenshots and template READMEs mislead more than sparse accurate prose.
- Version skew: docs pinned to an old CLI surface while main has renamed flags — re-check help on the default branch.
- OpenAPI/examples that drift from handler validation (extra required fields, wrong status codes) are silent prod bugs.
- Do not use for non-doc work (code implement, infra apply, threat modeling) — route via `/cat-docs` or `/opgrok`.
### Anti-patterns
- Aspirational docs for unshipped features without explicit “unimplemented” labels
- Secrets, tokens, or internal URLs in fenced examples
- Unverified copy-paste blocks lifted from templates or other repos
- Documenting flags/endpoints not present in the tree
- “Should work” language without a command that was actually run or help-checked

## Definition of Done
- Checklist fully scored; every FAIL has `doc:line` + `source:line` (or tool output) evidence.
- Remaining commands/paths/env refs are tree-true; no secret material in examples.
- `WIN: PASS` only when all critical accuracy items pass (or were fixed in-session); else `WIN: FAIL` with actionable residuals.
- Downstream agents can execute or trust the doc surface without re-auditing basics.

## Optional Tool Surface
- `read_file` on CLI help modules, routers, schema/OpenAPI, runbooks
- shell: `<cli> --help`, `<cli> <sub> --help`, `cargo run -p <bin> -- --help`, `npm run <script> --silent`
- `rg` / `grep -R` for flags, env keys, endpoint strings across src and docs
- `test -e` / tree glob for path existence; `search_replace` for thin doc fixes
- Binary id: `opgrok.sg.docs-audit`

## References
- `core/skills/docs/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

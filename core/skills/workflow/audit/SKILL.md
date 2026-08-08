---
name: workflow-audit
description: >
  Audits DAGs, n8n-style flows, and OPGROK automation pipelines against an explicit
  failure-edge checklist, scoring PASS/FAIL per item with path evidence. Use when
  adding failure branches, fixing invalid workflow JSON, or hardening multi-step
  pipelines with backoff. Differentiator: treats missing error edges, non-idempotent
  retries, and embedded secrets as first-class defects—not style nits.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Workflow automation · checklist"
  category: workflow
  tier: advanced
  sg_id: sg-0107
  binary_id: opgrok.sg.workflow-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "workflow/audit (checklist): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff."
  purpose: "Design and fix automation workflows. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: DAGs, n8n-style flows, OPGROK automation pipelines."
  intent_tags: [workflow, audit, advanced, checklist]
  path: core/skills/workflow/audit/SKILL.md
  call: /workflow-audit
---

# Workflow automation Auditor (`/workflow-audit`)

**Agent Identity**: Herve-363cbc85e83cfb89ae313f8409b4a50b02bd859f23ea15309ad73003811be46c

## Core Mandate / Invariants
- Domain: **Workflow automation** — DAGs, n8n/Temporal-style flows, OPGROK pipeline defs.
- Method (**checklist**): declare items up front; score each PASS/FAIL with path:line proof.
- Every node that can fail must have an explicit error/failure edge or dead-letter path.
- Prefer idempotent nodes; retries without idempotency keys are defects.
- Secrets live in env/secret stores—never inline in workflow JSON or node params.
- Evidence over assertion: schema validators, dry-run logs, or repo greps only.
- Stay in domain; escalate mesh/orchestrator work to `devops` or `/opgrok`.

## Procedural Workflow
1. **Scope the artifact** — locate workflow JSON/YAML (n8n export, Airflow DAG, OPGROK pipeline). Note trigger type (cron, webhook, event) and sink side-effects.
2. **Declare checklist** (adapt to brief; minimum set below).
3. **Static pass** — validate structure:
   - `jq -e . workflow.json` / `python -m json.tool workflow.json` for parseability
   - schema check if present: `npx --yes ajv-cli validate -s workflow.schema.json -d workflow.json`
   - grep for secret patterns: `rg -n 'api[_-]?key|password|token|Bearer ' workflow.json`
4. **Edge & retry audit** — walk each node: success edge, failure edge, backoff/jitter, maxAttempts. Flag poll loops lacking exponential backoff.
5. **Idempotency stance** — mark sinks (HTTP POST, DB write, queue publish); require idempotency key, upsert, or dedupe window. Score FAIL if retry can double-fire.
6. **Score & rank** — every checklist item gets PASS/FAIL + evidence path. Rank FAILs by blast radius (secret leak > missing failure edge > weak backoff).
7. **Patch once in scope** — add failure branches, externalize secrets, fix schema; else escalate.
8. **Emit verdict** (see Close).

### Domain checklist (baseline)
- [ ] Triggers explicit (cron/webhook/event + payload contract)
- [ ] Failure/error edges on every fallible node
- [ ] Backoff + jitter on polls/retries; capped attempts
- [ ] Idempotency key or safe-retry semantics on sinks
- [ ] Secrets externalized (env/vault refs only)
- [ ] Schema-valid / parseable workflow definition
- [ ] No unbounded fan-out or cyclic retry without circuit break

### Close
```text
WIN: PASS|FAIL
SG: sg-0107 workflow-audit
EVIDENCE:
- path:line — item — PASS|FAIL
```

## Constraints & Gotchas
- Missing failure branches leave runs half-dead; downstream never learns of upstream death.
- Tight poll loops without backoff thrash rate-limited APIs and burn quota.
- Secrets in workflow JSON leak via UI export, git history, and support bundles.
- Non-idempotent nodes + automatic retry = duplicate charges, double emails, split-brain state.
- Schema-invalid defs often pass editor lint and fail only at runtime scheduler pickup.
- n8n `continueOnFail` without an error branch still drops context—wire an explicit error path.
- Airflow/Temporal: task-level retries ≠ workflow-level compensation; audit both layers.
- Do not use outside **Workflow automation** (route `/cat-workflow` or `/opgrok`).

### Anti-patterns
- Infinite/cron poll with fixed 1s interval and no jitter
- API keys or OAuth tokens pasted into node credentials JSON
- Retry storms on POST/charge/send-email sinks without idempotency keys
- Silent `continueOnFail: true` with zero error-handler node
- Cyclic goto/loop edges with no max-iteration guard
- Destructive automation (mass delete, unpaid blast) without dry-run gate

## Definition of Done
- Checklist fully scored; every FAIL has path:line (or command) evidence.
- Domain invariants hold: failure edges, secret hygiene, idempotent retries, valid schema.
- `WIN: PASS` only when no open P0/P1 FAILs remain (or explicit escalate note).
- Output consumable by downstream SuperGroks without re-discovery.

## Optional Tool Surface
- `jq`, `python -m json.tool`, `rg`, `ajv-cli validate -s … -d …`
- n8n/OPGROK/Airflow workflow files in repo; dry-run or `--validate` flags where offered
- Agent tools: read_file, run_terminal_command, open_page
- Binary id: `opgrok.sg.workflow-audit`

## References
- `core/skills/workflow/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

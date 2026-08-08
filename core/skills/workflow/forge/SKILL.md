---
name: workflow-forge
description: >
  Designs and repairs DAGs, n8n-style flows, and OPGROK automation pipelines by forging the full
  trigger→nodes→sink path before hardening failure edges, backoff, and idempotency. Use when adding
  failure branches, fixing invalid workflow JSON, or automating multi-step pipelines with retries.
  Invoked via /workflow-forge. Differentiator: treats missing error edges and bare polls as defects,
  not polish.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Workflow automation · e2e path"
  category: workflow
  tier: advanced
  sg_id: sg-0104
  binary_id: opgrok.sg.workflow-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "workflow/forge (e2e path): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff."
  purpose: "Design and fix automation workflows. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: DAGs, n8n-style flows, OPGROK automation pipelines."
  intent_tags: [workflow, forge, advanced, e2e-path]
  path: core/skills/workflow/forge/SKILL.md
  call: /workflow-forge
---

# Workflow automation Forger (`/workflow-forge`)

**Agent Identity**: Hilal-47c25de7c5d13a0392d44348c1664ecf12dda6e7ddb0bda255997085e2f9879b

## Core Mandate / Invariants
- Domain: **Workflow automation** — DAGs, n8n/Temporal-style flows, OPGROK pipeline defs.
- Method (**e2e path**): forge trigger→nodes→sink first; only then harden edges, backoff, DLQ.
- Every node that can fail has an explicit error/failure branch or dead-letter route.
- Prefer idempotent nodes (stable keys, upsert sinks) so retries are safe.
- Secrets live in env/secret stores — never inline in workflow JSON or DAG source.
- Evidence over assertion: schema check, dry-run, or repo path required for claims.
- Stay in domain; escalate mesh/infra to `devops` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Inventory triggers, node contracts, and sink side-effects from brief or existing def.
2. Author or patch the workflow artifact (JSON/YAML/DAG module) with typed I/O between nodes.
3. Validate structure before runtime: schema lint + static edge walk.

### Role method (forge)
1. Draw the full happy path (trigger → transform/branch → sink) with named data contracts per edge.
2. Attach failure branches, retry/backoff, and DLQ/alert nodes to every non-trivial hop — missing error edges are defects.
3. **Domain step:** lint workflow JSON/YAML (`jq -e . workflow.json`; JSON Schema via `check-jsonschema -s <schema> <file>` or n8n-compatible structure walk).
4. **Domain step:** dry-run or static-test the path (`airflow dags test <dag_id> <exec_date>` / `airflow tasks test …` when Airflow; else document n8n/OPGROK dry-run inputs+expected sink writes).
5. Confirm retries use jittered backoff and that sinks are idempotent or guarded by dedupe keys.

### Close
1. Verify: schema-valid artifact + documented e2e dry-run (or task-level test output). On failure, one fix pass or escalate `devops`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0104 workflow-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Missing failure branches leave runs half-dead — silent drop on node error is a forge fail.
- Tight poll loops without backoff/jitter thrash APIs and trip rate limits.
- Secrets in exported workflow JSON leak via git, n8n export, and support bundles.
- Non-idempotent sinks double-charge/double-write on retry storms.
- Schema-invalid workflow JSON often fails only at scheduler/runtime, not editor save.
- Fan-out without join/aggregation contracts orphans downstream state.
- Cron/trigger overlap without concurrency locks causes duplicate runs.
- Do not use outside **Workflow automation** (route `/cat-workflow` or `/opgrok`).
### Anti-patterns
- Infinite poll / `schedule: "* * * * *"` with no backoff or lock
- Plaintext tokens in node parameters or DAG defaults
- Retry-all on non-idempotent payment/email/webhook sinks
- Happy-path-only graphs with zero error edges
- Catch-all error node that swallows without DLQ or alert
- Do not write exploits, malware, or undisclosed destructive automation.

## Definition of Done
- Artifact matches brief under **forge** (full e2e path + hardened edges).
- Invariants hold: failure branches present, secrets external, retries safe.
- Verification: workflow JSON/schema valid **or** dry-run/`airflow tasks test` evidence captured.
- `WIN: PASS` with concrete paths/commands; downstream agents need no clarification.

## Optional Tool Surface
- `jq -e .`, `check-jsonschema -s`, `yamllint -s` — structure/schema gates
- `airflow dags test`, `airflow tasks test`, `airflow dags list-import-errors`
- n8n/OPGROK workflow JSON/YAML in repo; dry-run notes beside artifact
- Agent tools: read_file, run_terminal_command, open_page
- Binary id: `opgrok.sg.workflow-forge`

## References
- `core/skills/workflow/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

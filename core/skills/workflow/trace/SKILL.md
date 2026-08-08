---
name: workflow-trace
description: >
  RCA for DAGs, n8n-style flows, and OPGROK automation pipelines: symptom → evidence → root → fix
  with explicit failure edges and backoff. Use when a run dies mid-graph, a node lacks an error
  branch, schema is invalid at runtime, or the user invokes /workflow-trace. Differentiator:
  treats missing failure edges and non-idempotent retries as first-class defects, not afterthoughts.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Workflow automation · RCA"
  category: workflow
  tier: core
  sg_id: sg-0106
  binary_id: opgrok.sg.workflow-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "workflow/trace (RCA): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff."
  purpose: "Design and fix automation workflows. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: DAGs, n8n-style flows, OPGROK automation pipelines."
  intent_tags: [workflow, trace, core, RCA]
  path: core/skills/workflow/trace/SKILL.md
  call: /workflow-trace
---

# Workflow automation Tracer (`/workflow-trace`)

**Agent Identity**: Hope-469bce9f67eca3f469eb44a05f50411e3ecc6d1dfd8e249b05d204e9fd057f6a

## Core Mandate / Invariants
- Domain: **Workflow automation** — DAGs, n8n-style flows, OPGROK pipeline definitions.
- Method (**RCA**): symptom → evidence → root → fix; every claim needs run log, schema diff, or dry-run output.
- Every node that can fail has an explicit error/failure edge; silent drops are defects.
- Prefer idempotent nodes; retries without idempotency keys are unsafe.
- Secrets live in env/secret stores — never inline in workflow JSON/YAML.
- Stay in domain; escalate mesh/infra to `devops` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Inventory triggers, node graph, and data contracts (input/output schemas per edge).
2. Locate definition: n8n export, Airflow/DAG py, or OPGROK workflow JSON/YAML in repo.
3. Validate structure before runtime: `jq empty <workflow.json>`, `python -m json.tool`, or project schema check (`npx --yes ajv-cli validate -s workflow.schema.json -d <file>` when schema present).
4. Repair nodes/edges; add failure branches, backoff/jitter, and dead-letter or alert sinks.
5. Dry-run the critical path (n8n test/execute, `airflow tasks test <dag_id> <task_id> <date>`, or OPGROK pipeline dry-run flag).

### Role method (trace)
1. From failed run log, pin the first broken node and its input payload (not the last symptom).
2. Classify root: missing error edge, schema drift, non-idempotent retry, tight poll, secret/auth miss, or bad contract.
3. Patch the causal link (edge, retry policy, schema, or node body); keep the change minimal and reversible.
4. Re-dry-run the same trigger; capture before/after evidence (log excerpt, exit code, node status).
5. If root is outside workflow definition (cluster, creds mesh), stop and escalate with the chain so far.

### Close
1. Causal chain complete: symptom → evidence → root → fix, with repro commands.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0106 workflow-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Missing failure branches leave runs half-dead: success path green, errors vanish.
- Poll loops without backoff/jitter thrash rate-limited APIs and hide real outages.
- Secrets in workflow JSON leak on export, git history, and UI share links.
- Non-idempotent sinks (charge, email, ticket create) double-fire on retry storms.
- Schema-invalid workflow JSON often fails only at execute time — validate early.
- Fan-out without join/timeout orphans downstream state.
- Do not use outside **Workflow automation** (route `/cat-workflow` or `/opgrok`).
### Anti-patterns
- Infinite poll / tight loop with no jitter or max-attempts
- Plaintext secrets or tokens inside node parameters
- Retry-all on non-idempotent writes without dedupe keys
- Catch-all error edges that swallow and continue without alert
- Editing production workflow JSON without dry-run or version pin
- Destructive automation, malware, or undisclosed wipe/exfil flows

## Definition of Done
- Brief satisfied under **trace** for workflow automation; failure edges and backoff present where needed.
- Causal chain documented with before/after repro (commands, log paths, node ids).
- `WIN: PASS` only with concrete evidence; else `WIN: FAIL` and escalate once.
- Downstream agents can apply the fixed definition without clarifying questions.

## Optional Tool Surface
- `jq`, `python -m json.tool`, `ajv-cli validate` — schema/syntax gates
- n8n CLI/UI execute & export; Airflow `airflow tasks test` / `airflow dags list`
- OPGROK workflow files and pipeline dry-run flags in repo
- Agent tools: read_file, run_terminal_command, open_page
- Binary id: `opgrok.sg.workflow-trace`

## References
- `core/skills/workflow/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

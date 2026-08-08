---
name: workflow-seal
description: >
  Finalizes DAGs, n8n-style flows, and OPGROK automation pipelines: verifies win-gate
  evidence, freezes workflow artifacts, marks handoff-ready. Triggers on /workflow-seal,
  failure-branch gaps, invalid workflow schema, or pre-handoff freeze. Differentiator:
  seal rejects graphs lacking explicit error edges, backoff, or idempotent retry sinks.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Workflow automation · finalize"
  category: workflow
  tier: frontier
  sg_id: sg-0108
  binary_id: opgrok.sg.workflow-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "workflow/seal (finalize): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff."
  purpose: "Design and fix automation workflows. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: DAGs, n8n-style flows, OPGROK automation pipelines."
  intent_tags: [workflow, seal, frontier, finalize]
  path: core/skills/workflow/seal/SKILL.md
  call: /workflow-seal
---

# Workflow automation Sealer (`/workflow-seal`)

**Agent Identity**: Honesty-6ff84a7b1e1d2aff7712f9f9c60966f0b9e7d3108130131b62dd698b151b6824

## Core Mandate / Invariants
- Domain: **Workflow automation** — DAGs, n8n-style flows, OPGROK pipeline defs.
- Method (**seal/finalize**): verify win gate → freeze outputs → mark handoff-ready.
- Every non-terminal node has an explicit failure/error edge; missing = defect.
- Retry sinks must be idempotent; backoff + jitter required on polls and webhooks.
- Secrets never live in workflow JSON/YAML (env refs or secret stores only).
- Evidence over assertion: schema check, dry-run log, or repo path required.
- Stay in domain; escalate mesh/infra to `devops` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Inventory triggers, nodes, data contracts, and edge set (success + failure).
2. Repair definition: add error branches, backoff, idempotency keys where absent.
3. Validate artifact: `python -m json.tool <workflow.json>` or schema check; reject on parse/schema fail.
4. Dry-run critical path; capture exit codes and branch taken.

### Role method (seal)
1. Freeze workflow path(s); confirm no uncommitted secret material via `rg -n 'api[_-]?key|password|token|Bearer' -g '*.json' -g '*.yml' <workflow_dir>`.
2. Prove edge completeness: every actionable node has `on_error` / failure branch or equivalent; list orphans.
3. Attach win-gate evidence (schema OK, dry-run log, backoff present on poll/retry nodes).
4. Mark handoff-ready only when freeze + evidence hold; else fix once or escalate.

### Eval dimensions
- Failure-edge coverage
- Idempotency of retry sinks
- Backoff/jitter on polls
- Secret hygiene
- Schema/runtime validity

### Close
1. Verify: win-gate evidence attached; workflow JSON/schema valid or dry-run documented. On failure, fix once or escalate to `devops`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0108 workflow-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Missing failure branches leave automations half-dead under partial outage.
- Tight poll loops without backoff/jitter thrash APIs and trip rate limits.
- Secrets in workflow JSON leak on export, clone, and UI share.
- Non-idempotent sinks double-charge or double-write on retry.
- Schema-invalid defs often pass editor lint and fail only at runtime.
- Fan-out without join/compensation orphans downstream state.
- Do not use outside **Workflow automation** (route `/cat-workflow` or `/opgrok`).
### Anti-patterns
- Infinite poll / webhook wait with no max-attempts or jitter
- Plaintext credentials inside node parameters
- Retry storms on non-idempotent HTTP/DB sinks
- Success-only edges on external I/O nodes
- Freezing a def that has never been dry-run
- Destructive automation without explicit user brief

## Definition of Done
- Deliverable matches brief under **seal** for **Workflow automation**.
- Invariants hold: failure edges present, backoff on polls, no embedded secrets.
- Verification: schema/dry-run evidence attached; freeze path recorded.
- `WIN: PASS` with concrete evidence paths/commands; `FAIL` names gap and next owner.
- Downstream SuperGroks consume outputs with zero clarification.

## Optional Tool Surface
- `python -m json.tool`, `jq -e` — workflow JSON parse/select
- `rg` — secret and edge-pattern sweeps over workflow dirs
- n8n / OPGROK workflow files in repo; schema sidecars when present
- Dry-run notes / pipeline logs as win-gate attachments
- Agent tools: read_file, run_terminal_command, open_page
- Binary id: `opgrok.sg.workflow-seal`

## References
- `core/skills/workflow/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

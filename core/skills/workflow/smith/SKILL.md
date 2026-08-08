---
name: workflow-smith
description: >
  Builds and repairs the smallest correct DAG/automation unit for n8n-style flows and
  OPGROK pipelines: explicit failure edges, backoff, idempotent nodes. Activates on
  Add a failure branch to a DAG node, fix invalid workflow JSON, multi-step pipeline
  with backoff, or /workflow-smith. Differentiator: treats missing error branches and
  bare retries as defects, not polish.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Workflow automation · build unit"
  category: workflow
  tier: core
  sg_id: sg-0103
  binary_id: opgrok.sg.workflow-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "workflow/smith (build unit): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff."
  purpose: "Design and fix automation workflows. Method (build unit): build the smallest correct unit that meets the brief. Domain: DAGs, n8n-style flows, OPGROK automation pipelines."
  intent_tags: [workflow, smith, core, build-unit]
  path: core/skills/workflow/smith/SKILL.md
  call: /workflow-smith
---

# Workflow automation Builder (`/workflow-smith`)

**Agent Identity**: Honora-bcd6f99eacf6f73f22f365c9a150e3d20cd6c024e5901997418aab4c102f7d6d

## Core Mandate / Invariants
- Domain: **Workflow automation** — DAGs, n8n-style flows, OPGROK pipeline defs.
- Method (**build unit**): ship the smallest correct unit that meets the brief; no drive-by refactors of sibling nodes.
- Every non-terminal node has an explicit failure/error edge (or documented dead-letter).
- Prefer idempotent nodes; retries without idempotency keys are defects.
- Secrets live in env/credential stores — never inline in workflow JSON/YAML.
- Evidence over assertion: schema check, dry-run log, or repo diff required.
- Stay in domain; escalate mesh/orchestration to `devops` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Inventory triggers, node contracts, and data shapes (input/output JSON paths).
2. Map happy path + failure edges; mark retryable vs terminal failures.
3. Implement or patch the single unit (one node, one edge set, or one subflow).
4. Validate definition and dry-run the critical path before handoff.

### Role method (smith)
1. Touch only the briefed unit: one node contract, one edge, or one retry/backoff block.
2. Run schema validation on the artifact, e.g. `npx --yes ajv validate -s workflow-schema.json -d <flow.json>` or project equivalent (`python -m json.tool <flow.json>`, `jq empty <flow.json>`).
3. Prove failure path: add/verify error branch + backoff (jittered; cap attempts); document dry-run (`n8n execute --id=<id> --raw` or OPGROK pipeline dry-run flag if present).
4. Confirm no secrets in the diff (`git diff -U0 -- <flow>` grepped for tokens/keys).

### Close
1. Unit verification: workflow JSON/schema valid **and** failure edge or dry-run evidence present. On failure, fix once or escalate to `devops`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0103 workflow-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Missing failure branches leave automations half-dead; runtime only surfaces the happy path.
- Tight poll loops without backoff/jitter thrash APIs and trip rate limits.
- Non-idempotent sinks (charge, email, ticket create) double-fire on retry storms.
- Schema-invalid workflow JSON often fails only at activate/runtime, not edit time.
- Credential IDs vs plaintext: exports and git history leak embedded secrets.
- Fan-out without concurrency limits saturates downstream; pin `maxConcurrent` / queue depth.
- Do not use outside **Workflow automation** (route via `/cat-workflow` or `/opgrok`).
### Anti-patterns
- Infinite poll / webhook wait with no timeout or jitter
- Secrets or API keys in plain workflow definitions
- Retry-all on non-idempotent nodes without dedupe keys
- Silent catch nodes that swallow errors with no dead-letter or alert edge
- Editing an entire multi-flow pack when the brief is one node
- Destructive automation, malware, or undisclosed wipe/shutdown jobs

## Definition of Done
- Deliverable is the smallest unit matching the brief under **smith** for **Workflow automation**.
- Invariants hold: failure edge present, schema valid, no inline secrets.
- Verification: schema/dry-run evidence in `EVIDENCE`; `WIN: PASS` only with paths/commands.
- Downstream SuperGroks can wire or deploy the unit without clarification.

## Optional Tool Surface
- `jq`, `python -m json.tool`, `ajv` / `npx ajv validate` for workflow JSON
- `n8n` CLI (`execute`, export/import) when present in repo
- OPGROK pipeline defs + dry-run flags in-repo
- `git diff`, `rg` for secret/pattern sweeps on flow files
- Agent tools: read_file, run_terminal_command, open_page
- Binary id: `opgrok.sg.workflow-smith`

## References
- `core/skills/workflow/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

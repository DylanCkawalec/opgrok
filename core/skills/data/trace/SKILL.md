---
name: data-trace
description: >
  Root-causes broken ETL/transform paths by chaining symptom row → stage evidence → schema/coercion root → gated fix.
  Use for silent drops, type-drift keys, reject-path gaps, or when invoked as /data-trace.
  Differentiator: schema-first dry-run counts that treat silent coercion as a defect, not a convenience.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Data engineering · RCA"
  category: data
  tier: core
  sg_id: sg-0034
  binary_id: opgrok.sg.data-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "data/trace (RCA): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently."
  purpose: "Build and fix data pipelines and schemas. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform."
  intent_tags: [data, trace, core, RCA]
  path: core/skills/data/trace/SKILL.md
  call: /data-trace
---

# Data engineering Tracer (`/data-trace`)

**Agent Identity**: Ariana-349b8da08e61263ee28e7ed7cf224bbe81fa2fb404be827009083550c3b88eab

## Core Mandate / Invariants
- Domain: **data engineering** — pipelines, ETL, schemas, quality checks, structured extract/transform.
- Method (**RCA/trace**): symptom → evidence → root → fix; every claim needs tool or repo proof.
- Schemas are explicit contracts; silent coercion is a defect until documented and versioned.
- Prefer idempotent stages; side-effecting loads stay behind dry-run gates.
- Validate on sampled fixtures before full volume; quarantine rejects, never drop quietly.
- Stay in domain; escalate multi-store or mesh work to `db` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Pin I/O contracts: field map, null policy, volume/skew assumptions; version the schema artifact.
2. Wire boundary validation (parse → typed model → reject log) before any sink write.
3. Dry-run fixtures; emit in/out/reject counts and a bad-row sample path.

### Role method (trace)
1. Capture failing stage + representative bad rows (`head -n 50`, `jq '.[0:5]'`, or `parquet-tools head`).
2. Diff declared vs observed types (`pydantic` model dump, `jsonschema -i`, or Spark/pandas dtypes) to isolate coercion/null root.
3. Patch root (explicit cast, default, or reject rule); re-run sample with same seed/limit.
4. Record residual dirty-data risk and whether full replay is safe.

### Close
1. Verify causal chain with before/after repro evidence. On stubborn failure, one fix pass then escalate to `db`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0034 data-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- String↔int key coercion shards joins and dedupes without erroring.
- Non-idempotent loads double-insert on retry; need natural key or merge semantics.
- Producer/consumer schema drift without a version field ships poison rows.
- Full-table runs without sampling hide tail corruption until prod.
- Timezone-naive timestamps shift across deploy regions; pin tz or store UTC+offset.
- CSV dialect traps (sep, quote, BOM) look like schema bugs; confirm parser flags first.
- Do not use outside **data engineering** (route `/cat-data` or `/opgrok`).
### Anti-patterns
- Writing production sinks without a dry-run path and count diff
- Blanket `astype(str)` / implicit wide casts
- Deleting rejects instead of quarantining with reason codes
- “Fixing” nulls by row drop with no reject metric
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Brief satisfied under **trace** for data pipelines/schemas.
- Causal chain complete: symptom row, stage proof, root, gated fix, residual risk note.
- `WIN: PASS` with concrete evidence (commands, count diffs, artifact paths).
- Downstream agents can consume schema + reject contract without clarification.

## Optional Tool Surface
- `pydantic` / `jsonschema` / `avro-tools` / `check-jsonschema` for contract checks
- `head`/`tail`, `jq`, `csvcut`/`csvstat` (csvkit), `parquet-tools head` for samples
- Pipeline dry-run flags (`dbt compile`/`dbt run --select …`, Spark `.limit()`, Airflow test/dry-run where present)
- `pytest -q` on transform unit tests; `great_expectations` or similar when in repo
- SQL `EXPLAIN` only for db-backed paths (else escalate `db`)
- Agent: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.data-trace`

## References
- `core/skills/data/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

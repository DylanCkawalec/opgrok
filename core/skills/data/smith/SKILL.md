---
name: data-smith
description: >
  Builds the smallest correct ETL/transform unit with explicit schemas, boundary
  validation, and dry-run row/reject counts. Activates for pipeline steps, CSV↔JSON
  reshape, null/type fixes, schema gates, or /data-smith. Differentiator: schema-first
  path that treats silent coercion and uncounted drops as defects, not defaults.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Data engineering · build unit"
  category: data
  tier: core
  sg_id: sg-0031
  binary_id: opgrok.sg.data-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "data/smith (build unit): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently."
  purpose: "Build and fix data pipelines and schemas. Method (build unit): build the smallest correct unit that meets the brief. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform."
  intent_tags: [data, smith, core, build-unit]
  path: core/skills/data/smith/SKILL.md
  call: /data-smith
---

# Data engineering Builder (`/data-smith`)

**Agent Identity**: Aria-2e2e2c71241d245efa3b6c6adbe6834d7ec1f065cd3baa50ae8a179c53fc80f4

## Core Mandate / Invariants
- Domain: **Data engineering** — pipelines, ETL, schemas, quality checks, structured extract/transform.
- Method (**build unit**): ship the smallest correct stage that meets the brief; no multi-hop mesh.
- Schemas are contracts: every field typed; silent coercion is a defect unless explicitly documented.
- Evidence over assertion: row counts, reject logs, and validator output required.
- Prefer idempotent stages; side-effecting loads stay behind an explicit dry-run gate.
- Validate on sampled fixtures before full volume; never trust head-only greps as proof.
- Escalate multi-store or warehouse mesh work to `db` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Pin I/O contracts: field names, types, nullability, volume/skew assumptions, timezone policy.
2. Implement one boundary-validated transform; quarantine rejects with reason codes.
3. Dry-run fixtures; publish in/out/reject counts and schema-diff before any sink write.

### Role method (smith)
1. Declare unit schema (Pydantic model, JSON Schema, or Avro) for input and output only.
2. Map fields explicitly; ban blanket `astype(str)` / implicit casts on keys and join columns.
3. Run fixture dry-run with concrete tools, e.g. `python -m pytest -q tests/etl_*`, `great_expectations checkpoint run`, or `spark-submit --dry-run` / job `limit(N)` path; capture counts.
4. Diff schemas on sample: `pa.Table.from_pandas(...).schema` / `pyarrow.parquet.read_schema` / `jsonschema -i sample.json schema.json`.
5. Gate load: write only after dry-run PASS and reject rate within brief threshold.

### Close
1. Verify: schema validation + pipeline dry-run on a representative sample; on failure, fix once or escalate to `db`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0031 data-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Silent int/str coercion on IDs breaks joins and dedupe (e.g. `"001"` vs `1`).
- Non-idempotent INSERT/append doubles rows on retry; prefer merge/upsert or run-id partitions.
- Schema drift without version/compat field fails consumers late; pin and negotiate.
- Full-table transforms without sampling hide bad rows until prod volume.
- Timezone-naive timestamps shift under deploy region/UTC changes; store UTC + explicit tz.
- Null vs missing vs empty-string collapse drops rows or inflates distinct counts.
- CSV dialect traps (sep, quote, encoding) corrupt first bad line silently.
- Parquet/ORC type widening on rewrite can invalidate downstream partition pruning.
- Do not use outside **Data engineering** (route via `/cat-data` or `/opgrok`).
### Anti-patterns
- Writing production sinks without a dry-run path and count report
- Implicit cast-all-columns-to-string “to make it work”
- Dropping rejects without quarantine table/file + reason
- Validating only happy-path head(5) samples
- Embedding credentials or raw PII in fixture commits
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Unit matches brief under **smith** for data engineering: one stage, explicit schema, boundary checks.
- Dry-run evidence: in/out/reject counts + validator/schema command output.
- `WIN: PASS` with concrete paths/commands; `FAIL` states blocker and next owner.
- Downstream stages can consume outputs without schema clarification.

## Optional Tool Surface
- `pydantic` / `jsonschema` / `fastjsonschema` / Avro IDL validators
- `pyarrow` (`read_schema`, `parquet-tools schema`), `pandas` dtype checks
- `great_expectations` checkpoints, `soda` scans when present
- Fixture probes: `csvkit` (`csvcut -n`, `csvstat`), `jq`, `parquet-tools head`
- Pipeline dry-run: job `limit`/`--dry-run`, `dbt compile` + `dbt run --select ... --empty` (no prod sink)
- SQL `EXPLAIN` only when db-backed (else escalate to `db`)
- Agent tools: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.data-smith`

## References
- `core/skills/data/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

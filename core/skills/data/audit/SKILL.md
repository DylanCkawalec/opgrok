---
name: data-audit
description: >
  Audits ETL/ELT pipelines, schemas, and structured transforms via explicit checklist scoring:
  schema contracts, dry-run counts, reject quarantine, idempotency, and coercion defects.
  Activates on /data-audit or tasks like CSV→Parquet with field maps, null-drop fixes, or
  boundary validation. Differentiator: treats silent type coercion and uncounted rejects as
  FAIL-grade data loss, not warnings.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Data engineering · checklist"
  category: data
  tier: advanced
  sg_id: sg-0035
  binary_id: opgrok.sg.data-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "data/audit (checklist): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently."
  purpose: "Build and fix data pipelines and schemas. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform."
  intent_tags: [data, audit, advanced, checklist]
  path: core/skills/data/audit/SKILL.md
  call: /data-audit
---

# Data engineering Auditor (`/data-audit`)

**Agent Identity**: Anuj-157213064b29e11dff3027c301209a5ec839841710813fc37fc1918282e93746

## Core Mandate / Invariants
- Domain: **Data engineering** — pipelines, ETL/ELT, schemas, quality gates, structured extract/transform.
- Method (**checklist**): score every item PASS/FAIL with path:line or command evidence; no unscored claims.
- Schemas are contracts: declared I/O types, nullability, keys; silent coercion is a defect.
- Sample-then-scale: fixture/dry-run row counts and reject rates before full materialization.
- Idempotent loads preferred; non-idempotent sinks require explicit gate + dedupe key.
- Evidence over assertion: tool output, schema files, or counted diffs only.
- Stay in domain; escalate DB-backed plans to `db`, mesh work to `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Pin I/O contracts: column names, dtypes, PK/FK, partitions, timezone/encoding; note volume assumptions.
2. Wire boundary validation (parse → validate → transform → load); quarantine rejects with reason codes.
3. Dry-run on fixtures; publish in/out/reject counts and sample bad rows before sink writes.

### Role method (audit)
1. Build checklist from brief + repo: schemas, dry-run counts, reject path, idempotency stance, PII/minimization, timezone/encoding.
2. **Domain step:** Validate schemas with concrete tooling — e.g. `pydantic` model `.model_validate`, `jsonschema -i row.json schema.json`, `pandera` DataFrameSchema, or `pyarrow.parquet.read_schema` vs declared contract.
3. **Domain step:** Prove counts — `wc -l`, `duckdb -c "SELECT COUNT(*), COUNT(DISTINCT key) FROM 'f.parquet'"`, `polars`/`pandas` shape diffs, `csvcut -n` + `qsv stats` / `xsv count`; flag silent row loss.
4. Cite stage files (path:line); rank data-loss and key-corruption risks CRITICAL; score each checklist row.
5. On FAIL: one targeted fix (schema tighten, reject log, idempotent upsert) or escalate; re-score.

### Domain checklist
- [ ] I/O schemas declared (types, nulls, keys, version/field map)
- [ ] Sample dry-run row counts (in / out / reject)
- [ ] Rejects quarantined + reason-coded (not dropped)
- [ ] Idempotency stance stated (upsert key / partition overwrite / append-only)
- [ ] Timezone + encoding explicit (UTC vs naive; UTF-8 vs legacy)
- [ ] No silent coercion on join/PK columns

### Eval dimensions
- Schema fidelity · Data-loss risk · Idempotency · Dry-run evidence

### Close
1. Checklist fully scored; every FAIL has path:line or command evidence.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0035 data-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Silent `astype(str)` / implicit CSV inference corrupts IDs (`"00123"` vs `123`) and join keys.
- Retrying non-idempotent INSERT doubles rows; need natural key + MERGE/upsert or sink truncate-by-partition.
- Producer/consumer schema drift without `schema_version` or contract test breaks downstream silently.
- Full-table transforms without sampled dry-run hide bad rows until prod SLAs fire.
- Timezone-naive timestamps shift across deploy regions; mix of `timestamp` vs `timestamptz` skews windows.
- UTF-8 vs Latin-1 / BOM in CSV flips columns or injects nulls; parquet writer version mismatches drop logical types.
- Null-vs-empty-string conflation drops rows in “required” checks or fan-out joins.
- Partition overwrite with wrong grain deletes adjacent data.
- Do not use outside **Data engineering** (route `/cat-data` or `/opgrok`).
### Anti-patterns
- Writing production sinks without a dry-run path and counted rejects
- Casting all columns to string “to be safe”
- Deleting rejected rows instead of quarantine + reason
- `ON CONFLICT DO NOTHING` without measuring skipped volume
- Schema-on-read with no contract test in CI
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable satisfies the brief under **audit** for **Data engineering**.
- All checklist items scored; FAILs carry path:line or command evidence.
- `WIN: PASS` only with concrete counts, schema refs, and reject handling proof.
- Downstream SuperGroks can consume outputs without re-deriving contracts.

## Optional Tool Surface
- `pydantic` / `jsonschema` / `pandera` / `pyarrow` schema checks
- `duckdb -c` / `polars` / `pandas` count & dtype probes; `qsv stats`, `xsv count`, `csvcut -n`
- `parquet-tools schema` / `pyarrow.parquet.read_schema`
- Pipeline dry-run flags (dbt `test`/`build --empty`, Spark `limit`, Airflow dry-run where present)
- SQL `EXPLAIN` only when db-backed (else escalate `db`)
- Agent: read_file, run_terminal_command, search_replace
- Binary: `opgrok.sg.data-audit`

## References
- `core/skills/data/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

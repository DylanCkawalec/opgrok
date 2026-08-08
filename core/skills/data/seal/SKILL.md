---
name: data-seal
description: >
  Finalizes data pipelines and ETL artifacts: freezes schemas, locks dry-run
  counts/rejects, and marks outputs handoff-ready. Use when sealing CSV→JSON
  maps, schema-validated transforms, or null/reject quarantine paths, or on
  /data-seal. Differentiator: treats silent coercion and uncounted row loss as
  seal blockers—acceptance requires fixture dry-run deltas plus versioned schema.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Data engineering · finalize"
  category: data
  tier: frontier
  sg_id: sg-0036
  binary_id: opgrok.sg.data-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "data/seal (finalize): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently."
  purpose: "Build and fix data pipelines and schemas. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform."
  intent_tags: [data, seal, frontier, finalize]
  path: core/skills/data/seal/SKILL.md
  call: /data-seal
---

# Data engineering Sealer (`/data-seal`)

**Agent Identity**: Ari-8ae8567ef4fc1bfbe54262d3137f3f16d0dd8f534429ab4430752d4405272ae1

## Core Mandate / Invariants
- Domain: pipelines, ETL, schemas, quality checks, structured extract/transform.
- Method (**seal/finalize**): verify win gate → freeze schemas & sample outputs → mark handoff-ready.
- Explicit schemas only; silent type coercion is a defect, not a convenience.
- Boundary validation required (ingress + egress); rejects quarantine, never drop.
- Prefer idempotent steps; side-effecting loads stay behind dry-run gates.
- Evidence over assertion: every claim ties to command output or repo artifact.
- Stay in data; escalate mesh/orchestration to `/opgrok`, persistence design to `db`.

## Procedural Workflow
### Domain procedure
1. Pin I/O contracts: field map, types, null policy, volume assumptions, schema version.
2. Implement transform with validators at boundaries (pydantic/jsonschema/avro).
3. Fixture dry-run before full pass; capture row in/out/reject counts and sample paths.

### Role method (seal)
1. Freeze acceptance bundle: versioned schema + dry-run count table + reject quarantine path.
2. Prove no silent loss: `wc -l` / `duckdb -c "SELECT count(*)…"` / `parquet-tools rowcount` on fixture vs output; delta must match documented rejects.
3. Gate loads: confirm sink writes are off or `--dry-run` equivalent; attach sample output paths only.
4. WIN with evidence block (below).

### Eval dimensions
- Schema fidelity (declared vs observed types/nulls)
- Data-loss risk (uncounted drops, coercion of keys)
- Idempotency (re-run safe or explicitly gated)
- Dry-run evidence (counts + samples attached)

### Close
1. Verify: win-gate evidence present—schema validation green and pipeline dry-run on sample. On failure, one fix pass or escalate to `db`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0036 data-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- String↔int id coercion breaks joins downstream; seal fails if key types drift.
- Retrying non-idempotent INSERT/COPY doubles rows; require natural key or merge semantics.
- Producer/consumer schema drift without `schema_version` (or Avro/Protobuf subject) is a handoff blocker.
- Full-table runs without fixture sampling hide bad rows until prod.
- Timezone-naive timestamps shift across deploy regions; pin UTC or offset at boundary.
- CSV dialect traps (sep, quoting, BOM) change column counts silently—validate header hash.
- Parquet/ORC dictionary encoding can mask null-rate surprises; check null counts explicitly.
- Do not use outside **data engineering** (route `/cat-data` or `/opgrok`).

### Anti-patterns
- Writing production sinks without a dry-run path and count delta
- `astype(str)` / blanket cast of all columns
- Deleting rejects instead of quarantine + reason codes
- “Schema optional” JSON blobs as sealed contracts
- Sealing on green unit tests alone with zero row-count evidence
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches brief under **seal** for data engineering.
- Invariants hold; verification = frozen schema + sample dry-run counts/rejects.
- `WIN: PASS` with concrete evidence paths/commands.
- Downstream SuperGroks consume outputs with no clarification on types, nulls, or volumes.

## Optional Tool Surface
- `pydantic` / `jsonschema` / `fastavro` validators; `pyarrow` schema inspect
- `duckdb -c` counts & casts; `csvcut`/`csvstat` (csvkit); `parquet-tools schema|rowcount`
- `jq 'length'` / `head`/`tail` on JSON/JSONL fixtures; pipeline `--dry-run` flags
- `great_expectations` or dbt `test` when repo already uses them
- SQL `EXPLAIN` only if db-backed (else escalate `db`)
- Agent tools: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.data-seal`

## References
- `core/skills/data/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

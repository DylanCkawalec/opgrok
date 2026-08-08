---
name: db-trace
description: >
  Traces database failures and regressions through a symptom→evidence→root→fix chain across SQL, migrations, indexes, and query plans. Activates on slow queries, failed migrations, lock contention, missing/unused indexes, or /db-trace. Differentiator: refuses ungrounded DROP and indexes not justified by EXPLAIN shape or workload evidence.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Databases · RCA"
  category: db
  tier: core
  sg_id: sg-0040
  binary_id: opgrok.sg.db-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "db/trace (RCA): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented."
  purpose: "Design and fix database schemas and queries. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: SQL, migrations, indexes, query performance."
  intent_tags: [db, trace, core, RCA]
  path: core/skills/db/trace/SKILL.md
  call: /db-trace
---

# Databases Tracer (`/db-trace`)

**Agent Identity**: Ashanti-ce051a8841a9e92cb13727e5357b04c2f185239e9915bc645b7491fc60983d80

## Core Mandate / Invariants
- Domain: **Databases** — SQL dialects, forward migrations, indexes, plans, locks, constraints.
- Method (**RCA**): symptom → evidence → root → fix; every claim needs plan output, migration log, or schema proof.
- Migrations are forward-only; reversible only when repo convention already supports down/rollback.
- Indexes require query-shape justification (filter/join/order columns + selectivity), never “add index and hope.”
- No DROP/TRUNCATE/CASCADE without explicit user confirmation and a restore path.
- Prefer minimal schema delta; do not rewrite healthy tables to paper over a bad query.
- Stay in db; escalate cross-domain data pipelines to `data` or mesh via `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Map schema surface: read `migrations/`, `schema.rb`/`structure.sql`, or `\d`/`SHOW CREATE` equivalents; note FKs, uniques, partial indexes.
2. Capture the failing artifact: slow SQL, migration error, lock wait, or constraint violation — with bind params redacted.
3. Produce the smallest forward change (migration or query rewrite) with lock/timeout strategy noted for large tables.

### Role method (trace)
1. **Symptom**: pin latency, error, or drift (e.g. p95 spike, `deadlock detected`, alembic/flyway revision fail).
2. **Evidence (domain)**: run `EXPLAIN (ANALYZE, BUFFERS)` / `EXPLAIN ANALYZE` on the hot query; for migrations, dry-run (`alembic upgrade --sql`, `flyway info`, `diesel migration list`, `sqlx migrate info`) and capture lock type.
3. **Root**: classify — seq scan on large table, missing/wrong composite order, skew stats, long TX holding locks, NOT VALID FK, ORM N+1, or irreversible column type change.
4. **Fix (domain)**: emit justified index (`CREATE INDEX CONCURRENTLY` where supported), rewrite predicate to be sargable, or forward migration with explicit `ON DELETE`/`NOT NULL`/`DEFAULT` behavior; never silent DROP.
5. Re-verify: second `EXPLAIN (ANALYZE, BUFFERS)` or migration dry path shows the causal link closed.

### Close
1. Causal chain complete with before/after plan or migration evidence. On residual failure, one bounded retry then escalate to `data`/`/opgrok`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0040 db-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Missing indexes on join/filter/ORDER BY columns → prod latency cliffs under real cardinality.
- Non-CONCURRENT index builds and unbatched rewrites take AccessExclusive locks and stall writers.
- ORMs mask N+1 and cartesian joins until load; always inspect generated SQL.
- Partial/expression indexes help only when predicates match exactly; mismatch = dead weight.
- Nullable UNIQUE treats NULLs as distinct → silent duplicate business keys; empty-string vs NULL duals same class of bug.
- Adding FK without `NOT VALID` / validate split can rewrite-scan huge tables in one TX.
- Stats drift (autovacuum lag) makes plans lie; `ANALYZE` before trusting a single EXPLAIN.
- Do not use outside **Databases** (route `/cat-db` or `/opgrok`).
### Anti-patterns
- `SELECT *` on hot paths or wide rows over the wire
- Unreviewed `DROP COLUMN` / `DROP TABLE` in prod migrations
- Indexes on boolean/low-cardinality columns without partial predicate or proven selectivity
- Composite index column order that ignores equality-then-range access
- Shipping N+1 or unbounded `IN (...)` lists without calling them out
- “Fix” via blanket `SET enable_seqscan = off` or session GUCs in app code
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable satisfies the brief under **trace** for **Databases**.
- Invariants hold; before/after EXPLAIN or migration dry-run evidence closes the chain.
- `WIN: PASS` with concrete paths/commands; `WIN: FAIL` states blocker and next owner.
- Downstream SuperGroks can apply the migration/query without clarification.

## Optional Tool Surface
- Migration runners: `alembic upgrade --sql`, `flyway info`/`migrate`, `diesel migration list`, `sqlx migrate info`
- Plans: `EXPLAIN (ANALYZE, BUFFERS)`, `EXPLAIN ANALYZE`, `EXPLAIN FORMAT=JSON` (read-only preferred)
- Schema: migrations folder, `pg_dump -s`, `sqlite3 .schema`, vendor `\d`/`SHOW CREATE TABLE`
- Lint: `sqlfluff lint` when configured
- Agent: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.db-trace`

## References
- `core/skills/db/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

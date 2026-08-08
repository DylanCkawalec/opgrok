---
name: db-forge
description: >
  Designs and hardens SQL schemas, forward migrations, indexes, and query paths
  via the forge method: ship the full e2e data path first, then lock edges.
  Activates on migration/index/query work or /db-forge. Differentiator: refuses
  ungrounded DROP and indexes lacking EXPLAIN or query-shape proof.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Databases · e2e path"
  category: db
  tier: advanced
  sg_id: sg-0038
  binary_id: opgrok.sg.db-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "db/forge (e2e path): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented."
  purpose: "Design and fix database schemas and queries. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: SQL, migrations, indexes, query performance."
  intent_tags: [db, forge, advanced, e2e-path]
  path: core/skills/db/forge/SKILL.md
  call: /db-forge
---

# Databases Forger (`/db-forge`)

**Agent Identity**: Armani-88a9220a8f77840f9b3a13a7584462b30a94bd39e89577f40768e4e37b38114d

## Core Mandate / Invariants
- Domain: **Databases** — SQL DDL/DML, migrations, indexes, query plans, FK/constraint design.
- Method (**forge / e2e path**): map app → tables → indexes → migration → verify plan; harden edges only after the path runs.
- Evidence over assertion: every index or rewrite needs EXPLAIN/ANALYZE output, migration dry-run, or repo query proof.
- Migrations forward-only; reversible when project convention supports down/rollback scripts.
- No DROP/TRUNCATE/CASCADE without explicit user confirmation and backup/restore path stated.
- Indexes justified by filter/join/order shape and cardinality — never cargo-cult.
- Stay in db; escalate multi-domain or mesh work to `/cat-db` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Inventory schema: read migrations folder, `schema.rb`/`structure.sql`, or `\d`/`SHOW CREATE` dumps; note existing indexes and FKs.
2. Capture hot paths: grep app for raw SQL/ORM queries touching target tables; note WHERE/JOIN/ORDER columns.
3. Draft change: forward migration + rollback notes; document ON DELETE/UPDATE and nullability choices.

### Role method (forge)
1. Map each app query path to concrete tables/columns; list missing indexes or constraint gaps before writing DDL.
2. Author migration with lock-aware DDL (e.g. `CREATE INDEX CONCURRENTLY` on Postgres large tables; avoid long ACCESS EXCLUSIVE where possible).
3. Ship code path that actually uses the new column/index/FK in the same change set — no orphan schema.
4. Verify: `EXPLAIN (ANALYZE, BUFFERS)` or engine equivalent on before/after; run migration dry-run (`alembic upgrade --sql`, `flyway info`, `diesel migration run` in safe env, `sqlx migrate run`); assert no seq-scan cliffs on hot filters.
5. Harden edges only after e2e path is green: partial/covering indexes, check constraints, NOT NULL backfills in batches.

### Close
1. Confirm migration applies cleanly, rollback path exists or is explicitly waived, indexes match proven query shapes.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0038 db-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Missing indexes on join/filter/FK columns → prod latency cliffs under load; always pair new FKs with supporting indexes unless engine auto-creates.
- Long-running migrations without lock strategy (non-CONCURRENTLY, table rewrites) block writers on large tables.
- ORMs mask N+1 and implicit SELECT *; surface them before claiming “query fixed.”
- Backfilling NOT NULL on populated columns without batched UPDATE + default strategy locks or fails.
- Unique constraints on nullable columns allow multiple NULLs (engine-dependent); empty-string vs NULL duals create silent dups.
- Partial indexes and expression indexes help only when queries match the predicate/expression exactly.
- Do not use for non-db work (analytics pipelines, app business logic without schema impact) — route via `/cat-db` or `/opgrok`.

### Anti-patterns
- SELECT * on hot paths or wide rows
- Unreviewed DROP COLUMN / DROP TABLE in prod-bound migrations
- Indexes on low-cardinality flags (boolean, status enum) without partial predicate or EXPLAIN proof
- Adding indexes “just in case” with no query referencing the leading column
- Mixing destructive data fixups inside schema migrations without explicit approval
- Blind `CASCADE` on FK delete without documenting dependent row fate

## Definition of Done
- Deliverable matches brief under forge e2e path for Databases.
- Migration is forward-safe; destructive ops confirmed or absent; indexes tied to EXPLAIN or concrete query evidence.
- `WIN: PASS` with evidence (migration paths, EXPLAIN snippets, commands run).
- Downstream agents can apply or review without clarifying schema intent.

## Optional Tool Surface
- Migration runners: `alembic upgrade head` / `alembic upgrade --sql`, `flyway migrate`, `diesel migration run`, `sqlx migrate run`, `rails db:migrate`
- Plans: `EXPLAIN (ANALYZE, BUFFERS)`, `EXPLAIN ANALYZE`, `EXPLAIN FORMAT=JSON`
- Lint/format: `sqlfluff lint`, `pg_format` when configured
- Inspect: migrations dir, `pg_indexes`/`sqlite_master`, schema dumps
- Agent tools: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.db-forge`

## References
- `core/skills/db/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

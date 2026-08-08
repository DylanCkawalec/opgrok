# SuperGrok Agent Glossary (full coverage)

Generated: 2026-08-08T18:51:28.359155+00:00

Total skills: **178**  
Kinds: core=2, navigator=25, special=1, supergrok=150

Order: alphabetical by skill `name` (slash command without `/`).

---

## Core entry points

### `leslie`
- **call:** `/leslie` · **path:** `core/skills/leslie/SKILL.md`
- **intent:** Authors falsifiable Winning Conditions and refusal gates for OPGROK harness packages and SuperGrok catalog law. Activates on /leslie, harness sealing, catalog validation, WC authorship, or specification gates. Differentiator: specifies admi
- **purpose:** Authors falsifiable Winning Conditions and refusal gates for OPGROK harness packages and SuperGrok catalog law. Activates on /leslie, harness sealing, catalog validation, WC authorship, or specification gates. Differentiator: specifies admi

### `opgrok`
- **call:** `/opgrok` · **path:** `core/skills/opgrok/SKILL.md`
- **intent:** Builds a sealed SuperGrok multi-agent harness from a natural-language goal: selects specialists, locks a Leslie Winning Condition, emits graph.json + one bin/opgrok-<slug> binary + one README, then executes dry-run or live multi-node Grok A
- **purpose:** Builds a sealed SuperGrok multi-agent harness from a natural-language goal: selects specialists, locks a Leslie Winning Condition, emits graph.json + one bin/opgrok-<slug> binary + one README, then executes dry-run or live multi-node Grok A

## Special skills

### `meta-asset-creator`
- **call:** `/meta-asset-creator` · **path:** `core/skills/meta/asset-creator/SKILL.md`
- **intent:** Owns the OPGROK Grok/xAI visual system under assets/: design tokens, deterministic SVG generation, and Grok Imagine atmospheric PNGs. Use for brand kits, UI icons, GitHub banners, empty states, protocol art, or /meta-asset-creator. Exact lo
- **purpose:** Owns the OPGROK Grok/xAI visual system under assets/: design tokens, deterministic SVG generation, and Grok Imagine atmospheric PNGs. Use for brand kits, UI icons, GitHub banners, empty states, protocol art, or /meta-asset-creator. Exact lo

## Category navigators

- `/cat-agent` → `core/skills/agent/SKILL.md` — Index 6 agent specialists for multi-agent routing and mesh.
- `/cat-binary` → `core/skills/binary/SKILL.md` — Index 6 binary specialists for native binaries, packaging, FFI.
- `/cat-code` → `core/skills/code/SKILL.md` — Index 6 code specialists for application code, modules, refactors.
- `/cat-data` → `core/skills/data/SKILL.md` — Index 6 data specialists for pipelines, ETL, schemas.
- `/cat-db` → `core/skills/db/SKILL.md` — Index 6 db specialists for SQL, migrations, query performance.
- `/cat-debug` → `core/skills/debug/SKILL.md` — Index 6 debug specialists for root-cause analysis, minimal fixes.
- `/cat-devops` → `core/skills/devops/SKILL.md` — Index 6 devops specialists for CI/CD, containers, deploy.
- `/cat-docs` → `core/skills/docs/SKILL.md` — Index 6 docs specialists for README, API docs, runbooks.
- `/cat-eval` → `core/skills/eval/SKILL.md` — Index 6 eval specialists for rubrics, judges, harnesses.
- `/cat-math` → `core/skills/math/SKILL.md` — Index 6 math specialists for algorithms, numerics, formal reasoning.
- `/cat-mcp` → `core/skills/mcp/SKILL.md` — Index 6 mcp specialists for MCP servers, schemas, discovery.
- `/cat-meta` → `core/skills/meta/SKILL.md` — Index 6 meta specialists for skill authoring, registry, asset systems.
- `/cat-plan` → `core/skills/plan/SKILL.md` — Index 6 plan specialists for design docs, ADRs, PR plans.
- `/cat-product` → `core/skills/product/SKILL.md` — Index 6 product specialists for specs, prioritization, requirements.
- `/cat-python` → `core/skills/python/SKILL.md` — Index 6 python specialists for Python packages, typing, async.
- `/cat-research` → `core/skills/research/SKILL.md` — Index 6 research specialists for multi-source grounded research.
- `/cat-review` → `core/skills/review/SKILL.md` — Index 6 review specialists for code and design review.
- `/cat-rust` → `core/skills/rust/SKILL.md` — Index 6 rust specialists for Rust crates, ownership, cargo.
- `/cat-security` → `core/skills/security/SKILL.md` — Index 6 security specialists for threat models, defensive audits.
- `/cat-test` → `core/skills/test/SKILL.md` — Index 6 test specialists for unit/integration/e2e tests.
- `/cat-tool` → `core/skills/tool/SKILL.md` — Index 6 tool specialists for CLI/API/browser tool orchestration.
- `/cat-ui` → `core/skills/ui/SKILL.md` — Index 6 ui specialists for interfaces, a11y, interaction states.
- `/cat-vision` → `core/skills/vision/SKILL.md` — Index 6 vision specialists for image/UI multimodal understanding.
- `/cat-web` → `core/skills/web/SKILL.md` — Index 6 web specialists for HTTP APIs, frontends, auth edges.
- `/cat-workflow` → `core/skills/workflow/SKILL.md` — Index 6 workflow specialists for n8n/DAG/pipeline automation.

---

## SuperGroks (alphabetical)

### 1. `agent-audit`
- **sg_id:** `sg-0101`
- **path:** `core/skills/agent/audit/SKILL.md`
- **nest:** `agent/audit`
- **call:** `/agent-audit` · binary `opgrok.sg.agent-audit`
- **category / role / tier:** `agent` / `audit` / `frontier`
- **intent:** agent/audit (checklist): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run.
- **purpose:** Plan and run multi-agent SuperGrok compositions. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- **when:** Audits multi-agent SuperGrok meshes against an explicit hire/graph/WC checklist, scoring PASS/FAIL with path evidence and Name-Hash peer resolution. Use when co

### 2. `agent-forge`
- **sg_id:** `sg-0098`
- **path:** `core/skills/agent/forge/SKILL.md`
- **nest:** `agent/forge`
- **call:** `/agent-forge` · binary `opgrok.sg.agent-forge`
- **category / role / tier:** `agent` / `forge` / `advanced`
- **intent:** agent/forge (e2e path): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run.
- **purpose:** Plan and run multi-agent SuperGrok compositions. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- **when:** Composes multi-agent SuperGrok meshes end-to-end: role graph, Name-Hash peer resolution, thrift context packs, and Leslie WC seal. Use when building a harness, 

### 3. `agent-scout`
- **sg_id:** `sg-0099`
- **path:** `core/skills/agent/scout/SKILL.md`
- **nest:** `agent/scout`
- **call:** `/agent-scout` · binary `opgrok.sg.agent-scout`
- **category / role / tier:** `agent` / `scout` / `frontier`
- **intent:** agent/scout (map): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run.
- **purpose:** Plan and run multi-agent SuperGrok compositions. Method (map): map structure and constraints before committing to edits. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- **when:** Maps multi-agent SuperGrok meshes before any hire: resolves peers by Name-Hash, drafts thrift context packs, and gates composition on Leslie WC. Use when compos

### 4. `agent-seal`
- **sg_id:** `sg-0102`
- **path:** `core/skills/agent/seal/SKILL.md`
- **nest:** `agent/seal`
- **call:** `/agent-seal` · binary `opgrok.sg.agent-seal`
- **category / role / tier:** `agent` / `seal` / `frontier`
- **intent:** agent/seal (finalize): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run.
- **purpose:** Plan and run multi-agent SuperGrok compositions. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- **when:** Finalizes multi-agent SuperGrok meshes: verifies Leslie WC, freezes harness artifacts, resolves peers by Name-Hash, and marks handoff-ready. Use when sealing a 

### 5. `agent-smith`
- **sg_id:** `sg-0097`
- **path:** `core/skills/agent/smith/SKILL.md`
- **nest:** `agent/smith`
- **call:** `/agent-smith` · binary `opgrok.sg.agent-smith`
- **category / role / tier:** `agent` / `smith` / `core`
- **intent:** agent/smith (build unit): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run.
- **purpose:** Plan and run multi-agent SuperGrok compositions. Method (build unit): build the smallest correct unit that meets the brief. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- **when:** Builds the smallest SuperGrok mesh unit that satisfies a multi-agent brief: role graph, Name-Hash hires, IPO contracts, and thrift context packs. Use when compo

### 6. `agent-trace`
- **sg_id:** `sg-0100`
- **path:** `core/skills/agent/trace/SKILL.md`
- **nest:** `agent/trace`
- **call:** `/agent-trace` · binary `opgrok.sg.agent-trace`
- **category / role / tier:** `agent` / `trace` / `frontier`
- **intent:** agent/trace (RCA): Compose a 6-node harness for a landing page goal; Route a goal to category roles with I/O contracts; Build a thrifty context pack for a mesh run.
- **purpose:** Plan and run multi-agent SuperGrok compositions. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: multi-agent routing, mesh plans, SuperGrok composition, context thrift.
- **when:** Traces multi-agent SuperGrok failures via RCA: symptom → evidence → root → fix across mesh plans, routing graphs, and thrift context packs. Use when a harness n

### 7. `binary-audit`
- **sg_id:** `sg-0095`
- **path:** `core/skills/binary/audit/SKILL.md`
- **nest:** `binary/audit`
- **call:** `/binary-audit` · binary `opgrok.sg.binary-audit`
- **category / role / tier:** `binary` / `audit` / `advanced`
- **intent:** binary/audit (checklist): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks.
- **purpose:** Build and package native binaries. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: Rust/native binaries, packaging, FFI, release artifacts.
- **when:** Audits Rust/native binaries, packaging, FFI boundaries, and release artifacts against an explicit pass/fail checklist with path evidence. Use when verifying CLI

### 8. `binary-forge`
- **sg_id:** `sg-0092`
- **path:** `core/skills/binary/forge/SKILL.md`
- **nest:** `binary/forge`
- **call:** `/binary-forge` · binary `opgrok.sg.binary-forge`
- **category / role / tier:** `binary` / `forge` / `advanced`
- **intent:** binary/forge (e2e path): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks.
- **purpose:** Build and package native binaries. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: Rust/native binaries, packaging, FFI, release artifacts.
- **when:** Forges Rust/native release binaries end-to-end: workspace build, version embedding, FFI boundary hardening, strip/checksum packaging, and --help/version smoke b

### 9. `binary-scout`
- **sg_id:** `sg-0093`
- **path:** `core/skills/binary/scout/SKILL.md`
- **nest:** `binary/scout`
- **call:** `/binary-scout` · binary `opgrok.sg.binary-scout`
- **category / role / tier:** `binary` / `scout` / `frontier`
- **intent:** binary/scout (map): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks.
- **purpose:** Build and package native binaries. Method (map): map structure and constraints before committing to edits. Domain: Rust/native binaries, packaging, FFI, release artifacts.
- **when:** Maps Rust/native binary layout, Cargo bin targets, FFI boundaries, and release packaging constraints before any edit. Activates on CLI subcommand/--help work, r

### 10. `binary-seal`
- **sg_id:** `sg-0096`
- **path:** `core/skills/binary/seal/SKILL.md`
- **nest:** `binary/seal`
- **call:** `/binary-seal` · binary `opgrok.sg.binary-seal`
- **category / role / tier:** `binary` / `seal` / `frontier`
- **intent:** binary/seal (finalize): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks.
- **purpose:** Build and package native binaries. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: Rust/native binaries, packaging, FFI, release artifacts.
- **when:** Finalizes Rust/native binary deliverables: freezes release artifacts, verifies CLI --help/version smoke, checksums, and FFI boundary docs before handoff. Activa

### 11. `binary-smith`
- **sg_id:** `sg-0091`
- **path:** `core/skills/binary/smith/SKILL.md`
- **nest:** `binary/smith`
- **call:** `/binary-smith` · binary `opgrok.sg.binary-smith`
- **category / role / tier:** `binary` / `smith` / `core`
- **intent:** binary/smith (build unit): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks.
- **purpose:** Build and package native binaries. Method (build unit): build the smallest correct unit that meets the brief. Domain: Rust/native binaries, packaging, FFI, release artifacts.
- **when:** Builds and packages Rust/native binaries, FFI boundaries, and release artifacts as the smallest correct unit that meets the brief. Activates on CLI subcommands 

### 12. `binary-trace`
- **sg_id:** `sg-0094`
- **path:** `core/skills/binary/trace/SKILL.md`
- **nest:** `binary/trace`
- **call:** `/binary-trace` · binary `opgrok.sg.binary-trace`
- **category / role / tier:** `binary` / `trace` / `core`
- **intent:** binary/trace (RCA): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks.
- **purpose:** Build and package native binaries. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: Rust/native binaries, packaging, FFI, release artifacts.
- **when:** Traces Rust/native binary failures from build symptom through link/FFI evidence to root cause and fix. Use for CLI subcommands, release packaging, --help/versio

### 13. `code-audit`
- **sg_id:** `sg-0005`
- **path:** `core/skills/code/audit/SKILL.md`
- **nest:** `code/audit`
- **call:** `/code-audit` · binary `opgrok.sg.code-audit`
- **category / role / tier:** `code` / `audit` / `advanced`
- **intent:** code/audit (checklist): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors.
- **purpose:** Implement and change application code. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: application code, modules, refactors, APIs.
- **when:** Audits and lands application code, modules, refactors, and APIs by explicit checklist: each item scored PASS/FAIL with path:line evidence. Triggers on /code-aud

### 14. `code-forge`
- **sg_id:** `sg-0002`
- **path:** `core/skills/code/forge/SKILL.md`
- **nest:** `code/forge`
- **call:** `/code-forge` · binary `opgrok.sg.code-forge`
- **category / role / tier:** `code` / `forge` / `advanced`
- **intent:** code/forge (e2e path): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors.
- **purpose:** Implement and change application code. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: application code, modules, refactors, APIs.
- **when:** Implements application code, modules, refactors, and APIs by forging the full vertical slice first, then hardening edges. Activates on /code-forge and tasks lik

### 15. `code-scout`
- **sg_id:** `sg-0003`
- **path:** `core/skills/code/scout/SKILL.md`
- **nest:** `code/scout`
- **call:** `/code-scout` · binary `opgrok.sg.code-scout`
- **category / role / tier:** `code` / `scout` / `frontier`
- **intent:** code/scout (map): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors.
- **purpose:** Implement and change application code. Method (map): map structure and constraints before committing to edits. Domain: application code, modules, refactors, APIs.
- **when:** Maps package graph, public surfaces, and call-site constraints before any code edit. Activates for scoped construction—pure functions + tests, stable-export ref

### 16. `code-seal`
- **sg_id:** `sg-0006`
- **path:** `core/skills/code/seal/SKILL.md`
- **nest:** `code/seal`
- **call:** `/code-seal` · binary `opgrok.sg.code-seal`
- **category / role / tier:** `code` / `seal` / `frontier`
- **intent:** code/seal (finalize): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors.
- **purpose:** Implement and change application code. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: application code, modules, refactors, APIs.
- **when:** Finalizes application code units—modules, pure functions, API handlers, boundary refactors—by verifying the win gate, freezing the diff, and marking handoff-rea

### 17. `code-smith`
- **sg_id:** `sg-0001`
- **path:** `core/skills/code/smith/SKILL.md`
- **nest:** `code/smith`
- **call:** `/code-smith` · binary `opgrok.sg.code-smith`
- **category / role / tier:** `code` / `smith` / `core`
- **intent:** code/smith (build unit): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors.
- **purpose:** Implement and change application code. Method (build unit): build the smallest correct unit that meets the brief. Domain: application code, modules, refactors, APIs.
- **when:** Implements application code, modules, refactors, and APIs by shipping the smallest reversible build unit that satisfies the brief with call-site awareness. Acti

### 18. `code-trace`
- **sg_id:** `sg-0004`
- **path:** `core/skills/code/trace/SKILL.md`
- **nest:** `code/trace`
- **call:** `/code-trace` · binary `opgrok.sg.code-trace`
- **category / role / tier:** `code` / `trace` / `core`
- **intent:** code/trace (RCA): Add a pure function + unit tests without touching the HTTP layer; Refactor a module boundary while keeping the public export stable; Implement one API handler with request validation and typed errors.
- **purpose:** Implement and change application code. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: application code, modules, refactors, APIs.
- **when:** Traces application defects and changes through symptom → evidence → root → fix, delivering the smallest reversible unit with call-site awareness. Activates on /

### 19. `data-audit`
- **sg_id:** `sg-0035`
- **path:** `core/skills/data/audit/SKILL.md`
- **nest:** `data/audit`
- **call:** `/data-audit` · binary `opgrok.sg.data-audit`
- **category / role / tier:** `data` / `audit` / `advanced`
- **intent:** data/audit (checklist): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently.
- **purpose:** Build and fix data pipelines and schemas. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform.
- **when:** Audits ETL/ELT pipelines, schemas, and structured transforms via explicit checklist scoring: schema contracts, dry-run counts, reject quarantine, idempotency, a

### 20. `data-forge`
- **sg_id:** `sg-0032`
- **path:** `core/skills/data/forge/SKILL.md`
- **nest:** `data/forge`
- **call:** `/data-forge` · binary `opgrok.sg.data-forge`
- **category / role / tier:** `data` / `forge` / `advanced`
- **intent:** data/forge (e2e path): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently.
- **purpose:** Build and fix data pipelines and schemas. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform.
- **when:** Builds and hardens ETL/ELT pipelines, schemas, and quality gates via the forge method: wire the full source→stages→sink path first, then harden edges with bound

### 21. `data-scout`
- **sg_id:** `sg-0033`
- **path:** `core/skills/data/scout/SKILL.md`
- **nest:** `data/scout`
- **call:** `/data-scout` · binary `opgrok.sg.data-scout`
- **category / role / tier:** `data` / `scout` / `frontier`
- **intent:** data/scout (map): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently.
- **purpose:** Build and fix data pipelines and schemas. Method (map): map structure and constraints before committing to edits. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform.
- **when:** Maps pipeline topology, schemas, volume assumptions, and reject paths before any ETL edit. Activates on schema-first inventory, dry-run count planning, CSV/Parq

### 22. `data-seal`
- **sg_id:** `sg-0036`
- **path:** `core/skills/data/seal/SKILL.md`
- **nest:** `data/seal`
- **call:** `/data-seal` · binary `opgrok.sg.data-seal`
- **category / role / tier:** `data` / `seal` / `frontier`
- **intent:** data/seal (finalize): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently.
- **purpose:** Build and fix data pipelines and schemas. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform.
- **when:** Finalizes data pipelines and ETL artifacts: freezes schemas, locks dry-run counts/rejects, and marks outputs handoff-ready. Use when sealing CSV→JSON maps, sche

### 23. `data-smith`
- **sg_id:** `sg-0031`
- **path:** `core/skills/data/smith/SKILL.md`
- **nest:** `data/smith`
- **call:** `/data-smith` · binary `opgrok.sg.data-smith`
- **category / role / tier:** `data` / `smith` / `core`
- **intent:** data/smith (build unit): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently.
- **purpose:** Build and fix data pipelines and schemas. Method (build unit): build the smallest correct unit that meets the brief. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform.
- **when:** Builds the smallest correct ETL/transform unit with explicit schemas, boundary validation, and dry-run row/reject counts. Activates for pipeline steps, CSV↔JSON

### 24. `data-trace`
- **sg_id:** `sg-0034`
- **path:** `core/skills/data/trace/SKILL.md`
- **nest:** `data/trace`
- **call:** `/data-trace` · binary `opgrok.sg.data-trace`
- **category / role / tier:** `data` / `trace` / `core`
- **intent:** data/trace (RCA): Add an ETL step with schema validation and reject logging; Reshape CSV→JSON with explicit field map; Fix null handling that dropped rows silently.
- **purpose:** Build and fix data pipelines and schemas. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: pipelines, ETL, schemas, quality checks, structured extract/transform.
- **when:** Root-causes broken ETL/transform paths by chaining symptom row → stage evidence → schema/coercion root → gated fix. Use for silent drops, type-drift keys, rejec

### 25. `db-audit`
- **sg_id:** `sg-0041`
- **path:** `core/skills/db/audit/SKILL.md`
- **nest:** `db/audit`
- **call:** `/db-audit` · binary `opgrok.sg.db-audit`
- **category / role / tier:** `db` / `audit` / `advanced`
- **intent:** db/audit (checklist): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented.
- **purpose:** Design and fix database schemas and queries. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: SQL, migrations, indexes, query performance.
- **when:** Audits SQL schemas, forward migrations, indexes, and query plans against an explicit pass/fail checklist with path:line evidence. Triggers on /db-audit, migrati

### 26. `db-forge`
- **sg_id:** `sg-0038`
- **path:** `core/skills/db/forge/SKILL.md`
- **nest:** `db/forge`
- **call:** `/db-forge` · binary `opgrok.sg.db-forge`
- **category / role / tier:** `db` / `forge` / `advanced`
- **intent:** db/forge (e2e path): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented.
- **purpose:** Design and fix database schemas and queries. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: SQL, migrations, indexes, query performance.
- **when:** Designs and hardens SQL schemas, forward migrations, indexes, and query paths via the forge method: ship the full e2e data path first, then lock edges. Activate

### 27. `db-scout`
- **sg_id:** `sg-0039`
- **path:** `core/skills/db/scout/SKILL.md`
- **nest:** `db/scout`
- **call:** `/db-scout` · binary `opgrok.sg.db-scout`
- **category / role / tier:** `db` / `scout` / `frontier`
- **intent:** db/scout (map): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented.
- **purpose:** Design and fix database schemas and queries. Method (map): map structure and constraints before committing to edits. Domain: SQL, migrations, indexes, query performance.
- **when:** Maps schema topology, migration history, lock risk, and query shapes before any DDL or index change. Activates on forward migrations, slow-query triage, FK/ON D

### 28. `db-seal`
- **sg_id:** `sg-0042`
- **path:** `core/skills/db/seal/SKILL.md`
- **nest:** `db/seal`
- **call:** `/db-seal` · binary `opgrok.sg.db-seal`
- **category / role / tier:** `db` / `seal` / `frontier`
- **intent:** db/seal (finalize): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented.
- **purpose:** Design and fix database schemas and queries. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: SQL, migrations, indexes, query performance.
- **when:** Finalizes SQL schemas, forward migrations, indexes, and query plans for handoff: verifies apply/rollback evidence, freezes migration paths, marks ready. Activat

### 29. `db-smith`
- **sg_id:** `sg-0037`
- **path:** `core/skills/db/smith/SKILL.md`
- **nest:** `db/smith`
- **call:** `/db-smith` · binary `opgrok.sg.db-smith`
- **category / role / tier:** `db` / `smith` / `core`
- **intent:** db/smith (build unit): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented.
- **purpose:** Design and fix database schemas and queries. Method (build unit): build the smallest correct unit that meets the brief. Domain: SQL, migrations, indexes, query performance.
- **when:** Designs and ships the smallest correct SQL unit—forward migrations, justified indexes, FK actions, query rewrites—against live schema and EXPLAIN evidence. Acti

### 30. `db-trace`
- **sg_id:** `sg-0040`
- **path:** `core/skills/db/trace/SKILL.md`
- **nest:** `db/trace`
- **call:** `/db-trace` · binary `opgrok.sg.db-trace`
- **category / role / tier:** `db` / `trace` / `core`
- **intent:** db/trace (RCA): Write a forward migration adding a column + index; Fix a slow query with a justified index; Add a foreign key with ON DELETE behavior documented.
- **purpose:** Design and fix database schemas and queries. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: SQL, migrations, indexes, query performance.
- **when:** Traces database failures and regressions through a symptom→evidence→root→fix chain across SQL, migrations, indexes, and query plans. Activates on slow queries, 

### 31. `debug-audit`
- **sg_id:** `sg-0047`
- **path:** `core/skills/debug/audit/SKILL.md`
- **nest:** `debug/audit`
- **call:** `/debug-audit` · binary `opgrok.sg.debug-audit`
- **category / role / tier:** `debug` / `audit` / `advanced`
- **intent:** debug/audit (checklist): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift).
- **purpose:** Find root cause and apply minimal fixes. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: failures, logs, reproducers, root cause.
- **when:** Audits failures, logs, and reproducers into a scored RCA checklist: every claim must map to path:line or command output before a fix is allowed. Activates on cr

### 32. `debug-forge`
- **sg_id:** `sg-0044`
- **path:** `core/skills/debug/forge/SKILL.md`
- **nest:** `debug/forge`
- **call:** `/debug-forge` · binary `opgrok.sg.debug-forge`
- **category / role / tier:** `debug` / `forge` / `advanced`
- **intent:** debug/forge (e2e path): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift).
- **purpose:** Find root cause and apply minimal fixes. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: failures, logs, reproducers, root cause.
- **when:** Traces failures from symptom to minimal root fix via the forge method: assemble the full end-to-end repro path before touching edges. Use for RCA from stack tra

### 33. `debug-scout`
- **sg_id:** `sg-0045`
- **path:** `core/skills/debug/scout/SKILL.md`
- **nest:** `debug/scout`
- **call:** `/debug-scout` · binary `opgrok.sg.debug-scout`
- **category / role / tier:** `debug` / `scout` / `frontier`
- **intent:** debug/scout (map): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift).
- **purpose:** Find root cause and apply minimal fixes. Method (map): map structure and constraints before committing to edits. Domain: failures, logs, reproducers, root cause.
- **when:** Maps failure surface—stack, repro, env drift, module boundaries—before any edit, then drives symptom→evidence→root→minimal fix. Use for RCA from crash/stack to 

### 34. `debug-seal`
- **sg_id:** `sg-0048`
- **path:** `core/skills/debug/seal/SKILL.md`
- **nest:** `debug/seal`
- **call:** `/debug-seal` · binary `opgrok.sg.debug-seal`
- **category / role / tier:** `debug` / `seal` / `frontier`
- **intent:** debug/seal (finalize): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift).
- **purpose:** Find root cause and apply minimal fixes. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: failures, logs, reproducers, root cause.
- **when:** Finalizes Debugging & RCA work: locks repro evidence, verifies the win gate (failing command now green), freezes minimal root-cause fix, and marks handoff. Use 

### 35. `debug-smith`
- **sg_id:** `sg-0043`
- **path:** `core/skills/debug/smith/SKILL.md`
- **nest:** `debug/smith`
- **call:** `/debug-smith` · binary `opgrok.sg.debug-smith`
- **category / role / tier:** `debug` / `smith` / `core`
- **intent:** debug/smith (build unit): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift).
- **purpose:** Find root cause and apply minimal fixes. Method (build unit): build the smallest correct unit that meets the brief. Domain: failures, logs, reproducers, root cause.
- **when:** Isolates production failures to a single root site via repro-first RCA, then lands the smallest correct fix unit. Activates on crash stacks, flaky tests, CI-onl

### 36. `debug-trace`
- **sg_id:** `sg-0046`
- **path:** `core/skills/debug/trace/SKILL.md`
- **nest:** `debug/trace`
- **call:** `/debug-trace` · binary `opgrok.sg.debug-trace`
- **category / role / tier:** `debug` / `trace` / `core`
- **intent:** debug/trace (RCA): RCA a crash from a stack trace to a one-line root fix; Stabilize a flaky test by removing shared state; Find why CI fails when local passes (env drift).
- **purpose:** Find root cause and apply minimal fixes. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: failures, logs, reproducers, root cause.
- **when:** Traces production and test failures from symptom through hard evidence to a single root cause and minimal fix. Activates on crash stacks, flaky tests, CI-only f

### 37. `devops-audit`
- **sg_id:** `sg-0089`
- **path:** `core/skills/devops/audit/SKILL.md`
- **nest:** `devops/audit`
- **call:** `/devops-audit` · binary `opgrok.sg.devops-audit`
- **category / role / tier:** `devops` / `audit` / `advanced`
- **intent:** devops/audit (checklist): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback.
- **purpose:** Build and fix delivery and platform automation. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config.
- **when:** Audits CI/CD workflows, container images, deploy pipelines, and runbooks against an explicit pass/fail checklist with path:line evidence. Use when fixing GitHub

### 38. `devops-forge`
- **sg_id:** `sg-0086`
- **path:** `core/skills/devops/forge/SKILL.md`
- **nest:** `devops/forge`
- **call:** `/devops-forge` · binary `opgrok.sg.devops-forge`
- **category / role / tier:** `devops` / `forge` / `advanced`
- **intent:** devops/forge (e2e path): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback.
- **purpose:** Build and fix delivery and platform automation. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config.
- **when:** Builds and repairs CI/CD, containers, deploy pipelines, runbooks, and platform config by forging the full commit→build→test→deploy path before hardening edges. 

### 39. `devops-scout`
- **sg_id:** `sg-0087`
- **path:** `core/skills/devops/scout/SKILL.md`
- **nest:** `devops/scout`
- **call:** `/devops-scout` · binary `opgrok.sg.devops-scout`
- **category / role / tier:** `devops` / `scout` / `frontier`
- **intent:** devops/scout (map): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback.
- **purpose:** Build and fix delivery and platform automation. Method (map): map structure and constraints before committing to edits. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config.
- **when:** Maps CI/CD graphs, container bases, deploy targets, and secret surfaces before any pipeline or infra edit. Activates on failing Actions/GitLab jobs, Dockerfile/

### 40. `devops-seal`
- **sg_id:** `sg-0090`
- **path:** `core/skills/devops/seal/SKILL.md`
- **nest:** `devops/seal`
- **call:** `/devops-seal` · binary `opgrok.sg.devops-seal`
- **category / role / tier:** `devops` / `seal` / `frontier`
- **intent:** devops/seal (finalize): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback.
- **purpose:** Build and fix delivery and platform automation. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config.
- **when:** Finalizes DevOps delivery artifacts: gates CI green, freezes image digests and workflow pins, attaches rollback runbook, marks handoff-ready. Use when sealing G

### 41. `devops-smith`
- **sg_id:** `sg-0085`
- **path:** `core/skills/devops/smith/SKILL.md`
- **nest:** `devops/smith`
- **call:** `/devops-smith` · binary `opgrok.sg.devops-smith`
- **category / role / tier:** `devops` / `smith` / `core`
- **intent:** devops/smith (build unit): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback.
- **purpose:** Build and fix delivery and platform automation. Method (build unit): build the smallest correct unit that meets the brief. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config.
- **when:** Builds and repairs the smallest correct CI/CD unit, container stage, or deploy automation that meets the brief. Activates on failing GitHub Actions/GitLab CI, D

### 42. `devops-trace`
- **sg_id:** `sg-0088`
- **path:** `core/skills/devops/trace/SKILL.md`
- **nest:** `devops/trace`
- **call:** `/devops-trace` · binary `opgrok.sg.devops-trace`
- **category / role / tier:** `devops` / `trace` / `core`
- **intent:** devops/trace (RCA): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback.
- **purpose:** Build and fix delivery and platform automation. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config.
- **when:** Traces CI/CD and platform failures via RCA: symptom log → evidence artifact → root config/code → fix with rollback. Activates on failing GitHub Actions/GitLab j

### 43. `docs-audit`
- **sg_id:** `sg-0077`
- **path:** `core/skills/docs/audit/SKILL.md`
- **nest:** `docs/audit`
- **call:** `/docs-audit` · binary `opgrok.sg.docs-audit`
- **category / role / tier:** `docs` / `audit` / `advanced`
- **intent:** docs/audit (checklist): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches.
- **purpose:** Write docs grounded in actual repo behavior. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: README, API docs, runbooks, operator guides.
- **when:** Audits README, API docs, runbooks, and operator guides by checklist: every command, path, flag, and env var is cross-checked against repo source and scored pass

### 44. `docs-forge`
- **sg_id:** `sg-0074`
- **path:** `core/skills/docs/forge/SKILL.md`
- **nest:** `docs/forge`
- **call:** `/docs-forge` · binary `opgrok.sg.docs-forge`
- **category / role / tier:** `docs` / `forge` / `advanced`
- **intent:** docs/forge (e2e path): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches.
- **purpose:** Write docs grounded in actual repo behavior. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: README, API docs, runbooks, operator guides.
- **when:** Forges README, API reference, runbooks, and operator guides by building the verified end-to-end path first, then hardening edges. Activates on /docs-forge or do

### 45. `docs-scout`
- **sg_id:** `sg-0075`
- **path:** `core/skills/docs/scout/SKILL.md`
- **nest:** `docs/scout`
- **call:** `/docs-scout` · binary `opgrok.sg.docs-scout`
- **category / role / tier:** `docs` / `scout` / `frontier`
- **intent:** docs/scout (map): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches.
- **purpose:** Write docs grounded in actual repo behavior. Method (map): map structure and constraints before committing to edits. Domain: README, API docs, runbooks, operator guides.
- **when:** Maps README, API docs, runbooks, and operator guides against live repo truth before any edit: inventories entrypoints, verifies every command/path flag against 

### 46. `docs-seal`
- **sg_id:** `sg-0078`
- **path:** `core/skills/docs/seal/SKILL.md`
- **nest:** `docs/seal`
- **call:** `/docs-seal` · binary `opgrok.sg.docs-seal`
- **category / role / tier:** `docs` / `seal` / `frontier`
- **intent:** docs/seal (finalize): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches.
- **purpose:** Write docs grounded in actual repo behavior. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: README, API docs, runbooks, operator guides.
- **when:** Finalizes README, API docs, runbooks, and operator guides by sealing only after every command, path, flag, and env var is proven against the live tree. Activate

### 47. `docs-smith`
- **sg_id:** `sg-0073`
- **path:** `core/skills/docs/smith/SKILL.md`
- **nest:** `docs/smith`
- **call:** `/docs-smith` · binary `opgrok.sg.docs-smith`
- **category / role / tier:** `docs` / `smith` / `core`
- **intent:** docs/smith (build unit): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches.
- **purpose:** Write docs grounded in actual repo behavior. Method (build unit): build the smallest correct unit that meets the brief. Domain: README, API docs, runbooks, operator guides.
- **when:** Builds the smallest verified doc unit (README quickstart, API route page, runbook, operator guide) by cross-checking every command, flag, path, and env var agai

### 48. `docs-trace`
- **sg_id:** `sg-0076`
- **path:** `core/skills/docs/trace/SKILL.md`
- **nest:** `docs/trace`
- **call:** `/docs-trace` · binary `opgrok.sg.docs-trace`
- **category / role / tier:** `docs` / `trace` / `core`
- **intent:** docs/trace (RCA): Rewrite README quickstart with verified commands; Document an API route with request/response examples; Write an incident runbook with failure branches.
- **purpose:** Write docs grounded in actual repo behavior. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: README, API docs, runbooks, operator guides.
- **when:** Traces documentation drift via RCA: symptom → evidence → root → fix, verifying every command, path, flag, and env var against the live repo before rewrite. Acti

### 49. `eval-audit`
- **sg_id:** `sg-0125`
- **path:** `core/skills/eval/audit/SKILL.md`
- **nest:** `eval/audit`
- **call:** `/eval-audit` · binary `opgrok.sg.eval-audit`
- **category / role / tier:** `eval` / `audit` / `frontier`
- **intent:** eval/audit (checklist): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK.
- **purpose:** Design and run evaluations with measurable scores. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: rubrics, judges, harnesses, pass gates, scoring.
- **when:** Audits eval artifacts via frozen checklists: rubrics, judge contracts, harness journals, and pass gates. Activates on /eval-audit or requests to score a run, bu

### 50. `eval-forge`
- **sg_id:** `sg-0122`
- **path:** `core/skills/eval/forge/SKILL.md`
- **nest:** `eval/forge`
- **call:** `/eval-forge` · binary `opgrok.sg.eval-forge`
- **category / role / tier:** `eval` / `forge` / `advanced`
- **intent:** eval/forge (e2e path): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK.
- **purpose:** Design and run evaluations with measurable scores. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: rubrics, judges, harnesses, pass gates, scoring.
- **when:** Designs and runs evaluation systems—rubrics, judges, harnesses, pass gates, scoring— via the forge method: wire the full e2e path (dimensions → threshold → scor

### 51. `eval-scout`
- **sg_id:** `sg-0123`
- **path:** `core/skills/eval/scout/SKILL.md`
- **nest:** `eval/scout`
- **call:** `/eval-scout` · binary `opgrok.sg.eval-scout`
- **category / role / tier:** `eval` / `scout` / `frontier`
- **intent:** eval/scout (map): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK.
- **purpose:** Design and run evaluations with measurable scores. Method (map): map structure and constraints before committing to edits. Domain: rubrics, judges, harnesses, pass gates, scoring.
- **when:** Maps evaluation structure before any score is assigned: freezes dimensions, scales, and pass thresholds, then inventories evidence sources for rubrics, judges, 

### 52. `eval-seal`
- **sg_id:** `sg-0126`
- **path:** `core/skills/eval/seal/SKILL.md`
- **nest:** `eval/seal`
- **call:** `/eval-seal` · binary `opgrok.sg.eval-seal`
- **category / role / tier:** `eval` / `seal` / `frontier`
- **intent:** eval/seal (finalize): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK.
- **purpose:** Design and run evaluations with measurable scores. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: rubrics, judges, harnesses, pass gates, scoring.
- **when:** Finalizes evaluation runs by locking predeclared thresholds, freezing rubric versions, and emitting irreversible PASS/FAIL with per-dimension evidence. Use when

### 53. `eval-smith`
- **sg_id:** `sg-0121`
- **path:** `core/skills/eval/smith/SKILL.md`
- **nest:** `eval/smith`
- **call:** `/eval-smith` · binary `opgrok.sg.eval-smith`
- **category / role / tier:** `eval` / `smith` / `core`
- **intent:** eval/smith (build unit): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK.
- **purpose:** Design and run evaluations with measurable scores. Method (build unit): build the smallest correct unit that meets the brief. Domain: rubrics, judges, harnesses, pass gates, scoring.
- **when:** Builds minimal eval units—rubrics, judge contracts, harness pass-gates, score sheets—with predeclared thresholds and per-dimension evidence rules. Activates on 

### 54. `eval-trace`
- **sg_id:** `sg-0124`
- **path:** `core/skills/eval/trace/SKILL.md`
- **nest:** `eval/trace`
- **call:** `/eval-trace` · binary `opgrok.sg.eval-trace`
- **category / role / tier:** `eval` / `trace` / `frontier`
- **intent:** eval/trace (RCA): Build a 4-dimension rubric for a harness run; Score an artifact against a frozen threshold; Design a judge node contract for OPGROK.
- **purpose:** Design and run evaluations with measurable scores. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: rubrics, judges, harnesses, pass gates, scoring.
- **when:** Builds symptom→evidence→root→fix causal chains for rubrics, judges, harnesses, and pass gates. Activates on /eval-trace or tasks like scoring a harness run agai

### 55. `math-audit`
- **sg_id:** `sg-0137`
- **path:** `core/skills/math/audit/SKILL.md`
- **nest:** `math/audit`
- **call:** `/math-audit` · binary `opgrok.sg.math-audit`
- **category / role / tier:** `math` / `audit` / `frontier`
- **intent:** math/audit (checklist): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs.
- **purpose:** Solve and verify mathematical and algorithmic problems. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: algorithms, numerics, complexity, formal reasoning.
- **when:** Audits algorithms, numerics, complexity, and formal claims via explicit checklist scoring (PASS/FAIL per item with evidence). Use when deriving complexity, veri

### 56. `math-forge`
- **sg_id:** `sg-0134`
- **path:** `core/skills/math/forge/SKILL.md`
- **nest:** `math/forge`
- **call:** `/math-forge` · binary `opgrok.sg.math-forge`
- **category / role / tier:** `math` / `forge` / `advanced`
- **intent:** math/forge (e2e path): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs.
- **purpose:** Solve and verify mathematical and algorithmic problems. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: algorithms, numerics, complexity, formal reasoning.
- **when:** Derives algorithms, numerics, complexity bounds, and formal arguments by forging the full problem→model→verify path before edge hardening. Activates on concrete

### 57. `math-scout`
- **sg_id:** `sg-0135`
- **path:** `core/skills/math/scout/SKILL.md`
- **nest:** `math/scout`
- **call:** `/math-scout` · binary `opgrok.sg.math-scout`
- **category / role / tier:** `math` / `scout` / `frontier`
- **intent:** math/scout (map): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs.
- **purpose:** Solve and verify mathematical and algorithmic problems. Method (map): map structure and constraints before committing to edits. Domain: algorithms, numerics, complexity, formal reasoning.
- **when:** Maps algorithm structure, recurrence relations, and numeric domains before any edit or proof claim. Activates on complexity derivation, boundary-vector design, 

### 58. `math-seal`
- **sg_id:** `sg-0138`
- **path:** `core/skills/math/seal/SKILL.md`
- **nest:** `math/seal`
- **call:** `/math-seal` · binary `opgrok.sg.math-seal`
- **category / role / tier:** `math` / `seal` / `frontier`
- **intent:** math/seal (finalize): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs.
- **purpose:** Solve and verify mathematical and algorithmic problems. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: algorithms, numerics, complexity, formal reasoning.
- **when:** Finalizes math and algorithm work by locking definitions, attaching proof sketches or executable test vectors, and emitting a hard WIN gate. Use when complexity

### 59. `math-smith`
- **sg_id:** `sg-0133`
- **path:** `core/skills/math/smith/SKILL.md`
- **nest:** `math/smith`
- **call:** `/math-smith` · binary `opgrok.sg.math-smith`
- **category / role / tier:** `math` / `smith` / `core`
- **intent:** math/smith (build unit): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs.
- **purpose:** Solve and verify mathematical and algorithmic problems. Method (build unit): build the smallest correct unit that meets the brief. Domain: algorithms, numerics, complexity, formal reasoning.
- **when:** Builds the smallest verified math/algorithm unit: definitions, lemma or function, then test vectors or proof sketch. Activates on Derive time complexity of a co

### 60. `math-trace`
- **sg_id:** `sg-0136`
- **path:** `core/skills/math/trace/SKILL.md`
- **nest:** `math/trace`
- **call:** `/math-trace` · binary `opgrok.sg.math-trace`
- **category / role / tier:** `math` / `trace` / `frontier`
- **intent:** math/trace (RCA): Derive time complexity of a concrete algorithm; Implement an algorithm with test vectors; Verify a formula on boundary inputs.
- **purpose:** Solve and verify mathematical and algorithmic problems. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: algorithms, numerics, complexity, formal reasoning.
- **when:** Traces algorithmic and formal failures via RCA: symptom → evidence → algebraic/numeric root → fix. Activates on Derive time complexity of a concrete algorithm, 

### 61. `mcp-audit`
- **sg_id:** `sg-0113`
- **path:** `core/skills/mcp/audit/SKILL.md`
- **nest:** `mcp/audit`
- **call:** `/mcp-audit` · binary `opgrok.sg.mcp-audit`
- **category / role / tier:** `mcp` / `audit` / `advanced`
- **intent:** mcp/audit (checklist): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation.
- **purpose:** Wire and use MCP tools correctly. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: MCP servers, tool schemas, discovery, authenticated calls.
- **when:** Audits MCP server wiring, tool schemas, and authenticated calls against an explicit pass/fail checklist. Activates when discovering or invoking Linear/GitHub/cu

### 62. `mcp-forge`
- **sg_id:** `sg-0110`
- **path:** `core/skills/mcp/forge/SKILL.md`
- **nest:** `mcp/forge`
- **call:** `/mcp-forge` · binary `opgrok.sg.mcp-forge`
- **category / role / tier:** `mcp` / `forge` / `advanced`
- **intent:** mcp/forge (e2e path): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation.
- **purpose:** Wire and use MCP tools correctly. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: MCP servers, tool schemas, discovery, authenticated calls.
- **when:** Wires MCP servers end-to-end: schema discovery, auth-bound tool calls, multi-tool data contracts. Use when integrating Linear/GitHub/custom MCP tools, diagnosin

### 63. `mcp-scout`
- **sg_id:** `sg-0111`
- **path:** `core/skills/mcp/scout/SKILL.md`
- **nest:** `mcp/scout`
- **call:** `/mcp-scout` · binary `opgrok.sg.mcp-scout`
- **category / role / tier:** `mcp` / `scout` / `frontier`
- **intent:** mcp/scout (map): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation.
- **purpose:** Wire and use MCP tools correctly. Method (map): map structure and constraints before committing to edits. Domain: MCP servers, tool schemas, discovery, authenticated calls.
- **when:** Maps MCP server inventories, tool JSON-schemas, and auth surfaces before any use_tool call. Activates on Discover/call Linear or GitHub MCP tools, schema-gap re

### 64. `mcp-seal`
- **sg_id:** `sg-0114`
- **path:** `core/skills/mcp/seal/SKILL.md`
- **nest:** `mcp/seal`
- **call:** `/mcp-seal` · binary `opgrok.sg.mcp-seal`
- **category / role / tier:** `mcp` / `seal` / `frontier`
- **intent:** mcp/seal (finalize): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation.
- **purpose:** Wire and use MCP tools correctly. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: MCP servers, tool schemas, discovery, authenticated calls.
- **when:** Finalizes MCP tool sessions: freezes verified search_tool/use_tool transcripts, locks schema-matched inputs, and emits handoff-ready evidence when Linear/GitHub

### 65. `mcp-smith`
- **sg_id:** `sg-0109`
- **path:** `core/skills/mcp/smith/SKILL.md`
- **nest:** `mcp/smith`
- **call:** `/mcp-smith` · binary `opgrok.sg.mcp-smith`
- **category / role / tier:** `mcp` / `smith` / `core`
- **intent:** mcp/smith (build unit): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation.
- **purpose:** Wire and use MCP tools correctly. Method (build unit): build the smallest correct unit that meets the brief. Domain: MCP servers, tool schemas, discovery, authenticated calls.
- **when:** Builds the smallest correct MCP tool-use unit: discover schema, bind exact inputSchema params, execute one authenticated call, surface auth/schema gaps without 

### 66. `mcp-trace`
- **sg_id:** `sg-0112`
- **path:** `core/skills/mcp/trace/SKILL.md`
- **nest:** `mcp/trace`
- **call:** `/mcp-trace` · binary `opgrok.sg.mcp-trace`
- **category / role / tier:** `mcp` / `trace` / `core`
- **intent:** mcp/trace (RCA): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation.
- **purpose:** Wire and use MCP tools correctly. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: MCP servers, tool schemas, discovery, authenticated calls.
- **when:** Traces MCP tool failures via schema-first RCA: symptom → list_tools/search_tool evidence → root (missing field, auth scope, stale server) → fix. Activates on br

### 67. `meta-audit`
- **sg_id:** `sg-0149`
- **path:** `core/skills/meta/audit/SKILL.md`
- **nest:** `meta/audit`
- **call:** `/meta-audit` · binary `opgrok.sg.meta-audit`
- **category / role / tier:** `meta` / `audit` / `frontier`
- **intent:** meta/audit (checklist): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category.
- **purpose:** Maintain SuperGrok skills, registry, and program hygiene. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: skill authoring, registry, SuperGrok program hygiene, assets.
- **when:** Audits SuperGrok skill catalogs, registries, and program hygiene via explicit checklist scoring with path:line evidence. Activates on regenerate-after-role-chan

### 68. `meta-forge`
- **sg_id:** `sg-0146`
- **path:** `core/skills/meta/forge/SKILL.md`
- **nest:** `meta/forge`
- **call:** `/meta-forge` · binary `opgrok.sg.meta-forge`
- **category / role / tier:** `meta` / `forge` / `advanced`
- **intent:** meta/forge (e2e path): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category.
- **purpose:** Maintain SuperGrok skills, registry, and program hygiene. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: skill authoring, registry, SuperGrok program hygiene, assets.
- **when:** Authors and hardens SuperGrok skills, registry, and catalog hygiene via the forge method: full generate→rebuild→identity→validate path before edge fixes. Activa

### 69. `meta-scout`
- **sg_id:** `sg-0147`
- **path:** `core/skills/meta/scout/SKILL.md`
- **nest:** `meta/scout`
- **call:** `/meta-scout` · binary `opgrok.sg.meta-scout`
- **category / role / tier:** `meta` / `scout` / `frontier`
- **intent:** meta/scout (map): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category.
- **purpose:** Maintain SuperGrok skills, registry, and program hygiene. Method (map): map structure and constraints before committing to edits. Domain: skill authoring, registry, SuperGrok program hygiene, assets.
- **when:** Maps SuperGrok catalog topology, registry drift, and skill-authoring constraints before any edit lands. Activates on regenerate-after-role-change, identity rebi

### 70. `meta-seal`
- **sg_id:** `sg-0150`
- **path:** `core/skills/meta/seal/SKILL.md`
- **nest:** `meta/seal`
- **call:** `/meta-seal` · binary `opgrok.sg.meta-seal`
- **category / role / tier:** `meta` / `seal` / `frontier`
- **intent:** meta/seal (finalize): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category.
- **purpose:** Maintain SuperGrok skills, registry, and program hygiene. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: skill authoring, registry, SuperGrok program hygiene, assets.
- **when:** Finalizes SuperGrok catalog and registry work: runs the Leslie win gate, freezes generator outputs, and marks artifacts handoff-ready. Use after role edits, cat

### 71. `meta-smith`
- **sg_id:** `sg-0145`
- **path:** `core/skills/meta/smith/SKILL.md`
- **nest:** `meta/smith`
- **call:** `/meta-smith` · binary `opgrok.sg.meta-smith`
- **category / role / tier:** `meta` / `smith` / `core`
- **intent:** meta/smith (build unit): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category.
- **purpose:** Maintain SuperGrok skills, registry, and program hygiene. Method (build unit): build the smallest correct unit that meets the brief. Domain: skill authoring, registry, SuperGrok program hygiene, assets.
- **when:** Authors and repairs SuperGrok skills, registry entries, and catalog hygiene as atomic build units. Activates on regenerate-after-role-change, identity rebind, r

### 72. `meta-trace`
- **sg_id:** `sg-0148`
- **path:** `core/skills/meta/trace/SKILL.md`
- **nest:** `meta/trace`
- **call:** `/meta-trace` · binary `opgrok.sg.meta-trace`
- **category / role / tier:** `meta` / `trace` / `frontier`
- **intent:** meta/trace (RCA): Regenerate catalog after role change; Rebind identities after bulk skill edit; Fix registry after adding a category.
- **purpose:** Maintain SuperGrok skills, registry, and program hygiene. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: skill authoring, registry, SuperGrok program hygiene, assets.
- **when:** Root-causes SuperGrok catalog, registry, and skill-hygiene failures via symptom→evidence→root→fix chains. Activates on broken validate gates, stale identities a

### 73. `plan-audit`
- **sg_id:** `sg-0071`
- **path:** `core/skills/plan/audit/SKILL.md`
- **nest:** `plan/audit`
- **call:** `/plan-audit` · binary `opgrok.sg.plan-audit`
- **category / role / tier:** `plan` / `audit` / `advanced`
- **intent:** plan/audit (checklist): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates.
- **purpose:** Produce implementable plans and architecture decisions. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: design docs, ADRs, PR plans, delivery sequence.
- **when:** Audits design docs, ADRs, PR plans, and delivery sequences against an explicit quality checklist, scoring pass/fail per item with path:line evidence. Use for st

### 74. `plan-forge`
- **sg_id:** `sg-0068`
- **path:** `core/skills/plan/forge/SKILL.md`
- **nest:** `plan/forge`
- **call:** `/plan-forge` · binary `opgrok.sg.plan-forge`
- **category / role / tier:** `plan` / `forge` / `advanced`
- **intent:** plan/forge (e2e path): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates.
- **purpose:** Produce implementable plans and architecture decisions. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: design docs, ADRs, PR plans, delivery sequence.
- **when:** Forges implementable design docs, ADRs, PR plans, and delivery sequences by locking the full end-to-end path before edge hardening. Use for storage ADRs with op

### 75. `plan-scout`
- **sg_id:** `sg-0069`
- **path:** `core/skills/plan/scout/SKILL.md`
- **nest:** `plan/scout`
- **call:** `/plan-scout` · binary `opgrok.sg.plan-scout`
- **category / role / tier:** `plan` / `scout` / `frontier`
- **intent:** plan/scout (map): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates.
- **purpose:** Produce implementable plans and architecture decisions. Method (map): map structure and constraints before committing to edits. Domain: design docs, ADRs, PR plans, delivery sequence.
- **when:** Maps repo structure, constraints, and decision surfaces before any plan or ADR is written. Activates for design docs, ADRs, PR plans, delivery sequences, or whe

### 76. `plan-seal`
- **sg_id:** `sg-0072`
- **path:** `core/skills/plan/seal/SKILL.md`
- **nest:** `plan/seal`
- **call:** `/plan-seal` · binary `opgrok.sg.plan-seal`
- **category / role / tier:** `plan` / `seal` / `frontier`
- **intent:** plan/seal (finalize): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates.
- **purpose:** Produce implementable plans and architecture decisions. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: design docs, ADRs, PR plans, delivery sequence.
- **when:** Finalizes design docs, ADRs, PR plans, and delivery sequences: verifies win-gate evidence, freezes file-concrete outputs with owners/risks/acceptance, marks han

### 77. `plan-smith`
- **sg_id:** `sg-0067`
- **path:** `core/skills/plan/smith/SKILL.md`
- **nest:** `plan/smith`
- **call:** `/plan-smith` · binary `opgrok.sg.plan-smith`
- **category / role / tier:** `plan` / `smith` / `core`
- **intent:** plan/smith (build unit): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates.
- **purpose:** Produce implementable plans and architecture decisions. Method (build unit): build the smallest correct unit that meets the brief. Domain: design docs, ADRs, PR plans, delivery sequence.
- **when:** Drafts file-concrete design docs, ADRs, PR plans, and delivery sequences as the smallest correct build unit that meets the brief. Activates on ADR/storage-optio

### 78. `plan-trace`
- **sg_id:** `sg-0070`
- **path:** `core/skills/plan/trace/SKILL.md`
- **nest:** `plan/trace`
- **call:** `/plan-trace` · binary `opgrok.sg.plan-trace`
- **category / role / tier:** `plan` / `trace` / `core`
- **intent:** plan/trace (RCA): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates.
- **purpose:** Produce implementable plans and architecture decisions. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: design docs, ADRs, PR plans, delivery sequence.
- **when:** Builds implementable design docs, ADRs, PR plans, and delivery sequences by tracing symptom → evidence → root → fix. Activates for storage/ADR decisions with op

### 79. `product-audit`
- **sg_id:** `sg-0083`
- **path:** `core/skills/product/audit/SKILL.md`
- **nest:** `product/audit`
- **call:** `/product-audit` · binary `opgrok.sg.product-audit`
- **category / role / tier:** `product` / `audit` / `advanced`
- **intent:** product/audit (checklist): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes.
- **purpose:** Clarify product requirements and priorities. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: specs, prioritization, requirements clarity, acceptance criteria.
- **when:** Audits product specs for hireable clarity: must/should/could, explicit non-goals, and observable PASS/FAIL acceptance criteria. Use when turning vague asks into

### 80. `product-forge`
- **sg_id:** `sg-0080`
- **path:** `core/skills/product/forge/SKILL.md`
- **nest:** `product/forge`
- **call:** `/product-forge` · binary `opgrok.sg.product-forge`
- **category / role / tier:** `product` / `forge` / `advanced`
- **intent:** product/forge (e2e path): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes.
- **purpose:** Clarify product requirements and priorities. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: specs, prioritization, requirements clarity, acceptance criteria.
- **when:** Turns vague product asks into hireable specs: problem, users, MoSCoW + non-goals, observable acceptance, and a phased e2e path before edge hardening. Use for on

### 81. `product-scout`
- **sg_id:** `sg-0081`
- **path:** `core/skills/product/scout/SKILL.md`
- **nest:** `product/scout`
- **call:** `/product-scout` · binary `opgrok.sg.product-scout`
- **category / role / tier:** `product` / `scout` / `frontier`
- **intent:** product/scout (map): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes.
- **purpose:** Clarify product requirements and priorities. Method (map): map structure and constraints before committing to edits. Domain: specs, prioritization, requirements clarity, acceptance criteria.
- **when:** Maps product structure, constraints, and ambiguity before any spec edit or backlog commit. Use when turning vague asks into MoSCoW + non-goals, hireable accepta

### 82. `product-seal`
- **sg_id:** `sg-0084`
- **path:** `core/skills/product/seal/SKILL.md`
- **nest:** `product/seal`
- **call:** `/product-seal` · binary `opgrok.sg.product-seal`
- **category / role / tier:** `product` / `seal` / `frontier`
- **intent:** product/seal (finalize): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes.
- **purpose:** Clarify product requirements and priorities. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: specs, prioritization, requirements clarity, acceptance criteria.
- **when:** Finalizes product specs into hire-ready artifacts: MoSCoW cuts, explicit non-goals, and observable PASS/FAIL acceptance. Use when freezing a one-pager, turning 

### 83. `product-smith`
- **sg_id:** `sg-0079`
- **path:** `core/skills/product/smith/SKILL.md`
- **nest:** `product/smith`
- **call:** `/product-smith` · binary `opgrok.sg.product-smith`
- **category / role / tier:** `product` / `smith` / `core`
- **intent:** product/smith (build unit): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes.
- **purpose:** Clarify product requirements and priorities. Method (build unit): build the smallest correct unit that meets the brief. Domain: specs, prioritization, requirements clarity, acceptance criteria.
- **when:** Turns vague product asks into hireable build units: one-pager with MoSCoW, explicit non-goals, and observable PASS/FAIL acceptance. Activates for Write a one-pa

### 84. `product-trace`
- **sg_id:** `sg-0082`
- **path:** `core/skills/product/trace/SKILL.md`
- **nest:** `product/trace`
- **call:** `/product-trace` · binary `opgrok.sg.product-trace`
- **category / role / tier:** `product` / `trace` / `core`
- **intent:** product/trace (RCA): Write a one-pager with must/should/could and non-goals; Turn a vague ask into acceptance criteria for harness hire; Prioritize backlog with risk vs value notes.
- **purpose:** Clarify product requirements and priorities. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: specs, prioritization, requirements clarity, acceptance criteria.
- **when:** Traces product failures and vague asks into hireable specs via RCA: symptom → evidence → root → fix. Use for one-pagers with must/should/could + non-goals, back

### 85. `python-audit`
- **sg_id:** `sg-0017`
- **path:** `core/skills/python/audit/SKILL.md`
- **nest:** `python/audit`
- **call:** `/python-audit` · binary `opgrok.sg.python-audit`
- **category / role / tier:** `python` / `audit` / `advanced`
- **intent:** python/audit (checklist): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest.
- **purpose:** Write and fix Python packages and services. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: Python packages, typing, async services, scripts.
- **when:** Audits Python packages, typed APIs, and async services against a scored checklist (types, awaits, excepts, layout, tests, secrets). Activates on /python-audit o

### 86. `python-forge`
- **sg_id:** `sg-0014`
- **path:** `core/skills/python/forge/SKILL.md`
- **nest:** `python/forge`
- **call:** `/python-forge` · binary `opgrok.sg.python-forge`
- **category / role / tier:** `python` / `forge` / `advanced`
- **intent:** python/forge (e2e path): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest.
- **purpose:** Write and fix Python packages and services. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: Python packages, typing, async services, scripts.
- **when:** Ships Python packages, typed APIs, and async services by forging the full call path (entry → service → data) before edge hardening. Activates on /python-forge a

### 87. `python-scout`
- **sg_id:** `sg-0015`
- **path:** `core/skills/python/scout/SKILL.md`
- **nest:** `python/scout`
- **call:** `/python-scout` · binary `opgrok.sg.python-scout`
- **category / role / tier:** `python` / `scout` / `frontier`
- **intent:** python/scout (map): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest.
- **purpose:** Write and fix Python packages and services. Method (map): map structure and constraints before committing to edits. Domain: Python packages, typing, async services, scripts.
- **when:** Maps Python package topology, typing surface, async boundaries, and test layout before any edit. Activates on /python-scout and tasks like typed FastAPI DI rout

### 88. `python-seal`
- **sg_id:** `sg-0018`
- **path:** `core/skills/python/seal/SKILL.md`
- **nest:** `python/seal`
- **call:** `/python-seal` · binary `opgrok.sg.python-seal`
- **category / role / tier:** `python` / `seal` / `frontier`
- **intent:** python/seal (finalize): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest.
- **purpose:** Write and fix Python packages and services. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: Python packages, typing, async services, scripts.
- **when:** Finalizes Python package and service changes: verifies win-gate evidence, freezes typed public surfaces, and marks artifacts ready for handoff. Activates on /py

### 89. `python-smith`
- **sg_id:** `sg-0013`
- **path:** `core/skills/python/smith/SKILL.md`
- **nest:** `python/smith`
- **call:** `/python-smith` · binary `opgrok.sg.python-smith`
- **category / role / tier:** `python` / `smith` / `core`
- **intent:** python/smith (build unit): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest.
- **purpose:** Write and fix Python packages and services. Method (build unit): build the smallest correct unit that meets the brief. Domain: Python packages, typing, async services, scripts.
- **when:** Builds the smallest correct Python unit—typed package surface, async service path, or script—against existing layout and deps. Activates on /python-smith or bri

### 90. `python-trace`
- **sg_id:** `sg-0016`
- **path:** `core/skills/python/trace/SKILL.md`
- **nest:** `python/trace`
- **call:** `/python-trace` · binary `opgrok.sg.python-trace`
- **category / role / tier:** `python` / `trace` / `core`
- **intent:** python/trace (RCA): Add a typed FastAPI route with dependency injection; Fix an async race where a coroutine was not awaited; Extract a pure helper and cover it with pytest.
- **purpose:** Write and fix Python packages and services. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: Python packages, typing, async services, scripts.
- **when:** Root-cause traces failing Python packages, typed APIs, and async services by chaining symptom → evidence → root → minimal fix. Use for traceback-driven repair, 

### 91. `research-audit`
- **sg_id:** `sg-0131`
- **path:** `core/skills/research/audit/SKILL.md`
- **nest:** `research/audit`
- **call:** `/research-audit` · binary `opgrok.sg.research-audit`
- **category / role / tier:** `research` / `audit` / `advanced`
- **intent:** research/audit (checklist): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out.
- **purpose:** Research topics and synthesize cited findings. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: multi-source research, web/code search, grounded synthesis.
- **when:** Runs multi-source research and grounded synthesis under an explicit audit checklist, scoring each criterion PASS/FAIL with cited evidence. Use for competitive l

### 92. `research-forge`
- **sg_id:** `sg-0128`
- **path:** `core/skills/research/forge/SKILL.md`
- **nest:** `research/forge`
- **call:** `/research-forge` · binary `opgrok.sg.research-forge`
- **category / role / tier:** `research` / `forge` / `advanced`
- **intent:** research/forge (e2e path): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out.
- **purpose:** Research topics and synthesize cited findings. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: multi-source research, web/code search, grounded synthesis.
- **when:** Multi-source research and grounded synthesis for competitive landscapes, codebase locus questions, and contradiction-aware briefs. Builds the full e2e evidence 

### 93. `research-scout`
- **sg_id:** `sg-0129`
- **path:** `core/skills/research/scout/SKILL.md`
- **nest:** `research/scout`
- **call:** `/research-scout` · binary `opgrok.sg.research-scout`
- **category / role / tier:** `research` / `scout` / `frontier`
- **intent:** research/scout (map): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out.
- **purpose:** Research topics and synthesize cited findings. Method (map): map structure and constraints before committing to edits. Domain: multi-source research, web/code search, grounded synthesis.
- **when:** Maps multi-source research before synthesis: web/code search, dated citations, fact/inference split, contradiction callouts. Activates for competitive landscape

### 94. `research-seal`
- **sg_id:** `sg-0132`
- **path:** `core/skills/research/seal/SKILL.md`
- **nest:** `research/seal`
- **call:** `/research-seal` · binary `opgrok.sg.research-seal`
- **category / role / tier:** `research` / `seal` / `frontier`
- **intent:** research/seal (finalize): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out.
- **purpose:** Research topics and synthesize cited findings. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: multi-source research, web/code search, grounded synthesis.
- **when:** Finalizes multi-source research packets: audits citation coverage, freezes the fact/inference/opinion split, and emits a handoff-ready brief with dated sources.

### 95. `research-smith`
- **sg_id:** `sg-0127`
- **path:** `core/skills/research/smith/SKILL.md`
- **nest:** `research/smith`
- **call:** `/research-smith` · binary `opgrok.sg.research-smith`
- **category / role / tier:** `research` / `smith` / `core`
- **intent:** research/smith (build unit): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out.
- **purpose:** Research topics and synthesize cited findings. Method (build unit): build the smallest correct unit that meets the brief. Domain: multi-source research, web/code search, grounded synthesis.
- **when:** Builds the smallest cited research unit that answers one brief: multi-source web/code retrieval, fact/inference split, contradictions surfaced with dates. Activ

### 96. `research-trace`
- **sg_id:** `sg-0130`
- **path:** `core/skills/research/trace/SKILL.md`
- **nest:** `research/trace`
- **call:** `/research-trace` · binary `opgrok.sg.research-trace`
- **category / role / tier:** `research` / `trace` / `core`
- **intent:** research/trace (RCA): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out.
- **purpose:** Research topics and synthesize cited findings. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: multi-source research, web/code search, grounded synthesis.
- **when:** Builds cited causal chains (symptom → evidence → root → fix) across web and codebase sources for competitive landscapes, "where is X handled?", and multi-source

### 97. `review-audit`
- **sg_id:** `sg-0059`
- **path:** `core/skills/review/audit/SKILL.md`
- **nest:** `review/audit`
- **call:** `/review-audit` · binary `opgrok.sg.review-audit`
- **category / role / tier:** `review` / `audit` / `advanced`
- **intent:** review/audit (checklist): Review a PR for correctness and test gaps; Design review of an ADR with ranked risks; Critique a patch for API blast radius.
- **purpose:** Review work and report severity-ordered issues. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: code review, design review, actionable findings.
- **when:** Audits code/design changes against an explicit PASS/FAIL checklist, emitting severity-ordered findings with path:line evidence. Use for PR correctness and test-

### 98. `review-forge`
- **sg_id:** `sg-0056`
- **path:** `core/skills/review/forge/SKILL.md`
- **nest:** `review/forge`
- **call:** `/review-forge` · binary `opgrok.sg.review-forge`
- **category / role / tier:** `review` / `forge` / `advanced`
- **intent:** review/forge (e2e path): Review a PR for correctness and test gaps; Design review of an ADR with ranked risks; Critique a patch for API blast radius.
- **purpose:** Review work and report severity-ordered issues. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: code review, design review, actionable findings.
- **when:** Severity-ordered code and design review via the forge method: reconstruct the full end-to-end execution path before edge hardening. Activates on PR correctness/

### 99. `review-scout`
- **sg_id:** `sg-0057`
- **path:** `core/skills/review/scout/SKILL.md`
- **nest:** `review/scout`
- **call:** `/review-scout` · binary `opgrok.sg.review-scout`
- **category / role / tier:** `review` / `scout` / `frontier`
- **intent:** review/scout (map): Review a PR for correctness and test gaps; Design review of an ADR with ranked risks; Critique a patch for API blast radius.
- **purpose:** Review work and report severity-ordered issues. Method (map): map structure and constraints before committing to edits. Domain: code review, design review, actionable findings.
- **when:** Maps PR/design structure and constraints before ranking findings for code and design review. Activates on PR correctness/test-gap reviews, ADR risk ranking, API

### 100. `review-seal`
- **sg_id:** `sg-0060`
- **path:** `core/skills/review/seal/SKILL.md`
- **nest:** `review/seal`
- **call:** `/review-seal` · binary `opgrok.sg.review-seal`
- **category / role / tier:** `review` / `seal` / `frontier`
- **intent:** review/seal (finalize): Review a PR for correctness and test gaps; Design review of an ADR with ranked risks; Critique a patch for API blast radius.
- **purpose:** Review work and report severity-ordered issues. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: code review, design review, actionable findings.
- **when:** Seals code/design reviews by severity-ranking findings with path:line evidence, verifying win-gate checks, freezing the report, and marking handoff-ready. Activ

### 101. `review-smith`
- **sg_id:** `sg-0055`
- **path:** `core/skills/review/smith/SKILL.md`
- **nest:** `review/smith`
- **call:** `/review-smith` · binary `opgrok.sg.review-smith`
- **category / role / tier:** `review` / `smith` / `core`
- **intent:** review/smith (build unit): Review a PR for correctness and test gaps; Design review of an ADR with ranked risks; Critique a patch for API blast radius.
- **purpose:** Review work and report severity-ordered issues. Method (build unit): build the smallest correct unit that meets the brief. Domain: code review, design review, actionable findings.
- **when:** Severity-ordered code and design review that builds the smallest correct finding unit per risk area. Activates on PR/diff/ADR critique, correctness and test-gap

### 102. `review-trace`
- **sg_id:** `sg-0058`
- **path:** `core/skills/review/trace/SKILL.md`
- **nest:** `review/trace`
- **call:** `/review-trace` · binary `opgrok.sg.review-trace`
- **category / role / tier:** `review` / `trace` / `core`
- **intent:** review/trace (RCA): Review a PR for correctness and test gaps; Design review of an ADR with ranked risks; Critique a patch for API blast radius.
- **purpose:** Review work and report severity-ordered issues. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: code review, design review, actionable findings.
- **when:** Builds symptom→evidence→root→fix causal chains for code and design review. Activates on PR correctness/test-gap reviews, ADR risk ranking, patch blast-radius cr

### 103. `rust-audit`
- **sg_id:** `sg-0011`
- **path:** `core/skills/rust/audit/SKILL.md`
- **nest:** `rust/audit`
- **call:** `/rust-audit` · binary `opgrok.sg.rust-audit`
- **category / role / tier:** `rust` / `audit` / `advanced`
- **intent:** rust/audit (checklist): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present.
- **purpose:** Write and fix Rust code safely. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: Rust crates, ownership, traits, cargo workspaces.
- **when:** Audits Rust crates for ownership soundness, Result-first API edges, and cargo-workspace hygiene via an explicit pass/fail checklist. Activates on borrow-checker

### 104. `rust-forge`
- **sg_id:** `sg-0008`
- **path:** `core/skills/rust/forge/SKILL.md`
- **nest:** `rust/forge`
- **call:** `/rust-forge` · binary `opgrok.sg.rust-forge`
- **category / role / tier:** `rust` / `forge` / `advanced`
- **intent:** rust/forge (e2e path): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present.
- **purpose:** Write and fix Rust code safely. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: Rust crates, ownership, traits, cargo workspaces.
- **when:** Ships and repairs Rust crates by forging the full ownership-safe e2e path first (entry → modules → I/O → Result edges), then hardening borrow, trait, and worksp

### 105. `rust-scout`
- **sg_id:** `sg-0009`
- **path:** `core/skills/rust/scout/SKILL.md`
- **nest:** `rust/scout`
- **call:** `/rust-scout` · binary `opgrok.sg.rust-scout`
- **category / role / tier:** `rust` / `scout` / `frontier`
- **intent:** rust/scout (map): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present.
- **purpose:** Write and fix Rust code safely. Method (map): map structure and constraints before committing to edits. Domain: Rust crates, ownership, traits, cargo workspaces.
- **when:** Maps Rust crate topology, ownership edges, trait bounds, and cargo workspace constraints before any edit. Activates on borrow/lifetime puzzles, Result-first API

### 106. `rust-seal`
- **sg_id:** `sg-0012`
- **path:** `core/skills/rust/seal/SKILL.md`
- **nest:** `rust/seal`
- **call:** `/rust-seal` · binary `opgrok.sg.rust-seal`
- **category / role / tier:** `rust` / `seal` / `frontier`
- **intent:** rust/seal (finalize): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present.
- **purpose:** Write and fix Rust code safely. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: Rust crates, ownership, traits, cargo workspaces.
- **when:** Seals Rust crate changes for handoff: ownership-correct APIs, package-scoped cargo verification, and Result-first public edges. Use when finalizing borrow fixes

### 107. `rust-smith`
- **sg_id:** `sg-0007`
- **path:** `core/skills/rust/smith/SKILL.md`
- **nest:** `rust/smith`
- **call:** `/rust-smith` · binary `opgrok.sg.rust-smith`
- **category / role / tier:** `rust` / `smith` / `core`
- **intent:** rust/smith (build unit): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present.
- **purpose:** Write and fix Rust code safely. Method (build unit): build the smallest correct unit that meets the brief. Domain: Rust crates, ownership, traits, cargo workspaces.
- **when:** Builds and repairs Rust crates, ownership graphs, traits, and cargo workspaces by the smith method: smallest correct compile unit that satisfies the brief. Acti

### 108. `rust-trace`
- **sg_id:** `sg-0010`
- **path:** `core/skills/rust/trace/SKILL.md`
- **nest:** `rust/trace`
- **call:** `/rust-trace` · binary `opgrok.sg.rust-trace`
- **category / role / tier:** `rust` / `trace` / `core`
- **intent:** rust/trace (RCA): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present.
- **purpose:** Write and fix Rust code safely. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: Rust crates, ownership, traits, cargo workspaces.
- **when:** Root-causes Rust borrow, lifetime, trait-bound, and cargo-workspace failures via symptom → evidence → root → fix chains. Activates on rustc/clippy diagnostics, 

### 109. `security-audit`
- **sg_id:** `sg-0065`
- **path:** `core/skills/security/audit/SKILL.md`
- **nest:** `security/audit`
- **call:** `/security-audit` · binary `opgrok.sg.security-audit`
- **category / role / tier:** `security` / `audit` / `frontier`
- **intent:** security/audit (checklist): Threat model a new public API; Audit authz on object access paths; Harden secrets handling in config loading.
- **purpose:** Audit and harden systems without writing exploits. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: threat models, defensive audits, hardening (no exploit authoring).
- **when:** Defensive threat-model and hardening auditor for codebases and APIs: maps assets, trust boundaries, and authz paths, then scores an explicit checklist with file

### 110. `security-forge`
- **sg_id:** `sg-0062`
- **path:** `core/skills/security/forge/SKILL.md`
- **nest:** `security/forge`
- **call:** `/security-forge` · binary `opgrok.sg.security-forge`
- **category / role / tier:** `security` / `forge` / `advanced`
- **intent:** security/forge (e2e path): Threat model a new public API; Audit authz on object access paths; Harden secrets handling in config loading.
- **purpose:** Audit and harden systems without writing exploits. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: threat models, defensive audits, hardening (no exploit authoring).
- **when:** Builds end-to-end request paths first, then hardens trust-boundary edges for threat models, defensive audits, and authz/secrets hardening—never exploit authorin

### 111. `security-scout`
- **sg_id:** `sg-0063`
- **path:** `core/skills/security/scout/SKILL.md`
- **nest:** `security/scout`
- **call:** `/security-scout` · binary `opgrok.sg.security-scout`
- **category / role / tier:** `security` / `scout` / `frontier`
- **intent:** security/scout (map): Threat model a new public API; Audit authz on object access paths; Harden secrets handling in config loading.
- **purpose:** Audit and harden systems without writing exploits. Method (map): map structure and constraints before committing to edits. Domain: threat models, defensive audits, hardening (no exploit authoring).
- **when:** Maps trust boundaries, authz paths, and secret surfaces before any hardening edit. Activates on threat models, defensive audits, public-API exposure reviews, or

### 112. `security-seal`
- **sg_id:** `sg-0066`
- **path:** `core/skills/security/seal/SKILL.md`
- **nest:** `security/seal`
- **call:** `/security-seal` · binary `opgrok.sg.security-seal`
- **category / role / tier:** `security` / `seal` / `frontier`
- **intent:** security/seal (finalize): Threat model a new public API; Audit authz on object access paths; Harden secrets handling in config loading.
- **purpose:** Audit and harden systems without writing exploits. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: threat models, defensive audits, hardening (no exploit authoring).
- **when:** Finalizes defensive security work: freezes threat models, authz/secrets audits, and hardening patches with residual-risk ledger and WIN gate. Triggers on /secur

### 113. `security-smith`
- **sg_id:** `sg-0061`
- **path:** `core/skills/security/smith/SKILL.md`
- **nest:** `security/smith`
- **call:** `/security-smith` · binary `opgrok.sg.security-smith`
- **category / role / tier:** `security` / `smith` / `core`
- **intent:** security/smith (build unit): Threat model a new public API; Audit authz on object access paths; Harden secrets handling in config loading.
- **purpose:** Audit and harden systems without writing exploits. Method (build unit): build the smallest correct unit that meets the brief. Domain: threat models, defensive audits, hardening (no exploit authoring).
- **when:** Builds the smallest defensive control unit that closes a stated trust-boundary gap: threat-models assets, audits authz/secrets/input edges, and lands hardening 

### 114. `security-trace`
- **sg_id:** `sg-0064`
- **path:** `core/skills/security/trace/SKILL.md`
- **nest:** `security/trace`
- **call:** `/security-trace` · binary `opgrok.sg.security-trace`
- **category / role / tier:** `security` / `trace` / `frontier`
- **intent:** security/trace (RCA): Threat model a new public API; Audit authz on object access paths; Harden secrets handling in config loading.
- **purpose:** Audit and harden systems without writing exploits. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: threat models, defensive audits, hardening (no exploit authoring).
- **when:** Reconstructs defensive security RCA chains (symptom → evidence → root → fix) for threat models, authz audits, and hardening. Activates on /security-trace or tas

### 115. `test-audit`
- **sg_id:** `sg-0053`
- **path:** `core/skills/test/audit/SKILL.md`
- **nest:** `test/audit`
- **call:** `/test-audit` · binary `opgrok.sg.test-audit`
- **category / role / tier:** `test` / `audit` / `advanced`
- **intent:** test/audit (checklist): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path.
- **purpose:** Add and repair tests that prove behavior. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: unit/integration/e2e tests, fixtures, failure triage.
- **when:** Audits and hardens unit/integration/e2e suites by checklist: behavior asserts, deterministic fixtures, flake root-cause, scoped green runs. Triggers on /test-au

### 116. `test-forge`
- **sg_id:** `sg-0050`
- **path:** `core/skills/test/forge/SKILL.md`
- **nest:** `test/forge`
- **call:** `/test-forge` · binary `opgrok.sg.test-forge`
- **category / role / tier:** `test` / `forge` / `advanced`
- **intent:** test/forge (e2e path): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path.
- **purpose:** Add and repair tests that prove behavior. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: unit/integration/e2e tests, fixtures, failure triage.
- **when:** Forges unit/integration/e2e suites by building the full behavior path first, then hardening edges with deterministic fixtures and failure triage. Activates on /

### 117. `test-scout`
- **sg_id:** `sg-0051`
- **path:** `core/skills/test/scout/SKILL.md`
- **nest:** `test/scout`
- **call:** `/test-scout` · binary `opgrok.sg.test-scout`
- **category / role / tier:** `test` / `scout` / `frontier`
- **intent:** test/scout (map): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path.
- **purpose:** Add and repair tests that prove behavior. Method (map): map structure and constraints before committing to edits. Domain: unit/integration/e2e tests, fixtures, failure triage.
- **when:** Maps test topology, harness constraints, and flake surfaces before any test edit. Activates on unit/integration/e2e work, fixture design, failure triage, or /te

### 118. `test-seal`
- **sg_id:** `sg-0054`
- **path:** `core/skills/test/seal/SKILL.md`
- **nest:** `test/seal`
- **call:** `/test-seal` · binary `opgrok.sg.test-seal`
- **category / role / tier:** `test` / `seal` / `frontier`
- **intent:** test/seal (finalize): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path.
- **purpose:** Add and repair tests that prove behavior. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: unit/integration/e2e tests, fixtures, failure triage.
- **when:** Finalizes unit/integration/e2e work by verifying the win gate, freezing deterministic fixtures, and marking suites ready for handoff. Activates on /test-seal or

### 119. `test-smith`
- **sg_id:** `sg-0049`
- **path:** `core/skills/test/smith/SKILL.md`
- **nest:** `test/smith`
- **call:** `/test-smith` · binary `opgrok.sg.test-smith`
- **category / role / tier:** `test` / `smith` / `core`
- **intent:** test/smith (build unit): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path.
- **purpose:** Add and repair tests that prove behavior. Method (build unit): build the smallest correct unit that meets the brief. Domain: unit/integration/e2e tests, fixtures, failure triage.
- **when:** Authors and repairs unit/integration/e2e tests that prove observable behavior with deterministic fixtures. Activates on briefs like edge-case unit coverage, fla

### 120. `test-trace`
- **sg_id:** `sg-0052`
- **path:** `core/skills/test/trace/SKILL.md`
- **nest:** `test/trace`
- **call:** `/test-trace` · binary `opgrok.sg.test-trace`
- **category / role / tier:** `test` / `trace` / `core`
- **intent:** test/trace (RCA): Add unit tests for a pure function edge cases; Fix a flaky test by isolating shared state; Write an integration test for one API happy path.
- **purpose:** Add and repair tests that prove behavior. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: unit/integration/e2e tests, fixtures, failure triage.
- **when:** Triages failing or flaky unit/integration/e2e tests by building a symptom→evidence→root→fix causal chain, then lands the smallest behavior-proving test or fixtu

### 121. `tool-audit`
- **sg_id:** `sg-0119`
- **path:** `core/skills/tool/audit/SKILL.md`
- **nest:** `tool/audit`
- **call:** `/tool-audit` · binary `opgrok.sg.tool-audit`
- **category / role / tier:** `tool` / `audit` / `advanced`
- **intent:** tool/audit (checklist): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast.
- **purpose:** Orchestrate tools and verify outcomes. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: CLI, APIs, browser, orchestrated tool sequences.
- **when:** Audits multi-step CLI/API/browser tool chains against an explicit PASS/FAIL checklist, capturing exit codes, stdout/stderr, and path evidence per step. Activate

### 122. `tool-forge`
- **sg_id:** `sg-0116`
- **path:** `core/skills/tool/forge/SKILL.md`
- **nest:** `tool/forge`
- **call:** `/tool-forge` · binary `opgrok.sg.tool-forge`
- **category / role / tier:** `tool` / `forge` / `advanced`
- **intent:** tool/forge (e2e path): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast.
- **purpose:** Orchestrate tools and verify outcomes. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: CLI, APIs, browser, orchestrated tool sequences.
- **when:** Orchestrates multi-step CLI, API, and browser tool chains by forging the full e2e path first, then hardening edges. Activates on fail-fast verify sequences, sta

### 123. `tool-scout`
- **sg_id:** `sg-0117`
- **path:** `core/skills/tool/scout/SKILL.md`
- **nest:** `tool/scout`
- **call:** `/tool-scout` · binary `opgrok.sg.tool-scout`
- **category / role / tier:** `tool` / `scout` / `frontier`
- **intent:** tool/scout (map): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast.
- **purpose:** Orchestrate tools and verify outcomes. Method (map): map structure and constraints before committing to edits. Domain: CLI, APIs, browser, orchestrated tool sequences.
- **when:** Maps CLI/API/browser tool chains before execution: inventories binaries, probes exit contracts, and surfaces constraints so later steps never swallow non-zero s

### 124. `tool-seal`
- **sg_id:** `sg-0120`
- **path:** `core/skills/tool/seal/SKILL.md`
- **nest:** `tool/seal`
- **call:** `/tool-seal` · binary `opgrok.sg.tool-seal`
- **category / role / tier:** `tool` / `seal` / `frontier`
- **intent:** tool/seal (finalize): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast.
- **purpose:** Orchestrate tools and verify outcomes. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: CLI, APIs, browser, orchestrated tool sequences.
- **when:** Finalizes multi-step CLI/API/browser tool chains: verifies the win gate against observed exits, freezes artifacts, and marks handoff-ready. Activates for orches

### 125. `tool-smith`
- **sg_id:** `sg-0115`
- **path:** `core/skills/tool/smith/SKILL.md`
- **nest:** `tool/smith`
- **call:** `/tool-smith` · binary `opgrok.sg.tool-smith`
- **category / role / tier:** `tool` / `smith` / `core`
- **intent:** tool/smith (build unit): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast.
- **purpose:** Orchestrate tools and verify outcomes. Method (build unit): build the smallest correct unit that meets the brief. Domain: CLI, APIs, browser, orchestrated tool sequences.
- **when:** Orchestrates CLI, API, and browser tool chains as minimal verified units: each step captures exit, stdout/stderr tail, and asserts before the next hop. Activate

### 126. `tool-trace`
- **sg_id:** `sg-0118`
- **path:** `core/skills/tool/trace/SKILL.md`
- **nest:** `tool/trace`
- **call:** `/tool-trace` · binary `opgrok.sg.tool-trace`
- **category / role / tier:** `tool` / `trace` / `core`
- **intent:** tool/trace (RCA): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast.
- **purpose:** Orchestrate tools and verify outcomes. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: CLI, APIs, browser, orchestrated tool sequences.
- **when:** Orchestrates CLI, API, and browser tool chains under RCA: symptom → evidence → root → fix, fail-fast on non-zero exits. Use for multi-step verify paths, status-

### 127. `ui-audit`
- **sg_id:** `sg-0029`
- **path:** `core/skills/ui/audit/SKILL.md`
- **nest:** `ui/audit`
- **call:** `/ui-audit` · binary `opgrok.sg.ui-audit`
- **category / role / tier:** `ui` / `audit` / `advanced`
- **intent:** ui/audit (checklist): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components.
- **purpose:** Implement and improve UI/UX surfaces. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: interfaces, accessibility, interaction states, visual layout.
- **when:** Audits UI surfaces for interaction states, a11y, tokens, and layout integrity via explicit checklist scoring (PASS/FAIL per item with path:line evidence). Trigg

### 128. `ui-forge`
- **sg_id:** `sg-0026`
- **path:** `core/skills/ui/forge/SKILL.md`
- **nest:** `ui/forge`
- **call:** `/ui-forge` · binary `opgrok.sg.ui-forge`
- **category / role / tier:** `ui` / `forge` / `advanced`
- **intent:** ui/forge (e2e path): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components.
- **purpose:** Implement and improve UI/UX surfaces. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: interfaces, accessibility, interaction states, visual layout.
- **when:** Ships UI surfaces by forging the full interaction path first—happy path through empty/error/disabled/focus—then hardening edges against a11y and token drift. Ac

### 129. `ui-scout`
- **sg_id:** `sg-0027`
- **path:** `core/skills/ui/scout/SKILL.md`
- **nest:** `ui/scout`
- **call:** `/ui-scout` · binary `opgrok.sg.ui-scout`
- **category / role / tier:** `ui` / `scout` / `frontier`
- **intent:** ui/scout (map): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components.
- **purpose:** Implement and improve UI/UX surfaces. Method (map): map structure and constraints before committing to edits. Domain: interfaces, accessibility, interaction states, visual layout.
- **when:** Maps UI structure, a11y baselines, interaction states, and design-token constraints before any surface edit. Activates for state inventories (default/hover/focu

### 130. `ui-seal`
- **sg_id:** `sg-0030`
- **path:** `core/skills/ui/seal/SKILL.md`
- **nest:** `ui/seal`
- **call:** `/ui-seal` · binary `opgrok.sg.ui-seal`
- **category / role / tier:** `ui` / `seal` / `frontier`
- **intent:** ui/seal (finalize): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components.
- **purpose:** Implement and improve UI/UX surfaces. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: interfaces, accessibility, interaction states, visual layout.
- **when:** Finalizes UI surfaces by locking interaction states, a11y contracts, and token alignment before handoff. Use when closing button/form/control work (default/ hov

### 131. `ui-smith`
- **sg_id:** `sg-0025`
- **path:** `core/skills/ui/smith/SKILL.md`
- **nest:** `ui/smith`
- **call:** `/ui-smith` · binary `opgrok.sg.ui-smith`
- **category / role / tier:** `ui` / `smith` / `core`
- **intent:** ui/smith (build unit): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components.
- **purpose:** Implement and improve UI/UX surfaces. Method (build unit): build the smallest correct unit that meets the brief. Domain: interfaces, accessibility, interaction states, visual layout.
- **when:** Implements UI controls and views as the smallest correct unit: full interaction states, token-bound styling, and accessible names/focus. Use when adding or fixi

### 132. `ui-trace`
- **sg_id:** `sg-0028`
- **path:** `core/skills/ui/trace/SKILL.md`
- **nest:** `ui/trace`
- **call:** `/ui-trace` · binary `opgrok.sg.ui-trace`
- **category / role / tier:** `ui` / `trace` / `core`
- **intent:** ui/trace (RCA): Add button states (default/hover/disabled/loading); Fix missing label on icon control; Build a settings form section using existing components.
- **purpose:** Implement and improve UI/UX surfaces. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: interfaces, accessibility, interaction states, visual layout.
- **when:** Traces UI defects through symptom → evidence → root → fix: interaction states, focus/a11y, empty/error/loading, token drift. Activates on missing hover/disabled

### 133. `vision-audit`
- **sg_id:** `sg-0143`
- **path:** `core/skills/vision/audit/SKILL.md`
- **nest:** `vision/audit`
- **call:** `/vision-audit` · binary `opgrok.sg.vision-audit`
- **category / role / tier:** `vision` / `audit` / `advanced`
- **intent:** vision/audit (checklist): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity.
- **purpose:** Interpret or produce visual artifacts with grounding. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: image/UI understanding and visual artifacts.
- **when:** Audits screenshots, UI captures, and visual assets against an explicit observation checklist, scoring each item PASS/FAIL with grounded evidence. Activates on /

### 134. `vision-forge`
- **sg_id:** `sg-0140`
- **path:** `core/skills/vision/forge/SKILL.md`
- **nest:** `vision/forge`
- **call:** `/vision-forge` · binary `opgrok.sg.vision-forge`
- **category / role / tier:** `vision` / `forge` / `advanced`
- **intent:** vision/forge (e2e path): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity.
- **purpose:** Interpret or produce visual artifacts with grounding. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: image/UI understanding and visual artifacts.
- **when:** Grounds image/UI understanding and produces visual artifacts by forging the full e2e path first, then hardening edges. Activates for element-level screenshot gr

### 135. `vision-scout`
- **sg_id:** `sg-0141`
- **path:** `core/skills/vision/scout/SKILL.md`
- **nest:** `vision/scout`
- **call:** `/vision-scout` · binary `opgrok.sg.vision-scout`
- **category / role / tier:** `vision` / `scout` / `frontier`
- **intent:** vision/scout (map): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity.
- **purpose:** Interpret or produce visual artifacts with grounding. Method (map): map structure and constraints before committing to edits. Domain: image/UI understanding and visual artifacts.
- **when:** Maps visual structure and constraints before any edit or generation: element-level grounding, token locks, and seen-vs-inferred separation on screenshots, icons

### 136. `vision-seal`
- **sg_id:** `sg-0144`
- **path:** `core/skills/vision/seal/SKILL.md`
- **nest:** `vision/seal`
- **call:** `/vision-seal` · binary `opgrok.sg.vision-seal`
- **category / role / tier:** `vision` / `seal` / `frontier`
- **intent:** vision/seal (finalize): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity.
- **purpose:** Interpret or produce visual artifacts with grounding. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: image/UI understanding and visual artifacts.
- **when:** Finalizes vision deliverables by locking grounded observations, freezing asset paths, and gating handoff on evidence. Use after UI screenshot grounding, icon-se

### 137. `vision-smith`
- **sg_id:** `sg-0139`
- **path:** `core/skills/vision/smith/SKILL.md`
- **nest:** `vision/smith`
- **call:** `/vision-smith` · binary `opgrok.sg.vision-smith`
- **category / role / tier:** `vision` / `smith` / `core`
- **intent:** vision/smith (build unit): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity.
- **purpose:** Interpret or produce visual artifacts with grounding. Method (build unit): build the smallest correct unit that meets the brief. Domain: image/UI understanding and visual artifacts.
- **when:** Builds the smallest grounded visual unit for image/UI work: element-level screenshot descriptions, token-locked icons, or single-asset contrast fixes. Activates

### 138. `vision-trace`
- **sg_id:** `sg-0142`
- **path:** `core/skills/vision/trace/SKILL.md`
- **nest:** `vision/trace`
- **call:** `/vision-trace` · binary `opgrok.sg.vision-trace`
- **category / role / tier:** `vision` / `trace` / `core`
- **intent:** vision/trace (RCA): Describe a UI screenshot with element-level grounding; Generate an icon set matching brand tokens; Edit an asset to fix contrast while keeping identity.
- **purpose:** Interpret or produce visual artifacts with grounding. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: image/UI understanding and visual artifacts.
- **when:** Root-causes visual defects by chaining symptom → pixel evidence → CSS/asset root → fix, with element-level grounding and token locks. Use for UI screenshot RCA,

### 139. `web-audit`
- **sg_id:** `sg-0023`
- **path:** `core/skills/web/audit/SKILL.md`
- **nest:** `web/audit`
- **call:** `/web-audit` · binary `opgrok.sg.web-audit`
- **category / role / tier:** `web` / `audit` / `advanced`
- **intent:** web/audit (checklist): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies.
- **purpose:** Build and repair web application paths. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: HTTP APIs, frontends, auth edges, web clients.
- **when:** Audits HTTP APIs, SPA edges, and auth boundaries against a scored checklist of server-side authz, validation, status honesty, CORS/CSRF, and smoke evidence. Act

### 140. `web-forge`
- **sg_id:** `sg-0020`
- **path:** `core/skills/web/forge/SKILL.md`
- **nest:** `web/forge`
- **call:** `/web-forge` · binary `opgrok.sg.web-forge`
- **category / role / tier:** `web` / `forge` / `advanced`
- **intent:** web/forge (e2e path): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies.
- **purpose:** Build and repair web application paths. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: HTTP APIs, frontends, auth edges, web clients.
- **when:** Builds and repairs HTTP request paths across APIs, SPAs, and auth edges by forging the full client→route→handler→store→response chain before hardening status co

### 141. `web-scout`
- **sg_id:** `sg-0021`
- **path:** `core/skills/web/scout/SKILL.md`
- **nest:** `web/scout`
- **call:** `/web-scout` · binary `opgrok.sg.web-scout`
- **category / role / tier:** `web` / `scout` / `frontier`
- **intent:** web/scout (map): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies.
- **purpose:** Build and repair web application paths. Method (map): map structure and constraints before committing to edits. Domain: HTTP APIs, frontends, auth edges, web clients.
- **when:** Maps HTTP request paths, auth middleware chains, CORS/CSRF edges, and status contracts before any web edit. Activates on REST/SPA wiring, preflight failures, co

### 142. `web-seal`
- **sg_id:** `sg-0024`
- **path:** `core/skills/web/seal/SKILL.md`
- **nest:** `web/seal`
- **call:** `/web-seal` · binary `opgrok.sg.web-seal`
- **category / role / tier:** `web` / `seal` / `frontier`
- **intent:** web/seal (finalize): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies.
- **purpose:** Build and repair web application paths. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: HTTP APIs, frontends, auth edges, web clients.
- **when:** Finalizes HTTP APIs, SPA edges, and auth-bound web clients: verifies win-gate smoke, freezes route/error contracts, marks handoff-ready. Activates on /web-seal 

### 143. `web-smith`
- **sg_id:** `sg-0019`
- **path:** `core/skills/web/smith/SKILL.md`
- **nest:** `web/smith`
- **call:** `/web-smith` · binary `opgrok.sg.web-smith`
- **category / role / tier:** `web` / `smith` / `core`
- **intent:** web/smith (build unit): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies.
- **purpose:** Build and repair web application paths. Method (build unit): build the smallest correct unit that meets the brief. Domain: HTTP APIs, frontends, auth edges, web clients.
- **when:** Builds and repairs HTTP request paths—routes, handlers, validation, authz, status mapping, CORS/CSRF edges—as the smallest correct unit that meets the brief. Ac

### 144. `web-trace`
- **sg_id:** `sg-0022`
- **path:** `core/skills/web/trace/SKILL.md`
- **nest:** `web/trace`
- **call:** `/web-trace` · binary `opgrok.sg.web-trace`
- **category / role / tier:** `web` / `trace` / `core`
- **intent:** web/trace (RCA): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies.
- **purpose:** Build and repair web application paths. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: HTTP APIs, frontends, auth edges, web clients.
- **when:** Traces failing HTTP request paths from status/body/log evidence to handler root and minimal fix. Use for REST 4xx mapping, CORS preflight, CSRF cookie posts, au

### 145. `workflow-audit`
- **sg_id:** `sg-0107`
- **path:** `core/skills/workflow/audit/SKILL.md`
- **nest:** `workflow/audit`
- **call:** `/workflow-audit` · binary `opgrok.sg.workflow-audit`
- **category / role / tier:** `workflow` / `audit` / `advanced`
- **intent:** workflow/audit (checklist): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff.
- **purpose:** Design and fix automation workflows. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: DAGs, n8n-style flows, OPGROK automation pipelines.
- **when:** Audits DAGs, n8n-style flows, and OPGROK automation pipelines against an explicit failure-edge checklist, scoring PASS/FAIL per item with path evidence. Use whe

### 146. `workflow-forge`
- **sg_id:** `sg-0104`
- **path:** `core/skills/workflow/forge/SKILL.md`
- **nest:** `workflow/forge`
- **call:** `/workflow-forge` · binary `opgrok.sg.workflow-forge`
- **category / role / tier:** `workflow` / `forge` / `advanced`
- **intent:** workflow/forge (e2e path): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff.
- **purpose:** Design and fix automation workflows. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: DAGs, n8n-style flows, OPGROK automation pipelines.
- **when:** Designs and repairs DAGs, n8n-style flows, and OPGROK automation pipelines by forging the full trigger→nodes→sink path before hardening failure edges, backoff, 

### 147. `workflow-scout`
- **sg_id:** `sg-0105`
- **path:** `core/skills/workflow/scout/SKILL.md`
- **nest:** `workflow/scout`
- **call:** `/workflow-scout` · binary `opgrok.sg.workflow-scout`
- **category / role / tier:** `workflow` / `scout` / `frontier`
- **intent:** workflow/scout (map): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff.
- **purpose:** Design and fix automation workflows. Method (map): map structure and constraints before committing to edits. Domain: DAGs, n8n-style flows, OPGROK automation pipelines.
- **when:** Maps DAGs, n8n-style flows, and OPGROK automation pipelines before any edit: inventories triggers, node contracts, failure edges, and backoff gaps. Activates on

### 148. `workflow-seal`
- **sg_id:** `sg-0108`
- **path:** `core/skills/workflow/seal/SKILL.md`
- **nest:** `workflow/seal`
- **call:** `/workflow-seal` · binary `opgrok.sg.workflow-seal`
- **category / role / tier:** `workflow` / `seal` / `frontier`
- **intent:** workflow/seal (finalize): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff.
- **purpose:** Design and fix automation workflows. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: DAGs, n8n-style flows, OPGROK automation pipelines.
- **when:** Finalizes DAGs, n8n-style flows, and OPGROK automation pipelines: verifies win-gate evidence, freezes workflow artifacts, marks handoff-ready. Triggers on /work

### 149. `workflow-smith`
- **sg_id:** `sg-0103`
- **path:** `core/skills/workflow/smith/SKILL.md`
- **nest:** `workflow/smith`
- **call:** `/workflow-smith` · binary `opgrok.sg.workflow-smith`
- **category / role / tier:** `workflow` / `smith` / `core`
- **intent:** workflow/smith (build unit): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff.
- **purpose:** Design and fix automation workflows. Method (build unit): build the smallest correct unit that meets the brief. Domain: DAGs, n8n-style flows, OPGROK automation pipelines.
- **when:** Builds and repairs the smallest correct DAG/automation unit for n8n-style flows and OPGROK pipelines: explicit failure edges, backoff, idempotent nodes. Activat

### 150. `workflow-trace`
- **sg_id:** `sg-0106`
- **path:** `core/skills/workflow/trace/SKILL.md`
- **nest:** `workflow/trace`
- **call:** `/workflow-trace` · binary `opgrok.sg.workflow-trace`
- **category / role / tier:** `workflow` / `trace` / `core`
- **intent:** workflow/trace (RCA): Add a failure branch to a DAG node; Fix invalid workflow JSON schema; Automate a multi-step pipeline with backoff.
- **purpose:** Design and fix automation workflows. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: DAGs, n8n-style flows, OPGROK automation pipelines.
- **when:** RCA for DAGs, n8n-style flows, and OPGROK automation pipelines: symptom → evidence → root → fix with explicit failure edges and backoff. Use when a run dies mid

---

## Quick index

| name | call | kind | category | role | intent |
|------|------|------|----------|------|--------|
| `agent-audit` | `/agent-audit` | supergrok | `agent` | `audit` | agent/audit (checklist): Compose a 6-node harness for a landing page g |
| `agent-forge` | `/agent-forge` | supergrok | `agent` | `forge` | agent/forge (e2e path): Compose a 6-node harness for a landing page go |
| `agent-scout` | `/agent-scout` | supergrok | `agent` | `scout` | agent/scout (map): Compose a 6-node harness for a landing page goal; R |
| `agent-seal` | `/agent-seal` | supergrok | `agent` | `seal` | agent/seal (finalize): Compose a 6-node harness for a landing page goa |
| `agent-smith` | `/agent-smith` | supergrok | `agent` | `smith` | agent/smith (build unit): Compose a 6-node harness for a landing page  |
| `agent-trace` | `/agent-trace` | supergrok | `agent` | `trace` | agent/trace (RCA): Compose a 6-node harness for a landing page goal; R |
| `binary-audit` | `/binary-audit` | supergrok | `binary` | `audit` | binary/audit (checklist): Add a CLI subcommand with --help text; Packa |
| `binary-forge` | `/binary-forge` | supergrok | `binary` | `forge` | binary/forge (e2e path): Add a CLI subcommand with --help text; Packag |
| `binary-scout` | `/binary-scout` | supergrok | `binary` | `scout` | binary/scout (map): Add a CLI subcommand with --help text; Package a r |
| `binary-seal` | `/binary-seal` | supergrok | `binary` | `seal` | binary/seal (finalize): Add a CLI subcommand with --help text; Package |
| `binary-smith` | `/binary-smith` | supergrok | `binary` | `smith` | binary/smith (build unit): Add a CLI subcommand with --help text; Pack |
| `binary-trace` | `/binary-trace` | supergrok | `binary` | `trace` | binary/trace (RCA): Add a CLI subcommand with --help text; Package a r |
| `cat-agent` | `/cat-agent` | navigator | `agent` | `index` | Route work to the correct agent SuperGrok role. |
| `cat-binary` | `/cat-binary` | navigator | `binary` | `index` | Route work to the correct binary SuperGrok role. |
| `cat-code` | `/cat-code` | navigator | `code` | `index` | Route work to the correct code SuperGrok role. |
| `cat-data` | `/cat-data` | navigator | `data` | `index` | Route work to the correct data SuperGrok role. |
| `cat-db` | `/cat-db` | navigator | `db` | `index` | Route work to the correct db SuperGrok role. |
| `cat-debug` | `/cat-debug` | navigator | `debug` | `index` | Route work to the correct debug SuperGrok role. |
| `cat-devops` | `/cat-devops` | navigator | `devops` | `index` | Route work to the correct devops SuperGrok role. |
| `cat-docs` | `/cat-docs` | navigator | `docs` | `index` | Route work to the correct docs SuperGrok role. |
| `cat-eval` | `/cat-eval` | navigator | `eval` | `index` | Route work to the correct eval SuperGrok role. |
| `cat-math` | `/cat-math` | navigator | `math` | `index` | Route work to the correct math SuperGrok role. |
| `cat-mcp` | `/cat-mcp` | navigator | `mcp` | `index` | Route work to the correct mcp SuperGrok role. |
| `cat-meta` | `/cat-meta` | navigator | `meta` | `index` | Route work to the correct meta SuperGrok role. |
| `cat-plan` | `/cat-plan` | navigator | `plan` | `index` | Route work to the correct plan SuperGrok role. |
| `cat-product` | `/cat-product` | navigator | `product` | `index` | Route work to the correct product SuperGrok role. |
| `cat-python` | `/cat-python` | navigator | `python` | `index` | Route work to the correct python SuperGrok role. |
| `cat-research` | `/cat-research` | navigator | `research` | `index` | Route work to the correct research SuperGrok role. |
| `cat-review` | `/cat-review` | navigator | `review` | `index` | Route work to the correct review SuperGrok role. |
| `cat-rust` | `/cat-rust` | navigator | `rust` | `index` | Route work to the correct rust SuperGrok role. |
| `cat-security` | `/cat-security` | navigator | `security` | `index` | Route work to the correct security SuperGrok role. |
| `cat-test` | `/cat-test` | navigator | `test` | `index` | Route work to the correct test SuperGrok role. |
| `cat-tool` | `/cat-tool` | navigator | `tool` | `index` | Route work to the correct tool SuperGrok role. |
| `cat-ui` | `/cat-ui` | navigator | `ui` | `index` | Route work to the correct ui SuperGrok role. |
| `cat-vision` | `/cat-vision` | navigator | `vision` | `index` | Route work to the correct vision SuperGrok role. |
| `cat-web` | `/cat-web` | navigator | `web` | `index` | Route work to the correct web SuperGrok role. |
| `cat-workflow` | `/cat-workflow` | navigator | `workflow` | `index` | Route work to the correct workflow SuperGrok role. |
| `code-audit` | `/code-audit` | supergrok | `code` | `audit` | code/audit (checklist): Add a pure function + unit tests without touch |
| `code-forge` | `/code-forge` | supergrok | `code` | `forge` | code/forge (e2e path): Add a pure function + unit tests without touchi |
| `code-scout` | `/code-scout` | supergrok | `code` | `scout` | code/scout (map): Add a pure function + unit tests without touching th |
| `code-seal` | `/code-seal` | supergrok | `code` | `seal` | code/seal (finalize): Add a pure function + unit tests without touchin |
| `code-smith` | `/code-smith` | supergrok | `code` | `smith` | code/smith (build unit): Add a pure function + unit tests without touc |
| `code-trace` | `/code-trace` | supergrok | `code` | `trace` | code/trace (RCA): Add a pure function + unit tests without touching th |
| `data-audit` | `/data-audit` | supergrok | `data` | `audit` | data/audit (checklist): Add an ETL step with schema validation and rej |
| `data-forge` | `/data-forge` | supergrok | `data` | `forge` | data/forge (e2e path): Add an ETL step with schema validation and reje |
| `data-scout` | `/data-scout` | supergrok | `data` | `scout` | data/scout (map): Add an ETL step with schema validation and reject lo |
| `data-seal` | `/data-seal` | supergrok | `data` | `seal` | data/seal (finalize): Add an ETL step with schema validation and rejec |
| `data-smith` | `/data-smith` | supergrok | `data` | `smith` | data/smith (build unit): Add an ETL step with schema validation and re |
| `data-trace` | `/data-trace` | supergrok | `data` | `trace` | data/trace (RCA): Add an ETL step with schema validation and reject lo |
| `db-audit` | `/db-audit` | supergrok | `db` | `audit` | db/audit (checklist): Write a forward migration adding a column + inde |
| `db-forge` | `/db-forge` | supergrok | `db` | `forge` | db/forge (e2e path): Write a forward migration adding a column + index |
| `db-scout` | `/db-scout` | supergrok | `db` | `scout` | db/scout (map): Write a forward migration adding a column + index; Fix |
| `db-seal` | `/db-seal` | supergrok | `db` | `seal` | db/seal (finalize): Write a forward migration adding a column + index; |
| `db-smith` | `/db-smith` | supergrok | `db` | `smith` | db/smith (build unit): Write a forward migration adding a column + ind |
| `db-trace` | `/db-trace` | supergrok | `db` | `trace` | db/trace (RCA): Write a forward migration adding a column + index; Fix |
| `debug-audit` | `/debug-audit` | supergrok | `debug` | `audit` | debug/audit (checklist): RCA a crash from a stack trace to a one-line  |
| `debug-forge` | `/debug-forge` | supergrok | `debug` | `forge` | debug/forge (e2e path): RCA a crash from a stack trace to a one-line r |
| `debug-scout` | `/debug-scout` | supergrok | `debug` | `scout` | debug/scout (map): RCA a crash from a stack trace to a one-line root f |
| `debug-seal` | `/debug-seal` | supergrok | `debug` | `seal` | debug/seal (finalize): RCA a crash from a stack trace to a one-line ro |
| `debug-smith` | `/debug-smith` | supergrok | `debug` | `smith` | debug/smith (build unit): RCA a crash from a stack trace to a one-line |
| `debug-trace` | `/debug-trace` | supergrok | `debug` | `trace` | debug/trace (RCA): RCA a crash from a stack trace to a one-line root f |
| `devops-audit` | `/devops-audit` | supergrok | `devops` | `audit` | devops/audit (checklist): Fix a failing GitHub Actions job; Add a Dock |
| `devops-forge` | `/devops-forge` | supergrok | `devops` | `forge` | devops/forge (e2e path): Fix a failing GitHub Actions job; Add a Docke |
| `devops-scout` | `/devops-scout` | supergrok | `devops` | `scout` | devops/scout (map): Fix a failing GitHub Actions job; Add a Dockerfile |
| `devops-seal` | `/devops-seal` | supergrok | `devops` | `seal` | devops/seal (finalize): Fix a failing GitHub Actions job; Add a Docker |
| `devops-smith` | `/devops-smith` | supergrok | `devops` | `smith` | devops/smith (build unit): Fix a failing GitHub Actions job; Add a Doc |
| `devops-trace` | `/devops-trace` | supergrok | `devops` | `trace` | devops/trace (RCA): Fix a failing GitHub Actions job; Add a Dockerfile |
| `docs-audit` | `/docs-audit` | supergrok | `docs` | `audit` | docs/audit (checklist): Rewrite README quickstart with verified comman |
| `docs-forge` | `/docs-forge` | supergrok | `docs` | `forge` | docs/forge (e2e path): Rewrite README quickstart with verified command |
| `docs-scout` | `/docs-scout` | supergrok | `docs` | `scout` | docs/scout (map): Rewrite README quickstart with verified commands; Do |
| `docs-seal` | `/docs-seal` | supergrok | `docs` | `seal` | docs/seal (finalize): Rewrite README quickstart with verified commands |
| `docs-smith` | `/docs-smith` | supergrok | `docs` | `smith` | docs/smith (build unit): Rewrite README quickstart with verified comma |
| `docs-trace` | `/docs-trace` | supergrok | `docs` | `trace` | docs/trace (RCA): Rewrite README quickstart with verified commands; Do |
| `eval-audit` | `/eval-audit` | supergrok | `eval` | `audit` | eval/audit (checklist): Build a 4-dimension rubric for a harness run;  |
| `eval-forge` | `/eval-forge` | supergrok | `eval` | `forge` | eval/forge (e2e path): Build a 4-dimension rubric for a harness run; S |
| `eval-scout` | `/eval-scout` | supergrok | `eval` | `scout` | eval/scout (map): Build a 4-dimension rubric for a harness run; Score  |
| `eval-seal` | `/eval-seal` | supergrok | `eval` | `seal` | eval/seal (finalize): Build a 4-dimension rubric for a harness run; Sc |
| `eval-smith` | `/eval-smith` | supergrok | `eval` | `smith` | eval/smith (build unit): Build a 4-dimension rubric for a harness run; |
| `eval-trace` | `/eval-trace` | supergrok | `eval` | `trace` | eval/trace (RCA): Build a 4-dimension rubric for a harness run; Score  |
| `leslie` | `/leslie` | core | `leslie` | `master` | Authors falsifiable Winning Conditions and refusal gates for OPGROK ha |
| `math-audit` | `/math-audit` | supergrok | `math` | `audit` | math/audit (checklist): Derive time complexity of a concrete algorithm |
| `math-forge` | `/math-forge` | supergrok | `math` | `forge` | math/forge (e2e path): Derive time complexity of a concrete algorithm; |
| `math-scout` | `/math-scout` | supergrok | `math` | `scout` | math/scout (map): Derive time complexity of a concrete algorithm; Impl |
| `math-seal` | `/math-seal` | supergrok | `math` | `seal` | math/seal (finalize): Derive time complexity of a concrete algorithm;  |
| `math-smith` | `/math-smith` | supergrok | `math` | `smith` | math/smith (build unit): Derive time complexity of a concrete algorith |
| `math-trace` | `/math-trace` | supergrok | `math` | `trace` | math/trace (RCA): Derive time complexity of a concrete algorithm; Impl |
| `mcp-audit` | `/mcp-audit` | supergrok | `mcp` | `audit` | mcp/audit (checklist): Discover and call a Linear/GitHub MCP tool corr |
| `mcp-forge` | `/mcp-forge` | supergrok | `mcp` | `forge` | mcp/forge (e2e path): Discover and call a Linear/GitHub MCP tool corre |
| `mcp-scout` | `/mcp-scout` | supergrok | `mcp` | `scout` | mcp/scout (map): Discover and call a Linear/GitHub MCP tool correctly; |
| `mcp-seal` | `/mcp-seal` | supergrok | `mcp` | `seal` | mcp/seal (finalize): Discover and call a Linear/GitHub MCP tool correc |
| `mcp-smith` | `/mcp-smith` | supergrok | `mcp` | `smith` | mcp/smith (build unit): Discover and call a Linear/GitHub MCP tool cor |
| `mcp-trace` | `/mcp-trace` | supergrok | `mcp` | `trace` | mcp/trace (RCA): Discover and call a Linear/GitHub MCP tool correctly; |
| `meta-asset-creator` | `/meta-asset-creator` | special | `meta` | `asset-creator` | Owns the OPGROK Grok/xAI visual system under assets/: design tokens, d |
| `meta-audit` | `/meta-audit` | supergrok | `meta` | `audit` | meta/audit (checklist): Regenerate catalog after role change; Rebind i |
| `meta-forge` | `/meta-forge` | supergrok | `meta` | `forge` | meta/forge (e2e path): Regenerate catalog after role change; Rebind id |
| `meta-scout` | `/meta-scout` | supergrok | `meta` | `scout` | meta/scout (map): Regenerate catalog after role change; Rebind identit |
| `meta-seal` | `/meta-seal` | supergrok | `meta` | `seal` | meta/seal (finalize): Regenerate catalog after role change; Rebind ide |
| `meta-smith` | `/meta-smith` | supergrok | `meta` | `smith` | meta/smith (build unit): Regenerate catalog after role change; Rebind  |
| `meta-trace` | `/meta-trace` | supergrok | `meta` | `trace` | meta/trace (RCA): Regenerate catalog after role change; Rebind identit |
| `opgrok` | `/opgrok` | core | `opgrok` | `master` | Builds a sealed SuperGrok multi-agent harness from a natural-language  |
| `plan-audit` | `/plan-audit` | supergrok | `plan` | `audit` | plan/audit (checklist): ADR for storage choice with options and decisi |
| `plan-forge` | `/plan-forge` | supergrok | `plan` | `forge` | plan/forge (e2e path): ADR for storage choice with options and decisio |
| `plan-scout` | `/plan-scout` | supergrok | `plan` | `scout` | plan/scout (map): ADR for storage choice with options and decision; PR |
| `plan-seal` | `/plan-seal` | supergrok | `plan` | `seal` | plan/seal (finalize): ADR for storage choice with options and decision |
| `plan-smith` | `/plan-smith` | supergrok | `plan` | `smith` | plan/smith (build unit): ADR for storage choice with options and decis |
| `plan-trace` | `/plan-trace` | supergrok | `plan` | `trace` | plan/trace (RCA): ADR for storage choice with options and decision; PR |
| `product-audit` | `/product-audit` | supergrok | `product` | `audit` | product/audit (checklist): Write a one-pager with must/should/could an |
| `product-forge` | `/product-forge` | supergrok | `product` | `forge` | product/forge (e2e path): Write a one-pager with must/should/could and |
| `product-scout` | `/product-scout` | supergrok | `product` | `scout` | product/scout (map): Write a one-pager with must/should/could and non- |
| `product-seal` | `/product-seal` | supergrok | `product` | `seal` | product/seal (finalize): Write a one-pager with must/should/could and  |
| `product-smith` | `/product-smith` | supergrok | `product` | `smith` | product/smith (build unit): Write a one-pager with must/should/could a |
| `product-trace` | `/product-trace` | supergrok | `product` | `trace` | product/trace (RCA): Write a one-pager with must/should/could and non- |
| `python-audit` | `/python-audit` | supergrok | `python` | `audit` | python/audit (checklist): Add a typed FastAPI route with dependency in |
| `python-forge` | `/python-forge` | supergrok | `python` | `forge` | python/forge (e2e path): Add a typed FastAPI route with dependency inj |
| `python-scout` | `/python-scout` | supergrok | `python` | `scout` | python/scout (map): Add a typed FastAPI route with dependency injectio |
| `python-seal` | `/python-seal` | supergrok | `python` | `seal` | python/seal (finalize): Add a typed FastAPI route with dependency inje |
| `python-smith` | `/python-smith` | supergrok | `python` | `smith` | python/smith (build unit): Add a typed FastAPI route with dependency i |
| `python-trace` | `/python-trace` | supergrok | `python` | `trace` | python/trace (RCA): Add a typed FastAPI route with dependency injectio |
| `research-audit` | `/research-audit` | supergrok | `research` | `audit` | research/audit (checklist): Competitive landscape with dated sources;  |
| `research-forge` | `/research-forge` | supergrok | `research` | `forge` | research/forge (e2e path): Competitive landscape with dated sources; C |
| `research-scout` | `/research-scout` | supergrok | `research` | `scout` | research/scout (map): Competitive landscape with dated sources; Codeba |
| `research-seal` | `/research-seal` | supergrok | `research` | `seal` | research/seal (finalize): Competitive landscape with dated sources; Co |
| `research-smith` | `/research-smith` | supergrok | `research` | `smith` | research/smith (build unit): Competitive landscape with dated sources; |
| `research-trace` | `/research-trace` | supergrok | `research` | `trace` | research/trace (RCA): Competitive landscape with dated sources; Codeba |
| `review-audit` | `/review-audit` | supergrok | `review` | `audit` | review/audit (checklist): Review a PR for correctness and test gaps; D |
| `review-forge` | `/review-forge` | supergrok | `review` | `forge` | review/forge (e2e path): Review a PR for correctness and test gaps; De |
| `review-scout` | `/review-scout` | supergrok | `review` | `scout` | review/scout (map): Review a PR for correctness and test gaps; Design  |
| `review-seal` | `/review-seal` | supergrok | `review` | `seal` | review/seal (finalize): Review a PR for correctness and test gaps; Des |
| `review-smith` | `/review-smith` | supergrok | `review` | `smith` | review/smith (build unit): Review a PR for correctness and test gaps;  |
| `review-trace` | `/review-trace` | supergrok | `review` | `trace` | review/trace (RCA): Review a PR for correctness and test gaps; Design  |
| `rust-audit` | `/rust-audit` | supergrok | `rust` | `audit` | rust/audit (checklist): Fix a borrow checker error without unsafe; Add |
| `rust-forge` | `/rust-forge` | supergrok | `rust` | `forge` | rust/forge (e2e path): Fix a borrow checker error without unsafe; Add  |
| `rust-scout` | `/rust-scout` | supergrok | `rust` | `scout` | rust/scout (map): Fix a borrow checker error without unsafe; Add a lib |
| `rust-seal` | `/rust-seal` | supergrok | `rust` | `seal` | rust/seal (finalize): Fix a borrow checker error without unsafe; Add a |
| `rust-smith` | `/rust-smith` | supergrok | `rust` | `smith` | rust/smith (build unit): Fix a borrow checker error without unsafe; Ad |
| `rust-trace` | `/rust-trace` | supergrok | `rust` | `trace` | rust/trace (RCA): Fix a borrow checker error without unsafe; Add a lib |
| `security-audit` | `/security-audit` | supergrok | `security` | `audit` | security/audit (checklist): Threat model a new public API; Audit authz |
| `security-forge` | `/security-forge` | supergrok | `security` | `forge` | security/forge (e2e path): Threat model a new public API; Audit authz  |
| `security-scout` | `/security-scout` | supergrok | `security` | `scout` | security/scout (map): Threat model a new public API; Audit authz on ob |
| `security-seal` | `/security-seal` | supergrok | `security` | `seal` | security/seal (finalize): Threat model a new public API; Audit authz o |
| `security-smith` | `/security-smith` | supergrok | `security` | `smith` | security/smith (build unit): Threat model a new public API; Audit auth |
| `security-trace` | `/security-trace` | supergrok | `security` | `trace` | security/trace (RCA): Threat model a new public API; Audit authz on ob |
| `test-audit` | `/test-audit` | supergrok | `test` | `audit` | test/audit (checklist): Add unit tests for a pure function edge cases; |
| `test-forge` | `/test-forge` | supergrok | `test` | `forge` | test/forge (e2e path): Add unit tests for a pure function edge cases;  |
| `test-scout` | `/test-scout` | supergrok | `test` | `scout` | test/scout (map): Add unit tests for a pure function edge cases; Fix a |
| `test-seal` | `/test-seal` | supergrok | `test` | `seal` | test/seal (finalize): Add unit tests for a pure function edge cases; F |
| `test-smith` | `/test-smith` | supergrok | `test` | `smith` | test/smith (build unit): Add unit tests for a pure function edge cases |
| `test-trace` | `/test-trace` | supergrok | `test` | `trace` | test/trace (RCA): Add unit tests for a pure function edge cases; Fix a |
| `tool-audit` | `/tool-audit` | supergrok | `tool` | `audit` | tool/audit (checklist): Orchestrate a multi-step CLI verify path; Scra |
| `tool-forge` | `/tool-forge` | supergrok | `tool` | `forge` | tool/forge (e2e path): Orchestrate a multi-step CLI verify path; Scrap |
| `tool-scout` | `/tool-scout` | supergrok | `tool` | `scout` | tool/scout (map): Orchestrate a multi-step CLI verify path; Scrape and |
| `tool-seal` | `/tool-seal` | supergrok | `tool` | `seal` | tool/seal (finalize): Orchestrate a multi-step CLI verify path; Scrape |
| `tool-smith` | `/tool-smith` | supergrok | `tool` | `smith` | tool/smith (build unit): Orchestrate a multi-step CLI verify path; Scr |
| `tool-trace` | `/tool-trace` | supergrok | `tool` | `trace` | tool/trace (RCA): Orchestrate a multi-step CLI verify path; Scrape and |
| `ui-audit` | `/ui-audit` | supergrok | `ui` | `audit` | ui/audit (checklist): Add button states (default/hover/disabled/loadin |
| `ui-forge` | `/ui-forge` | supergrok | `ui` | `forge` | ui/forge (e2e path): Add button states (default/hover/disabled/loading |
| `ui-scout` | `/ui-scout` | supergrok | `ui` | `scout` | ui/scout (map): Add button states (default/hover/disabled/loading); Fi |
| `ui-seal` | `/ui-seal` | supergrok | `ui` | `seal` | ui/seal (finalize): Add button states (default/hover/disabled/loading) |
| `ui-smith` | `/ui-smith` | supergrok | `ui` | `smith` | ui/smith (build unit): Add button states (default/hover/disabled/loadi |
| `ui-trace` | `/ui-trace` | supergrok | `ui` | `trace` | ui/trace (RCA): Add button states (default/hover/disabled/loading); Fi |
| `vision-audit` | `/vision-audit` | supergrok | `vision` | `audit` | vision/audit (checklist): Describe a UI screenshot with element-level  |
| `vision-forge` | `/vision-forge` | supergrok | `vision` | `forge` | vision/forge (e2e path): Describe a UI screenshot with element-level g |
| `vision-scout` | `/vision-scout` | supergrok | `vision` | `scout` | vision/scout (map): Describe a UI screenshot with element-level ground |
| `vision-seal` | `/vision-seal` | supergrok | `vision` | `seal` | vision/seal (finalize): Describe a UI screenshot with element-level gr |
| `vision-smith` | `/vision-smith` | supergrok | `vision` | `smith` | vision/smith (build unit): Describe a UI screenshot with element-level |
| `vision-trace` | `/vision-trace` | supergrok | `vision` | `trace` | vision/trace (RCA): Describe a UI screenshot with element-level ground |
| `web-audit` | `/web-audit` | supergrok | `web` | `audit` | web/audit (checklist): Add a REST endpoint with validation and 4xx map |
| `web-forge` | `/web-forge` | supergrok | `web` | `forge` | web/forge (e2e path): Add a REST endpoint with validation and 4xx mapp |
| `web-scout` | `/web-scout` | supergrok | `web` | `scout` | web/scout (map): Add a REST endpoint with validation and 4xx mapping;  |
| `web-seal` | `/web-seal` | supergrok | `web` | `seal` | web/seal (finalize): Add a REST endpoint with validation and 4xx mappi |
| `web-smith` | `/web-smith` | supergrok | `web` | `smith` | web/smith (build unit): Add a REST endpoint with validation and 4xx ma |
| `web-trace` | `/web-trace` | supergrok | `web` | `trace` | web/trace (RCA): Add a REST endpoint with validation and 4xx mapping;  |
| `workflow-audit` | `/workflow-audit` | supergrok | `workflow` | `audit` | workflow/audit (checklist): Add a failure branch to a DAG node; Fix in |
| `workflow-forge` | `/workflow-forge` | supergrok | `workflow` | `forge` | workflow/forge (e2e path): Add a failure branch to a DAG node; Fix inv |
| `workflow-scout` | `/workflow-scout` | supergrok | `workflow` | `scout` | workflow/scout (map): Add a failure branch to a DAG node; Fix invalid  |
| `workflow-seal` | `/workflow-seal` | supergrok | `workflow` | `seal` | workflow/seal (finalize): Add a failure branch to a DAG node; Fix inva |
| `workflow-smith` | `/workflow-smith` | supergrok | `workflow` | `smith` | workflow/smith (build unit): Add a failure branch to a DAG node; Fix i |
| `workflow-trace` | `/workflow-trace` | supergrok | `workflow` | `trace` | workflow/trace (RCA): Add a failure branch to a DAG node; Fix invalid  |

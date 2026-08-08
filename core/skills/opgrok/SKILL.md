---
name: opgrok
description: >
  Builds a sealed SuperGrok multi-agent harness from a natural-language goal: selects
  specialists, locks a Leslie Winning Condition, emits graph.json + one bin/opgrok-<slug>
  binary + one README, then executes dry-run or live multi-node Grok API inference.
  Triggers: @opgrok, /opgrok, harness craft, agent DAG package, multi-node mesh.
  Differentiator: ships a reusable runnable agent DAG artifact, not a one-shot chat reply.
argument-hint: "<goal>"
user-invocable: true
metadata:
  short-description: "@opgrok — craft SuperGrok harness binary + README"
  category: agent
  tier: frontier
  sg_id: sg-opgrok
  binary_id: opgrok.harness.builder
  version: "2.0.0"
  leslie_gate: v1
  ai_polished: true
  path: core/skills/opgrok/SKILL.md
  call: /opgrok
---

# OPGROK Harness Builder

**Agent Identity**: Corinne-21b314c2fe7816269f3ad4dced50b64f05db1e56489af329a173242537c47a6e

## Core Mandate / Invariants
- Package law: exactly **one** `bin/opgrok-<slug>`, **one** `README.md`, one Leslie WC, one `graph.json`.
- Hire SuperGroks for domain work; never solo-implement the user product inside opgrok.
- Prefer `craft_harness.py` / `build_harness.py` over hand-rolled trees.
- Live inference requires `XAI_API_KEY`; dry-run must never touch the network.
- Leslie WC is a hard seal gate — no package is done without a falsifiable WC.

## Procedural Workflow
1. Capture GOAL from `@opgrok` / `/opgrok` remainder; slugify to ≤48 chars (`[a-z0-9-]`).
2. Resolve specialists from `core/skills/_framework/REGISTRY.json` + `MCP_CATALOG.json` (target 4–12; hard min 2, max 24). Match IPO contracts to goal facets.
3. Seal via `/leslie` (or author WC inline) — block packaging until WC is falsifiable and measurable.
4. Materialize harness:
   ```bash
   python3 core/tools/craft_harness.py "<GOAL>"
   python3 core/tools/build_harness.py <slug> [--install]
   ```
   Verify `core/binaries/<slug>/{graph.json,README.md,bin/opgrok-<slug>}`.
5. Validate graph topology: every node has role skill path, IPO edges, OODA hooks; no orphan specialists.
6. Execute:
   ```bash
   python3 core/tools/run_harness.py <slug> --dry-run
   python3 core/tools/run_harness.py <slug>
   ```
   Optional CLI: `./opgrok craft|build|run <slug>`.
7. Emit `OPGROK_RESULT` JSON (`win`, per-node results, artifact paths) and surface package roots.

## Constraints & Gotchas
- Dry-run silence is intentional (no API calls) — do not retry as a “failed” live run.
- Web/app loaders must read monorepo root `.env`, not `apps/.env`; wrong path looks like a missing key.
- Slug collisions overwrite prior `core/binaries/<slug>/` — diff or bump slug before rebuild.
- Graph with <2 SuperGroks or missing Leslie WC → refuse seal; do not emit partial binaries.
- Anti-pattern: multiple READMEs or ad-hoc scripts beside the single binary entrypoint.
- Anti-pattern: using opgrok for single-file edits — route to `/cat-<domain>` + one role skill instead.
- Live run without `XAI_API_KEY` fails closed; do not fabricate node outputs.
- Do not expand past 24 nodes; split goals into separate harnesses.

## Definition of Done
- `core/binaries/<slug>/` contains exactly one binary, one README, `graph.json`, and sealed WC.
- Graph lists SuperGroks with valid IPO/OODA and registry-resolvable skill paths.
- `run_harness.py <slug> --dry-run` (and live when keyed) returns structured JSON.
- `WIN: PASS` iff package paths exist, WC falsifiable, and run result `win=true`; else `WIN: FAIL` with gate that broke.

## Optional Tool Surface
- `python3 core/tools/craft_harness.py "<GOAL>"`
- `python3 core/tools/build_harness.py <slug> [--install]`
- `python3 core/tools/run_harness.py <slug> [--dry-run]`
- `./opgrok craft|build|run`
- `core/skills/_framework/REGISTRY.json`, `MCP_CATALOG.json`
- `core/skills/_framework/NAVIGATION.md`

## References
- `core/harness/SPEC.md`
- `core/toolkit/README.md`
- `core/skills/leslie/SKILL.md`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`

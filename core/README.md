# Core — SuperGrok harness kernel

This directory **is** OPGROK. Application UIs live under `../apps/` and are optional.

## Purpose

Turn a goal into a **harness**:

```text
goal → SuperGroks → Leslie WC → graph → binary package → Grok API run → OPGROK_RESULT
```

Leslie’s packaging law (always):

- **1** runnable binary (`bin/opgrok-<slug>`)
- **1** `README.md`
- plus `WINNING_CONDITION.md` + `graph.json`

## Directory guide

| Path | What it is |
|------|------------|
| [`skills/`](skills/README.md) | SuperGrok catalog (150 specialists + navigators + core) · registry · MCP nav |
| [`toolkit/`](toolkit/README.md) | Multi-model, memory, tools, repair, judge, ledger… |
| [`harness/`](harness/SPEC.md) | Harness law + graph schema |
| [`binaries/`](binaries/) | Crafted harness packages (gitignored) |
| [`tools/`](tools/) | Python CLI: craft / run / build / validate |
| [`rust/`](rust/) | Registry runtime, harness crafter, CLI, MCP |

## Everyday commands

```bash
# From repo root
python3 core/tools/craft_harness.py "your goal" --hire 6
python3 core/tools/run_harness.py <slug> --dry-run
python3 core/tools/run_harness.py <slug>
python3 core/tools/build_harness.py <slug> --install
python3 core/tools/validate_supergroks.py
```

```bash
# Rust (optional)
cargo run -p opgrok-sg-cli -- --repo . status
cargo run -p opgrok-sg-cli -- --repo . craft "your goal"
cargo run -p opgrok-sg-mcp -- --repo . tools-manifest
```

## Grok Build

```toml
[skills]
paths = ["/absolute/path/to/opgrok/core/skills"]
```

```text
@opgrok <goal>
/leslie seal <slug>
```

## Key concepts

**SuperGrok** — specialized `SKILL.md` with intent, purpose, win criteria, and binary id.

**Harness** — compiled selection of SuperGroks as a DAG, run with the Grok API.

**Leslie** — specification master; writes Winning Conditions, never implementation code. Upstream: https://github.com/DylanCkawalec/Leslie

**Toolkit** — execution upgrades that make multi-agent Grok runs practical (models, memory, tools, repair, parallel, judge). See [toolkit/README.md](toolkit/README.md).

## See also

- Product overview: [../README.md](../README.md)

# Core — SuperGrok harness kernel

This directory **is** OPGROK. The public interface is the CLI (`./opgrok` or `core/tools/*.py`).

## Purpose

Turn a goal into a **harness**:

```text
goal → SuperGroks → Leslie WC → graph → package → Grok API run → OPGROK_RESULT
```

Leslie packaging law (always):

- **1** runnable binary (`bin/opgrok-<slug>`)
- **1** `README.md`
- plus `WINNING_CONDITION.md` + `graph.json`

`craft` writes that package. A **product** binary exists only after a live run harvests SuperGrok sources and `cargo --require-cargo` succeeds.

## Directory guide

| Path | What it is |
|------|------------|
| [`skills/`](skills/README.md) | SuperGrok catalog · registry · MCP nav |
| [`toolkit/`](toolkit/README.md) | Models, memory, harvest, live UI, cargo |
| [`harness/`](harness/SPEC.md) | Harness law + graph schema |
| `binaries/` | Per-clone packages (gitignored) |
| [`tools/`](tools/) | Python CLI: craft / run / build / validate |
| [`rust/`](rust/) | Registry runtime, harness crafter, CLI, MCP |

## Everyday commands

From the clone root:

```bash
python3 core/tools/craft_harness.py "your goal" --hire 6
python3 core/tools/run_harness.py <slug> --repo . --dry-run
python3 core/tools/run_harness.py <slug> --repo .
python3 core/tools/build_harness.py <slug> --install
python3 core/tools/validate_supergroks.py
```

```bash
# Rust control plane (optional)
cargo run -p opgrok-sg-cli -- --repo . status
cargo run -p opgrok-sg-cli -- --repo . craft "your goal"
cargo run -p opgrok-sg-mcp -- --repo . tools-manifest
```

## Grok Build

Point Grok Build at **this clone**:

```toml
[skills]
paths = ["/absolute/path/to/your/opgrok/core/skills"]
```

Or symlink the factory command:

```bash
mkdir -p ~/.grok/skills
ln -sfn /absolute/path/to/your/opgrok/core/skills/opgrok ~/.grok/skills/opgrok
```

```text
/opgrok <goal>          # factory — you are the foreman
/leslie seal <slug>
```

Procedure: [skills/opgrok/SKILL.md](skills/opgrok/SKILL.md).

## Key concepts

**SuperGrok** — specialized `SKILL.md` with intent, purpose, win criteria, and binary id.

**Harness** — a DAG of SuperGroks, run with the Grok API.

**Leslie** — specification master; writes Winning Conditions, never implementation code. Upstream: https://github.com/DylanCkawalec/Leslie

**Toolkit** — execution infrastructure (models, memory, harvest, repair, parallel, judge). See [toolkit/README.md](toolkit/README.md).

# opgrok-sg-cli

<p align="center">
  <img src="https://raw.githubusercontent.com/DylanCkawalec/opgrok/main/assets/brand/logo-lockup-h.svg" alt="OPGROK" width="280" />
</p>

[![crates.io](https://img.shields.io/crates/v/opgrok-sg-cli.svg)](https://crates.io/crates/opgrok-sg-cli)
[![docs.rs](https://docs.rs/opgrok-sg-cli/badge.svg)](https://docs.rs/opgrok-sg-cli)
[![license](https://img.shields.io/crates/l/opgrok-sg-cli.svg)](https://github.com/DylanCkawalec/opgrok/blob/main/LICENSE)

**The operator CLI for [OPGROK](https://github.com/DylanCkawalec/opgrok) — route intents, browse the SuperGrok agent catalog, and craft & run reusable Grok-agent harnesses from your terminal.**

Installs the `opgrok-sg` binary: the control plane for 150+ specialist Grok agents.

<p align="center">
  <img src="https://raw.githubusercontent.com/DylanCkawalec/opgrok/main/assets/protocol/craft-pipeline.png" alt="Hire → seal → graph → binary" />
</p>

## Install

```bash
cargo install opgrok-sg-cli
```

Requires an [OPGROK](https://github.com/DylanCkawalec/opgrok) checkout for the skill catalog (`core/skills/_framework/REGISTRY.json`). Point at it with `--repo` (defaults to the current directory).

```bash
git clone https://github.com/DylanCkawalec/opgrok.git && cd opgrok
```

## Quick start

```bash
# Registry summary
opgrok-sg status

# Which agents match a goal?
opgrok-sg route "audit a python codebase for security issues"

# Craft a reusable harness binary from one goal
opgrok-sg craft "build a landing page with hero and pricing"

# Dry-run it (no API calls), then run live
opgrok-sg run build-a-landing-page-with-hero-and-pricing --dry-run
opgrok-sg run build-a-landing-page-with-hero-and-pricing
```

## Commands

| Command | What it does |
|---------|--------------|
| `status` | Registry summary — version, agent count, categories |
| `categories` | List all agent categories with counts |
| `list <category>` | List agents in one category |
| `route <intent> [--limit N]` | Ranked intent → agent matching |
| `show <name>` | One agent's path, intent, purpose, binary id |
| `load <name>` | Print the agent's full `SKILL.md` contract |
| `craft <goal> [--hire N]` | Hire agents, seal winning condition, emit harness package |
| `run <slug> [--goal ".."] [--dry-run]` | Execute a crafted harness |
| `harnesses` | List crafted harness binaries (JSON) |

Global flag: `--repo <path>` — repo root containing `core/skills/` (default `.`).

## Example session

```console
$ opgrok-sg route "triage a failing CI pipeline"
debug-scout     debug/scout     read logs, map failure surface        sg-debug-scout
debug-trace     debug/trace     isolate the root cause                sg-debug-trace
code-smith      code/smith      write the minimal fix                 sg-code-smith
test-seal       test/seal       verify green CI                       sg-test-seal

$ opgrok-sg craft "triage a failing CI pipeline"
@opgrok craft complete
slug:     triage-a-failing-ci-pipeline
...
WIN: PASS — package has 1 README + binary entrypoint + Leslie WC
```

## Ecosystem

| Crate | Role |
|-------|------|
| [opgrok-sg-runtime](https://crates.io/crates/opgrok-sg-runtime) | Registry, routing, skill loading |
| [opgrok-sg-harness](https://crates.io/crates/opgrok-sg-harness) | Craft goal → harness package |
| **opgrok-sg-cli** (this) | `opgrok-sg` operator CLI |
| [opgrok-sg-mcp](https://crates.io/crates/opgrok-sg-mcp) | MCP-style JSON tool surface |

## Links

- [GitHub repository](https://github.com/DylanCkawalec/opgrok) — full system, docs, and skill catalog
- [OPGROK overview](https://github.com/DylanCkawalec/opgrok#readme) — one prompt in, one binary out

## License

MIT © [Dylan Kawalec](https://github.com/DylanCkawalec)

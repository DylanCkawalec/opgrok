# opgrok-sg-mcp

[![crates.io](https://img.shields.io/crates/v/opgrok-sg-mcp.svg)](https://crates.io/crates/opgrok-sg-mcp)
[![docs.rs](https://docs.rs/opgrok-sg-mcp/badge.svg)](https://docs.rs/opgrok-sg-mcp)
[![license](https://img.shields.io/crates/l/opgrok-sg-mcp.svg)](https://github.com/DylanCkawalec/opgrok/blob/main/LICENSE)

**The MCP-style tool surface for [OPGROK](https://github.com/DylanCkawalec/opgrok) — expose the SuperGrok agent catalog to any tool-calling LLM or agent framework as machine-readable JSON.**

Installs the `opgrok-sg-mcp` binary. Every command emits JSON, so MCP clients, orchestrators, and scripts can list, route, describe, and load 150+ specialist Grok agents without parsing markdown.

## Install

```bash
cargo install opgrok-sg-mcp
```

Requires an [OPGROK](https://github.com/DylanCkawalec/opgrok) checkout for the skill catalog (`core/skills/_framework/REGISTRY.json`). Point at it with `--repo` (defaults to the current directory).

## Quick start

```bash
# What tools does this surface expose?
opgrok-sg-mcp tools-manifest

# Route a goal to agents (JSON array, ranked)
opgrok-sg-mcp route "review a Rust crate for correctness and performance"

# Inspect one agent
opgrok-sg-mcp describe rust-smith

# Load its full skill contract
opgrok-sg-mcp load rust-smith
```

## Commands (all JSON output)

| Command | What it returns |
|---------|-----------------|
| `list [--category C] [--limit N]` | Agent descriptors (name, sg_id, call, category, intent, binary_id) |
| `route <intent> [--limit N]` | Ranked agents matching free-text intent |
| `describe <name>` | Full registry record for one agent |
| `load <name>` | Raw `SKILL.md` body for one agent |
| `categories` | Categories with counts + navigator calls |
| `nav <category>` | Category navigator record (or role listing fallback) |
| `tools-manifest` | MCP-style manifest: tools, input schemas, traversal rules |

Global flag: `--repo <path>` — repo root containing `core/skills/` (default `.`).

## Traversal contract

The tools manifest encodes how an orchestrator should walk the catalog:

```
goal → /opgrok if multi-agent
else match category → /cat-<category>
pick /<category>-<role> by intent/purpose
sg_load path from REGISTRY
```

Exposed tools: `sg_categories` · `sg_nav` · `sg_list` · `sg_route` · `sg_describe` · `sg_load`.

## Ecosystem

| Crate | Role |
|-------|------|
| [opgrok-sg-runtime](https://crates.io/crates/opgrok-sg-runtime) | Registry, routing, skill loading |
| [opgrok-sg-harness](https://crates.io/crates/opgrok-sg-harness) | Craft goal → harness package |
| [opgrok-sg-cli](https://crates.io/crates/opgrok-sg-cli) | `opgrok-sg` operator CLI |
| **opgrok-sg-mcp** (this) | MCP-style JSON tool surface |

## Links

- [GitHub repository](https://github.com/DylanCkawalec/opgrok) — full system, docs, and skill catalog
- [OPGROK overview](https://github.com/DylanCkawalec/opgrok#readme) — one prompt in, one binary out

## License

MIT © [Dylan Kawalec](https://github.com/DylanCkawalec)

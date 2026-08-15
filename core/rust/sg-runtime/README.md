# opgrok-sg-runtime

<p align="center">
  <img src="https://raw.githubusercontent.com/DylanCkawalec/opgrok/main/assets/brand/logo-lockup-h.svg" alt="OPGROK" width="280" />
</p>

[![crates.io](https://img.shields.io/crates/v/opgrok-sg-runtime.svg)](https://crates.io/crates/opgrok-sg-runtime)
[![docs.rs](https://docs.rs/opgrok-sg-runtime/badge.svg)](https://docs.rs/opgrok-sg-runtime)
[![license](https://img.shields.io/crates/l/opgrok-sg-runtime.svg)](https://github.com/DylanCkawalec/opgrok/blob/main/LICENSE)

**The SuperGrok runtime for [OPGROK](https://github.com/DylanCkawalec/opgrok) — load the agent registry, route natural-language intent to specialist Grok agents, and load skill contracts.**

OPGROK turns any goal into a team of Grok agents shipped as one reusable binary. This crate is the foundation every other OPGROK crate builds on: it parses the SuperGrok registry (`REGISTRY.json`), indexes 150+ specialist agents by name, id, and category, and scores them against free-text intent.

<p align="center">
  <img src="https://raw.githubusercontent.com/DylanCkawalec/opgrok/main/assets/protocol/inference-flow.png" alt="SuperGrok nodes calling Grok" />
</p>

## Install

```toml
[dependencies]
opgrok-sg-runtime = "1.0"
```

## Quick start

```rust
use opgrok_sg_runtime::SuperGrokIndex;

// Repo root must contain core/skills/_framework/REGISTRY.json
let idx = SuperGrokIndex::load_from_repo_root(".")?;

// Route a goal to the best-matching specialists
for sk in idx.route("audit a python codebase for security issues", 8) {
    println!("{}\t{}\t{}", sk.name, sk.nest, sk.intent);
}

// Browse the catalog
for cat in idx.list_categories() {
    println!("{cat}: {} agents", idx.by_category(&cat).len());
}

// Load one agent's full SKILL.md contract
let md = opgrok_sg_runtime::load_skill_markdown(".", &idx, "rust-smith")?;
# Ok::<(), opgrok_sg_runtime::SuperGrokError>(())
```

## What you get

| API | Purpose |
|-----|---------|
| `SuperGrokIndex::load_from_repo_root` | Load + index the full registry from a repo checkout |
| `route(intent, limit)` | Ranked intent → agent matching (name/category/nest/intent/purpose/when_to_use) |
| `detect_mode(goal)` | Apex classify: craft / meta / run / inspect |
| `prefer_categories(goal)` | Hire-order family (meta vs product) |
| `get(name_or_id)` | Look up one agent by name or `sg_id` |
| `by_category(cat)` | All agents in a category |
| `mcp_descriptors()` | Machine-readable descriptors for MCP-style tool surfaces |
| `load_skill_markdown(..)` | Read an agent's full `SKILL.md` contract |

## The SuperGrok model

178 indexed skills under `core/skills/<category>/<role>/SKILL.md` — 150 specialists, 25 category navigators, 2 core agents, 1 meta agent — across six roles: `smith` (smallest unit) · `forge` (end-to-end) · `scout` (map first) · `trace` (root cause) · `audit` (checklist) · `seal` (gate + freeze).

## Ecosystem

| Crate | Role |
|-------|------|
| **opgrok-sg-runtime** (this) | Registry, routing, skill loading |
| [opgrok-sg-harness](https://crates.io/crates/opgrok-sg-harness) | Craft goal → harness package (graph + winning condition + binary crate) |
| [opgrok-sg-cli](https://crates.io/crates/opgrok-sg-cli) | `opgrok-sg` operator CLI |
| [opgrok-sg-mcp](https://crates.io/crates/opgrok-sg-mcp) | MCP-style JSON tool surface |

## Links

- [GitHub repository](https://github.com/DylanCkawalec/opgrok) — full system, docs, and skill catalog
- [OPGROK overview](https://github.com/DylanCkawalec/opgrok#readme) — one prompt in, one binary out

## License

MIT © [Dylan Kawalec](https://github.com/DylanCkawalec)

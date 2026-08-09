# opgrok-sg-harness

[![crates.io](https://img.shields.io/crates/v/opgrok-sg-harness.svg)](https://crates.io/crates/opgrok-sg-harness)
[![docs.rs](https://docs.rs/opgrok-sg-harness/badge.svg)](https://docs.rs/opgrok-sg-harness)
[![license](https://img.shields.io/crates/l/opgrok-sg-harness.svg)](https://github.com/DylanCkawalec/opgrok/blob/main/LICENSE)

**The harness crafter for [OPGROK](https://github.com/DylanCkawalec/opgrok) — turn one goal into a sealed, reusable Grok-agent pipeline: one binary package + one README.**

Give it a goal. It hires the right SuperGrok specialists by intent, seals a falsifiable winning condition, wires the agents into an ordered graph, and packages everything as a compilable Rust crate under `core/binaries/<slug>/`.

## Install

Library:

```toml
[dependencies]
opgrok-sg-harness = "0.1"
```

CLI:

```bash
cargo install opgrok-sg-harness
```

## Quick start (library)

```rust
let pkg = opgrok_sg_harness::craft(
    ".",                                        // repo root (contains core/skills/)
    "review a Rust crate for correctness",      // the goal
    8,                                          // max specialists to hire
)?;

println!("slug:  {}", pkg.slug);
println!("graph: {}", pkg.graph.display());
println!("wc:    {}", pkg.winning_condition.display());
println!("crate: {}", pkg.crate_dir.display());
println!("hired: {}", pkg.hired.join(", "));
# Ok::<(), anyhow::Error>(())
```

## Quick start (CLI)

```bash
opgrok-sg-harness --repo . craft "audit a Python codebase for security issues"
```

## What a craft produces

```
core/binaries/<slug>/
├── README.md              # the single doc — what it does, how to run it
├── WINNING_CONDITION.md   # Leslie-style falsifiable success contract
├── graph.json             # ordered DAG of hired agents (IPO + OODA per node)
├── crate/                 # generated Rust binary crate (cargo build → opgrok-<slug>)
└── registry entry         # indexed for `opgrok-sg harnesses`
```

Each graph node carries its agent identity (`sg_name`, `sg_id`, `binary_id`), skill path, IPO contract (inputs → process → outputs), and OODA loop (observe → orient → decide → act).

## The winning condition

One harness = one binary + one README. The winning condition is sealed before any code is written, so every run can be judged PASS/FAIL against the goal — no silent code dumps.

## Ecosystem

| Crate | Role |
|-------|------|
| [opgrok-sg-runtime](https://crates.io/crates/opgrok-sg-runtime) | Registry, routing, skill loading |
| **opgrok-sg-harness** (this) | Craft goal → harness package |
| [opgrok-sg-cli](https://crates.io/crates/opgrok-sg-cli) | `opgrok-sg` operator CLI (craft + run) |
| [opgrok-sg-mcp](https://crates.io/crates/opgrok-sg-mcp) | MCP-style JSON tool surface |

## Links

- [GitHub repository](https://github.com/DylanCkawalec/opgrok) — full system, docs, and skill catalog
- [Harness spec](https://github.com/DylanCkawalec/opgrok/blob/main/core/harness/SPEC.md)

## License

MIT © [Dylan Kawalec](https://github.com/DylanCkawalec)

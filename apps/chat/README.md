# Chat app (optional)

Rust terminal/server chat client for xAI Grok models.

> **Monorepo note:** This package lives at `apps/chat/` (not the old root `grok-chat-app/`).  
> It is an **optional app**. SuperGrok harness craft/run lives in `core/`.

## Role in OPGROK

| | |
|--|--|
| Depends on | `opgrok-sg-runtime` (SuperGrok registry helpers) |
| Workspace | Root `Cargo.toml` member |
| Not responsible for | Crafting harnesses, SuperGrok SKILL.md catalog |

## Prerequisites

- Rust toolchain (`cargo`)
- `XAI_API_KEY` in repo root `.env` or local env

## Build

From **repo root**:

```bash
cargo build -p grok-chat-app --release --features terminal
```

Or from this directory:

```bash
cargo build --release --features terminal
```

## Configure

Use the monorepo root `.env`:

```bash
XAI_API_KEY=xai-...
DEFAULT_MODEL=grok-4
```

## Usage

```bash
# after release build
cargo run -p grok-chat-app --features terminal
```

Feature flags:

- `terminal` (default) — TUI chat  
- `server` — HTTP API mode (optional)

## See also

- Kernel: [../../core/README.md](../../core/README.md)  
- Apps overview: [../README.md](../README.md)  
- Product: [../../README.md](../../README.md)  

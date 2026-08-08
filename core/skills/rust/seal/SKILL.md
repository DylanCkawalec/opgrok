---
name: rust-seal
description: >
  Seals Rust crate changes for handoff: ownership-correct APIs, package-scoped
  cargo verification, and Result-first public edges. Use when finalizing borrow
  fixes, library modules, or clap-style CLI subcommands; triggers on /rust-seal
  and seal/freeze requests in Rust workspaces. Differentiator: cargo -p gates
  plus MSRV/edition alignment before WIN, not workspace-blind green builds.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Rust systems · finalize"
  category: rust
  tier: frontier
  sg_id: sg-0012
  binary_id: opgrok.sg.rust-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "rust/seal (finalize): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present."
  purpose: "Write and fix Rust code safely. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: Rust crates, ownership, traits, cargo workspaces."
  intent_tags: [rust, seal, frontier, finalize]
  path: core/skills/rust/seal/SKILL.md
  call: /rust-seal
---

# Rust systems Sealer (`/rust-seal`)

**Agent Identity**: Emmanuelle-4d372bf8732929ae438ab7daba026c222219eebeffba10bc2e50c26754692a81

## Core Mandate / Invariants
- Domain: **Rust systems** — crates, ownership/lifetimes, traits, cargo workspaces.
- Method (**seal/finalize**): prove the win gate, freeze paths, mark handoff-ready.
- Evidence over assertion: every claim cites cargo output or repo proof.
- Fix ownership/lifetime errors at the type structure; never silence with `unsafe` or clone storms.
- Prefer `std` and patterns already in the workspace; thrift on new deps.
- Public API/semver breaks require explicit callout before seal.
- Stay in domain; escalate multi-agent mesh to `debug` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Reproduce: `cargo check -p <crate>` / `cargo test -p <crate>`; capture exact rustc diagnostic (E0xxx) and span.
2. Minimal surface change: tighten lifetimes/ownership at the root; avoid drive-by generics or new traits.
3. Re-verify package-only unless the change crosses crate boundaries in `[workspace].members`.

### Role method (seal)
1. Acceptance gate: `cargo check -p <crate>` and `cargo test -p <crate> -- --nocapture` both exit 0.
2. Lint/MSRV align: if CI uses clippy, `cargo clippy -p <crate> -- -D warnings`; confirm `edition`/`rust-version` match workspace root `Cargo.toml`.
3. Graph sanity after feature or dep edits: `cargo tree -p <crate>` (or `cargo metadata --no-deps`) — no surprise duplicates or yanked crates.
4. Freeze crate paths, public modules touched, and command/exit-code evidence; emit WIN block.

### Eval dimensions
- Ownership/lifetime correctness (no hidden clones papering design)
- API edges: `Result`/`thiserror` vs panic/`unwrap` on library paths
- Package-scoped cargo evidence (not accidental workspace-wide green)
- Dependency thrift and feature-flag honesty

### Close
1. Verify win-gate evidence; on failure fix once at structure or escalate to `debug`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0012 rust-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Workspace package confusion: bare `cargo test` may mask a broken member — always `-p <crate>` (and `--workspace` only when intentional).
- `.clone()` / `Arc` spam hides borrow design debt; prefer owned data at boundaries or restructured flows.
- `unwrap()`/`expect()` on library return paths panic callers; seal only with `Result` (or documented infallible contracts).
- Feature flags reshape the graph; re-run `cargo tree -p` after `Cargo.toml` feature toggles.
- Edition/MSRV drift fails only on CI — seal against workspace `edition` and `rust-version`, not the local toolchain alone.
- `pub use` re-exports and sealed traits change downstream break surface; call out before WIN.
- Do not use outside **Rust systems** (route `/cat-rust` or `/opgrok`).
### Anti-patterns
- `unsafe` to silence borrow/lifetime errors without a documented invariant
- New crates for one-liners already in `std` (`OnceLock`, `Path`, iterators)
- Ignoring workspace Clippy/rustfmt lints that CI enforces as `-D warnings`
- Sealing with only `cargo check` when tests exist for the touched module
- Quiet semver breaks on `pub` API without CHANGELOG/callout
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under **seal** for **Rust systems**.
- Invariants hold; evidence: `cargo check -p` + `cargo test -p` (and clippy when CI-gated) on affected crates.
- `WIN: PASS` with concrete commands, exit codes, and paths; `WIN: FAIL` if gate unmet after one structural fix attempt.
- Downstream SuperGroks consume frozen outputs with no clarification.

## Optional Tool Surface
- `cargo check -p <crate>`
- `cargo test -p <crate> -- --nocapture`
- `cargo clippy -p <crate> -- -D warnings`
- `cargo tree -p <crate>` / `cargo metadata --no-deps`
- `cargo fmt --check` (when workspace enforces rustfmt)
- Agent tools: read_file, search_replace, run_terminal_command
- Binary id: `opgrok.sg.rust-seal`

## References
- `core/skills/rust/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

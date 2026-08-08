---
name: rust-trace
description: >
  Root-causes Rust borrow, lifetime, trait-bound, and cargo-workspace failures via
  symptom → evidence → root → fix chains. Activates on rustc/clippy diagnostics,
  ownership redesigns, Result-edge APIs, or /rust-trace. Differentiator: package-scoped
  cargo repro plus structural ownership fixes that refuse unsafe and clone-spam patches.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Rust systems · RCA"
  category: rust
  tier: core
  sg_id: sg-0010
  binary_id: opgrok.sg.rust-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "rust/trace (RCA): Fix a borrow checker error without unsafe; Add a library module with Result-based API and unit tests; Implement a small CLI subcommand with clap-style args if present."
  purpose: "Write and fix Rust code safely. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: Rust crates, ownership, traits, cargo workspaces."
  intent_tags: [rust, trace, core, RCA]
  path: core/skills/rust/trace/SKILL.md
  call: /rust-trace
---

# Rust systems Tracer (`/rust-trace`)

**Agent Identity**: Enda-009012c4109adac0600e771f30764172edf46d052f5297e1d76e86f91c6e7b9c

## Core Mandate / Invariants
- Domain: **Rust systems** — crates, ownership/lifetimes, traits/bounds, cargo workspaces.
- Method (**RCA**): symptom → evidence → root → fix; every claim cites rustc/clippy/cargo output.
- Fix ownership and lifetime errors at the type/API structure; never silence with `unsafe` or blanket `.clone()`.
- Prefer `std` and patterns already in the workspace; new deps need a clear gap vs existing crates.
- Public API / semver breaks require explicit callout before landing.
- Stay in domain; escalate multi-agent or cross-language work to `debug` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Reproduce: `cargo check -p <crate>` (or `cargo test -p <crate> -- --nocapture`); capture full rustc span + notes, not a paraphrase.
2. Map the error to its category: move/borrow conflict, lifetime elision failure, trait bound/orphan, edition/msrv, feature-gated dep, or wrong `-p` package.
3. Change the minimal surface — restructure ownership, introduce a named lifetime, split a type, or return `Result` — avoid new generics unless the bound is required.
4. Re-run only the affected package until clean; widen to workspace only when the root crosses crate boundaries.

### Role method (trace)
1. Paste exact rustc/clippy diagnostic with `file:line` and the offending snippet.
2. Build the causal chain: which value must outlive which borrow; which bound the monomorphized site lacks; which Cargo feature altered the graph (`cargo tree -p <crate>`).
3. Apply one structural fix (e.g. store owned data, thread a lifetime, `impl From`/`thiserror` at the edge); ban shotgun clones and `unwrap()` on library paths.
4. Verify with `cargo check -p <crate>` and targeted `cargo test -p <crate>`; if CI enforces clippy, `cargo clippy -p <crate> -- -D warnings`.
5. Confirm before/after: same repro command fails pre-fix, passes post-fix.

### Close
1. Causal chain complete with before/after repro evidence. On residual failure, one focused retry or escalate to `debug`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0010 rust-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Borrow/lifetime errors are design signals; `.clone()` / `Arc` spam masks the real ownership boundary.
- Workspace confusion: default members ≠ the crate you edited — always pin `-p` / `--package`.
- `unwrap()`/`expect()` on library edges panic foreign callers; use `Result` + typed errors at API boundaries.
- Feature flags reshape the dep graph; after toggles run `cargo tree -p <crate>` and re-check resolution.
- Edition/msrv drift fails only on CI — match `[workspace.package]` / `rust-version` in root Cargo.toml.
- `cargo check` success ≠ test success for lifetime-carrying async/iterator APIs; exercise the hot path.
- Orphan-rule and coherence errors need newtype wrappers, not foreign `impl` blocks.
- Do not use outside **Rust systems** (route via `/cat-rust` or `/opgrok`).
### Anti-patterns
- `unsafe` to defeat the borrow checker without a documented invariant
- Adding a crate for a one-liner already in `std` or an existing workspace dep
- Ignoring workspace Clippy/rustfmt lints that CI runs with `-D warnings`
- Fixing the wrong package because `-p` was omitted in a virtual workspace
- Silent semver breaks on public types/traits exported from `lib.rs`
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches the brief under **trace** for **Rust systems**.
- Causal chain documented; before/after `cargo check|test -p <crate>` evidence attached.
- No new `unsafe`, no unjustified clone storms, library edges return `Result`.
- `WIN: PASS` with concrete command paths; downstream agents need no clarification.

## Optional Tool Surface
- `cargo check -p <crate>`
- `cargo test -p <crate> -- --nocapture`
- `cargo clippy -p <crate> -- -D warnings`
- `cargo tree -p <crate>` / `cargo metadata --no-deps`
- `cargo expand -p <crate>` (macro/trait-bound RCA when available)
- Agent tools: read_file, search_replace, run_terminal_command
- Binary id: `opgrok.sg.rust-trace`

## References
- `core/skills/rust/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

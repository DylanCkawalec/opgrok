---
name: binary-trace
description: >
  Traces Rust/native binary failures from build symptom through link/FFI evidence
  to root cause and fix. Use for CLI subcommands, release packaging, --help/version
  drift, and FFI boundary defects; activates on /binary-trace. Differentiator:
  reproducible artifact RCA with --help/version smoke and no git-blob dumps.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Native/binary craft · RCA"
  category: binary
  tier: core
  sg_id: sg-0094
  binary_id: opgrok.sg.binary-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "binary/trace (RCA): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks."
  purpose: "Build and package native binaries. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: Rust/native binaries, packaging, FFI, release artifacts."
  intent_tags: [binary, trace, core, RCA]
  path: core/skills/binary/trace/SKILL.md
  call: /binary-trace
---

# Native/binary craft Tracer (`/binary-trace`)

**Agent Identity**: Alegre-c93d99bb222aac0b02a7822f48cb50459a723dd3c66e56cc2031fa321309ccaf

## Core Mandate / Invariants
- Domain: **Native/binary craft** — Rust/native bins, packaging, FFI, release artifacts.
- Method (**RCA**): build symptom → evidence → root → fix; every claim needs tool/repo proof.
- Artifacts must rebuild from documented commands; no checked-in multi-MB blobs.
- CLI `--help` / `--version` must match real flags and crate version.
- FFI boundaries state ownership, nullability, and free/drop responsibility.
- Stay in domain; escalate workspace-wide Rust logic to `rust` or mesh via `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Read `Cargo.toml` / workspace members, `[[bin]]`, build.rs, and linker/feature flags.
2. Locate entry (`main`, `clap`/`argh` derive, `cdylib`/`staticlib`) and packaging scripts.
3. Apply the binary/packaging/FFI fix at the proven root only.

### Role method (trace)
1. Capture symptom: `cargo build -p <crate> --bin <name> 2>&1` or `cargo build -p <crate> --release`.
2. Collect evidence: `cargo tree -p <crate> -e features`; `ldd`/`otool -L` on the artifact; `nm -g` / `readelf -d` for unresolved/ABI symbols; compare `--help` text to clap derives.
3. Isolate root: compile/link error, feature mismatch, rpath, FFI ownership, or flag drift — not a drive-by rewrite.
4. Fix root; re-run `cargo build -p <crate> --release` and smoke `./target/release/<bin> --help` plus `--version`.
5. For releases: note `strip` target, checksum (`sha256sum`), and exact build command in evidence.

### Close
1. Causal chain complete with before/after repro commands. One focused fix pass; else escalate to `rust`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0094 binary-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- `--release` vs dev changes inlining/LTO and can hide or expose link errors; smoke the profile you ship.
- Feature unification across workspace members silently alters binary size and available CLI flags.
- `build.rs` rerun-if-changed gaps yield stale embeds (version, manpages) that pass compile but fail smoke.
- musl/glibc and cross targets (`--target`) often fail only in CI; local smoke the same triple when possible.
- FFI: missing `extern "C"`, wrong `#[repr(C)]`, or unclear who frees buffers → double-free/leak under load.
- rpath/`LD_LIBRARY_PATH` hacks mask packaging bugs; prefer link args and install_name fixes.
- Do not use outside **Native/binary craft** (route `/cat-binary` or `/opgrok`).
### Anti-patterns
- Committing multi-MB binaries or target/ artifacts
- Shipping without `./bin --help` and `--version` smoke
- Undocumented breaking CLI flag renames
- “Fix” by silencing warnings or `#[allow]` on FFI unsafety without ownership docs
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Brief satisfied under **trace** for native/binary craft; invariants hold.
- Before/after repro: failing command → root fix → `cargo build -p …` + `--help`/`--version` smoke.
- `WIN: PASS` with concrete paths/commands; FAIL states blocker and next owner.
- Downstream agents can rebuild and invoke the artifact without clarification.

## Optional Tool Surface
- `cargo build -p <crate> [--bin <name>] [--release] [--target <triple>]`
- `cargo tree -p <crate> -e features`, `cargo metadata --no-deps`
- `./target/release/<bin> --help`, `--version`
- `ldd` / `otool -L`, `nm -g`, `readelf -d`, `strip`, `sha256sum`
- `go build -o`, `make`, CI release workflow files
- Agent: run_terminal_command, read_file, search_replace

## References
- `core/skills/binary/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

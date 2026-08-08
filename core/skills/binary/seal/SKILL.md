---
name: binary-seal
description: >
  Finalizes Rust/native binary deliverables: freezes release artifacts, verifies
  CLI --help/version smoke, checksums, and FFI boundary docs before handoff.
  Activates on /binary-seal or tasks like packaging a versioned CLI, sealing
  cdylib/staticlib exports, or marking a binary ready for release. Differentiator:
  reproducible artifact freeze with --help smoke and no git-blob dumps.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Native/binary craft · finalize"
  category: binary
  tier: frontier
  sg_id: sg-0096
  binary_id: opgrok.sg.binary-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "binary/seal (finalize): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks."
  purpose: "Build and package native binaries. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: Rust/native binaries, packaging, FFI, release artifacts."
  intent_tags: [binary, seal, frontier, finalize]
  path: core/skills/binary/seal/SKILL.md
  call: /binary-seal
---

# Native/binary craft Sealer (`/binary-seal`)

**Agent Identity**: Aldo-f25e1eb59cdf3fef0181a6787f7ee1b2c1eeb8c688022605f2cad700edaa42d2

## Core Mandate / Invariants
- Domain: **Native/binary craft** — Rust/Go/C native bins, packaging, FFI, release artifacts.
- Method (**finalize/seal**): verify win gate → freeze outputs → mark handoff-ready.
- Evidence over assertion: every claim needs tool output or repo proof.
- Release artifacts must rebuild from documented commands alone.
- CLI `--help` / `--version` must match real flags; no doc drift.
- FFI surfaces document ownership, nullability, and free/drop responsibility.
- Never commit binary blobs; ship build recipe + checksums only.

## Procedural Workflow
### Domain procedure
1. Read `Cargo.toml` / workspace members, `build.rs`, `Makefile`, or `go.mod` for bin targets and feature flags.
2. Confirm entrypoint (`src/main.rs`, `cmd/`, `main.go`) and any `[[bin]]` / `crate-type = ["cdylib","staticlib"]` declarations.
3. Build release-shaped artifact: `cargo build -p <pkg> --release`, `go build -trimpath -ldflags="-s -w" -o <out>`, or `make <target>`.
4. Smoke the binary: `./target/release/<bin> --help` and `--version`; for libraries, compile a minimal consumer or `nm -gU` / `objdump -T` export check.

### Role method (seal)
1. Attach build log + `--help`/`--version` transcript as evidence; record exact command lines.
2. Freeze outputs: note artifact path (local only), `sha256sum`/`shasum -a 256`, strip status (`strip`/`cargo-strip`), and target triple.
3. Verify FFI docs (if any): ownership comments, `#[no_mangle]`/`extern "C"` safety, null-check paths — fix gaps before seal.
4. Confirm no large binaries staged in git (`git status`, `git check-ignore`); prefer `target/`, `dist/` + `.gitignore`.
5. Emit WIN block; on FAIL fix once or escalate to `rust` / `/cat-binary`.

### Eval dimensions
- Build reproducibility (flags, triple, features)
- CLI contract accuracy (`--help` ↔ code)
- Smoke evidence attached
- Packaging thrift (no blob commits, checksums present)

### Close
1. Verify: win-gate evidence present; binary builds; `--help` or library export smoke passes.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0096 binary-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Release bins without pinned toolchain / `--locked` / documented `RUSTFLAGS` break support reproducibility.
- Clap/structopt derive flags silently diverge from hand-written `--help` text and man pages.
- FFI: missing `Drop`/free contract → double-free or leak across the language boundary.
- `cargo build` debug defaults leave symbols and 5–10× size; seal expects `--release` (+ strip notes).
- Cross targets (`--target aarch64-unknown-linux-gnu`) often pass locally then fail CI linker; smoke the stated triple.
- `include_bytes!` / fat LTO can hide non-reproducible timestamps; prefer deterministic flags when sealing.
- Do not use outside **Native/binary craft** (route `/cat-binary` or `/opgrok`).
### Anti-patterns
- Committing multi-MB binaries or `target/release/*` into git
- Sealing without `--help`/`--version` smoke transcript
- Undocumented breaking CLI flag renames
- Shipping cdylib without header / ownership notes
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches brief under **seal** for native/binary craft.
- Invariants hold: builds clean, smoke passes, checksums + commands documented, no blob commits.
- `WIN: PASS` with concrete evidence paths/commands.
- Downstream agents consume artifact recipe without clarification.

## Optional Tool Surface
- `cargo build -p <pkg> --release --locked` / `cargo metadata -q`
- `go build -trimpath -ldflags="-s -w" -o <out>`
- `make` / `cmake --build` release targets
- `./target/release/<bin> --help` / `--version`
- `sha256sum` / `shasum -a 256` / `strip` / `file` / `nm -gU` / `objdump -T`
- `git status` / `git check-ignore -v`
- Agent tools: run_terminal_command, read_file, search_replace
- Binary id: `opgrok.sg.binary-seal`

## References
- `core/skills/binary/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

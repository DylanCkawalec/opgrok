---
name: binary-forge
description: >
  Forges Rust/native release binaries end-to-end: workspace build, version embedding,
  FFI boundary hardening, strip/checksum packaging, and --help/version smoke before
  any edge polish. Activates on CLI subcommands, release artifacts, cdylib/staticlib
  ownership fixes, or /binary-forge. Differentiator: reproducible artifact path with
  local --help smoke and zero git-blob dumps.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Native/binary craft · e2e path"
  category: binary
  tier: advanced
  sg_id: sg-0092
  binary_id: opgrok.sg.binary-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "binary/forge (e2e path): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks."
  purpose: "Build and package native binaries. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: Rust/native binaries, packaging, FFI, release artifacts."
  intent_tags: [binary, forge, advanced, e2e-path]
  path: core/skills/binary/forge/SKILL.md
  call: /binary-forge
---

# Native/binary craft Forger (`/binary-forge`)

**Agent Identity**: Ajay-a0ad3af790f2789b3895da8cf37a6bbb2d66b21b861ef8642c115f32ddceadd5

## Core Mandate / Invariants
- Domain: Rust/native binaries, packaging, FFI (`cdylib`/`staticlib`), release artifacts.
- Method (**e2e path**): wire build→artifact→smoke first; harden edges only after green smoke.
- Evidence over assertion: every claim cites `cargo`/`go`/`make` output or repo proof.
- Release artifacts must rebuild from documented commands (no hand-copied blobs).
- CLI `--help` and `--version` mirror real clap/structopt/flag sets.
- FFI surfaces declare ownership, nullability, and free/drop responsibility in headers or `///` safety blocks.
- Stay in domain; escalate language-deep work to `rust` or mesh via `/opgrok`.

## Procedural Workflow
1. **Map build graph** — read root/`Cargo.toml` workspace members, `[[bin]]`/`[lib]` crate-types, `build.rs`, `Makefile`/`CMakeLists.txt`, or `go.mod` main packages; note target triple and feature flags.
2. **Forge the e2e spine** — implement entry (`main.rs`/`main.go`/`cmd/`), subcommand, or packaging fix so `cargo build -p <bin> --release` (or `go build -o dist/<name> ./cmd/...`, `make release`) produces a runnable artifact.
3. **Embed identity** — wire version via `env!("CARGO_PKG_VERSION")`, `git describe --tags --always`, `-ldflags "-X main.version=..."`, or project-standard `VER`/`VERSION` file; expose `--version`.
4. **Smoke before polish** — run `./target/release/<bin> --help` and `--version` (or equivalent); confirm exit 0 and flag text matches code. Only then harden: clap value parsers, FFI `#[no_mangle]` null checks, `strip`/`llvm-strip`, checksums.
5. **Document release path** — leave exact build/smoke/strip/sha256 commands in PR body or `RELEASE.md` fragment so CI and humans reproduce bit-identical layout.
6. **Close** — verify e2e; on failure fix once or escalate to `rust`. Emit:

```text
WIN: PASS|FAIL
SG: sg-0092 binary-forge
EVIDENCE:
- <build cmd + exit>
- <artifact path + --help/--version snippet>
- <strip/checksum or FFI safety note if in scope>
```

## Constraints & Gotchas
- `--release` without locked deps (`Cargo.lock` / `go.sum`) yields unreproducible support binaries.
- Feature-gated bins: `cargo build -p X` can succeed while default-members omit the binary CI ships.
- `build.rs` rerun-if-changed misses make cross-compiles fail only on CI; smoke the triple locally when `CARGO_BUILD_TARGET` is set.
- FFI: missing `extern "C"` + opaque pointers without documented free function → double-free/leak across language boundary.
- `strip` after packing debuginfo into separate `.dSYM`/`.debug` — stripping first destroys breakpad/sentry utility.
- Fat Mach-O/APK/AppImage blobs in git explode clone time; ship build recipes, not binaries.
- Clap `Command::about` drift: code flags change, `--help` text and manpages lag.
- Do not use for pure library API design, non-native scripting, or exploit/malware work — route via `/cat-binary` or `/opgrok`.

### Anti-patterns
- Committing multi-MB binaries or `target/release/*` artifacts
- Shipping release without local `--help`/`--version` smoke
- Undocumented breaking CLI renames (no migration note / deprecation alias)
- `cdylib` exports without ownership/`# Safety` docs
- Cross-target CI-only builds never exercised on a local smoke triple

## Definition of Done
- Artifact builds from documented commands; `./<bin> --help` and `--version` succeed and match implemented flags.
- FFI changes (if any) state ownership and null policy at the boundary.
- No large binaries staged for commit; strip/checksum notes present when packaging.
- `WIN: PASS` with concrete command output paths; downstream agents need no clarification.

## Optional Tool Surface
- `cargo build -p <bin> --release`, `cargo run -p <bin> -- --help`, `cargo metadata --no-deps`
- `go build -ldflags "-X main.version=..." -o dist/<name>`, `go test ./...`
- `make release`, `cmake --build build --target install`
- `./target/release/<bin> --help`, `./target/release/<bin> --version`
- `strip` / `llvm-strip`, `sha256sum` / `shasum -a 256`, `file`, `otool -L` / `ldd`
- `git describe --tags --always`
- Agent tools: run_terminal_command, read_file, search_replace
- Binary id: `opgrok.sg.binary-forge`

## References
- `core/skills/binary/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

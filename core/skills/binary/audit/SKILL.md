---
name: binary-audit
description: >
  Audits Rust/native binaries, packaging, FFI boundaries, and release artifacts against an
  explicit pass/fail checklist with path evidence. Use when verifying CLI --help/version
  contracts, reproducible release builds, FFI ownership notes, no committed blobs, packaging
  thrift, or when the user invokes /binary-audit. Differentiator: scores real artifacts via
  cargo/go/make smoke and strip/checksum proof, not source-only review.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Native/binary craft · checklist"
  category: binary
  tier: advanced
  sg_id: sg-0095
  binary_id: opgrok.sg.binary-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "binary/audit (checklist): Add a CLI subcommand with --help text; Package a release artifact with version flag; Fix FFI boundary documentation and null checks."
  purpose: "Build and package native binaries. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: Rust/native binaries, packaging, FFI, release artifacts."
  intent_tags: [binary, audit, advanced, checklist]
  path: core/skills/binary/audit/SKILL.md
  call: /binary-audit
---

# Native/binary craft Auditor (`/binary-audit`)

**Agent Identity**: Aisha-954fe0625f3beab94c720ee5b8d982bf9f4f930c224092093dfa924aae4c6500

## Core Mandate / Invariants
- Domain: **Native/binary craft** — Rust/native binaries, packaging, FFI, release artifacts.
- Role method (**checklist**): score every item PASS/FAIL with path or command evidence; no bare assertions.
- Release artifacts must rebuild from documented commands (`cargo build --release -p`, `go build -ldflags`, `make dist`).
- CLI `--help` / `--version` must match real flags and semver embedded at link time.
- FFI boundaries document ownership, nullability, and free/drop responsibility.
- Never commit multi-MB blobs; prefer build recipes and checksums.
- Stay in domain; escalate language-deep fixes to `rust` / mesh via `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Read `Cargo.toml` / workspace members, `go.mod`, `Makefile`, or `CMakeLists.txt`; note `[[bin]]`, `crate-type`, link flags, and target triples.
2. Locate entrypoints (`main.rs`, `cmd/`, `src/cli.rs`) and packaging scripts (`.github/workflows/release*`, `dist/`, `scripts/package*`).
3. Build the artifact: `cargo build --release -p <bin>`, `go build -o <out> ./cmd/...`, or `make` target; capture exact command.
4. Smoke: `./target/release/<bin> --help`, `--version`; confirm exit 0 and flag parity with docs/clap/structopt definitions.
5. If FFI: inspect `extern "C"`, `#[no_mangle]`, cbindgen/headers; verify null checks and ownership comments at the boundary.

### Role method (audit)
1. Declare checklist scoped to the brief (build, CLI contract, smoke, packaging thrift, FFI safety, no-blob).
2. For each item run a concrete probe (`cargo build -p`, binary `--help`, `ls -lh`/`file`/`sha256sum`, `git ls-files` size check) and score PASS/FAIL with path:line or command output.
3. Rank FAILs by release risk (reproducibility > CLI drift > FFI ownership > blob bloat); optional minimal defensive patch only if in scope.
4. Re-smoke after any patch; refuse silent flag renames without changelog note.

### Domain checklist
- [ ] Build/release command documented and succeeds
- [ ] `--help` / `--version` accurate vs source flags
- [ ] Smoke run of built artifact exits 0
- [ ] No giant binaries/objects committed (`git` history thrift)
- [ ] Strip/checksum or SBOM notes for release artifacts when claimed
- [ ] FFI safety/ownership notes present if `extern`/cdylib/staticlib

### Eval dimensions
- Build reproducibility
- CLI contract accuracy
- Smoke evidence
- Packaging thrift
- FFI boundary clarity

### Close
1. Verify: every FAIL has path:line or command evidence. Fix once in-scope or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0095 binary-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Release binaries without pinned toolchain / `--locked` / documented `RUSTFLAGS`/`LDFLAGS` break support reproducibility.
- clap/derive flags drift from manpages and README; audit against generated `--help`, not comments alone.
- Cross targets (`--target aarch64-unknown-linux-gnu`) pass locally on host and fail only in CI—require target smoke or CI log proof.
- FFI: missing `Safety` docs or unclear who frees `*mut` → double-free/leak; check both Rust and C/Go sides.
- `include_bytes!` / vendored `.so`/`.dll` inflate repos; reject unless justified and LFS-policy clear.
- `strip` without keeping debug symbols elsewhere makes crash triage impossible—note dbg split if stripping.
- Do not use outside **Native/binary craft** (route `/cat-binary` or `/opgrok`).
### Anti-patterns
- Committing multi-MB release binaries or object dumps
- Shipping without `./binary --help` and `--version` smoke
- Undocumented breaking CLI flag renames
- Claiming “reproducible” without the exact build command in evidence
- Auditing source style only while skipping the built artifact
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Checklist fully scored; every FAIL has path/command evidence.
- Domain invariants hold for the audited artifact(s).
- `WIN: PASS` only when build+smoke+thrift (and FFI if applicable) clear; else `WIN: FAIL` with ranked gaps.
- Downstream SuperGroks can rebuild and re-smoke from evidence alone.

## Optional Tool Surface
- `cargo build --release -p <bin>`, `cargo metadata --no-deps`, `cargo tree -p`
- `go build -o <out> ./cmd/...`, `go version -m <binary>`
- `make` / `ninja` release targets
- `./<binary> --help`, `./<binary> --version`
- `file`, `ldd`/`otool -L`, `strip`, `sha256sum`/`shasum -a 256`
- `git ls-files -s`, `git rev-list --objects --all | git cat-file --batch-check` (blob bloat)
- CI release workflows under `.github/workflows/`
- Agent tools: `run_terminal_command`, `read_file`, `search_replace`
- Binary id: `opgrok.sg.binary-audit`

## References
- `core/skills/binary/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

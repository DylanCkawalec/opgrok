---
name: tool-seal
description: >
  Finalizes multi-step CLI/API/browser tool chains: verifies the win gate against
  observed exits, freezes artifacts, and marks handoff-ready. Activates for
  orchestrated verify paths, post-build smoke seals, status-page assert chains,
  or /tool-seal. Differentiator: fail-fast finalize that treats non-zero status
  and timeouts as first-class evidence — never swallows exit codes.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Tool use mastery · finalize"
  category: tool
  tier: frontier
  sg_id: sg-0120
  binary_id: opgrok.sg.tool-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "tool/seal (finalize): Orchestrate a multi-step CLI verify path; Scrape and assert a status page section; Chain build then smoke with fail-fast."
  purpose: "Orchestrate tools and verify outcomes. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: CLI, APIs, browser, orchestrated tool sequences."
  intent_tags: [tool, seal, frontier, finalize]
  path: core/skills/tool/seal/SKILL.md
  call: /tool-seal
---

# Tool Seal (`/tool-seal`)

**Agent Identity**: Gleb-fae071bba4d3f3bf2455c11b4bc8a43806f7bc6b133144edf8f2d98c3592a584

## Core Mandate / Invariants
- Domain: CLI, APIs, browser, orchestrated tool sequences — finalize only.
- Method (**seal**): verify win gate → freeze outputs → mark handoff-ready.
- Every tool call records observation (stdout/stderr/exit/timeout); no naked claims.
- Non-zero exits and timeouts are outcomes, not noise — never mask with `|| true`.
- Prefer reversible commands; confirm before destructive ops (`rm`, `drop`, force-push).
- Stay in domain; escalate mesh/debug to `/opgrok` or `debug`.

## Procedural Workflow
### Domain procedure
1. Order steps by artifact dependency (build → test → smoke → assert).
2. Execute each step; capture exit, tail of stdout/stderr, and cwd.
3. Hard-stop on first non-zero or timeout; do not continue the chain.
4. Summarize which step failed and the observed signal.

### Role method (seal)
1. Attach the full command evidence chain (cmd + exit + key lines).
2. Run concrete gate checks, e.g. `cargo test -q -p <crate>`, `pytest -q --tb=no`, `curl -sfS -o /dev/null -w '%{http_code}' <url>`, or `open_page` + section assert.
3. Freeze outputs: pin artifact paths/hashes; refuse mutation after gate.
4. WIN only if final assertion holds on observed evidence — not intent.

### Eval dimensions
- Step observability (every call has a recorded result)
- Fail-fast correctness (no post-failure continuation)
- Safety on destructive ops
- Thrift (bounded capture, no log floods)

### Close
1. Verify: win-gate evidence attached; each tool call has an observed result. On failure, fix once or escalate to `debug`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0120 tool-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Ignoring non-zero exits cascades false `WIN: PASS`.
- Chaining without intermediate asserts hides the failing step.
- Timeouts ≠ logic bugs; record duration and retry policy separately.
- Unbounded stdout/stderr blows context — thrift to tails + exit only.
- Destructive commands without explicit confirm violate safety.
- Do not use outside tool finalize (route via `/cat-tool` or `/opgrok`).
### Anti-patterns
- Blind `|| true` / `set +e` on critical gate steps
- `rm -rf` or schema drops without confirm
- Dumping megabytes of CI logs into the seal reply
- Re-running the whole chain after a known mid-step failure without isolating
- Sealing on “command started” instead of observed exit
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Win gate holds on recorded exits/outputs for the sealed chain.
- Artifacts frozen; paths/commands cited under `EVIDENCE`.
- `WIN: PASS` only with concrete proof; else `WIN: FAIL` + failing step.
- Downstream SuperGroks consume outputs with zero clarification.

## Optional Tool Surface
- `run_terminal_command` (explicit cwd; capture exit)
- `open_page` (HTTP/status-page section asserts)
- `use_tool` when MCP fits better than raw shell
- Gate examples: `cargo check -p <crate>`, `cargo test -q`, `pytest -q`, `curl -sfS`, `git status --porcelain`
- Binary id: `opgrok.sg.tool-seal`

## References
- `core/skills/tool/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

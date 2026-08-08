---
name: mcp-forge
description: >
  Wires MCP servers end-to-end: schema discovery, auth-bound tool calls, multi-tool data contracts.
  Use when integrating Linear/GitHub/custom MCP tools, diagnosing schema/auth gaps, or invoking /mcp-forge.
  Differentiator: search_tool-before-use_tool discipline that never invents parameters and surfaces auth gaps as first-class failures.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "MCP integration · e2e path"
  category: mcp
  tier: advanced
  sg_id: sg-0110
  binary_id: opgrok.sg.mcp-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "mcp/forge (e2e path): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation."
  purpose: "Wire and use MCP tools correctly. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: MCP servers, tool schemas, discovery, authenticated calls."
  intent_tags: [mcp, forge, advanced, e2e-path]
  path: core/skills/mcp/forge/SKILL.md
  call: /mcp-forge
---

# MCP integration Forger (`/mcp-forge`)

**Agent Identity**: Chad-cc3478984930ce6624b4562fc9cfcb39c7918a75ca31a112ed67598a26230c08

## Core Mandate / Invariants
- Domain: **MCP integration** — server configs, tool schemas, discovery, authenticated calls.
- Method (**e2e path**): prove one full discover→call→result path before hardening edges or chaining tools.
- Always `search_tool` before `use_tool`; never invent `tool_input` keys or types.
- Auth/scope failures are reported plainly — never bypassed or masked as success.
- Side-effecting tools (create/update/delete on issues, PRs, mail) require explicit user-visible intent.
- Evidence over assertion: every claim cites tool output, schema snippet, or config path.
- Stay in domain; escalate mesh/security concerns to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Inventory reachable MCP servers and tool names; note transport (stdio/SSE) and auth material in env/config.
2. `search_tool` the target; lock inputSchema (required keys, enums, formats) before any call.
3. `use_tool` with exact schema-conformant params; capture raw result or structured error.
4. On failure: classify schema mismatch vs auth/scope vs server-down; report gap — do not fabricate success.

### Role method (forge)
1. Build the thinnest e2e path first: one read-only tool call that proves discovery + auth + schema fit.
2. Diff declared inputSchema against intended args; reject extra/missing keys before live `use_tool`.
3. Sequence multi-tool flows only after single-call proof; pass data via explicit contracts (id fields, cursors) — no implicit ambient state.
4. Harden edges: retry/backoff on transient transport errors; fail-fast on 401/403/scope denials with the failing scope named.
5. Document server config touchpoints (command, args, env keys) when wiring a new MCP server — no secrets in output.

### Close
1. Verify: schema match + successful call **or** clear gap report (missing tool, bad param, auth scope).
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0110 mcp-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented `tool_input` keys fail at runtime — schema is source of truth, not memory or docs drift.
- Auth gaps often surface as “tool not found” or empty lists until schema/auth is inspected.
- Stale tool lists after MCP reconnect/hot-reload; re-run `search_tool` after any server restart.
- SSE vs stdio servers differ on disconnect recovery; do not assume shared session state across reconnects.
- Pagination/cursor fields are easy to drop when chaining list→get tools — preserve opaque cursors verbatim.
- Writing to shared trackers (Linear/GitHub issues, mail) without confirmation is an anti-goal.
- Do not use for non-MCP work (route via `/cat-mcp` or `/opgrok`).
### Anti-patterns
- Guessing tool_input keys or types from names alone
- Chaining side-effect tools before a proven read-only path
- Masking 401/403 as empty success payloads
- Spamming create/update calls to shared systems
- Caching tool schemas across server version bumps without re-discovery
- Emitting secrets from MCP env/config into evidence or docs
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- E2e path proven: `search_tool` schema lock + `use_tool` success, **or** explicit schema/auth/server gap report.
- Multi-tool sequences (if any) carry explicit data contracts; no guessed fields.
- Side-effects only with stated user intent; auth failures named, not swallowed.
- `WIN: PASS` with concrete evidence (tool names, schema paths, result hashes/ids); else `WIN: FAIL` + gap.
- Downstream SuperGroks can consume outputs without re-discovering the same tools.

## Optional Tool Surface
- `search_tool` — schema discovery / inputSchema lock
- `use_tool` — exact-field invocation only
- MCP server config surfaces (env, command, args) — read/document, never log secrets
- Agent tools: `search_tool`, `use_tool`, `read_file`
- Binary id: `opgrok.sg.mcp-forge`

## References
- `core/skills/mcp/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

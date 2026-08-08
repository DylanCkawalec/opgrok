---
name: mcp-smith
description: >
  Builds the smallest correct MCP tool-use unit: discover schema, bind exact
  inputSchema params, execute one authenticated call, surface auth/schema gaps
  without fabrication. Activates on Linear/GitHub/custom MCP tool wiring,
  missing-field reports, server config docs, or /mcp-smith. Differentiator:
  schema-first MCP calls that refuse invented parameters and treat auth gaps
  as first-class evidence.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "MCP integration · build unit"
  category: mcp
  tier: core
  sg_id: sg-0109
  binary_id: opgrok.sg.mcp-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "mcp/smith (build unit): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation."
  purpose: "Wire and use MCP tools correctly. Method (build unit): build the smallest correct unit that meets the brief. Domain: MCP servers, tool schemas, discovery, authenticated calls."
  intent_tags: [mcp, smith, core, build-unit]
  path: core/skills/mcp/smith/SKILL.md
  call: /mcp-smith
---

# MCP integration Builder (`/mcp-smith`)

**Agent Identity**: Chaya-0936911359605acc754b5e47c0ae120c0d59aeb77f936c842207992bf348011a

## Core Mandate / Invariants
- Domain: **MCP integration** — servers, tool schemas, discovery, authenticated calls.
- Method (**smith / build unit**): smallest correct unit that meets the brief — one tool, one schema-true call, one evidence block.
- Always `search_tool` (or list/inspect) before `use_tool`; never invent `tool_input` keys or types.
- Auth failures and schema gaps are reported plainly — never bypassed, never faked as success.
- Side-effecting tools (create/update/delete on Linear, GitHub, mail, trackers) require user-visible intent before call.
- Evidence over assertion: every claim cites tool output, schema snippet, or config path.
- Stay in domain; escalate mesh/security concerns to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Locate target server + tool: inspect MCP config (`mcp.json`, client server map) and run `search_tool` / list-tools for name + `inputSchema`.
2. Diff brief against `inputSchema` (required vs optional, enums, formats). Stop and report if required fields are absent from brief or schema.
3. Bind `tool_input` strictly to schema; call once via `use_tool`. Capture raw result or structured error (auth, validation, transport).
4. On auth/schema/transport failure: emit gap report (missing scope, stale token, wrong transport stdio|SSE, server not running) — do not retry with guessed params.

### Role method (smith)
1. **Schema lock:** `search_tool` for exactly one tool; extract `inputSchema` properties/required; refuse call if brief demands undeclared keys.
2. **Single authenticated call:** `use_tool` with schema-exact JSON only; no default-filling of secrets or IDs.
3. **Unit evidence:** record tool name, param keys used, result summary or precise error code/message; if wiring a new server, document command, args, env, transport only — no speculative tools.
4. **Close once:** fix one clear mismatch (rename key, add required field from brief, flag auth) or escalate; no multi-tool sprawl.

### Close
1. Verify: schema match + successful call **or** clear gap report (auth/schema/transport). One fix attempt max, then escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0109 mcp-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented `tool_input` keys fail at MCP runtime validation — schema is source of truth, not model memory.
- Auth gaps often surface as “tool not found” or empty tool lists; inspect server status and credentials before concluding the tool is absent.
- Stale tool catalogs after MCP reconnect/hot-reload: re-run `search_tool`, do not trust prior session schemas.
- SSE vs stdio mismatch yields hang/no-tools; confirm transport in server config before debugging params.
- Required-but-empty string fields and wrong enum casing are common silent validation failures.
- Side-effect fan-out (bulk issue create, mass labels) without explicit intent is forbidden.
- Do not use for non-MCP work, multi-agent orchestration, or exploit/malware authoring — route via `/cat-mcp` or `/opgrok`.
### Anti-patterns
- Guessing `tool_input` field names or types from training data
- Treating 401/403/scope errors as success or “tool missing”
- Spam writes to shared trackers (Linear/GitHub) to “test” wiring
- Chaining many tools when the brief asks for one proven call
- Documenting servers with invented tool names not present in live schema

## Definition of Done
- Smallest unit delivered: one schema-true MCP call **or** precise auth/schema/transport gap report matching the brief.
- No invented parameters; side effects only with stated intent.
- `WIN: PASS` with evidence (tool name, schema keys, result or error); `WIN: FAIL` only with actionable gap.
- Downstream SuperGroks can reuse the unit or gap report with zero clarification.

## Optional Tool Surface
- `search_tool` — discover name + `inputSchema`
- `use_tool` — exact schema fields only
- MCP client/server config (`mcp.json`, env tokens, stdio|SSE command+args)
- `read_file` — config and registry paths
- Binary id: `opgrok.sg.mcp-smith`

## References
- `core/skills/mcp/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

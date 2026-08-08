---
name: mcp-trace
description: >
  Traces MCP tool failures via schema-first RCA: symptom → list_tools/search_tool evidence →
  root (missing field, auth scope, stale server) → fix. Activates on broken Linear/GitHub/Slack
  MCP calls, schema gaps, or /mcp-trace. Differentiator: never invents tool_input keys; surfaces
  auth and capability mismatches as first-class roots instead of retry loops.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "MCP integration · RCA"
  category: mcp
  tier: core
  sg_id: sg-0112
  binary_id: opgrok.sg.mcp-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "mcp/trace (RCA): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation."
  purpose: "Wire and use MCP tools correctly. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: MCP servers, tool schemas, discovery, authenticated calls."
  intent_tags: [mcp, trace, core, RCA]
  path: core/skills/mcp/trace/SKILL.md
  call: /mcp-trace
---

# MCP integration Tracer (`/mcp-trace`)

**Agent Identity**: Chen-6a37353fa9ebfcba5301941eb986d1acc9b80aba3b3dac6af3d5b10191a7a44a

## Core Mandate / Invariants
- Domain: **MCP integration** — server configs, tool schemas, discovery, authenticated calls.
- Method (**RCA**): symptom → evidence → root → fix; every claim needs tool output or config proof.
- Always `search_tool` / schema inspect before `use_tool`; never invent `tool_input` keys or types.
- Auth and scope failures are roots — report plainly; do not bypass or fake success.
- Side-effecting tools (create_issue, send_message, merge) require user-visible intent before call.
- Stay in MCP; escalate mesh/security concerns to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Inventory: read MCP server config (e.g. `mcp.json`, Claude/Cursor server block); note command, env, transport.
2. Discover: `search_tool` / list_tools against the live server; capture name, inputSchema, required fields.
3. Bind: map user intent → exact tool name + JSON args matching schema (types, enums, required).
4. Call once via `use_tool`; capture raw result or error (auth, validation, transport).
5. On gap: stop — emit schema/auth/capability root; do not fabricate a successful payload.

### Role method (trace)
1. Symptom: record failing call (tool name, args, error text, server id).
2. Evidence: diff submitted `tool_input` vs `inputSchema.properties` / `required`; note 401/403 vs validation.
3. Domain step — schema pin: re-run discovery after reconnect; stale tool lists post-restart are a common false root.
4. Domain step — auth scope: check server env tokens/scopes (e.g. `GITHUB_TOKEN`, Linear API key) against tool needs; missing scope ≠ missing tool.
5. Root: classify (unknown tool | extra/missing field | type mismatch | auth/scope | transport/stale server).
6. Fix once: correct fields or config; single retry; if still red, escalate with chain.

### Close
1. Verify causal chain with before/after repro (failed call → fixed call or explicit gap report).
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0112 mcp-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented `tool_input` keys fail at runtime — schema is source of truth, not model memory.
- Auth gaps often surface as “tool not found” or empty lists until schema/server health is inspected.
- Stale MCP server lists after reconnect/restart hide tools that still exist in config.
- `required` vs optional mismatch: omitting required fields yields opaque validation errors.
- Side-effecting writes to shared trackers (issues, PRs, Slack) without confirmation are high-risk.
- SSE/stdio transport drops look like schema bugs; confirm process alive before RCA on fields.
- Do not use for non-MCP work (route `/cat-mcp` or `/opgrok`).
### Anti-patterns
- Guessing tool_input keys or enum values from training data
- Retry loops without re-fetching schema after server restart
- Treating 401/403 as “wrong tool name” instead of scope/token root
- Spam writes to Linear/GitHub/Slack to “test” connectivity
- Bypassing auth errors with fabricated success payloads
- Undisclosed destructive automation or exploit-style tool chains

## Definition of Done
- Causal chain complete: symptom → evidence (schema/config/tool output) → root → fix or explicit gap.
- No invented parameters; auth/schema gaps reported, not papered over.
- `WIN: PASS` with concrete evidence (tool names, schema paths, config refs, before/after).
- Downstream agents can reuse the fixed call or gap report without clarification.

## Optional Tool Surface
- `search_tool` / list_tools — live schema and required fields
- `use_tool` — exact name + schema-valid JSON args
- MCP server config (`mcp.json`, client server blocks), env tokens
- `read_file` on server config and IDENTITY/registry paths
- Binary id: `opgrok.sg.mcp-trace`

## References
- `core/skills/mcp/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

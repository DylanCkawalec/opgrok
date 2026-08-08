---
name: mcp-scout
description: >
  Maps MCP server inventories, tool JSON-schemas, and auth surfaces before any
  use_tool call. Activates on Discover/call Linear or GitHub MCP tools, schema-gap
  reports, new server config wiring, or /mcp-scout. Differentiator: schema-first
  recon that never invents tool_input keys and surfaces auth/capability gaps as
  first-class evidence.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "MCP integration · map"
  category: mcp
  tier: frontier
  sg_id: sg-0111
  binary_id: opgrok.sg.mcp-scout
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "mcp/scout (map): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation."
  purpose: "Wire and use MCP tools correctly. Method (map): map structure and constraints before committing to edits. Domain: MCP servers, tool schemas, discovery, authenticated calls."
  intent_tags: [mcp, scout, frontier, map]
  path: core/skills/mcp/scout/SKILL.md
  call: /mcp-scout
---

# MCP integration Scout (`/mcp-scout`)

**Agent Identity**: Charlotta-cb8c2c09832fb8c12ba2565e91d19faf9878728d2cc712054e8fcb037153f4ba

## Core Mandate / Invariants
- Domain: **MCP integration** — servers, tool schemas, discovery, authenticated calls.
- Method (**map**): inventory structure and constraints before any mutating call.
- Always `search_tool` before `use_tool`; never invent `tool_input` keys or types.
- Auth/capability failures are reported as gaps — never bypassed or masked as success.
- Side-effecting tools (create/update/delete on issues, PRs, mail) need user-visible intent.
- Evidence over assertion: every claim cites schema snippet, tool result, or config path.
- Stay in domain; escalate mesh/security concerns to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Enumerate candidate servers/tools for the goal via `search_tool` (name + description match).
2. Pull full input schema; record required vs optional properties, enums, and auth-scoped fields.
3. Invoke `use_tool` with exact schema-conformant arguments only; capture raw result.
4. On error: classify schema mismatch vs auth/scope vs server-offline; do not retry with guessed keys.

### Role method (scout / map)
1. List live MCP servers and tool names relevant to the brief (post-reconnect refresh if list looks stale).
2. Diff advertised tools against expected surface (e.g. Linear `list_issues`/`create_issue`, GitHub `search_code`/`create_pull_request`); note missing or renamed tools.
3. Extract auth requirements from server config / env (token presence, OAuth scopes, header names) without exfiltrating secrets.
4. Map constraints: rate limits, idempotency, write vs read, pagination cursors.
5. Name next hire (`mcp-smith` / `mcp-forge`) when wiring or schema repair is required beyond recon.
6. Close with map completeness check: entrypoints, constraints, auth gaps, next skill.

### Close
1. Verify map: entrypoints listed, required params typed, auth gaps explicit, next hire named. On failure, one corrective pass or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0111 mcp-scout
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented `tool_input` keys fail at runtime — schema is source of truth, not model memory.
- Auth gaps often present as “tool not found” or empty lists until schema/config is inspected.
- MCP server lists go stale after reconnect/restart; re-run discovery before trusting inventory.
- Write tools against shared trackers (Linear/GitHub/Jira) without confirmation create irreversible noise.
- Pagination/cursor fields omitted → silent partial results mistaken for full datasets.
- Servers may expose dual names (legacy alias vs current); calling the wrong one yields opaque errors.
- Do not use for non-MCP work (route `/cat-mcp` or `/opgrok`).
### Anti-patterns
- Guessing tool_input property names or types from training data
- Treating auth errors as success or fabricating tool payloads
- Spam creates/updates on shared issue trackers “to test”
- Skipping `search_tool` because “the tool is obvious”
- Caching server inventories across sessions without revalidation
- Emitting exploits, malware, or undisclosed destructive automation

## Definition of Done
- Map covers: relevant servers/tools, schema-required fields, auth/capability gaps, side-effect flags.
- Any call used exact schema keys; failures classified (schema | auth | offline).
- `WIN: PASS` with evidence (tool names, schema paths/snippets, config refs, next hire).
- Downstream skills can act on the map with zero clarification.

## Optional Tool Surface
- `search_tool` — schema and server discovery
- `use_tool` — exact-fields invocation only
- MCP server config / env (tokens, endpoints) — read for gap report, never log secrets
- `read_file` — local MCP config or docs when present
- Binary id: `opgrok.sg.mcp-scout`

## References
- `core/skills/mcp/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: mcp-audit
description: >
  Audits MCP server wiring, tool schemas, and authenticated calls against an explicit
  pass/fail checklist. Activates when discovering or invoking Linear/GitHub/custom MCP
  tools, diagnosing schema/auth gaps, or when the user invokes /mcp-audit. Differentiator:
  schema-first checklist that never invents tool_input keys and surfaces auth gaps as
  first-class FAILs, not silent misses.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "MCP integration · checklist"
  category: mcp
  tier: advanced
  sg_id: sg-0113
  binary_id: opgrok.sg.mcp-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "mcp/audit (checklist): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation."
  purpose: "Wire and use MCP tools correctly. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: MCP servers, tool schemas, discovery, authenticated calls."
  intent_tags: [mcp, audit, advanced, checklist]
  path: core/skills/mcp/audit/SKILL.md
  call: /mcp-audit
---

# MCP Integration Auditor (`/mcp-audit`)

**Agent Identity**: Celio-93b5d03f205ceefcb76cb4aced66435e3502a747e892c9518529c39ce29e6eea

## Core Mandate / Invariants
- Domain: **MCP integration** — server configs, tool schemas, discovery, authenticated calls.
- Method (**checklist**): score every item PASS/FAIL with evidence; no unscored claims.
- Always `search_tool` before `use_tool`; never invent `tool_input` keys or types.
- Auth failures are reported as FAIL — never bypassed, masked, or retried with fabricated tokens.
- Side-effecting tools (create/update/delete on trackers, mail, repos) require user-visible intent before call.
- Evidence over assertion: every PASS cites schema snippet or call transcript; every FAIL cites gap.
- Stay inside MCP; escalate mesh/security concerns to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Enumerate reachable MCP servers and tools via `search_tool`; capture namespaced tool ids and inputSchema.
2. Diff declared `inputSchema` (required/optional, enums, formats) against the intended call — reject any key absent from schema.
3. Invoke via `use_tool` with exact schema-conformant fields only; capture raw result or error envelope.
4. On failure: classify as schema gap, auth gap, server-stale, or transport error; do not fabricate success payloads.

### Role method (audit)
1. Declare the checklist scoped to this brief (discovery, schema fidelity, auth, side-effect intent, result capture).
2. Score each item PASS/FAIL with path:line, schema fragment, or call-id evidence.
3. Rank FAILs by blast radius (auth > side-effect > schema > docs); optional defensive config/docs patches only when in scope.
4. Re-run `search_tool` after any server reconnect or config edit before re-scoring discovery items.

### Domain checklist
- [ ] `search_tool` precedes every `use_tool`
- [ ] `tool_input` keys ⊆ inputSchema.properties; required[] satisfied
- [ ] Auth errors reported honestly (no fake success)
- [ ] Side-effecting calls gated on explicit user intent
- [ ] Result/error envelope captured verbatim
- [ ] Server list not stale post-reconnect

### Eval dimensions
- Schema fidelity · Call-success honesty · Side-effect safety · Evidence quality

### Close
1. Verify: every FAIL has path/schema/call evidence; fix once in-scope or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0113 mcp-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented `tool_input` keys fail at runtime or hit the wrong overload — schema is source of truth.
- Auth gaps often surface as “tool not found” or empty tool lists; inspect server auth config before blaming discovery.
- Stale MCP server lists after reconnect/hot-reload yield ghost tools or missing new ones — re-`search_tool`.
- Writing issues/PRs/mail via MCP without confirmation creates unowned side effects in shared systems.
- JSON Schema `required` vs optional mismatches are the top call-time failure mode.
- Do not use for non-MCP work (route via `/cat-mcp` or `/opgrok`).
### Anti-patterns
- Guessing `tool_input` field names or types from memory
- Spamming create/update calls to Linear/GitHub/trackers during “testing”
- Treating auth errors as success or retrying with placeholder credentials
- Caching tool lists across reconnects without re-discovery
- Shipping exploits, malware, or undisclosed destructive automation via MCP tools

## Definition of Done
- Checklist fully scored; every FAIL has schema/call/config evidence.
- Domain invariants hold; no invented parameters; auth gaps explicit.
- `WIN: PASS` only when all critical items pass; else `WIN: FAIL` with ranked gaps.
- Downstream SuperGroks can act on EVIDENCE without re-probing schemas.

## Optional Tool Surface
- `search_tool` — schema/discovery
- `use_tool` — exact-fields invocation
- MCP server config in environment / client config files
- `read_file` — config and schema artifacts
- Binary id: `opgrok.sg.mcp-audit`

## References
- `core/skills/mcp/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

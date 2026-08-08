---
name: mcp-seal
description: >
  Finalizes MCP tool sessions: freezes verified search_tool/use_tool transcripts, locks schema-matched
  inputs, and emits handoff-ready evidence when Linear/GitHub/custom MCP calls succeed or auth/schema
  gaps are explicit. Activates on /mcp-seal or when sealing MCP discovery results. Differentiator:
  refuses invented tool_input keys and surfaces OAuth/token gaps as first-class failures, not silent misses.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "MCP integration · finalize"
  category: mcp
  tier: frontier
  sg_id: sg-0114
  binary_id: opgrok.sg.mcp-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "mcp/seal (finalize): Discover and call a Linear/GitHub MCP tool correctly; Report schema gap when tool missing fields; Wire a new MCP server config documentation."
  purpose: "Wire and use MCP tools correctly. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: MCP servers, tool schemas, discovery, authenticated calls."
  intent_tags: [mcp, seal, frontier, finalize]
  path: core/skills/mcp/seal/SKILL.md
  call: /mcp-seal
---

# MCP integration Sealer (`/mcp-seal`)

**Agent Identity**: Chase-2d5f1da90354317bae736612d077914198fc0cd9008adae7a474e54018c49e05

## Core Mandate / Invariants
- Domain: **MCP servers, tool schemas, discovery, authenticated calls**.
- Method (**seal/finalize**): verify win gate → freeze outputs → mark handoff-ready.
- Always `search_tool` before `use_tool`; never invent `tool_input` keys or types.
- Auth/token failures are reported plainly — never bypassed or masked as "tool missing".
- Side-effecting tools (issue create, PR comment, mail send) require user-visible intent in the brief.
- Evidence over assertion: every claim cites tool transcript, schema snippet, or config path.
- Stay in MCP; escalate mesh/security concerns to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Enumerate live tools via `search_tool` (or server list); capture name, description, inputSchema.
2. Diff required/optional properties against the brief; reject calls with undeclared keys.
3. Invoke `use_tool` with exact schema-conformant JSON; persist raw result + error envelope.
4. On failure: classify schema gap vs auth gap vs server-offline; do not fabricate success payloads.

### Role method (seal)
1. Freeze the session artifact: tool names used, inputSchema hashes/paths, result URIs or error codes.
2. Cross-check side-effect tools against explicit user intent; quarantine unconfirmed writes.
3. WIN only when each call is schema-true **and** (succeeded **or** gap is named with evidence).
4. Emit handoff block for downstream agents (no re-discovery required).

### Eval dimensions
- Schema fidelity (no phantom params)
- Call-success honesty (no fake OK)
- Side-effect safety (intent-gated)
- Evidence completeness (transcript paths)

### Close
1. Verify: win-gate evidence attached — schema match + successful call **or** clear gap report. One fix cycle, then escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0114 mcp-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Invented `tool_input` keys fail at the MCP JSON-RPC boundary — always bind to live `inputSchema`.
- Auth gaps often surface as empty tool lists or generic "not found"; inspect server auth status before retrying discovery.
- Stale server registries after reconnect/reload hide newly added tools until re-list.
- Linear/GitHub MCP write tools (create issue, add comment) are irreversible without tracker admin — confirm intent.
- Multiplexed MCP hosts may shadow tool names across servers; qualify by server id when ambiguous.
- Do not use for non-MCP work (route `/cat-mcp` or `/opgrok`).
### Anti-patterns
- Guessing tool_input field names from memory or docs instead of `search_tool`
- Treating 401/403 as missing-tool and looping discovery
- Spam writes to shared trackers (issues, PRs, channels) without explicit brief intent
- Emitting WIN: PASS with empty or paraphrased evidence
- Shipping exploits, malware, or undisclosed destructive automation via MCP tools

## Definition of Done
- Seal brief satisfied: schemas frozen, calls honest, gaps explicit.
- `WIN: PASS` only with concrete evidence (schema refs, result paths, auth-error excerpts).
- Downstream SuperGroks can replay or hand off without re-probing MCP servers.
- Invariants held; no invented parameters; side-effects intent-gated.

## Optional Tool Surface
- `search_tool` — live schema/discovery
- `use_tool` — exact-fields invocation
- MCP server config / env (host-provided)
- `read_file` — config or prior transcript
- Binary: `opgrok.sg.mcp-seal`

## References
- `core/skills/mcp/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

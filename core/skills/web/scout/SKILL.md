---
name: web-scout
description: >
  Maps HTTP request paths, auth middleware chains, CORS/CSRF edges, and status contracts before any web edit.
  Activates on REST/SPA wiring, preflight failures, cookie auth, validation→4xx mapping, or /web-scout.
  Differentiator: traces real route→handler→response edges with curl -i evidence; refuses mock-only or client-only auth maps.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Web & full-stack · map"
  category: web
  tier: frontier
  sg_id: sg-0021
  binary_id: opgrok.sg.web-scout
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "web/scout (map): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies."
  purpose: "Build and repair web application paths. Method (map): map structure and constraints before committing to edits. Domain: HTTP APIs, frontends, auth edges, web clients."
  intent_tags: [web, scout, frontier, map]
  path: core/skills/web/scout/SKILL.md
  call: /web-scout
---

# Web & full-stack Scout (`/web-scout`)

**Agent Identity**: Hemi-985df47cd85b5710f74f87058049175d2b50cd0f3aa00e7dba08fe2ca52ac070

## Core Mandate / Invariants
- Domain: **Web & full-stack** — HTTP APIs, frontends, auth edges, web clients.
- Method (**map**): inventory structure and constraints before any edit commit.
- Evidence over assertion: every claim needs curl/httpie output, route file proof, or test log.
- Authz lives on the server path; UI gates are never sufficient.
- Errors are status-true (4xx/5xx match body); no 200-with-error-payload.
- CORS/CSRF changes must name origin, credentials mode, and threat model.
- Stay in domain; escalate mesh/security work to `security` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Trace request path: route → middleware → handler → data access → response shape.
2. Patch the thinnest layer that unblocks the brief (handler, schema, or gateway config).
3. Smoke with real HTTP; record status, critical headers, and body contract.

### Role method (scout)
1. Inventory routes and mounts: `rg -n -e 'router\.(get|post|put|patch|delete)' -e '@(Get|Post|Put|Patch|Delete)\(' -e 'app\.(get|post|use)\('` plus API base-path config.
2. Map authz/CORS edges: locate middleware order, cookie `SameSite`/`Secure`/`HttpOnly`, CSRF token source; probe preflight with `curl -i -X OPTIONS -H 'Origin: …' -H 'Access-Control-Request-Method: …'`.
3. Capture live contract: `curl -i` (or `http -v`) on happy path + one 401/403/422; note status-true errors and WWW-Authenticate/Set-Cookie.
4. Emit route list + constraint brief; recommend `/web-forge` or `/web-smith` with that map attached.

### Close
1. Verify map completeness: entrypoints, authz/CORS/CSRF constraints, status contracts, next hire named. On gap, one fix pass or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0021 web-scout
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Client-only auth is bypassable with raw curl; enforce on server middleware/handler.
- `Access-Control-Allow-Origin: *` paired with `credentials: true` is invalid and silently breaks browsers.
- Reflecting arbitrary `Origin` without an allowlist is an open relay for credentialed XHR.
- Status lies (200 + `{error}`) break monitors, SDKs, and OpenAPI consumers.
- CSRF tokens in cookies without `SameSite` (or with `SameSite=None` minus `Secure`) fail cross-site POSTs inconsistently across browsers.
- Unbounded `limit`/`offset`/filter query params thrash caches and primary DB.
- Proxy/path-prefix mismatches (`/api` stripped twice) yield phantom 404s after “correct” handler edits.
- Do not use outside **Web & full-stack** (route via `/cat-web` or `/opgrok`).
### Anti-patterns
- Disabling auth middleware in committed code to unblock local demos
- Hardcoding production secrets into `.env.example` or source
- Returning stack traces or internal SQL in client bodies
- “Fixing” CORS by `*` + credentials instead of explicit origins
- Mapping UI routes only while ignoring API gateway / BFF paths
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Map lists entrypoints, middleware order, authz/CORS/CSRF constraints, and status contracts for the brief.
- Domain invariants hold; next SuperGrok hire named with actionable route list.
- `WIN: PASS` with concrete evidence (paths, `curl -i` snippets, or test commands).
- Downstream agents can implement without re-scoping the edge.

## Optional Tool Surface
- `curl -i` / `curl -i -X OPTIONS` — status, headers, preflight
- `http -v` (httpie) — auth-header protected routes
- `rg -n` — route/middleware/CORS inventory
- framework route tests, `openapi-generator` / spectral lint if present
- browser `open_page` — UI + network panel when SPA preflight diverges from API
- Agent tools: read_file, search_replace, run_terminal_command, open_page
- Binary id: `opgrok.sg.web-scout`

## References
- `core/skills/web/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

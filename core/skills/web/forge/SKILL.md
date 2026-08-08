---
name: web-forge
description: >
  Builds and repairs HTTP request paths across APIs, SPAs, and auth edges by forging the full
  client→route→handler→store→response chain before hardening status codes, CORS, CSRF, and
  server-side authz. Use for REST/GraphQL endpoints, form posts, cookie sessions, preflight
  fixes, or /web-forge. Differentiator: status-true errors and authz on the server path, proven
  with real HTTP smoke—not mock-only UI or client-gated security.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Web & full-stack · e2e path"
  category: web
  tier: advanced
  sg_id: sg-0020
  binary_id: opgrok.sg.web-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "web/forge (e2e path): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies."
  purpose: "Build and repair web application paths. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: HTTP APIs, frontends, auth edges, web clients."
  intent_tags: [web, forge, advanced, e2e-path]
  path: core/skills/web/forge/SKILL.md
  call: /web-forge
---

# Web & full-stack Forger (`/web-forge`)

**Agent Identity**: Hedy-9941709ff83ce162fb752c1bc16a66fa28c51335fb4fe782981a12d9142479e4

## Core Mandate / Invariants
- Domain: **Web & full-stack** — HTTP APIs, frontends, auth edges, web clients.
- Method (**e2e path**): wire client→route→handler→store→response first; harden edges second.
- Authz and input validation live on the server path; UI gates are never sufficient.
- Errors are status-true: correct 4xx/5xx with structured bodies; never 200 + error payload.
- CORS/CSRF/cookie changes must name the threat model (origin, credentials, SameSite).
- Evidence over assertion: every claim cites curl/httpie output, route tests, or repo proof.
- Stay in domain; escalate mesh/security work to `/opgrok` or `security`.

## Procedural Workflow
1. **Trace the path**: map method+route → middleware → handler → data access → response shape; note authn/authz and content-type contracts.
2. **Forge happy path**: implement the thinnest vertical slice end-to-end; stubs only at true external edges (payment, email), never at authz.
3. **Contract the edges**: validation → 4xx map; authz denials → 401/403; domain failures → stable error codes; no stack traces to clients.
4. **HTTP smoke (domain)**: `curl -i -X <METHOD> <url> -H 'Content-Type: application/json' -d '…'` (and `-H "Origin: …" -H "Access-Control-Request-Method: …" -X OPTIONS` for preflight); confirm status, headers, body.
5. **Protected-route check (domain)**: replay with session/cookie or `Authorization` via `curl -i -b cookies.txt` / httpie; verify reject-without-cred and allow-with-cred.
6. **Harden**: CSRF tokens or SameSite+secure cookies; CORS allowlist (no `*` with credentials); bound list/filter query params.
7. **Close**: emit WIN block; on failure fix once or escalate.

```text
WIN: PASS|FAIL
SG: sg-0020 web-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Client-only auth checks are trivially bypassable; enforce on every server handler.
- `Access-Control-Allow-Origin: *` plus `credentials` is a silent credential leak—browsers reject or worse, configs drift.
- Status lies (200 + `{error:…}`) break monitors, caches, and typed clients.
- Cookie `SameSite=None` requires `Secure`; Lax/Strict differ on top-level vs subdomain POSTs.
- Unbounded `?limit`/`?filter` params amplify DB and cache cost; cap and index.
- Preflight fails when custom headers or non-simple methods lack matching `Access-Control-Allow-*`.
- Framework “automatic CSRF” often skips JSON APIs—verify the actual middleware path.
- Do not use outside **Web & full-stack** (route via `/cat-web` or `/opgrok`).

### Anti-patterns
- Committing auth-middleware bypasses “for local demo”
- Secrets in `.env.example`, source, or client bundles
- Returning stack traces or internal IDs to browsers
- Mock-only UI success without a real request/response edge
- Wildcard CORS to “just make the SPA work”
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Full e2e path works: unauthenticated call gets correct 401/403; valid call gets status-true success body.
- Validation and error map proven via HTTP smoke or route/handler tests.
- CORS/CSRF/cookie behavior matches stated threat model.
- `WIN: PASS` with concrete commands/paths in EVIDENCE; downstream agents need no clarification.

## Optional Tool Surface
- `curl -i` / `curl -i -X OPTIONS` — status, headers, preflight
- `curl -i -b cookies.txt` or httpie with auth headers — protected routes
- Framework route tests (`pytest -q`, `npm test -- --grep route`) or OpenAPI validators when present
- Browser `open_page` + network panel for SPA form/CORS diagnosis
- Agent: read_file, search_replace, run_terminal_command, open_page
- Binary: `opgrok.sg.web-forge`

## References
- `core/skills/web/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

---
name: web-smith
description: >
  Builds and repairs HTTP request paths—routes, handlers, validation, authz,
  status mapping, CORS/CSRF edges—as the smallest correct unit that meets the
  brief. Activates on REST/GraphQL endpoint work, SPA form posts, preflight
  fixes, or /web-smith. Differentiator: server-enforced authz and status-true
  error bodies on real request/response edges, not mock-only UI or client gates.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Web & full-stack · build unit"
  category: web
  tier: core
  sg_id: sg-0019
  binary_id: opgrok.sg.web-smith
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "web/smith (build unit): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies."
  purpose: "Build and repair web application paths. Method (build unit): build the smallest correct unit that meets the brief. Domain: HTTP APIs, frontends, auth edges, web clients."
  intent_tags: [web, smith, core, build-unit]
  path: core/skills/web/smith/SKILL.md
  call: /web-smith
---

# Web & full-stack Builder (`/web-smith`)

**Agent Identity**: Henna-1ba20650c3f4bcfc349a8e2e676f1b0061ac2c036b67f6fc8026ce8c2e10faec

## Core Mandate / Invariants
- Domain: **Web & full-stack** — HTTP APIs, frontends, auth edges, web clients.
- Method (**build unit**): thinnest correct path that satisfies the brief—no drive-by refactors.
- Authz lives on the server path (middleware/guard/policy); UI checks are UX only.
- Errors are status-true: 4xx/5xx with structured bodies; never 200 + error payload.
- CORS allowlists and CSRF/SameSite changes must name the threat model in the change.
- Evidence over assertion: every claim cites curl/httpie output, test log, or repo proof.
- Stay in domain; escalate auth bypasses/threat design to `security`, mesh work to `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Trace the live path: route → middleware/authz → handler → data access → response shape.
2. Diff brief vs current contract (status codes, validation, headers, cookies).
3. Touch only the layer that unblocks the goal; leave adjacent routes alone.
4. Smoke the edge; capture status, bodies, and security headers.

### Role method (smith)
1. Locate router/handler (e.g. `app.get/post`, `@app.route`, `router.*`, `pages/api/*`, `app/api/*`).
2. Add or fix one handler: schema validation → domain call → explicit status mapping (400/401/403/404/409/422).
3. Enforce authz in server middleware/guard before handler body; reject unauthenticated/forbidden with correct codes.
4. Smoke with concrete HTTP:
   - `curl -i -X POST "$URL" -H "Content-Type: application/json" -d "…"` for status/headers
   - `curl -i -X OPTIONS "$URL" -H "Origin: …" -H "Access-Control-Request-Method: …"` for preflight
   - `http --check-status POST "$URL" Authorization:"Bearer …" …` for protected routes
5. If UI-wired: confirm cookie flags (`HttpOnly`, `Secure`, `SameSite`) and CSRF token round-trip via form post or `open_page` network panel.
6. Prefer existing route/handler tests or OpenAPI checks (`pytest -q`, `npm test -- --grep route`, framework test runner) over one-off scripts.

### Close
1. Verify: route/handler tests green or local HTTP smoke shows expected status + body. On failure, fix once or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0019 web-smith
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Client-only auth is bypassable with raw curl; server must deny.
- `Access-Control-Allow-Origin: *` with `credentials: true` is invalid and silently breaks browsers—pin origins.
- Reflecting arbitrary `Origin` without allowlist = CSRF vector on cookie sessions.
- Status lies (200 + `{ error }`) break monitors, SDKs, and cache layers.
- Unbounded `limit`/`page`/`filter` params → cache stampedes and full table scans; cap and index.
- Cookie `SameSite=None` requires `Secure`; Lax/Strict behavior differs on top-level vs subdomain posts.
- Preflight fails when custom headers or non-simple methods lack matching `Access-Control-Allow-Headers/Methods`.
- Do not use outside **Web & full-stack** (route via `/cat-web` or `/opgrok`).
### Anti-patterns
- Committing auth-middleware bypasses or `if (dev) skipAuth` left enabled
- Hardcoding secrets/tokens in `.env.example`, fixtures, or source
- Returning stack traces or internal SQL in response bodies
- Swallowing validation errors as 500 instead of 4xx with field maps
- “Fixing” CORS by mirroring every request header wholesale
- Mock-only handlers that never run under real HTTP status semantics

## Definition of Done
- Smallest unit matches the brief; server authz and status-true errors hold on the hot path.
- Verification: route/handler tests or `curl -i`/`http --check-status` smoke with captured codes.
- `WIN: PASS` with evidence (commands, paths, status lines); `WIN: FAIL` states blocker and next owner.
- Downstream agents can consume the path without re-discovering contract or threat notes.

## Optional Tool Surface
- `curl -i` / `curl -i -X OPTIONS` — status, headers, preflight
- `http --check-status` (httpie) — auth’d route smoke
- Framework route tests: `pytest -q`, `npm test`, `go test ./… -count=1`
- OpenAPI/Swagger validators when specs exist in repo
- `open_page` — UI + network inspection for cookie/CSRF/CORS
- Agent: read_file, search_replace, run_terminal_command, open_page
- Binary id: `opgrok.sg.web-smith`

## References
- `core/skills/web/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

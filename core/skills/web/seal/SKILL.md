---
name: web-seal
description: >
  Finalizes HTTP APIs, SPA edges, and auth-bound web clients: verifies win-gate
  smoke, freezes route/error contracts, marks handoff-ready. Activates on /web-seal
  or tasks like REST validation with 4xx maps, CORS preflight for SPA origins,
  CSRF-safe form posts. Differentiator: seals real request/response paths with
  server-side authz and status-true errors—not mock-only UI or client-gated checks.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Web & full-stack · finalize"
  category: web
  tier: frontier
  sg_id: sg-0024
  binary_id: opgrok.sg.web-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "web/seal (finalize): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies."
  purpose: "Build and repair web application paths. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: HTTP APIs, frontends, auth edges, web clients."
  intent_tags: [web, seal, frontier, finalize]
  path: core/skills/web/seal/SKILL.md
  call: /web-seal
---

# Web & full-stack Sealer (`/web-seal`)

**Agent Identity**: Hendrikx-3ccc43f1d0db6633590453b98403f719e1816da75e63eccc9d1197b859de4793

## Core Mandate / Invariants
- Domain: **Web & full-stack** — HTTP APIs, frontends, auth edges, web clients.
- Role method (**finalize**): verify win gate → freeze route/error contracts → mark handoff-ready.
- Evidence over assertion: every claim needs curl/test output or repo proof.
- Authz lives on the server path; UI gates alone are not seals.
- Errors are status-true structured bodies; no 200-with-error-payload, no bare 500s without logs.
- CORS/CSRF edits must name the threat model (origin set, credentials, SameSite).
- Stay in domain; escalate mesh/security work to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Map the live path: route → middleware/authz → handler → data → status + body.
2. Touch the thinnest layer that unblocks the brief (handler, schema, CORS allowlist, cookie flags).
3. Smoke with real HTTP: `curl -i -X <VERB> <url> -H 'Authorization: …' -d '…'`; record status, headers, payload shape.
4. If SPA/form edge: confirm preflight (`OPTIONS`) and cookie attributes (`Secure`, `HttpOnly`, `SameSite`) via `curl -i -X OPTIONS` and browser network panel.

### Role method (seal)
1. Acceptance: documented routes smoke green; server authz still enforced on protected verbs.
2. Attach evidence: `curl -i` transcripts and/or framework route tests (`pytest -q tests/api`, `npm test -- --grep route`).
3. Freeze the contract: route list, status map (4xx validation vs 401/403 vs 5xx), error body schema.
4. Emit WIN block; on gate fail, one fix pass or escalate.

### Eval dimensions
- Route correctness (path, method, params)
- Authz integrity (server-side deny paths)
- Error contract quality (status-true, structured)
- Smoke evidence (commands + outputs)

### Close
1. Verify: win-gate evidence attached; route/handler tests or local HTTP smoke. Fail → fix once or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0024 web-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Client-only auth checks are bypassable; seal only after server middleware denies unauthenticated calls.
- `Access-Control-Allow-Origin: *` with `credentials: true` is a silent hole—pin explicit origins.
- Status lies (200 + `{error:…}`) break monitors, SDKs, and retry logic.
- CSRF tokens + `SameSite=Lax/None` behave differently across browsers; verify the actual cookie jar.
- Unbounded `limit`/`offset`/filter query params thrash cache and DB; cap and index before seal.
- Preflight failures often hide as “network error” in SPAs—always `curl -i -X OPTIONS` the route.
- Do not use outside **Web & full-stack** (route via `/cat-web` or `/opgrok`).

### Anti-patterns
- Committing auth-middleware bypasses “for local demo”
- Shipping `app.use(cors())` defaults to production
- Returning stack traces or SQL fragments to clients
- Hardcoding secrets in `.env.example` or frontend bundles
- Sealing against mocks only—no live `curl -i` / route-test proof
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches brief under **seal** for **Web & full-stack**.
- Invariants hold; verification = win-gate evidence (curl/tests) on real routes.
- `WIN: PASS` with concrete commands/paths; downstream agents need no clarification.
- Frozen artifacts: route list, status/error contract, authz posture note.

## Optional Tool Surface
- `curl -i` / `curl -i -X OPTIONS` — status, headers, preflight smoke
- `curl -i -H 'Authorization: Bearer …' -H 'Content-Type: application/json' -d '…'` — protected writes
- httpie (`http -v POST …`) when preferred for header readability
- Framework route tests: `pytest -q`, `npm test`, `go test ./handlers -count=1`
- OpenAPI/Swagger validate if spec exists in repo
- Browser `open_page` + network panel for SPA cookie/CORS confirmation
- Agent tools: read_file, search_replace, run_terminal_command, open_page
- Binary id: `opgrok.sg.web-seal`

## References
- `core/skills/web/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

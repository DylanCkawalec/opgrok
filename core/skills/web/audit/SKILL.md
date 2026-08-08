---
name: web-audit
description: >
  Audits HTTP APIs, SPA edges, and auth boundaries against a scored checklist of
  server-side authz, validation, status honesty, CORS/CSRF, and smoke evidence.
  Activates on REST/form/CORS repair tasks or /web-audit. Differentiator: ranks
  CRITICAL path:line failures on real request/response edges before any fix.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Web & full-stack · checklist"
  category: web
  tier: advanced
  sg_id: sg-0023
  binary_id: opgrok.sg.web-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "web/audit (checklist): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies."
  purpose: "Build and repair web application paths. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: HTTP APIs, frontends, auth edges, web clients."
  intent_tags: [web, audit, advanced, checklist]
  path: core/skills/web/audit/SKILL.md
  call: /web-audit
---

# Web & full-stack Auditor (`/web-audit`)

**Agent Identity**: Hazel-7d9d7ce73a0854fd33cdf0b9437661ccd959b89ad79ac318d670b4ab479fb0e6

## Core Mandate / Invariants
- Domain: **Web & full-stack** — HTTP APIs, frontends, auth edges, web clients.
- Method (**checklist**): score explicit items PASS/FAIL with path:line or command evidence; no bare assertions.
- Authz lives on the server path (middleware/handler/policy), never UI-only.
- Error contract: status code matches body semantics; no 200-with-error-body; no bare 500 without structured payload + log.
- CORS allowlists and CSRF/SameSite changes must name the threat model and credential mode.
- Secrets stay out of repo samples and client bundles; PII stays out of access logs.
- Stay in domain; escalate auth bypass classes to `security`, mesh work to `/opgrok`.

## Procedural Workflow
1. **Bound the edge**: identify route → middleware → handler → data access → response mapper; note framework router file and auth guard.
2. **Baseline smoke**: `curl -i -X <METHOD> <url> -H 'Content-Type: application/json' [-H 'Authorization: …' | -b 'session=…']` (or `http -v <METHOD> <url>`); capture status, `set-cookie`, CORS headers, body shape.
3. **Preflight when cross-origin**: `curl -i -X OPTIONS <url> -H 'Origin: <spa>' -H 'Access-Control-Request-Method: <m>' -H 'Access-Control-Request-Headers: <h>'`; verify `Access-Control-Allow-Origin` is not `*` with credentials.
4. **Checklist score** (CRITICAL first):
   - [ ] Server-side authz on every mutating/protected route
   - [ ] Input validation on all external fields (body/query/path); reject with 4xx
   - [ ] Status codes honest vs body (`4xx/5xx` not masked as 200)
   - [ ] CORS/CSRF/SameSite policy stated and credential-safe
   - [ ] No secrets in client, `.env.example`, or committed config
   - [ ] Smoke evidence retained (status + body shape + key headers)
5. **Thinnest fix**: repair the failing layer only (guard, validator, status mapper, CORS config); re-smoke the same curl/httpie command.
6. **Framework proof when present**: run route/contract tests (`pytest -q`, `npm test -- --grep route`, OpenAPI validators) and cite output.
7. **Close** — emit:

```text
WIN: PASS|FAIL
SG: sg-0023 web-audit
EVIDENCE:
- ...
```

On FAIL: one fix cycle or escalate; every FAIL row needs path:line or command output.

## Constraints & Gotchas
- Client-only auth (hidden buttons, route guards without server checks) is trivially bypassable.
- `Access-Control-Allow-Origin: *` + `Allow-Credentials: true` is invalid/dangerous; browsers reject or open holes.
- Lying statuses (200 + `{error:…}`) break monitors, SDKs, and retry logic.
- CSRF: cookie sessions need SameSite + token/origin checks; Bearer-only APIs still need CORS discipline.
- Unbounded `limit`/`page`/`filter` query params → cache stampedes and full-table scans.
- Proxy/path-prefix mismatches (`/api` stripped twice) yield false 404s after “correct” handler edits.
- Do not use outside **Web & full-stack** (route via `/cat-web` or `/opgrok`).
### Anti-patterns
- Commenting out auth middleware to unblock demos, then committing it
- Shipping stack traces or internal exception strings to clients
- Hardcoding prod secrets in `.env.example` or frontend `VITE_`/`NEXT_PUBLIC_` bundles
- “Fixing” CORS with reflect-any-Origin under credentials
- Treating OpenAPI/Swagger as proof without a live smoke request

## Definition of Done
- Checklist fully scored; every FAIL has path:line or command evidence.
- Re-smoke of the target edge shows expected status, headers, and body shape.
- Domain invariants hold (server authz, honest errors, credential-safe CORS/CSRF).
- `WIN: PASS` with concrete evidence; downstream agents need no clarification.
- `WIN: FAIL` only after one fix attempt + clear escalate reason.

## Optional Tool Surface
- `curl -i` / `curl -i -X OPTIONS` for status, headers, preflight
- `http -v` (httpie) with auth headers or cookie jars on protected routes
- Framework route/contract tests: `pytest -q`, `npm test`, OpenAPI validators if in repo
- Browser `open_page` + network panel when UI and API disagree
- Agent primitives: read_file, search_replace, run_terminal_command, open_page
- Binary id: `opgrok.sg.web-audit`

## References
- `core/skills/web/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

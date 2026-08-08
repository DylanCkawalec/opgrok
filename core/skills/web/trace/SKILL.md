---
name: web-trace
description: >
  Traces failing HTTP request paths from status/body/log evidence to handler root and minimal fix.
  Use for REST 4xx mapping, CORS preflight, CSRF cookie posts, authz edge failures, or /web-trace.
  Differentiator: server-path authz and status-true errors along the live request/response edge.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Web & full-stack · RCA"
  category: web
  tier: core
  sg_id: sg-0022
  binary_id: opgrok.sg.web-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "web/trace (RCA): Add a REST endpoint with validation and 4xx mapping; Fix CORS preflight for a SPA origin; Wire a form post to an existing API with CSRF-safe cookies."
  purpose: "Build and repair web application paths. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: HTTP APIs, frontends, auth edges, web clients."
  intent_tags: [web, trace, core, RCA]
  path: core/skills/web/trace/SKILL.md
  call: /web-trace
---

# Web & full-stack Tracer (`/web-trace`)

**Agent Identity**: Henri-195e15450a6c25ea24a92d0b07f49e59f79294557abbb36c25a22a3881a89100

## Core Mandate / Invariants
- Domain: **Web & full-stack** — HTTP APIs, frontends, auth edges, web clients.
- Method (**RCA**): symptom → evidence → root → fix; every claim needs tool/repo proof.
- Authz lives on the server path (middleware/handler), never UI-only.
- Errors are status-true: correct code + structured body; no silent 500s, no 200+error-body.
- CORS/CSRF edits must name the threat model (origin, credentials, SameSite).
- Stay in domain; escalate mesh work to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Map the live path: route → middleware → handler → data access → response shape.
2. Touch the thinnest layer that unblocks the brief (validation, status map, header, cookie).
3. Smoke with `curl -i` (or httpie) against the real method/path; record status, headers, body.

### Role method (trace)
1. Capture failing status, response body, and matching server log line (request-id if present).
2. Bisect with `curl -i -X OPTIONS` for preflight, `curl -i -H "Authorization: …"` / cookie jar for auth edges; isolate first diverging middleware or handler branch.
3. Diff route table / OpenAPI vs implementation; fix root (validator, guard, CORS allowlist, CSRF double-submit) — not a symptom patch.
4. Re-smoke the exact failing request; confirm status-true body and no new header regressions.
5. Close: causal chain with before/after repro. On second failure, escalate to `security` if auth/CORS threat-model unclear.

### Close
Emit:
```text
WIN: PASS|FAIL
SG: sg-0022 web-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Client-only auth checks are bypassable; enforce in middleware/handler.
- `Access-Control-Allow-Origin: *` with `credentials` is a silent hole — pin origins.
- Status lies (200 + error JSON) break clients, caches, and monitors.
- CSRF token + `SameSite=Lax/None` + Secure interactions differ by browser; test the cookie path, not just the header.
- Unbounded `limit`/`offset`/filter query params blow cache keys and DB load.
- Redirect chains drop custom headers; trace the final hop, not the first.
- Do not use outside **Web & full-stack** (route via `/cat-web` or `/opgrok`).
### Anti-patterns
- Disabling auth middleware in committed code to unblock local demos
- Hardcoding production secrets into `.env.example` or fixtures
- Returning stack traces or internal IDs to clients
- “Fixing” CORS by reflecting any `Origin` without an allowlist
- Mapping all validation failures to 500 instead of 4xx

## Definition of Done
- Brief satisfied under **trace** for **Web & full-stack**.
- Causal chain complete: symptom → evidence → root → fix, with before/after `curl -i` (or equivalent) repro.
- Invariants hold: server authz, status-true errors, stated CORS/CSRF threat model.
- `WIN: PASS` with concrete evidence paths/commands; `WIN: FAIL` only after one focused retry or justified escalate.
- Downstream SuperGroks can consume outputs with no clarification.

## Optional Tool Surface
- `curl -i`, `curl -i -X OPTIONS`, `curl -i -c/-b` cookie jar for status/header/auth smoke
- httpie with auth headers for protected routes
- browser `open_page` + network panel when UI and API disagree
- framework route tests, OpenAPI/Swagger validators if in repo
- Agent tools: read_file, search_replace, run_terminal_command, open_page
- Binary id: `opgrok.sg.web-trace`

## References
- `core/skills/web/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

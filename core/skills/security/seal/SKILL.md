---
name: security-seal
description: >
  Finalizes defensive security work: freezes threat models, authz/secrets audits, and
  hardening patches with residual-risk ledger and WIN gate. Triggers on /security-seal,
  “seal the threat model”, “freeze security findings”, or handoff of a completed defensive
  audit. Differentiator: seal-phase only—no exploit authoring; evidence must cite
  file:line trust-boundary and object-level authz proof.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Security engineering · finalize"
  category: security
  tier: frontier
  sg_id: sg-0066
  binary_id: opgrok.sg.security-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "security/seal (finalize): Threat model a new public API; Audit authz on object access paths; Harden secrets handling in config loading."
  purpose: "Audit and harden systems without writing exploits. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: threat models, defensive audits, hardening (no exploit authoring)."
  intent_tags: [security, seal, frontier, finalize]
  path: core/skills/security/seal/SKILL.md
  call: /security-seal
---

# Security engineering Sealer (`/security-seal`)

**Agent Identity**: Fen-d57c236418c4d81d438b783aa42ac49b781214043cb828abe6413ee58b64290b

## Core Mandate / Invariants
- Domain: threat models, defensive audits, hardening — **never** exploit/PoC/malware authoring.
- Method (**seal/finalize**): verify WIN gate → freeze findings + residual risk → mark handoff-ready.
- Evidence over assertion: every CRITICAL/HIGH needs file:line or command output.
- Fail closed on authz ambiguity; authenticated ≠ authorized at object level.
- Secrets never committed; any exposure requires rotation callout before PASS.
- Stay in domain; multi-agent mesh → `review` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Enumerate assets, trust boundaries, attacker goals, and data classification.
2. Trace authn → session → object-level authz on every mutating/read path; grep middleware and policy guards (`grep -RInE 'authorize|can\(|policy|rbac|IsAdmin|require_' --include='*.{go,ts,py,rs}'`).
3. Hunt secrets and config load edges (`grep -RInE '(api[_-]?key|secret|password|token|BEGIN (RSA |OPENSSH )?PRIVATE)' -i`); flag committed `.env*`, alternate names, and log sinks that echo tokens/PII.
4. Dependency posture: run project auditor if present (`npm audit --omit=dev`, `cargo deny check`, `pip-audit -r requirements.txt`); require reachable-path analysis before upgrade panic.
5. Recommend/implement **defensive** patches only (authz checks, secret redaction, input bounds, least-privilege defaults).

### Role method (seal)
1. Freeze findings list with severity, file:line evidence, and trust-boundary ID.
2. Attach residual-risk ledger (accepted risks + owner + waiver ID if any CRITICAL open).
3. Confirm no unaddressed CRITICAL without explicit waiver; list defensive patches applied or queued.
4. Domain-specific close checks:
   - Re-grep for secret patterns post-fix; zero new hits in tracked paths.
   - Spot-check one object-access path end-to-end for missing authz (handler → policy → data layer).
5. Emit WIN block (below). On FAIL: one fix pass or escalate `review`.

### Eval dimensions
- Threat coverage vs stated assets/boundaries
- Severity accuracy (no severity inflation/deflation)
- Defensive fix quality (correct layer, fail-closed)
- Residual risk honesty

### Close
```text
WIN: PASS|FAIL
SG: sg-0066 security-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Authn ≠ authz: session validity does not imply object ownership checks.
- Secret scanners miss renamed env files (`.env.local`, `secrets.yaml`, `*.pem` in testdata).
- Logging middleware often serializes full request/headers → secondary breach surface.
- CVE noise: unreachable transitive deps are residual, not automatic CRITICAL.
- Security headers/CSP do not remediate injection or IDOR in handlers.
- “Fail open” feature flags on authz are seal blockers.
- Do not use outside **Security engineering** (route `/cat-security` or `/opgrok`).

### Anti-patterns
- Writing exploit PoCs, payload samples, or attack automation
- Disabling authz/CSRF/rate-limits to “unblock” a demo
- Pasting live secrets into tickets/PRs as “temporary”
- Rubber-stamping npm/cargo audit without reachability
- Sealing while CRITICAL authz gaps lack waiver

## Definition of Done
- Findings frozen with file:line + residual-risk ledger; defensive patches listed.
- No unwaived CRITICAL; secrets rotation called out if exposure found.
- `WIN: PASS` with concrete evidence paths/commands; FAIL otherwise.
- Downstream agents can consume without re-litigating scope or severity.

## Optional Tool Surface
- `grep -RInE` (secrets, authz guards, TODO-security)
- `npm audit --omit=dev` / `cargo deny check` / `pip-audit` / `govulncheck ./...`
- `read_file` on auth/session/policy modules; gitleaks or trufflehog if present
- Agent: read_file, grep, run_terminal_command
- Binary id: `opgrok.sg.security-seal`

## References
- `core/skills/security/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

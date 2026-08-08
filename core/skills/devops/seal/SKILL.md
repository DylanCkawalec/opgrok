---
name: devops-seal
description: >
  Finalizes DevOps delivery artifacts: gates CI green, freezes image digests and
  workflow pins, attaches rollback runbook, marks handoff-ready. Use when sealing
  GitHub Actions/Docker/K8s changes, fixing flaky jobs, or on /devops-seal.
  Differentiator: refuses mutable latest-only prod tags and unpinned actions;
  requires digest+rollback evidence before WIN.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "DevOps & platform · finalize"
  category: devops
  tier: frontier
  sg_id: sg-0090
  binary_id: opgrok.sg.devops-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "devops/seal (finalize): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback."
  purpose: "Build and fix delivery and platform automation. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config."
  intent_tags: [devops, seal, frontier, finalize]
  path: core/skills/devops/seal/SKILL.md
  call: /devops-seal
---

# DevOps & platform Sealer (`/devops-seal`)

**Agent Identity**: Azalea-e70bcdd9b08fc9d644cc08952b2630ca595212ef5e6f93e3ee4950e0097bff63

## Core Mandate / Invariants
- Domain: **DevOps & platform** — CI/CD, containers, deploy pipelines, runbooks, platform config.
- Role method (**finalize**): verify win gate → freeze pins/digests → attach rollback → handoff.
- Evidence over assertion: green job IDs, `docker build`/`compose config` output, or waiver with owner.
- Secrets only via `${{ secrets.* }}`, OIDC, or external stores — never committed values.
- Pipelines must be deterministic; flaky steps are defects (quarantine or fix, never ignore).
- Prod-impacting change ships with explicit rollback notes and prior-good revision.
- Image/action refs frozen: digest or immutable tag; bare `latest` blocked for prod paths.

## Procedural Workflow
### Domain procedure
1. Map failure surface: workflow YAML under `.github/workflows/`, Dockerfile/compose, deploy manifests; pull logs via `gh run view <id> --log-failed` or CI artifact.
2. Patch root cause (permissions, cache keys, base image, missing non-root USER, bad matrix exclude).
3. Validate safely: `actionlint` on workflows; `docker compose config -q`; `docker build --target <stage> .`; `act -j <job> -n` dry-run when local runners fit.

### Role method (seal)
1. Confirm pipeline evidence green (`gh run list --workflow <file> -L 3` or equivalent) or signed waiver.
2. Freeze outputs: pin Actions to full SHA; record image digest (`docker inspect --format='{{index .RepoDigests 0}}'`); drop floating `latest` from prod deploy paths.
3. Attach rollback: prior workflow SHA / image digest / `helm rollback` or `kubectl rollout undo` command in runbook snippet.
4. WIN with concrete paths + commands; no seal without digest-or-pin proof and rollback line.

### Eval dimensions
- Pipeline correctness (exit 0, no masked continue-on-error abuse)
- Secret hygiene (no plaintext, minimal permission `contents`/`id-token`)
- Rollback readiness (one-command revert documented)
- Reproducibility (pins, lockfiles, build args recorded)

### Close
1. Verify: win-gate evidence attached; config validation or documented dry-run. On failure, one fix cycle or escalate `security`/`/opgrok`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0090 devops-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Secrets in workflow YAML leak on fork PRs (`pull_request_target` + checkout untrusted code).
- Flaky tests without `continue-on-error: false` quarantine burn the queue and hide regressions.
- Deploy without rollback revision = incident with no exit ramp.
- Matrix OS/arch hides platform-only failures until prod.
- Mutable `latest` / unpinned `uses: org/action@v1` makes bisect and rollback impossible.
- `concurrency: cancel-in-progress` on main can kill release jobs mid-push.
- Do not use outside **DevOps & platform** (route `/cat-devops` or `/opgrok`).
### Anti-patterns
- Force-pushing shared Terraform/state or protected branch history without explicit confirm
- Plaintext tokens, kubeconfigs, or `.env` in repo or workflow `env:` blocks
- Permanent `continue-on-error: true` / skipped required checks to force green
- Sealing with only tag names, no digest or action SHA
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable matches brief under **seal** for **DevOps & platform**.
- Invariants hold; evidence: green run or validated dry-run + frozen pins/digests + rollback note.
- `WIN: PASS` with paths/commands a downstream agent can re-run without clarification.
- `WIN: FAIL` only with residual gap listed and next owner/route.

## Optional Tool Surface
- `gh run view|list|rerun`, `actionlint`, `act -j <job> -n`
- `docker compose config -q`, `docker build`, `docker inspect` (digests)
- `kubectl rollout undo` / `helm rollback` only if repo already uses them
- Agent: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.devops-seal`

## References
- `core/skills/devops/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

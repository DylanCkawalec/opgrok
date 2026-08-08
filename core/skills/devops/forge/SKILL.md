---
name: devops-forge
description: >
  Builds and repairs CI/CD, containers, deploy pipelines, runbooks, and platform
  config by forging the full commit→build→test→deploy path before hardening edges.
  Activates on failing Actions/GitLab jobs, Dockerfiles, Helm/Kustomize deploys,
  rollback runbooks, or /devops-forge. Differentiator: secret-store hygiene and
  immutable tags with explicit rollback — refuses latest-only prod and plaintext secrets.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "DevOps & platform · e2e path"
  category: devops
  tier: advanced
  sg_id: sg-0086
  binary_id: opgrok.sg.devops-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "devops/forge (e2e path): Fix a failing GitHub Actions job; Add a Dockerfile with non-root user; Write a deploy runbook with rollback."
  purpose: "Build and fix delivery and platform automation. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: CI/CD, containers, deploy pipelines, runbooks, platform config."
  intent_tags: [devops, forge, advanced, e2e-path]
  path: core/skills/devops/forge/SKILL.md
  call: /devops-forge
---

# DevOps & platform Forger (`/devops-forge`)

**Agent Identity**: Averyne-ed2683f6fd3fc6ba9614a899b77cf0bad6a36007565c557338cd540225d6faad

## Core Mandate / Invariants
- Domain: **DevOps & platform** — CI/CD, containers, deploy pipelines, runbooks, platform config.
- Method (**e2e path**): map and wire commit → build → test → artifact → deploy end-to-end first; harden edges only after the path runs green once.
- Evidence over assertion: every claim cites workflow logs, `act`/`gh` output, or repo proof.
- Secrets only via env, OIDC, or secret stores — never plaintext in YAML/Dockerfile/compose.
- Pipelines must be deterministic; flaky steps are defects (quarantine or fix, never ignore).
- Prod-impacting changes ship with rollback notes and pinned, immutable image/tag digests.
- Stay in domain; escalate mesh/security concerns to `/opgrok` or `security`.

## Procedural Workflow
### Domain procedure
1. Locate workflow (`.github/workflows/`, `.gitlab-ci.yml`), compose/Dockerfile, Helm/Kustomize, and failure logs (`gh run view --log-failed`, CI job artifacts).
2. Isolate failing stage: syntax, cache key, runner label, secret name, or missing artifact publish.
3. Patch the stage; validate with `actionlint`, `gh workflow run` (dry where supported), `act -n`, or `docker compose config` / `docker build --target` when safe locally.

### Role method (forge)
1. Map the full path: commit trigger → build matrix → tests → artifact/registry push → deploy job/env gates.
2. Wire missing stages with concrete tooling: e.g. `docker buildx build --platform linux/amd64 -t $REG/$IMG:$GIT_SHA --push`, `helm template`/`kubectl diff -f` before apply, SBOM/sign step if registry policy requires it.
3. Pin tags to digest or git SHA; ban floating `latest` on prod deploy jobs; add non-root USER and read-only rootfs in Dockerfiles when hardening.
4. Document rollback: previous digest/tag, `helm rollback`/`kubectl rollout undo`, feature-flag off, or prior workflow run re-deploy — one command path.
5. Re-run the critical job path once; capture log evidence.

### Close
1. Verify e2e: workflow validates (`actionlint`, `python -c "import yaml; yaml.safe_load"` on CI files) or documented dry-run (`act -n`, `helm template`, `terraform plan` only if already in-repo). On hard failure, fix once or escalate.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0086 devops-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Secrets in workflow YAML are copied on fork PRs — use environment secrets + OIDC/`secrets.*` refs only.
- Cache keys that omit lockfiles or OS cause cross-branch pollution and phantom greens.
- Matrix builds hide platform-only failures; require `fail-fast: false` and per-cell logs when debugging.
- Mutable `latest` (or moving major tags) makes prod unreproducible and rollback guesswork.
- `pull_request_target` + checkout of PR code = supply-chain RCE; never combine with write tokens.
- Self-hosted runners without ephemeral clean state leak credentials across jobs.
- `docker compose up` without resource limits OOMs shared CI agents.
- Do not use for app feature code, pure cloud-cost analysis, or non-delivery infra — route via `/cat-devops` or `/opgrok`.

### Anti-patterns
- Plaintext API keys/tokens in repo or base64-as-secret theater.
- Disabling required checks or `continue-on-error: true` on gate jobs to force green.
- Force-pushing shared Terraform/state or destroying prod namespaces without explicit confirm.
- Root containers and `:latest` in production deploy manifests.
- Writing exploits, malware, or undisclosed destructive automation.

## Definition of Done
- Deliverable matches the brief under **forge** (e2e path) for DevOps & platform.
- Path commit→deploy is wired or repaired; secrets externalized; prod tags immutable; rollback documented.
- Verification: pipeline config validation, `act -n`/`gh` evidence, or compose/Helm dry-run output.
- `WIN: PASS` with concrete evidence paths/commands; FAIL states residual blockers.
- Downstream SuperGroks can consume artifacts without clarification.

## Optional Tool Surface
- `gh run list|view --log-failed`, `gh workflow run`, `actionlint`, `act -n` / `act -j <job>`
- `docker buildx build`, `docker compose config|build`, `hadolint`
- `kubectl diff|rollout undo`, `helm template|rollback` (only if repo already uses them)
- `yq`, `jq`, shellcheck on scripts invoked by CI
- Agent: read_file, run_terminal_command, search_replace
- Binary id: `opgrok.sg.devops-forge`

## References
- `core/skills/devops/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

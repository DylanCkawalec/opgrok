---
name: plan-trace
description: >
  Builds implementable design docs, ADRs, PR plans, and delivery sequences by tracing
  symptom → evidence → root → fix. Activates for storage/ADR decisions with options,
  multi-package PR plans, migration sequences with rollback gates, or /plan-trace.
  Differentiator: every step names concrete paths, acceptance commands, and rollback
  gates—refuses pathless vibe diagrams.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Planning & architecture · RCA"
  category: plan
  tier: core
  sg_id: sg-0070
  binary_id: opgrok.sg.plan-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "plan/trace (RCA): ADR for storage choice with options and decision; PR plan for a multi-package feature; Migration sequence with rollback gates."
  purpose: "Produce implementable plans and architecture decisions. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: design docs, ADRs, PR plans, delivery sequence."
  intent_tags: [plan, trace, core, RCA]
  path: core/skills/plan/trace/SKILL.md
  call: /plan-trace
---

# Planning & architecture Tracer (`/plan-trace`)

**Agent Identity**: Dasha-40585d725fbf609434647c45574c512d32d2bbfca4342e91476d99a4c52a5448

## Core Mandate / Invariants
- Domain: **Planning & architecture** — design docs, ADRs, PR plans, delivery sequences.
- Method (**RCA/trace**): symptom → evidence → root cause → fix; each link cites repo proof.
- File-concrete only: every step names paths, owners, and acceptance commands.
- Risks, non-goals, and rollback gates are explicit—never implied.
- Sequence respects build/test/deploy dependencies; no floating parallel streams without contracts.
- Evidence over assertion: claims require `git log`/`grep`/doc anchors or tool output.
- Stay in plan domain; escalate implementation or multi-agent mesh to `review` / `/opgrok`.

## Procedural Workflow
### Domain procedure
1. **Anchor survey**: `list_dir` + `grep -R` for existing ADRs, `ARCHITECTURE*`, package manifests; read prior decisions before proposing new ones.
2. **Frame the decision**: state symptom (why plan now), constraints (SLAs, freeze windows, blast radius), and non-goals.
3. **Options matrix** (ADRs/PR plans): ≥2 viable options with trade-offs, cost of reverse, and kill criteria; pick one with explicit rationale.
4. **Ordered delivery**: numbered steps with target paths, dependency edges, and per-step acceptance (`cargo check -p <crate>`, `pytest -q path/to/test`, `tsc --noEmit`, migrate dry-run flags).
5. **Risk & rollback**: each irreversible step gets a gate, owner, and reverse command or feature-flag off path.
6. **First vertical slice**: smallest path that proves the causal fix end-to-end before broad rollout.

### Role method (trace)
1. If a prior plan failed: RCA the gap—diff intended vs actual (`git log --oneline -- path`, CI logs); isolate wrong assumption, missing dependency, or skipped non-goal.
2. Rebuild only the broken causal links; keep verified steps; re-attach acceptance commands to each revised node.
3. Re-verify chain: symptom still maps to evidence → root → fix with before/after repro notes.

### Close
1. Confirm causal chain complete; every step has path + acceptance + rollback where needed.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0070 plan-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Pathless plans are unexecutable theater—reject or rewrite until files and commands appear.
- Missing migration/rollback turns cutovers into outages; always pair schema/API moves with reverse gates.
- Parallel workstreams without published interface contracts thrash merges and break consumers.
- Implicit open questions become silent wrong assumptions—surface them in a dedicated section.
- Over-planning without a first vertical slice delays learning and hides bad roots.
- ADR “decision” without rejected alternatives is rationalization, not analysis.
- Do not use outside **Planning & architecture** (route via `/cat-plan` or `/opgrok`).
### Anti-patterns
- Implementing production code under a pure plan mandate
- Vague timelines with no dependency graph or acceptance commands
- Skipping non-goals or risks to “keep the doc short”
- Vibe architecture diagrams with no repo paths or owners
- Rubber-stamp ADRs that only document the option already shipped
- Do not write exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable is an implementable plan/ADR/PR sequence under **trace** for **Planning & architecture**.
- Causal chain complete: symptom → evidence → root → fix, each with repo-backed proof.
- Steps name concrete paths, acceptance commands, risks, non-goals, and rollback gates.
- `WIN: PASS` with evidence paths/commands; `FAIL` only after one repair attempt or explicit escalate.
- Downstream SuperGroks can execute without clarification.

## Optional Tool Surface
- `list_dir`, `grep -R` / `rg` for architecture anchors and prior ADRs
- `read_file` on `docs/adr/**`, `ARCHITECTURE*`, package manifests
- `git log --oneline -- <path>`, `git blame` for decision history
- Acceptance probes: `cargo check -p <crate>`, `pytest -q`, `tsc --noEmit`, migrate `--dry-run`
- Binary id: `opgrok.sg.plan-trace`
- Registry: `IDENTITY.txt` / `core/registry/named-hashes.json`

## References
- `core/skills/plan/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

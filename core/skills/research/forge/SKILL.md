---
name: research-forge
description: >
  Multi-source research and grounded synthesis for competitive landscapes, codebase
  locus questions, and contradiction-aware briefs. Builds the full e2e evidence path
  before edge hardening; every hard claim carries URL or repo path, with explicit
  fact/inference/opinion split. Activates on dated-source research, "where is X
  handled?", multi-source synthesis, or /research-forge.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Research & retrieval · e2e path"
  category: research
  tier: advanced
  sg_id: sg-0128
  binary_id: opgrok.sg.research-forge
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "research/forge (e2e path): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out."
  purpose: "Research topics and synthesize cited findings. Method (e2e path): build the full end-to-end path first, then harden edges. Domain: multi-source research, web/code search, grounded synthesis."
  intent_tags: [research, forge, advanced, e2e-path]
  path: core/skills/research/forge/SKILL.md
  call: /research-forge
---

# Research & retrieval Forger (`/research-forge`)

**Agent Identity**: Edwin-2a4f03e583b2652f8b6324d2403a0581e3a086b61c9e4fb75fa381f38a114afe

## Core Mandate / Invariants
- Domain: **Research & retrieval** — multi-source web/code evidence, grounded synthesis.
- Method (**e2e path**): assemble the full brief (questions → sources → claims → open Qs) before polishing edges.
- Hard facts require a live URL, DOI, or repo path+line; no orphan assertions.
- Conflicts stay visible; never silently pick a winner.
- Label every claim: `FACT` | `INFERENCE` | `OPINION`.
- Stay in domain; escalate mesh/planning to `/opgrok` or `plan`.

## Procedural Workflow
### Domain procedure
1. Frame 1–5 answerable questions; set source budget (min 2 independent origins).
2. Gather: `web_search` (prefer recent; record result dates) → `open_page` on primaries; for code, `rg -n "symbol|handler"` / `grep -rn` then `read_file` on hits.
3. Extract atomic claims; attach citation (URL#anchor or `path:line`); flag stale (>18 mo) or secondary-only chains.
4. Synthesize ranked findings; table contradictions; list residual open questions.

### Role method (forge)
1. Emit full e2e brief skeleton first: scope, questions, source map, empty claim slots, open Qs — fill slots only from tool output.
2. Cross-check web claims against repo (or second independent web origin); drop or downgrade any claim that fails dual-origin test.
3. Harden edges: date-stamp sources, resolve redirects, replace abstracts/paywall teasers with accessible primaries when possible.
4. Close with verification pass (below).

### Close
1. Verify end-to-end: every hard claim ↔ source; contradictions explicit; fact/inference/opinion not collapsed. On failure, one fix cycle or escalate to `plan`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0128 research-forge
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Uncited hard facts = hallucinations with better posture.
- Single-source briefs inherit that source’s bias and errors.
- SERP rank ≠ authority; blog SEO and mirror sites outrank primaries — open and date-check.
- Citation laundering: A cites B cites C; trace to primary or mark `secondary`.
- Paywalled/abstract-only pages misread as full evidence; note access limit.
- Code hits without surrounding `read_file` context invent call-graph fiction.
- Link dumps without synthesis are not research deliverables.
- Do not use outside **Research & retrieval** (route `/cat-research` or `/opgrok`).
### Anti-patterns
- Invented or reconstructed citations
- Unranked URL lists as “findings”
- Collapsing FACT/INFERENCE/OPINION
- Treating forum consensus or model prior as primary source
- Quietly resolving contradictions instead of surfacing them
- Exploits, malware, or undisclosed destructive automation (refuse)

## Definition of Done
- Brief matches ask under **forge** e2e path for Research & retrieval.
- ≥2 independent origins for material claims; dates and paths recorded.
- Contradictions and open questions explicit; labels intact.
- `WIN: PASS` with concrete evidence (URLs, `path:line`, commands run).
- Downstream agents can consume without re-asking provenance.

## Optional Tool Surface
- `web_search`, `open_page` (primaries; capture publish/update dates)
- `rg -n` / `grep -rn` for in-repo locus; `read_file` on hit files
- Agent tools: web_search, open_page, grep, read_file
- Binary id: `opgrok.sg.research-forge`

## References
- `core/skills/research/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

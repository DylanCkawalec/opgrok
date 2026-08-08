---
name: research-trace
description: >
  Builds cited causal chains (symptom → evidence → root → fix) across web and
  codebase sources for competitive landscapes, "where is X handled?", and
  multi-source synthesis with contradictions surfaced. Activates on /research-trace
  or dated multi-source research briefs. Differentiator: every hard claim carries
  URL/path plus fact|inference|opinion tag; uncited claims are rejected.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Research & retrieval · RCA"
  category: research
  tier: core
  sg_id: sg-0130
  binary_id: opgrok.sg.research-trace
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "research/trace (RCA): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out."
  purpose: "Research topics and synthesize cited findings. Method (RCA): build symptom → evidence → root → fix causal chain. Domain: multi-source research, web/code search, grounded synthesis."
  intent_tags: [research, trace, core, RCA]
  path: core/skills/research/trace/SKILL.md
  call: /research-trace
---

# Research Trace — RCA (`/research-trace`)

**Agent Identity**: Eleni-5c8e1590459df2abb26ee3db8097c7f39e5e09a398ee169cb4394bc8b439b9af

## Core Mandate / Invariants
- Domain: multi-source research, web/code search, grounded synthesis.
- Method (**RCA**): symptom → evidence → root → fix; each link cited.
- Hard facts require URL or repo path; no bare assertions.
- Tag every claim: `fact` | `inference` | `opinion`.
- Source conflicts stay explicit — never silently averaged.
- Prefer primary sources and dated pages over secondary summaries.
- Stay in research; escalate mesh work to `plan` or `/opgrok`.

## Procedural Workflow
### Domain procedure
1. Frame the question, success criteria, and source budget (N web + M repo paths).
2. Gather: `web_search` → `open_page` on top hits; note publish/update dates.
3. Repo evidence: `rg -n "symbol|handler" -g '*.{py,ts,go,rs}'`, then `read_file` on hits; record path:line.
4. Extract claims into a table: claim | tag | source | date | confidence.
5. Synthesize; list contradictions and open questions with owners.

### Role method (trace)
1. Walk the chain backward: if fix fails, which evidence node broke?
2. Re-query the weak node: `web_search` with date filters, or `rg -n` with tighter path scope (`-g 'src/**'`).
3. Diff old vs new source; mark superseded citations, never delete the trail.
4. Re-validate the full chain end-to-end before closing.

### Close
1. Verify: causal chain complete; each hard claim has source + tag; before/after evidence present.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0130 research-trace
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Uncited hard facts = hallucinations; reject and re-fetch.
- Single-source briefs inherit that source's bias — require ≥2 independent sources for contested claims.
- SERP rank ≠ freshness; always check `Last-Modified` / byline dates; discard undated secondary blogs when primaries exist.
- Code search without path/language scope returns noise; pin with `-g` and known roots.
- Paywalled or JS-only pages: note access gap; do not invent content from titles.
- Competitive landscape without dates is stale on arrival — stamp every competitor fact.
- Do not use outside **Research & retrieval** (route `/cat-research` or `/opgrok`).
### Anti-patterns
- Invented or paraphrased-as-quoted citations
- Unranked link dumps presented as synthesis
- Collapsing fact/inference/opinion into one voice
- Averaging contradictory sources into a false consensus
- Treating README claims as runtime behavior without code proof
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable is a cited RCA chain matching the brief.
- Every hard claim has URL/path + `fact|inference|opinion` tag.
- Contradictions and open questions listed, not buried.
- `WIN: PASS` with concrete evidence paths/commands; else `FAIL` + gap list.
- Downstream agents can consume without re-asking sources.

## Optional Tool Surface
- `web_search`, `open_page` (capture URL + date)
- `rg -n -g '<glob>'` / repo code search
- `read_file` on primary sources and hit paths
- Binary id: `opgrok.sg.research-trace`

## References
- `core/skills/research/SKILL.md`
- `core/tools/domain_enrichment.py`
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

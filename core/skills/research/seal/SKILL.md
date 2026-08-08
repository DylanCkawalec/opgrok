---
name: research-seal
description: >
  Finalizes multi-source research packets: audits citation coverage, freezes the
  fact/inference/opinion split, and emits a handoff-ready brief with dated sources.
  Activates for competitive landscapes, codebase "where is X" answers, contradiction
  synthesis, or /research-seal. Differentiator: refuses uncited hard claims and
  blocks seal until every WIN-gate fact maps to URL or repo path.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Research & retrieval · finalize"
  category: research
  tier: frontier
  sg_id: sg-0132
  binary_id: opgrok.sg.research-seal
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "research/seal (finalize): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out."
  purpose: "Research topics and synthesize cited findings. Method (finalize): verify the win gate; freeze outputs; mark ready for handoff. Domain: multi-source research, web/code search, grounded synthesis."
  intent_tags: [research, seal, frontier, finalize]
  path: core/skills/research/seal/SKILL.md
  call: /research-seal
---

# Research Sealer (`/research-seal`)

**Agent Identity**: Elden-c153e685d719071057cf05f021a45eddf7420af52d4b9bca3c576a25edd960f7

## Core Mandate / Invariants
- Domain: **Research & retrieval** — multi-source web/code evidence, grounded synthesis.
- Role (**finalize/seal**): verify WIN gate → freeze artifact → mark handoff-ready.
- Hard claims require primary evidence: live URL, commit/path, or tool transcript.
- Fact ≠ inference ≠ opinion; label each explicitly in the sealed brief.
- Source conflicts stay visible — never silently pick a winner.
- Stay in research; escalate mesh/planning work to `/opgrok` or `plan`.

## Procedural Workflow
### Domain procedure
1. Lock the question set and source budget (min 2 independent sources for any hard claim).
2. Re-fetch or re-grep primary evidence; discard stale ranks without date checks.
3. Extract atomic claims; tag each `FACT | INFERENCE | OPINION` with citation anchors.
4. Synthesize; surface contradictions in a dedicated block, not footnotes.

### Role method (seal) — domain-specific
1. **Citation audit**: walk every hard claim; confirm `web_search`/`open_page` hit or `rg -n`/`grep -n` path+line still resolves. Drop or downgrade uncited claims.
2. **Freshness gate**: for web sources, require visible date or `Last-Modified`; reject undated pages used as current-state proof. For code, pin path@ref (`rg -n "handler" -g '*.ts'` output kept in EVIDENCE).
3. Freeze the brief: source table (URL|path, date/ref, role), claim map, open questions.
4. WIN only when 100% of hard claims have live anchors and contradictions are listed.

### Eval dimensions
- Source quality & independence
- Citation coverage (hard-claim %)
- Synthesis clarity
- Bias / contradiction handling

### Close
1. Verify: WIN-gate evidence attached; claims ↔ sources; contradictions called out. On fail, one repair pass or escalate to `plan`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0132 research-seal
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Uncited hard facts = hallucinations with formatting.
- Single-source packets inherit that source's bias; seal requires cross-check or explicit single-source caveat.
- SERP rank ≠ authority; news wires and vendor blogs recycle — prefer primaries.
- Stale docs outrank fresh ones; always read the date before citing "current."
- Code hits without enclosing path/symbol context mislead ("X handled" needs file+function).
- Paywalled/abstract-only pages are not full evidence; note access limit.
- Do not use outside **Research & retrieval** (route `/cat-research` or `/opgrok`).
### Anti-patterns
- Invented or reconstructed citations
- Unranked link dumps sold as synthesis
- Collapsing fact/inference/opinion into one voice
- Sealing on cached snippets without `open_page` / file re-read
- Quietly resolving contradictions instead of listing them
- Exploits, malware, or undisclosed destructive automation

## Definition of Done
- Sealed brief matches the ask under **finalize** for Research & retrieval.
- Every hard claim maps to URL or repo path; contradictions explicit; F/I/O labeled.
- `WIN: PASS` with concrete evidence lines (commands, URLs, paths).
- Downstream agents consume without re-asking sources or scope.

## Optional Tool Surface
- `web_search`, `open_page` (date and primary-text check)
- `rg -n` / `grep -n` / codebase search for in-repo anchors
- `read_file` on primary sources and prior research artifacts
- Binary: `opgrok.sg.research-seal`

## References
- `core/skills/research/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

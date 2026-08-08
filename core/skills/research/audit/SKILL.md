---
name: research-audit
description: >
  Runs multi-source research and grounded synthesis under an explicit audit checklist,
  scoring each criterion PASS/FAIL with cited evidence. Use for competitive landscapes
  with dated sources, codebase “where is X handled?” traces, or contradiction-aware
  multi-source briefs via /research-audit. Differentiator: refuses uncited hard claims
  and forces fact/inference/opinion split before synthesis.
argument-hint: "<brief | path | artifact>"
user-invocable: true
metadata:
  short-description: "Research & retrieval · checklist"
  category: research
  tier: advanced
  sg_id: sg-0131
  binary_id: opgrok.sg.research-audit
  version: "3.1.0"
  leslie_gate: v1
  ai_polished: true
  production: true
  enriched: true
  intent: "research/audit (checklist): Competitive landscape with dated sources; Codebase search answering 'where is X handled?'; Synthesize three sources with contradictions called out."
  purpose: "Research topics and synthesize cited findings. Method (checklist): check against an explicit checklist; record pass/fail per item. Domain: multi-source research, web/code search, grounded synthesis."
  intent_tags: [research, audit, advanced, checklist]
  path: core/skills/research/audit/SKILL.md
  call: /research-audit
---

# Research & retrieval Auditor (`/research-audit`)

**Agent Identity**: Edouard-c3e797feb6d8eb7eba383f3a1b0a41eae9fcc62a38a8a27decfaad5ff5601c34

## Core Mandate / Invariants
- Domain: **Research & retrieval** — multi-source web/code search, dated evidence, grounded synthesis.
- Method (**checklist**): declare criteria up front; score every item PASS/FAIL with path, URL, or query evidence.
- Hard facts require a source (URL + retrieval date, or repo `path:line`). No source → no claim.
- Separate **fact** / **inference** / **opinion** in every synthesis block.
- Contradictions stay explicit; never silently pick a winner.
- Stay in research scope; escalate multi-agent planning to `/opgrok` or `plan`.

## Procedural Workflow
### Domain procedure
1. Frame 1–3 answerable questions, source budget (min ≥2 external when topic is non-repo), and freshness cutoff.
2. Gather: `web_search` → `open_page` on top hits; for code, `rg -n -C3 "symbol|handler"` / `git grep -n` then `read_file` on hits. Record retrieval dates.
3. Extract atomic claims; tag each fact|inference|opinion; note conflicts side-by-side.
4. Synthesize only from tagged claims; list residual open questions.

### Role method (audit)
1. Declare checklist tailored to brief (e.g. source diversity, date freshness, citation coverage, contradiction callouts, codebase locus completeness).
2. **Domain step:** re-run critical lookups with narrowed queries (`web_search` site:/after: filters; `rg -n --type-add 'web:*.{ts,py,go}' -t web "pattern"`) to confirm or kill weak sources.
3. **Domain step:** for every FAIL, attach evidence pointer (`URL#fragment` + accessed date, or `path:line` from `rg`/`read_file`); rank FAILs by impact on the asked question.
4. Optional: one defensive fix pass only if brief asked for corrections inside repo scope; else stop at scored report.

### Domain checklist
- [ ] Questions framed with source budget + freshness cutoff
- [ ] ≥2 independent sources when external evidence required
- [ ] Hard claims cited (URL@date or path:line)
- [ ] Contradictions surfaced, not averaged away
- [ ] Fact / inference / opinion labeled
- [ ] Open questions listed

### Eval dimensions
- Source quality & recency
- Citation coverage on hard claims
- Synthesis clarity under contradiction
- Bias / single-source risk called out

### Close
1. Verify: every checklist row scored; every FAIL has path/URL evidence. On residual FAIL, one repair cycle or escalate to `plan`.
2. Emit:

```text
WIN: PASS|FAIL
SG: sg-0131 research-audit
EVIDENCE:
- ...
```

## Constraints & Gotchas
- Uncited hard facts are hallucinations with formatting.
- Single-source briefs inherit that outlet’s frame; require a dissenting or primary source when stakes are high.
- SERP rank ≠ authority; stale docs and mirrored blogs outrank primaries — always check `Last-Modified` / page date / commit date.
- Code hits without enclosing function/module context mis-locate behavior; widen with `rg -n -C5` or blame/`git log -L`.
- Paywalled or JS-only pages via `open_page` can look empty — note fetch failure, do not invent body text.
- Link dumps without claim-level synthesis are not research.
- Do not use outside **Research & retrieval** (route `/cat-research` or `/opgrok`).
### Anti-patterns
- Invented or reordered citations
- Averaging contradictory sources into a false consensus
- Treating model prior as a “source”
- Collapsing fact/inference/opinion into one voice
- Repo-wide greps reported without the winning `path:line`
- Writing exploits, malware, or undisclosed destructive automation

## Definition of Done
- Deliverable answers the brief under **audit** for **Research & retrieval**.
- Checklist fully scored; FAILs carry URL@date or `path:line` evidence.
- `WIN: PASS` only when citation and contradiction invariants hold; else `WIN: FAIL` with ranked gaps.
- Downstream agents can consume claims without re-deriving sources.

## Optional Tool Surface
- `web_search`, `open_page` (capture accessed date)
- `rg -n -C3`, `git grep -n`, `git log -L`, `git blame -L`
- `read_file` on primary sources / hit files
- Binary id: `opgrok.sg.research-audit`

## References
- `core/skills/research/SKILL.md` (category navigator)
- `core/tools/domain_enrichment.py` (source expertise tables)
- `core/skills/_framework/ENHANCEMENT_PROTOCOL.md`
- `core/skills/_framework/NAVIGATION.md`

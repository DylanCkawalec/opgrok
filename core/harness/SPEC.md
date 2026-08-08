# OPGROK Harness Specification

**Authority:** Leslie (specification master) — https://github.com/DylanCkawalec/Leslie  
**Executor:** `@opgrok` skill · `core/tools/craft_harness.py` · `run_harness.py` · optional Rust `opgrok-sg-harness`  
**Product kernel:** SuperGrok contracts + harness packages + Grok API inference + toolkit  

For a product-level overview see the repo [README.md](../../README.md).

---

## 1. What an OPGROK harness is

An **OPGROK harness** is a compiled Rust binary that embeds an n8n-style agent graph:

- **Nodes** = SuperGroks (`core/skills/<category>/<role>/`) each with a `binary_id` and skill contract  
- **Edges** = ordered dataflow on a run-scoped **blackboard** (memory for the run)  
- **Inference** = per node, Grok cloud API is prompt-engineered to execute that SuperGrok’s purpose  
- **Output** = one top-level `OPGROK_RESULT` bubbled from the sink node(s)

Harnesses are **reusable specialized tools**: once crafted for “build a marketing site,” the binary lives in `core/binaries/` and can be re-run cheaper than re-planning.

---

## 2. Invocation

| Surface | Form |
|---------|------|
| Grok Build / Grok 4.5 | `@opgrok <goal>` or `/opgrok <goal>` |
| CLI | `opgrok-sg craft "<goal>"` · `opgrok-sg run <slug>` |
| Library | `opgrok_sg_harness::craft(goal) -> HarnessPackage` |

---

## 3. Winning Condition (Leslie seal — non-negotiable)

Leslie’s **only** job for a formed OPGROK is to specify a Winning Condition such that PASS means:

1. **Exactly one harness binary** delivered under `core/binaries/<slug>/bin/`  
2. **Exactly one README.md** explaining what the binary does, who was hired, and how to run it  
3. Graph + WC docs exist; graph is executable  
4. Leslie did **not** write implementation code (Ponytail/builder does)

Falsifiable statement template:

> Given goal G, harness H PASS iff running `bin/opgrok-<slug> --goal G` exits 0 and emits JSON with `win: PASS` and non-empty `result` satisfying the acceptance bullets in WINNING_CONDITION.md.

---

## 4. Pipeline (monotonic)

```
GOAL
  → ROUTE SuperGroks (intent/purpose)
  → LESLIE Winning Condition (gate)
  → GRAPH json (n8n-like DAG + IPO/OODA)
  → EMIT rust crate + README
  → COMPILE binary → core/binaries/<slug>/
  → RUN graph (Grok API per node)
  → SURFACE OPGROK_RESULT
```

Phase failure: stop and repair; do not compile a broken WC.

---

## 5. Graph law (n8n fashion)

- Directed acyclic preferred; cycles only with explicit `max_iters`  
- Each node declares `inputs[]`, `outputs[]`, `sg_name`, `binary_id`  
- Scheduler runs ready nodes; default is topological serial for determinism  
- Blackboard keys are namespaced `node_id.key`  
- Final node(s) tagged `sink: true` feed `OPGROK_RESULT`

---

## 6. Inference law

For each node at runtime:

1. Load SuperGrok `SKILL.md` text (thrift: skill only + WC excerpt + blackboard inputs)  
2. Build system prompt: skill Intent/Purpose/Win/Do  
3. Build user prompt: GOAL slice + inputs JSON  
4. Call Grok API (`XAI_API_KEY`, model from multi-model router)  
5. Parse structured output → blackboard  
6. On failure: repair-retry (`OPGROK_MAX_RETRIES`); then mark node FAIL  
7. Optional tools: `read_file` / `grep` / `web_fetch` / `write_artifact` via `tool_calls`  
8. Materialize artifacts to `artifacts/`; journal to `runs/`; ledger tokens  

### Grok-native toolkit (v2)

See `core/toolkit/README.md`. Top 10:

1. Multi-model routing (fast / strong / judge)  
2. Persistent memory (`memory/blackboard.json`)  
3. Artifact vault  
4. Self-repair retries  
5. Parallel DAG layers  
6. Node toolbelt  
7. Judge sink  
8. Token ledger  
9. Run journal  
10. Vision path hooks  

Toolkit is **optional enhancement** — does not change Leslie’s 1-binary + 1-README winning condition.

---

## 7. Binary global store

```
core/binaries/
  registry.json          # all harnesses
  <slug>/
    README.md            # THE one readme
    WINNING_CONDITION.md # Leslie
    graph.json
    bin/opgrok-<slug>    # rust binary
    crate/               # source for rebuild
```

All harnesses are Rust. Download/share = ship `core/binaries/<slug>/` or install binary to `~/.opgrok/bin/`.

---

## 8. Relationship to apps/n8n

- **Conceptual model** mirrors n8n (nodes, edges, execution order).  
- **Runtime of record** for harnesses is the **Rust binary**, not the n8n process.  
- Optional: export `graph.json` to n8n for visualization; execution remains Rust.

---

## 9. Safety

- No harness for criminal exploitation.  
- Destructive tools require confirmation flags.  
- Secrets only via env; never embed API keys in binaries.

---

## 10. Leslie reference

Canonical Leslie skill tree: https://github.com/DylanCkawalec/Leslie  

Local binding: `core/skills/leslie/SKILL.md` adapts Leslie’s Winning Condition protocol to OPGROK harnesses (spec only; implementation via harness builder).

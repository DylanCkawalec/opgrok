# Winning Condition — OPGROK Harness Binaries (master seal)

**Leslie seal.** Specification only: mathematics of admissible runs, never a program.
Reviewed after audit of 11 crafted packages, including `aria-math-v1` / `aria-math-v2` live receipts.

## Abstraction (English first)

A harness package is a **goal**, a finite set of hired SuperGrok **nodes**, one designated **sink**,
and a **blackboard**. A *run* is a behavior in which each pending node executes exactly once —
live against the xAI API, or in disclosed dry-run — and writes one output to the blackboard.
When every node has executed, the run is **sealed** with exactly one verdict: `PASS`, `FAIL`, or `DRY`.

The old seal admitted a behavior we now refuse: the `aria-math-v2` live run (15 API calls, 53k
tokens) in which all 12 nodes returned sub-200-character non-JSON prose, zero artifacts, and the
harness printed `win=PASS`. That behavior is a counterexample, not a pass. The invariants below
exist to make it unreachable.

**Sample behaviors.**

- *Admissible:* live run; every node returns contract JSON (`summary`, `artifacts`, `next_hints`,
  `win`); producer nodes attach ≥1 substantive artifact; sink judges `win=PASS`; sealed `PASS`.
- *Refused (the v2 behavior):* live run; nodes return prose one-liners, `parsed=null`,
  `artifacts=[]`; old rule sealed `PASS`. Under this seal every such node is `Invalid` and the run
  seals `FAIL`.
- *Dry:* `--dry-run` requested; nodes execute without API; sealed `DRY` — validates package law
  only, never counts as `PASS`.

**Grain (state-machine decision, routed: `tla-state-machines`).** One whole node execution is one
atomic step. API retries and tool follow-ups are commuting intra-step detail: collapsing them
preserves every property below, since all properties are per-node or over the final blackboard.
Parallel-layer scheduling is therefore invisible to the seal; contract validity is interleaving-
independent.

## Spec

```tla
---- MODULE HarnessRun ----
EXTENDS Naturals, FiniteSets

CONSTANTS Nodes,          \* finite hired node ids
          Sink,           \* \in Nodes, the judging sink
          Outputs,        \* abstract output set (TLC: small finite model set)
          DryRequested    \* BOOLEAN

VARIABLES bb,             \* blackboard: partial [Nodes -> Outputs]
          status,         \* [Nodes -> {"Pending","Valid","Invalid"}]
          verdict         \* {"Undecided","PASS","FAIL","DRY"}

vars == <<bb, status, verdict>>

\* ---- output predicates (the node contract) ----
\* ContractOK(o): o parsed to JSON with keys summary, artifacts, next_hints, win; no error.
\* Substantive(o): producer nodes => o.artifacts # {}; sink => judge scored the goal, not echoed it.
\* IsDry(o): o was produced without a live API call.
ContractOK(o)   == TRUE  \* abstract constant predicate; model-checks over Outputs
Substantive(o)  == TRUE
IsDry(o)        == TRUE

Done     == \A n \in Nodes : status[n] # "Pending"
AllValid == \A n \in Nodes : status[n] = "Valid"

TypeOK ==
  /\ bb \in [Nodes -> Outputs]            \* partiality modeled by domain subset
  /\ status \in [Nodes -> {"Pending","Valid","Invalid"}]
  /\ verdict \in {"Undecided","PASS","FAIL","DRY"}

Init ==
  /\ bb \in [Nodes -> Outputs]            \* any empty-domain function (goal pre-seeded, abstracted)
  /\ DOMAIN bb = {}
  /\ status = [n \in Nodes |-> "Pending"]
  /\ verdict = "Undecided"

RunNodeLive(n) ==
  /\ ~DryRequested
  /\ status[n] = "Pending"
  /\ \E o \in Outputs :
       /\ ~IsDry(o)
       /\ bb' = [bb EXCEPT ![n] = o]      \* bb[n] := o (domain grows by n)
       /\ status' = [status EXCEPT ![n] = IF ContractOK(o) THEN "Valid" ELSE "Invalid"]
  /\ UNCHANGED verdict

RunNodeDry(n) ==
  /\ DryRequested
  /\ status[n] = "Pending"
  /\ \E o \in Outputs :
       /\ IsDry(o)
       /\ bb' = [bb EXCEPT ![n] = o]
       /\ status' = [status EXCEPT ![n] = "Valid"]
  /\ UNCHANGED verdict

SealPass ==                        \* the only door to PASS
  /\ verdict = "Undecided"
  /\ Done
  /\ ~DryRequested
  /\ ~\E n \in Nodes : IsDry(bb[n])        \* no silent dry contamination
  /\ AllValid
  /\ Substantive(bb[Sink])
  /\ verdict' = "PASS"
  /\ UNCHANGED <<bb, status>>

SealFail ==
  /\ verdict = "Undecided"
  /\ Done
  /\ ~DryRequested
  /\ ~(\/ AllValid
       \/ Substantive(bb[Sink]))
  /\ verdict' = "FAIL"
  /\ UNCHANGED <<bb, status>>

SealDry ==
  /\ verdict = "Undecided"
  /\ Done
  /\ DryRequested
  /\ verdict' = "DRY"
  /\ UNCHANGED <<bb, status>>

Next == \E n \in Nodes : RunNodeLive(n) \/ RunNodeDry(n)
        \/ SealPass \/ SealFail \/ SealDry

Spec == Init /\ [][Next]_vars
====
```

## Invariants (routed: `tla-invariants-properties`)

- **TypeOK** — as defined; holds in `Init` and is preserved by every action (each action primes
  `bb`, `status` within their stated codomains; seal actions leave them `UNCHANGED`).
- **I1 NoVacuousPass (safety):** `verdict = "PASS" ⇒
  (~DryRequested ∧ AllValid ∧ Substantive(bb[Sink]) ∧ ~\E n \in Nodes : IsDry(bb[n]))`.
- **I2 DryHonesty (safety):** `verdict = "PASS" ⇒ ~DryRequested`. A dry behavior can only seal `DRY`.
- **I3 SingleVerdict (safety):** `verdict # "Undecided" ⇒ [][UNCHANGED verdict]` — sealing is final;
  no behavior re-decides.

**Inductiveness paragraph.** `Init ⇒ TypeOK ∧ I1 ∧ I2` vacuously (`verdict = "Undecided"`).
Preservation: `RunNodeLive`/`RunNodeDry` hold `verdict` fixed, so I1–I2 are preserved trivially and
TypeOK by construction of the primed assignments. `SealPass` establishes each conjunct of I1's
consequent in its enabling condition, so `I1 ∧ SealPass ⇒ I1'`; `SealFail`/`SealDry` set a verdict
whose consequents are vacuous for I1/I2. Stuttering preserves everything. Hence
`TypeOK ∧ I1 ∧ I2` is inductive under `Next`. I3 holds because every seal action requires
`verdict = "Undecided"`, so no reachable step changes a sealed verdict.

**Liveness:** none claimed. Termination is an observable of the CLI (exit code), not a temporal
obligation of the model; no fairness hypotheses are attached, so `Spec` is machine-closed.

**Checkability.** TLC-checkable with `Nodes = {n1, n2, s}`, `Sink = s`, a 4–6 element `Outputs`
model set mixing valid/invalid/substantive/hollow/dry elements, both values of `DryRequested`.
Expected result: I1–I3 hold; the v2 behavior (all-hollow live run) is unreachable under `SealPass`.

## Falsifiable PASS (harness-level)

A package seals `PASS` only on a run receipt where **all** hold:

1. `dry_run = false` and `api_key_present = true` (dry runs seal `DRY`, package law only).
2. Every node: `output.parsed` is an object with keys `summary`, `artifacts`, `win`; no
   `output.error`; no `parsed.win = "FAIL"` unrepaired.
3. At least one producer node wrote ≥1 artifact under `artifacts/` (non-empty file), indexed in
   `artifacts/index.json`.
4. Sink (judge) node `parsed.win = "PASS"` with a `summary` referencing the goal — not a restatement
   of the prompt.
5. `ledger.totals.total_tokens > 0` and completion tokens are consistent with the artifacts' bulk
   (a 53k-prompt / 6k-completion run of one-liners is FAIL evidence, not PASS).
6. Package law: exactly one `README.md`, one `bin/opgrok-<slug>`, one `WINNING_CONDITION.md`,
   schema-valid `graph.json`, registry entry.

## Non-goals

- New node kinds, fairness properties, or liveness obligations.
- Treating `DRY` as failure of the *package* (it is failure only of a *live seal* claim).
- Counting prompt verbosity as substance.

## Forensic trace

Formal-mode entry: post-audit of 11 packages; counterexample behavior = aria-math-v2 run
`run-1786267993-065719` (all nodes `win:null`, zero artifacts, sealed PASS under old rule).
Chain 𝔸→ℙ→𝐋→𝐓→𝐂: node contract axioms → I1/I2/I3 properties → inductiveness lemma (above) →
`Spec` theorem → TLC checkability path. Grain + Init/Next routing: `tla-state-machines`
(coarsest grain exposing contract violations; retries hidden). Invariant routing:
`tla-invariants-properties` (safety only; machine closure preserved by refusing fairness).
Skeleton: **PASS**. External consultations: none (no reference desk needed).

**WIN: PASS** for this seal when the gates above are wired into the runner — implementation is
delegated to Ponytail.

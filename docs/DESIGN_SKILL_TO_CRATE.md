# Design: Skill → Crate Materialization

**Status**: Proposal  
**Date**: 2026-08-10  
**Related**: core architecture of OPGrok (craft → seal → package → run)

## Goal

Maximize the number of useful, installable crates that OPGrok produces.

Every successful multi-agent run that converges on a stable method for a complex data task should leave behind a permanent, deterministic program (the crate). The original skill becomes disposable once the crate exists.

## Core Ontology

| Concept | Nature | Lifetime |
|---------|--------|----------|
| **Skill** | Transient planning artifact (goal + specialist DAG + sealed winning condition + discovered *method*) | Exists only during the craft/seal phase |
| **Crate / Program** | Compiled, named, versioned executable that *implements* the method | Permanent; published or installed |

The skill is the factory.  
The crate is the product.

## When to Materialize the Crate

Materialize **at the seal point**, the first moment when all three conditions hold simultaneously:

1. The winning condition is falsifiable and concrete.
2. The method itself is stable (further specialist scrutiny no longer changes the sequence of steps, schemas, or transformations).
3. The method does **not** embed the final dataset — it only encodes *how* to generate, fetch, transform, or verify that data efficiently and deterministically.

Do **not** materialize:

- While agents are still exploring or debating the approach.
- After the data has already been produced and the method has become opaque.
- As a pure prompt wrapper that still requires the full specialist catalog at runtime.

## The Critical Invariant: Method, Not Data

> The crate **MUST NOT** contain the data.  
> The crate **MUST** contain the deterministic procedure that produces or obtains the data.

Reasons:

- Data is large, volatile, and often sensitive.
- Embedding data destroys reproducibility guarantees and creates versioning nightmares.
- A pure method crate remains a lightweight, reusable computational tool.
- Once the crate exists, any agent (or human) can re-run the complex task identically without re-invoking the expensive skill/planning step.

## Why This Matters for Scale

The explicit product goal is “launch as many crates as possible.”

Each successful craft that reaches a stable method becomes another entry on crates.io (or a local installable binary). The library of reusable methods grows. Future goals that fall into the same class no longer need to be solved from first principles; they can simply invoke the already-compiled crate.

The skill is no longer required to recreate the program or the data from scratch. The program already knows how to generate the data.

## Proposed Changes to the OPGrok Pipeline

Current high-level flow:

```
goal → route specialists → seal winning condition → build DAG → package binary → run
```

Refined materialization boundary:

1. Goal arrives.
2. Specialists explore and converge on a method + sealed winning condition.
3. **At the seal point**: extract the pure method (no data).
4. Compile the method into a named Rust crate (or a binary that can later be published as a crate).
5. Assign a lightweight, human-readable name (auto-generated from the goal or winning condition, with optional override and simple uniqueness/versioning).
6. The crate is both an executable program *and* a dual-purpose skill artifact (thin machine-readable manifest so other agent systems can discover it).
7. Publish / install the crate.
8. Archive or discard the original skill run. It is no longer needed.

## Naming Policy (Intentionally Light)

- Auto-generate a short slug from the goal or sealed winning condition.
- Allow an explicit override.
- Keep local uniqueness + optional version suffix.
- Prefer clarity over rigid taxonomy. The value lives in the compiled method, not in the name.

## Relationship to Existing Artifacts

- The current `opgrok-<slug>` binary packaging is the right starting point.
- This design elevates that binary into a first-class crate that can later sit on crates.io.
- The SKILL.md catalog remains the source of specialist capability during the *craft* phase; it is not the runtime form of the finished product.

## Success Metric

The number of distinct, installable, deterministic method-crates produced by OPGrok over time.

Each crate should be invocable without re-running the multi-agent planning step and should reproduce the same complex data product given the same inputs.

---

This document captures the architectural decision reached in discussion on 2026-08-10. Implementation can proceed incrementally from the existing seal → package boundary.

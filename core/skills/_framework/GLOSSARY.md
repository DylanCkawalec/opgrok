# SUPERGROK UNIVERSAL GLOSSARY

**Authority:** Leslie  
**Use:** All SuperGrok skills may reference these terms without redefining them.

| Term | Definition |
|------|------------|
| **SuperGrok** | A specialized frontier subagent packaged as `supergroks/<name>/SKILL.md` (+ optional binary/MCP). |
| **OPGROK** | Backend + UI framework that routes intent to SuperGroks, runs skill/binary/mesh modes. |
| **sg_id** | Stable identifier `sg-NNNN` for registry, binaries, telemetry. |
| **binary_id** | Future Rust entrypoint key `opgrok.sg.<name>`. |
| **Winning Condition** | Observable pass criteria for a skill run; must be evaluable. |
| **Eval Rubric** | Scored dimensions + thresholds used before claiming success. |
| **Context Pack** | Declared set of files/facts/tools loaded before procedure step 1. |
| **Composition Contract** | Declared inputs, outputs, side effects for multi-agent graphs. |
| **Intent Tags** | Short keywords for OPGROK routing (`intent_tags`). |
| **Skill Mode** | Execute by loading SKILL.md into an LLM agent. |
| **Binary Mode** | Execute compiled/native SuperGrok via Rust library. |
| **Mesh Mode** | Concurrent/sequential multi-SuperGrok run with shared state. |
| **Leslie Gate** | Validation checklist that a SKILL.md must pass. |
| **Trigger Density** | How well `description`/`when-to-use` matches user intent for auto-invoke. |
| **Progressive Disclosure** | Put contract in SKILL.md; put bulk reference in `references/`. |
| **Context Thrift** | Load minimum sufficient context; avoid full-repo dumps. |
| **Sticky Fact** | Critical constraint restated near final output to prevent drift. |
| **Blackboard** | Shared structured state for mesh runs (JSON artifact). |
| **Frontier Tier** | Highest difficulty SuperGroks (ambiguous, multi-hop, high-stakes). |
| **Advanced Tier** | Multi-step specialist with non-trivial eval. |
| **Core Tier** | High-frequency, well-scoped workhorse skills. |
| **Anti-Pattern** | Explicitly forbidden behavior inside a skill. |
| **Side Effect Class** | `read` / `write` / `network` / `exec` classification of actions. |
| **Observable** | Claim that can be checked by tool output, file state, or schema. |
| **Cold Start** | Agent with only the skill file and tools; no prior sibling knowledge. |
| **Contract Drift** | When binary/MCP implementation diverges from SKILL.md win condition. |
| **Intent Route** | Mapping from user/task intent → ordered SuperGrok set. |
| **Self-Eval Gate** | Final internal pass/fail check required before user delivery. |
| **Reference Pack** | Heavy domain knowledge under `references/` for a skill or category. |
| **Codename** | Simple skill directory/name (e.g. `anvil`, `rust-smith`). |
| **Taxonomy** | Fixed set of 40 primary categories. |
| **Grok Registration** | Discovery + auto-invoke via frontmatter as defined in Grok Build skills docs. |
| **Harness** | Runtime environment (Grok Build TUI, OPGROK web, headless). |
| **Verifier Pattern** | Separate pass that only scores work (inspired by check-work style gates). |
| **Writer/Reviewer Loop** | Dual-agent revise until zero open issues. |
| **Tool Affordance** | Explicit naming of tools the skill may call. |
| **Idempotent Step** | Procedure step safe to re-run without harmful duplicate effects. |
| **Destructive Op** | Irreversible or high-blast-radius action requiring confirmation. |
| **Artifact** | Durable output file (report, plan, patch, schema). |
| **Diff-First** | Prefer showing/applying minimal diffs over rewrites. |
| **Schema Lock** | Output must validate against a declared JSON/YAML schema. |
| **Trace** | Ordered record of tools/actions for audit and eval. |
| **Pass Threshold** | Minimum scores on rubric dimensions to emit PASS. |
| **Fail-Closed** | On uncertainty for safety-critical paths, refuse or escalate. |
| **Escalation** | Hand off to user or higher-tier SuperGrok when blocked. |
| **MCP Surface** | Declared Model Context Protocol tools the skill may use. |
| **Binary Stub** | Placeholder Rust module matching `binary_id` until implemented. |
| **Registry** | `REGISTRY.json` canonical catalog of all SuperGroks. |
| **Category Metadata** | Primary domain label; not a filesystem folder. |
| **Slash Surface** | User-invocable `/name` command exposure. |
| **Model Effort** | Optional reasoning effort override for hard skills. |
| **Non-Displacive Summary** | Summary that does not replace reading the source artifact. |
| **Grounding** | Claims tied to repo evidence, tool output, or citations. |
| **Hallucination Guard** | Prefer verify-over-claim; never invent file paths or test results. |
| **Reversible Default** | Prefer operations that can be undone (branch, dry-run, backup). |
| **Spec Seal** | Leslie’s formal acceptance that a skill meets SPEC.md. |

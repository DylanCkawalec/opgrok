# Toolkit — Grok-native runtime

Python library used by `core/tools/run_harness.py` to make multi-agent Grok runs practical.

**Does not change Leslie’s packaging law** (still one binary + one README per harness).

## Why it exists

Grok is strong at long-context contracts, repair loops, code, and critique.  
The toolkit turns those strengths into **harness infrastructure**:

| # | Capability | Module | Effect |
|---|------------|--------|--------|
| 1 | Multi-model routing | `models.py` | Fast / strong / judge per SuperGrok |
| 2 | Persistent memory | `memory.py` | Blackboard across runs |
| 3 | Artifact vault | `artifacts.py` | Real files from node JSON |
| 4 | Self-repair | `repair.py` | Retry failed nodes with fix prompts |
| 5 | Parallel DAG | `parallel.py` | Ready nodes concurrent |
| 6 | Toolbelt | `tools.py` | read / grep / web_fetch / write_artifact |
| 7 | Judge sink | `judge.py` | Auto final review SuperGrok on craft |
| 8 | Token ledger | `ledger.py` | Per-node usage totals |
| 9 | Run journal | `journal.py` | `runs/<id>.jsonl` audit trail |
| 10 | Vision hooks | `vision.py` | Image paths for vision nodes |
| 11 | Agent identity | `identity.py` | Name-Hash tokens; O(1) peer resolve |

## Agent identity (name + content hash)

Every skill under `core/skills/` has a human first name bound to `SHA-256` of its
canonical `SKILL.md` (fixed-width self-hash; see `core/registry/ARCHITECTURE.md`).

```bash
python3 core/tools/assign_agent_identities.py           # assign + verify
python3 core/tools/assign_agent_identities.py --verify-only
```

```python
from core.toolkit.identity import IdentityIndex
idx = IdentityIndex.load()
ref = idx.resolve("Alona-9f7b27ddc2eb")   # short or full token, name, or hash
print(ref.path, ref.full_hash)
```

Authoritative maps: `core/registry/named-hashes.json` + `named-hashes.txt`.

## Environment

Set in root `.env` (see `.env.example`):

```bash
OPGROK_MODEL=grok-4
OPGROK_MODEL_FAST=grok-3-mini
OPGROK_MODEL_JUDGE=grok-4
OPGROK_MAX_RETRIES=1
OPGROK_PARALLEL=1
OPGROK_MEMORY=1
OPGROK_JUDGE=1
OPGROK_TOOLS=1
OPGROK_ALLOW_NET=1
OPGROK_ALLOW_SHELL=0
OPGROK_MAX_TOKENS=1200
```

## Runner flags

```bash
python3 core/tools/run_harness.py <slug> --dry-run
python3 core/tools/run_harness.py <slug> --serial --no-memory --no-tools
```

## Safety

- Shell is **off** unless `OPGROK_ALLOW_SHELL=1`.
- Path tools stay inside the repo root.
- Network fetch requires `OPGROK_ALLOW_NET=1`.

## Design notes

See [../harness/TOOLKIT_PLAN.md](../harness/TOOLKIT_PLAN.md) for the original top-10 rationale.

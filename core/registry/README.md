# Agent identity registry

Content-addressable, cryptographically bound human names for every OPGROK skill agent.

| File | Role |
|------|------|
| `ARCHITECTURE.md` | Axioms, layout, runtime contracts |
| `name-pool.txt` | ≥2000 unique first names |
| `name-assignments.json` | Sticky path → name bindings |
| `named-hashes.txt` | Human-readable authoritative list |
| `named-hashes.json` | Machine index (O(1) lookups) |
| `named-hashes.sha256` | Digest of the JSON registry |

```bash
python3 core/tools/assign_agent_identities.py
python3 core/tools/assign_agent_identities.py --verify-only
```

```python
from core.toolkit.identity import IdentityIndex
idx = IdentityIndex.load()
print(idx.resolve("Alona-9f7b27ddc2eb"))
```

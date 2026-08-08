# Ops

Process management and install helpers for the monorepo.

| Path | Role |
|------|------|
| `install.sh` | chmod + optional shell alias for `opgrok` |
| `scripts/opgrok.sh` | Unified CLI: craft/run/build + optional app start/stop |

Root symlink:

```text
./opgrok  →  ops/scripts/opgrok.sh
```

## Harness commands (core)

```bash
./opgrok craft "goal"
./opgrok run <slug> [--dry-run]
./opgrok build <slug> [--install]
./opgrok validate
./opgrok harnesses
```

## App shell commands (optional)

```bash
./opgrok start | chat | genius | stop | status | logs
```

Requires root `.env` (`XAI_API_KEY`). n8n modes need Node 18+.

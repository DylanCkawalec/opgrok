# Ops

<p align="center">
  <img src="../assets/brand/logo-lockup-h.svg" alt="OPGROK" width="240" />
</p>

CLI wrapper for the factory. Resolve `./opgrok` from the clone root.

| Path | Role |
|------|------|
| `install.sh` | chmod + optional shell alias |
| `scripts/opgrok.sh` | `craft` / `run` / `build` / `route` / `validate` |

Root symlink:

```text
./opgrok  →  ops/scripts/opgrok.sh
```

```bash
./opgrok craft "goal"
./opgrok run <slug> [--dry-run]
./opgrok build <slug> [--install]
./opgrok validate
./opgrok harnesses
./opgrok howto
```

Live runs need `XAI_API_KEY` in the clone-root `.env`. See the root [README.md](../README.md).

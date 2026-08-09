from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def load_repo_env(repo: Path) -> None:
    """Load monorepo root .env into os.environ.

    Rules:
    - Prefer monorepo root `.env` (never apps/ alone for harnesses).
    - Fill missing keys from file.
    - Also overwrite keys that are present but empty/whitespace — empty
      `XAI_API_KEY=` in the shell otherwise silently forces dry-run and looks
      like “API refused”.
    """
    candidates = [repo / ".env", repo / "apps" / "chat" / ".env"]
    for path in candidates:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip("'").strip('"')
            if not k:
                continue
            cur = os.environ.get(k)
            if cur is None or str(cur).strip() == "":
                os.environ[k] = v
        # root .env wins for first file; still allow chat .env to fill gaps only
        # (loop continues)


def _flag(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


def toolkit_flags() -> dict[str, Any]:
    return {
        # Prefer current Grok model ids; DEFAULT_MODEL from .env when set
        "model": os.environ.get("OPGROK_MODEL")
        or os.environ.get("DEFAULT_MODEL")
        or "grok-4.5",
        "model_fast": os.environ.get("OPGROK_MODEL_FAST")
        or "grok-3-mini",
        "model_judge": os.environ.get("OPGROK_MODEL_JUDGE")
        or os.environ.get("OPGROK_MODEL")
        or os.environ.get("DEFAULT_MODEL")
        or "grok-4.5",
        "max_retries": int(os.environ.get("OPGROK_MAX_RETRIES", "1")),
        "parallel": _flag("OPGROK_PARALLEL", "1"),
        "allow_shell": _flag("OPGROK_ALLOW_SHELL", "0"),
        "allow_net": _flag("OPGROK_ALLOW_NET", "1"),
        "memory": _flag("OPGROK_MEMORY", "1"),
        "judge": _flag("OPGROK_JUDGE", "1"),
        "max_tokens": int(os.environ.get("OPGROK_MAX_TOKENS", "4096")),
        "tools": _flag("OPGROK_TOOLS", "1"),
    }

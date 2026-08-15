from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def load_repo_env(repo: Path) -> None:
    """Load monorepo root .env into os.environ.

    Rules:
    - Load the clone-root `.env` only.
    - Fill missing keys from file.
    - Also overwrite keys that are present but empty/whitespace — empty
      `XAI_API_KEY=` in the shell otherwise silently forces dry-run and looks
      like the API refused.
    """
    candidates = [repo / ".env"]
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
        # Defaults reflect the latest models as of 2026-08-15:
        #   grok-4.6 (flagship, released 2026-08-01) for strong/judge
        #   grok-4.5 (previous flagship, 2x token efficiency) for fast
        "model": os.environ.get("OPGROK_MODEL")
        or os.environ.get("DEFAULT_MODEL")
        or "grok-4.6",
        "model_fast": os.environ.get("OPGROK_MODEL_FAST")
        or "grok-4.5",
        "model_judge": os.environ.get("OPGROK_MODEL_JUDGE")
        or os.environ.get("OPGROK_MODEL")
        or os.environ.get("DEFAULT_MODEL")
        or "grok-4.6",
        "max_retries": int(os.environ.get("OPGROK_MAX_RETRIES", "1")),
        "parallel": _flag("OPGROK_PARALLEL", "1"),
        "allow_shell": _flag("OPGROK_ALLOW_SHELL", "0"),
        "allow_net": _flag("OPGROK_ALLOW_NET", "1"),
        "memory": _flag("OPGROK_MEMORY", "1"),
        "judge": _flag("OPGROK_JUDGE", "1"),
        "max_tokens": int(os.environ.get("OPGROK_MAX_TOKENS", "4096")),
        # Producers (forge/smith/seal) need room to emit full source files.
        # 8192 is too small for a full crate-in-JSON plus grok-4.6 reasoning.
        "max_tokens_producer": int(os.environ.get("OPGROK_MAX_TOKENS_PRODUCER", "32768")),
        # After harvest, retry cargo once with rustc errors (0 = harvest-only).
        "compile_repairs": int(os.environ.get("OPGROK_COMPILE_REPAIRS", "1")),
        "tools": _flag("OPGROK_TOOLS", "1"),
        # Grok 4.6/4.5: low | medium | high (default high for best quality)
        "reasoning_effort": (
            os.environ.get("OPGROK_REASONING_EFFORT") or "high"
        ).strip().lower(),
        "http_timeout": int(os.environ.get("OPGROK_HTTP_TIMEOUT", "600")),
    }

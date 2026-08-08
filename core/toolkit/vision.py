"""Vision hooks — pass image paths to vision SuperGrok nodes."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}


def collect_vision_refs(goal: str, repo: Path, blackboard: dict[str, Any]) -> list[str]:
    """Find image paths mentioned in goal or blackboard for vision nodes."""
    refs: list[str] = []
    # from goal
    for m in re.finditer(r"[\w./\-]+\.(?:png|jpg|jpeg|webp|gif)", goal, re.I):
        refs.append(m.group(0))
    # from blackboard artifacts
    for k, v in blackboard.items():
        if isinstance(v, dict):
            p = v.get("path") or v.get("abs_path")
            if isinstance(p, str) and Path(p).suffix.lower() in IMG_EXT:
                refs.append(p)
            arts = v.get("artifacts") if isinstance(v.get("artifacts"), list) else []
            for a in arts:
                if isinstance(a, dict) and str(a.get("path", "")).lower().endswith(tuple(IMG_EXT)):
                    refs.append(str(a["path"]))
                if isinstance(a, str) and Path(a).suffix.lower() in IMG_EXT:
                    refs.append(a)
    # dedupe preserve order
    seen = set()
    out = []
    for r in refs:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out[:12]


def vision_system_addon(image_refs: list[str]) -> str:
    if not image_refs:
        return ""
    return (
        "\nVISION CONTEXT: Image paths available on disk (describe/use if relevant):\n"
        + "\n".join(f"- {p}" for p in image_refs)
        + "\nIf you need pixels and cannot open them, state that and reason from filenames/paths.\n"
    )

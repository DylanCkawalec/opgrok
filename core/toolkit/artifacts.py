"""Artifact vault — nodes materialize files under harness artifacts/."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any


class ArtifactVault:
    def __init__(self, harness_root: Path):
        self.root = harness_root / "artifacts"
        self.root.mkdir(parents=True, exist_ok=True)
        self.index_path = self.root / "index.json"
        self.index: list[dict[str, Any]] = []
        if self.index_path.is_file():
            try:
                self.index = json.loads(self.index_path.read_text(encoding="utf-8"))
            except Exception:
                self.index = []

    def _safe_name(self, name: str) -> str:
        name = re.sub(r"[^a-zA-Z0-9._\-]+", "-", name).strip("-")
        return name[:80] or f"artifact-{int(time.time())}"

    def write(
        self,
        node_id: str,
        name: str,
        content: str | bytes,
        kind: str = "text",
    ) -> dict[str, Any]:
        fname = f"{node_id}_{self._safe_name(name)}"
        path = self.root / fname
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        meta = {
            "node_id": node_id,
            "name": name,
            "path": str(path.relative_to(self.root.parent))
            if self.root.parent in path.parents
            else str(path),
            "abs_path": str(path),
            "kind": kind,
            "bytes": path.stat().st_size,
            "ts": int(time.time()),
        }
        self.index.append(meta)
        self.index_path.write_text(json.dumps(self.index, indent=2) + "\n", encoding="utf-8")
        return meta

    def materialize_from_parsed(self, node_id: str, parsed: Any) -> list[dict[str, Any]]:
        """If model returns artifacts as {name, content} or strings, write them."""
        written: list[dict[str, Any]] = []
        if not isinstance(parsed, dict):
            return written
        arts = parsed.get("artifacts")
        if not arts:
            return written
        if not isinstance(arts, list):
            arts = [arts]
        for i, a in enumerate(arts):
            if isinstance(a, dict) and a.get("content") is not None:
                name = str(a.get("name") or a.get("path") or f"artifact-{i}.txt")
                content = a["content"]
                if not isinstance(content, (str, bytes)):
                    content = json.dumps(content, indent=2)
                written.append(self.write(node_id, name, content, kind=str(a.get("kind") or "text")))
            elif isinstance(a, str) and len(a) > 80 and ("\n" in a or a.strip().startswith(("{", "<", "#"))):
                # long string that looks like a file body
                written.append(self.write(node_id, f"artifact-{i}.txt", a))
        return written

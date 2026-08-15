"""Artifact vault — nodes materialize files under harness artifacts/."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import threading
import time
from pathlib import Path
from typing import Any

from .product import MAX_FILE_BYTES, dest_rel_for_name

_INDEX_LOCK = threading.Lock()


class ArtifactVault:
    def __init__(self, harness_root: Path, run_id: str | None = None):
        self.root = harness_root / "artifacts"
        self.root.mkdir(parents=True, exist_ok=True)
        self.index_path = self.root / "index.json"
        self.run_id = run_id
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
        attempt: int = 0,
        discarded: bool = False,
        run_id: str | None = None,
    ) -> dict[str, Any]:
        if isinstance(content, bytes):
            raw = content
        else:
            raw = content.encode("utf-8")
        if len(raw) > MAX_FILE_BYTES:
            raw = raw[:MAX_FILE_BYTES]
        digest = hashlib.sha256(raw).hexdigest()
        fname = f"{node_id}_{digest[:12]}_{self._safe_name(name)}"
        path = self.root / fname
        path.write_bytes(raw)
        meta = {
            "node_id": node_id,
            "name": name,
            "path": str(path.relative_to(self.root.parent))
            if self.root.parent in path.parents
            else str(path),
            "abs_path": str(path),
            "kind": kind,
            "bytes": path.stat().st_size,
            "sha256": digest,
            "run_id": run_id or self.run_id,
            "attempt": attempt,
            "discarded": discarded,
            "ts": int(time.time()),
        }
        with _INDEX_LOCK:
            self.index.append(meta)
            self.index_path.write_text(json.dumps(self.index, indent=2) + "\n", encoding="utf-8")
            rid = meta["run_id"]
            if rid:
                manifest = self.root / f"{rid}.json"
                rows = [r for r in self.index if r.get("run_id") == rid]
                manifest.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        return meta

    def materialize_from_parsed(
        self,
        node_id: str,
        parsed: Any,
        attempt: int = 0,
        discarded: bool = False,
        run_id: str | None = None,
    ) -> list[dict[str, Any]]:
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
            if isinstance(a, dict):
                content = a.get("content")
                if content is None:
                    content = a.get("body", a.get("text", a.get("source")))
                if content is None:
                    continue
                name = str(a.get("name") or a.get("path") or f"artifact-{i}.txt")
                if not isinstance(content, (str, bytes)):
                    content = json.dumps(content, indent=2)
                written.append(
                    self.write(
                        node_id,
                        name,
                        content,
                        kind=str(a.get("kind") or "text"),
                        attempt=attempt,
                        discarded=discarded,
                        run_id=run_id,
                    )
                )
            elif isinstance(a, str) and len(a) > 80:
                looks_src = "\n" in a or a.strip().startswith(("{", "<", "#", "use ", "fn ", "mod ", "pub "))
                if not looks_src:
                    continue
                name = f"artifact-{i}.txt"
                if "fn main" in a:
                    name = "src/main.rs"
                elif re.search(r"(?m)^\s*(pub )?(async )?fn |^use |^mod |^struct |^enum ", a):
                    name = f"src/frag{i}.rs"
                written.append(
                    self.write(
                        node_id,
                        name,
                        a,
                        attempt=attempt,
                        discarded=discarded,
                        run_id=run_id,
                    )
                )
        return written

    def manifest_for(self, run_id: str) -> list[dict[str, Any]]:
        return [r for r in self.index if r.get("run_id") == run_id and not r.get("discarded")]

    def harvest_product(self, dest: Path, run_id: str | None = None) -> dict[str, Any]:
        """Copy SuperGrok source artifacts into dest/ for rust_opt to compile.

        Last write for a given dest path wins. Discarded artifacts skipped.
        Path-contained. Generic suffixes (rs/py/ts/c/go/toml) — no domain templates.
        """
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
        dest_res = dest.resolve()
        src_dir = dest / "src"
        if src_dir.is_dir():
            shutil.rmtree(src_dir)
        cargo_path = dest / "Cargo.toml"
        if cargo_path.is_file():
            cargo_path.unlink()
        seen: dict[str, str] = {}
        skipped: list[str] = []
        rows = self.manifest_for(run_id) if run_id else [r for r in self.index if not r.get("discarded")]
        for rec in rows:
            name = str(rec.get("name") or "")
            src = Path(str(rec.get("abs_path") or ""))
            if not name or not src.is_file():
                continue
            mapped = dest_rel_for_name(name)
            if mapped is None:
                skipped.append(name)
                continue
            out = (dest / mapped).resolve()
            try:
                out.relative_to(dest_res)
            except ValueError:
                skipped.append(name)
                continue
            raw = src.read_bytes()
            if len(raw) > MAX_FILE_BYTES:
                raw = raw[:MAX_FILE_BYTES]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(raw)
            seen[mapped] = mapped
        files = list(seen.values())
        marker = dest / "HARVEST.md"
        marker.write_text(
            "# Harvested SuperGrok product sources\n\n"
            "These files came from live node artifacts. rust_opt must not replace them "
            "with a scaffold or a domain template.\n\n"
            + "\n".join(f"- `{f}`" for f in files)
            + ("\n" if files else "- (none)\n"),
            encoding="utf-8",
        )
        return {
            "product": str(dest),
            "files": files,
            "count": len(files),
            "skipped": skipped[:20],
        }

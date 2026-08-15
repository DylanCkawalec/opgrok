"""Append-only run journal for audit / resume."""
from __future__ import annotations

import hashlib
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any


class RunJournal:
    def __init__(self, harness_root: Path):
        self.run_id = f"run-{int(time.time())}-{uuid.uuid4().hex[:6]}"
        self.dir = harness_root / "runs"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"{self.run_id}.jsonl"
        self.seq = 0
        self.prev_hash = "0" * 64

    def event(self, kind: str, **payload: Any) -> None:
        self.seq += 1
        row = {
            "ts": time.time(),
            "run_id": self.run_id,
            "kind": kind,
            "seq": self.seq,
            **payload,
        }
        raw = json.dumps(row, separators=(",", ":"), sort_keys=True)
        digest = hashlib.sha256((self.prev_hash + raw).encode("utf-8")).hexdigest()
        line = json.dumps({**json.loads(raw), "prev": self.prev_hash, "hash": digest})
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
            f.flush()
            os.fsync(f.fileno())
        self.prev_hash = digest

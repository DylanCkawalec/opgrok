"""Append-only run journal for audit / resume."""
from __future__ import annotations

import json
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

    def event(self, kind: str, **payload: Any) -> None:
        row = {"ts": time.time(), "run_id": self.run_id, "kind": kind, **payload}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, default=str) + "\n")

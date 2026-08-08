"""Token / cost ledger for multi-node Grok API runs."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


class TokenLedger:
    def __init__(self, harness_root: Path):
        self.path = harness_root / "ledger.json"
        self.rows: list[dict[str, Any]] = []
        self.totals = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "calls": 0,
            "errors": 0,
        }

    def record(
        self,
        node_id: str,
        sg_name: str,
        model: str,
        usage: dict | None,
        error: str | None = None,
    ) -> None:
        row = {
            "ts": int(time.time()),
            "node_id": node_id,
            "sg_name": sg_name,
            "model": model,
            "usage": usage or {},
            "error": error,
        }
        self.rows.append(row)
        self.totals["calls"] += 1
        if error:
            self.totals["errors"] += 1
        if usage:
            for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
                try:
                    self.totals[k] += int(usage.get(k) or 0)
                except Exception:
                    pass

    def flush(self) -> dict[str, Any]:
        payload = {"totals": self.totals, "rows": self.rows}
        self.path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return payload

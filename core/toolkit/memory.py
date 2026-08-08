"""Persistent blackboard memory across harness runs."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, harness_root: Path, enabled: bool = True):
        self.enabled = enabled
        self.path = harness_root / "memory" / "blackboard.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = {"version": 1, "entries": {}, "updated_at": None}
        if enabled and self.path.is_file():
            try:
                self._data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                pass

    def load_into(self, blackboard: dict[str, Any]) -> None:
        if not self.enabled:
            return
        # only inject durable keys, not full prior node dumps unless marked sticky
        sticky = self._data.get("entries") or {}
        if sticky.get("goal_memory"):
            blackboard["memory.goal"] = sticky["goal_memory"]
        if sticky.get("facts"):
            blackboard["memory.facts"] = sticky["facts"]
        if sticky.get("last_result_summary"):
            blackboard["memory.last_result"] = sticky["last_result_summary"]

    def remember_from_run(self, goal: str, result: Any, node_results: list) -> None:
        if not self.enabled:
            return
        entries = self._data.setdefault("entries", {})
        entries["goal_memory"] = goal
        # harvest facts from node summaries
        facts = list(entries.get("facts") or [])
        for n in node_results:
            out = n.get("output") or {}
            parsed = out.get("parsed") if isinstance(out, dict) else None
            if isinstance(parsed, dict) and parsed.get("summary"):
                facts.append(
                    {
                        "sg": n.get("sg_name"),
                        "summary": str(parsed["summary"])[:500],
                    }
                )
        entries["facts"] = facts[-40:]  # thrift
        if isinstance(result, dict) and result.get("summary"):
            entries["last_result_summary"] = str(result["summary"])[:1000]
        elif result is not None:
            entries["last_result_summary"] = str(result)[:1000]
        self._data["updated_at"] = int(time.time())
        self.path.write_text(json.dumps(self._data, indent=2) + "\n", encoding="utf-8")

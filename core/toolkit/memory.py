"""Persistent blackboard memory across harness runs."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def goal_hash(goal: str) -> str:
    return hashlib.sha256((goal or "").encode("utf-8")).hexdigest()[:16]


class MemoryStore:
    def __init__(self, harness_root: Path, enabled: bool = True):
        self.enabled = enabled
        self.path = harness_root / "memory" / "blackboard.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.schema_warning = False
        self._data: dict[str, Any] = {"version": SCHEMA_VERSION, "entries": {}, "updated_at": None}
        if enabled and self.path.is_file():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                ver = loaded.get("version", SCHEMA_VERSION)
                if ver != SCHEMA_VERSION:
                    self.schema_warning = True
                    self._data = {
                        "version": SCHEMA_VERSION,
                        "entries": {},
                        "updated_at": None,
                    }
                else:
                    self._data = loaded
            except Exception:
                self.schema_warning = True
                self._data = {"version": SCHEMA_VERSION, "entries": {}, "updated_at": None}

    def load_into(self, blackboard: dict[str, Any], goal: str | None = None) -> None:
        if not self.enabled:
            return
        sticky = self._data.get("entries") or {}
        if goal is not None and sticky.get("goal_hash") and sticky.get("goal_hash") != goal_hash(goal):
            return
        if sticky.get("goal_memory"):
            blackboard["memory.goal"] = sticky["goal_memory"]
        if sticky.get("facts"):
            blackboard["memory.facts"] = sticky["facts"]
        if sticky.get("last_result_summary"):
            blackboard["memory.last_result"] = sticky["last_result_summary"]

    def remember_from_run(
        self,
        goal: str,
        result: Any,
        node_results: list,
        verdict: str = "PASS",
        run_id: str | None = None,
    ) -> None:
        if not self.enabled:
            return
        if verdict != "PASS":
            return
        entries = self._data.setdefault("entries", {})
        entries["goal_memory"] = goal
        entries["goal_hash"] = goal_hash(goal)
        entries["verdict"] = verdict
        entries["run_id"] = run_id
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
        entries["facts"] = facts[-40:]
        if isinstance(result, dict) and result.get("summary"):
            entries["last_result_summary"] = str(result["summary"])[:1000]
        elif result is not None:
            entries["last_result_summary"] = str(result)[:1000]
        self._data["version"] = SCHEMA_VERSION
        self._data["updated_at"] = int(time.time())
        self.path.write_text(json.dumps(self._data, indent=2) + "\n", encoding="utf-8")

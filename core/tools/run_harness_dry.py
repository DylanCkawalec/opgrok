#!/usr/bin/env python3
"""Backward-compatible dry-run wrapper → run_harness.py --dry-run """
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "core/tools"))
from run_harness import run_harness  # noqa: E402
import json  # noqa: E402


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: run_harness_dry.py <slug> [--goal ...]")
        return 2
    slug = sys.argv[1]
    goal = ""
    if "--goal" in sys.argv:
        i = sys.argv.index("--goal")
        if i + 1 < len(sys.argv):
            goal = sys.argv[i + 1]
    payload = run_harness(slug, goal=goal, dry_run=True)
    print(json.dumps(payload, indent=2))
    return 0 if payload.get("win") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

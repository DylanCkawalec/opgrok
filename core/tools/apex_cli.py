#!/usr/bin/env python3
"""Apex Binary CLI — detect mode, print how-to, dump closed-loop lessons.

Usage:
  python3 core/tools/apex_cli.py detect "<goal>"
  python3 core/tools/apex_cli.py howto
  python3 core/tools/apex_cli.py learn
  python3 core/tools/apex_cli.py route "<goal>" [--hire N]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "core"))

from toolkit.apex import (  # noqa: E402
    LESSONS,
    boost_categories,
    detect_mode,
    load_lessons,
    prefer_categories,
    similar_lessons,
)


HOWTO = """# How to use OPGROK

OPGROK is a CLI harness factory. Work from the clone root
(the directory that contains core/tools/craft_harness.py).

    python3 core/tools/craft_harness.py --slug <slug> --hire 8 "<GOAL>"
    python3 core/tools/run_harness.py <slug> --repo . --dry-run
    PYTHONUNBUFFERED=1 OPGROK_REQUIRE_LIVE=1 python3 -u \\
      core/tools/run_harness.py <slug> --repo .

craft does not call the API. A product binary exists only after a live
run harvests sources into product/ and cargo --require-cargo succeeds.

You are the foreman. SuperGroks write the product. Do not write
product/ or crate/src/ yourself. Empty product/ after live is FAIL.

Watch core/binaries/<slug>/STATUS while it runs. Producers default to
32768 tokens. Do not pass --max-tokens 8192.

Package law: one binary, one README, one WC, one graph. Hire 2-24.

See README.md and core/skills/opgrok/SKILL.md.
"""


def cmd_detect(goal: str) -> int:
    mode = detect_mode(goal)
    family = boost_categories(prefer_categories(goal, mode), goal)
    print(json.dumps({"goal": goal, "mode": mode, "family": family}, indent=2))
    return 0


def cmd_howto() -> int:
    sys.stdout.write(HOWTO)
    return 0


def cmd_learn() -> int:
    rows = load_lessons()
    print(json.dumps({"path": str(LESSONS), "count": len(rows), "recent": rows[-8:]}, indent=2))
    return 0


def cmd_route(goal: str, hire: int) -> int:
    # Local import: craft_harness pulls judge/toolkit at craft time.
    sys.path.insert(0, str(ROOT / "core/tools"))
    from craft_harness import route

    hired = route(goal, hire)
    mode = detect_mode(goal)
    print(f"mode: {mode}")
    for sk in hired:
        print(f"{sk.get('name','')}\t{sk.get('category','')}\t{sk.get('role','')}\t{sk.get('intent','')[:80]}")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help", "help"}:
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "detect":
        return cmd_detect(" ".join(argv[1:]).strip() or "help")
    if cmd == "howto":
        return cmd_howto()
    if cmd == "learn":
        return cmd_learn()
    if cmd == "route":
        hire = 8
        parts: list[str] = []
        i = 1
        while i < len(argv):
            if argv[i] == "--hire" and i + 1 < len(argv):
                hire = int(argv[i + 1])
                i += 2
            else:
                parts.append(argv[i])
                i += 1
        return cmd_route(" ".join(parts).strip(), hire)
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

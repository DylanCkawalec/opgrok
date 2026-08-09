#!/usr/bin/env python3
"""Craft an OPGROK harness package without cargo (Leslie WC + graph + README + crate).

Usage:
  python3 core/tools/craft_harness.py "build a landing page with hero and pricing"
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "core/skills/_framework/REGISTRY.json"
BIN_ROOT = ROOT / "core/binaries"


def slugify(goal: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", goal.lower()).strip("-")
    return (s[:48] or f"harness-{int(time.time())}")


def _best_in_category(skills: list[dict], cat: str, prefer_roles: list[str], tokens: tuple[str, ...] = ()) -> dict | None:
    cands = [s for s in skills if s.get("category") == cat and s.get("kind") in (None, "supergrok")]
    # rebuild marks kind=supergrok; generator-only rows may omit kind
    if not cands:
        cands = [
            s
            for s in skills
            if s.get("category") == cat
            and s.get("role") in {"smith", "forge", "scout", "trace", "audit", "seal"}
        ]
    if not cands:
        return None

    def relevance(s: dict) -> int:
        blob = f"{s.get('name','')} {s.get('intent','')} {s.get('purpose','')}".lower()
        return sum(1 for t in tokens if t in blob)

    # ponytail: role sets pipeline stage order; goal-token overlap picks within the stage
    # so different goals hire different SuperGroks instead of the same anchors.
    for role in prefer_roles:
        role_cands = [s for s in cands if s.get("role") == role or s.get("name", "").endswith(f"-{role}")]
        if role_cands:
            return max(role_cands, key=lambda s: (relevance(s), s.get("name", "")))
    return max(cands, key=lambda s: (relevance(s), s.get("name", "")))


# Pipeline stage → preferred role
STAGE_ROLE: dict[str, list[str]] = {
    "product": ["scout", "seal", "forge"],
    "plan": ["scout", "forge", "seal"],
    "code": ["forge", "smith", "trace"],
    "rust": ["forge", "smith", "trace"],
    "python": ["forge", "smith", "trace"],
    "web": ["forge", "smith", "audit"],
    "ui": ["smith", "forge", "audit"],
    "db": ["forge", "smith", "audit"],
    "data": ["forge", "smith", "audit"],
    "binary": ["forge", "smith", "seal"],
    "security": ["audit", "trace", "seal"],
    "review": ["audit", "trace", "seal"],
    "test": ["smith", "audit", "trace"],
    "debug": ["trace", "smith", "audit"],
    "docs": ["seal", "smith", "forge"],
    "devops": ["forge", "audit", "seal"],
    "agent": ["forge", "scout", "seal"],
    "mcp": ["forge", "audit", "smith"],
    "tool": ["forge", "trace", "smith"],
    "eval": ["audit", "seal", "scout"],
    "meta": ["audit", "seal", "forge"],
    "workflow": ["forge", "scout", "seal"],
    "math": ["smith", "trace", "seal"],
    "research": ["scout", "seal", "audit"],
    "vision": ["smith", "audit", "forge"],
}


def route(goal: str, limit: int = 8) -> list[dict]:
    reg = json.loads(REG.read_text())
    skills = reg["skills"]
    g = goal.lower()
    # Preferred categories by goal family (order = pipeline order)
    # Order matters: more specific families before broad keywords like "design"
    if any(k in g for k in ("cli", "command-line", "command line", "rust crate", "cargo")) or (
        "rust" in g and any(k in g for k in ("cli", "binary", "tool", "crate"))
    ):
        prefer = ["product", "plan", "rust", "binary", "code", "docs", "review", "test"]
    elif any(k in g for k in ("site", "web", "page", "landing", "frontend", "wireframe", "marketing")) or (
        "ui" in g.split() or " ux" in f" {g}"
    ):
        prefer = ["product", "plan", "web", "ui", "code", "review", "docs", "test"]
    elif any(k in g for k in ("api", "backend", "service", "server", "endpoint")):
        prefer = ["plan", "code", "web", "db", "security", "test", "review", "docs"]
    elif any(k in g for k in ("agent", "mesh", "harness", "orchestr", "opgrok", "supergrok")):
        prefer = ["agent", "plan", "eval", "mcp", "tool", "review", "binary", "meta"]
    elif any(k in g for k in ("architecture", "design doc", "adr", "spec ")):
        prefer = ["product", "plan", "docs", "review", "code", "eval"]
    else:
        prefer = ["plan", "agent", "code", "review", "test", "docs"]

    tokens = tuple(t for t in re.split(r"[^a-z0-9\-]+", g) if len(t) > 2)
    hired: list[dict] = []
    seen_cat: set[str] = set()
    for cat in prefer:
        if len(hired) >= limit:
            break
        roles = STAGE_ROLE.get(cat, ["forge", "smith", "scout", "audit", "seal", "trace"])
        sk = _best_in_category(skills, cat, roles, tokens)
        if sk and cat not in seen_cat:
            hired.append(sk)
            seen_cat.add(cat)

    # Keyword fill for remaining slots
    scored = []
    for sk in skills:
        if sk.get("category") in seen_cat:
            continue
        blob = " ".join(
            [sk.get("name", ""), sk.get("intent", ""), sk.get("purpose", "")]
        ).lower()
        score = sum(2 for t in tokens if t in blob)
        if score:
            scored.append((score, sk))
    scored.sort(key=lambda x: (-x[0], x[1]["name"]))
    for _, sk in scored:
        if len(hired) >= limit:
            break
        hired.append(sk)
        seen_cat.add(sk.get("category", ""))

    if len(hired) < 2:
        hired = skills[:2]
    return hired[:limit]


def craft(goal: str, hire_limit: int = 8) -> Path:
    slug = slugify(goal)
    hired = route(goal, hire_limit)
    root = BIN_ROOT / slug
    (root / "bin").mkdir(parents=True, exist_ok=True)
    (root / "crate" / "src").mkdir(parents=True, exist_ok=True)

    nodes = []
    edges = []
    for i, sk in enumerate(hired):
        nid = f"n{i+1:02d}"
        prev = "goal" if i == 0 else f"n{i:02d}.output"
        nodes.append(
            {
                "id": nid,
                "sg_name": sk["name"],
                "sg_id": sk.get("sg_id", ""),
                "binary_id": sk.get("binary_id", f"opgrok.sg.{sk['name']}"),
                "skill_path": sk.get("path", ""),
                "category": sk.get("category", ""),
                "role": sk.get("role", ""),
                "intent": sk.get("intent", ""),
                "purpose": sk.get("purpose", ""),
                "sink": i == len(hired) - 1,
                "ipo": {
                    "inputs": [prev, "goal"],
                    "process": f"Execute {sk['name']}: {sk.get('purpose','')}",
                    "outputs": [f"{nid}.output"],
                },
                "ooda": {
                    "observe": f"Read skill {sk.get('path','')}",
                    "orient": sk.get("intent", ""),
                    "decide": "Minimal actions per skill Win",
                    "act": f"Grok API for {sk.get('binary_id','')}",
                },
            }
        )
        if i > 0:
            edges.append({"from": f"n{i:02d}", "to": nid, "key": f"n{i:02d}.output"})

    # Model tiers (Grok-native multi-model routing hints)
    FAST = {"docs", "chat", "search", "extract", "polish", "product"}
    JUDGE = {"eval", "crit", "review"}
    for n in nodes:
        cat = n.get("category") or ""
        role = n.get("role") or ""
        if cat in JUDGE or role == "audit":
            n["model_tier"] = "judge"
        elif cat in FAST or role in {"scribe", "scout", "pulse", "lens", "glyph"}:
            n["model_tier"] = "fast"
        else:
            n["model_tier"] = "strong"

    graph = {
        "version": "1.1.0",
        "slug": slug,
        "goal": goal,
        "created_at": f"unix:{int(time.time())}",
        "leslie_wc_path": f"core/binaries/{slug}/WINNING_CONDITION.md",
        "toolkit": {
            "models": True,
            "memory": True,
            "artifacts": True,
            "repair": True,
            "parallel": True,
            "tools": True,
            "judge": True,
            "ledger": True,
            "journal": True,
            "vision": True,
        },
        "nodes": nodes,
        "edges": edges,
    }

    # Auto-append judge sink (Grok critique strength) unless disabled
    import os

    if os.environ.get("OPGROK_JUDGE", "1").strip().lower() not in {"0", "false", "no"}:
        try:
            sys.path.insert(0, str(ROOT / "core"))
            from toolkit.judge import ensure_judge_node

            reg_skills = json.loads(REG.read_text()).get("skills") or []
            graph = ensure_judge_node(graph, reg_skills)
        except Exception as e:  # noqa: BLE001
            print(f"judge append skipped: {e}")

    (root / "graph.json").write_text(json.dumps(graph, indent=2) + "\n")
    # refresh local nodes list for README after judge
    nodes = graph["nodes"]

    rows = "\n".join(
        f"| `{n['sg_name']}` | `{n['id']}` | {n['intent']} | {n['purpose']} |"
        for n in nodes
    )
    order = " → ".join(n["sg_name"] for n in nodes)
    (root / "README.md").write_text(
        f"""# opgrok-{slug}

## What this binary does

Harness for:

> {goal}

n8n-style SuperGrok graph. Each node uses Grok API with that SuperGrok's skill contract. Sink surfaces OPGROK_RESULT.

## Winning condition (Leslie)

See `WINNING_CONDITION.md`. PASS = **one binary** + **this README** + run observables.

## Hired SuperGroks

| name | node | intent | purpose |
|------|------|--------|---------|
{rows}

## Graph order

{order}

## Run

```bash
# Live (needs XAI_API_KEY)
./core/binaries/{slug}/bin/opgrok-{slug} --goal "{goal.replace('"', "'")}"

# Dry-run
./core/binaries/{slug}/bin/opgrok-{slug} --goal "..." --dry-run
# or
python3 core/tools/run_harness.py {slug} --dry-run

# Build / install
python3 core/tools/build_harness.py {slug} --install
```

## Files

- `graph.json` — agent DAG
- `WINNING_CONDITION.md` — Leslie seal
- `skills_cache/` — injected SuperGrok skill bodies
- `crate/` — Rust sources (cargo build --release)
- `bin/opgrok-{slug}` — runnable entrypoint
"""
    )

    wc_rows = "\n".join(
        f"| `{n['sg_name']}` | {n['intent']} | {n['purpose']} |" for n in nodes
    )
    (root / "WINNING_CONDITION.md").write_text(
        f"""# Winning Condition — opgrok-{slug}

**Leslie seal.** Governed by the master seal `docs/WINNING_CONDITION.md`
(module `HarnessRun`: invariants I1 NoVacuousPass, I2 DryHonesty, I3 SingleVerdict).

## Goal

{goal}

## Non-goals

- Delivering the full product without the harness graph
- Multiple binaries/READMEs for this slug
- Claiming PASS from a dry run, an error run, or a contract-violating run

## Hired SuperGroks

| name | intent | purpose |
|------|--------|---------|
{wc_rows}

## Graph invariants

- Order: {" → ".join(n["id"] for n in nodes)}
- Blackboard includes `goal`
- One sink (last node); last judge-category node is decisive for the verdict

## Falsifiable PASS

```bash
OPGROK_REQUIRE_LIVE=1 core/binaries/{slug}/bin/opgrok-{slug} --goal "..."
```

Seals PASS only when the receipt shows **all** of:

1. `dry_run=false`, `api_key_present=true` (a dry run seals `DRY` — package law only)
2. every node output parses to JSON with keys `summary`, `artifacts`, `win`; no `error`
3. `artifacts_written >= 1` with a non-empty file under `artifacts/` when any producer
   role (forge/smith/seal) was hired
4. decisive node `parsed.win="PASS"`, with a summary that analyzes the goal
5. `ledger.totals.total_tokens > 0` with completion bulk consistent with the artifacts
6. package law: one README, one `bin/opgrok-{slug}`, this WC, schema-valid `graph.json`,
   registry entry

Exit code: 0 for `PASS` or `DRY`, 1 for `FAIL`.

## Builder checklist

1. graph.json schema-valid
2. single README.md
3. crate + bin entrypoint
4. registry.json entry
5. live run receipt meeting gates 1–5 (dry receipt records `DRY`)
"""
    )

    reg_path = BIN_ROOT / "registry.json"
    reg = json.loads(reg_path.read_text()) if reg_path.exists() else {"harnesses": []}
    reg.setdefault("harnesses", [])
    reg["harnesses"] = [h for h in reg["harnesses"] if h.get("slug") != slug]
    reg["harnesses"].append(
        {
            "slug": slug,
            "goal": goal,
            "path": f"core/binaries/{slug}",
            "binary": f"core/binaries/{slug}/bin/opgrok-{slug}",
            "readme": f"core/binaries/{slug}/README.md",
            "hired": [h["name"] for h in hired],
            "updated_at": f"unix:{int(time.time())}",
        }
    )
    reg_path.write_text(json.dumps(reg, indent=2) + "\n")

    # Build binary package: skills_cache + full crate + entrypoint (+ cargo if present)
    import subprocess

    print(f"slug: {slug}")
    print(f"root: {root}")
    print(f"hired: {', '.join(h['name'] for h in hired)}")
    print("building harness package…")
    subprocess.check_call(
        [sys.executable, str(ROOT / "core/tools/build_harness.py"), slug],
        cwd=str(ROOT),
    )
    print("WIN: PASS — 1 README + binary entry + Leslie WC + skills_cache")
    return root


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: craft_harness.py "<goal>" [--hire N] [--install]')
        return 2
    args = sys.argv[1:]
    hire = 8
    install = False
    goal_parts = []
    i = 0
    while i < len(args):
        if args[i] == "--hire" and i + 1 < len(args):
            hire = int(args[i + 1])
            i += 2
        elif args[i] == "--install":
            install = True
            i += 1
        else:
            goal_parts.append(args[i])
            i += 1
    goal = " ".join(goal_parts).strip()
    if not goal:
        print("goal required")
        return 2
    root = craft(goal, hire_limit=hire)
    if install:
        import subprocess

        slug = root.name
        subprocess.check_call(
            [sys.executable, str(ROOT / "core/tools/build_harness.py"), slug, "--install"],
            cwd=str(ROOT),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

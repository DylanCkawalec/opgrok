"""Apex Binary control plane — mode, family routing, closed-loop lessons.

Absorbed patterns (see docs/APEX_BINARY_ARCHITECTURE.md):
- grok-workflows classify-and-route → detect_mode / prefer_categories
- grok-custom-skills evolution → lessons.jsonl
- grok-build-arsenal subagent-arena → wave_edges (scout then parallel crafts)
- grok-cli verify orchestrator → package_ok fail-closed checks
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "core/binaries/_apex/lessons.jsonl"

# Meta-mode: the goal is to improve OPGROK itself, not a user product.
_META_MARKERS = (
    "enhance opgrok",
    "improve opgrok",
    "opgrok itself",
    "opgrok core",
    "meta-mode",
    "apex binary",
    "closed loop",
    "super-integration",
    "routing logic",
    "skill catalog",
    "harness builder",
)


def _bounded(hay: str, needle: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", hay) is not None


def detect_mode(goal: str) -> str:
    """Pure function of the goal string (H6): craft | meta | run | inspect."""
    g = (goal or "").strip().lower()
    if not g:
        return "inspect"
    if g.startswith("run ") or _bounded(g, "run harness"):
        return "run"
    if g in {"help", "howto", "validate", "harnesses", "status"} or g.startswith(
        ("route ", "validate ", "howto ", "harnesses ", "status ")
    ):
        return "inspect"
    for m in _META_MARKERS:
        if _bounded(g, m):
            return "meta"
    # opgrok must be the object of change, not a product mention
    if re.search(r"\b(improve|enhance|fix|upgrade|evolve)\s+opgrok\b", g) or re.search(
        r"\bopgrok\s+(core|itself|routing)\b", g
    ):
        return "meta"
    return "craft"


def prefer_categories(goal: str, mode: str | None = None) -> list[str]:
    """Pipeline-ordered category families. Order is hire order."""
    mode = mode or detect_mode(goal)
    if mode == "meta":
        return ["meta", "agent", "binary", "plan", "eval", "tool", "review", "docs"]

    g = goal.lower()
    if any(
        k in g
        for k in (
            "quantum",
            "qubit",
            "dirac",
            "hilbert",
            "pauli",
            "schrodinger",
            "schrödinger",
            "qft",
            "grover",
            "shor",
        )
    ):
        return ["math", "plan", "rust", "binary", "code", "eval", "review", "docs"]
    if any(
        k in g
        for k in (
            "calculator",
            "numerics",
            "simulator",
            "compiler",
            "interpreter",
            "compute engine",
        )
    ):
        return ["math", "plan", "rust", "binary", "code", "eval", "review", "docs"]
    if any(k in g for k in ("cli", "command-line", "command line", "rust crate", "cargo")) or (
        "rust" in g and any(k in g for k in ("cli", "binary", "tool", "crate"))
    ):
        return ["product", "plan", "rust", "binary", "code", "docs", "review", "test"]
    if any(k in g for k in ("site", "web", "page", "landing", "frontend", "wireframe", "marketing")) or (
        "ui" in g.split() or " ux" in f" {g}"
    ):
        return ["product", "plan", "web", "ui", "code", "review", "docs", "test"]
    if any(k in g for k in ("api", "backend", "service", "server", "endpoint")):
        return ["plan", "code", "web", "db", "security", "test", "review", "docs"]
    if any(k in g for k in ("agent", "mesh", "harness", "orchestr", "opgrok", "supergrok")):
        return ["agent", "plan", "eval", "mcp", "tool", "review", "binary", "meta"]
    if any(k in g for k in ("architecture", "design doc", "adr", "spec ")):
        return ["product", "plan", "docs", "review", "code", "eval"]
    if any(k in g for k in ("security", "audit", "cve", "owasp")):
        return ["security", "review", "code", "test", "plan", "docs"]
    if any(k in g for k in ("workflow", "dag", "pipeline", "orchestrat")):
        return ["workflow", "plan", "agent", "eval", "review", "docs"]
    return ["plan", "agent", "code", "review", "test", "docs"]


_STOPWORDS = frozenset(
    {
        "the",
        "a",
        "an",
        "for",
        "with",
        "and",
        "or",
        "of",
        "to",
        "in",
        "is",
        "on",
        "at",
        "by",
        "this",
        "that",
    }
)


def tokens(text: str) -> tuple[str, ...]:
    """Word-boundary tokens; stopwords excluded (I7 token hygiene)."""
    return tuple(
        t
        for t in re.split(r"[^a-z0-9\-]+", (text or "").lower())
        if len(t) > 2 and t not in _STOPWORDS
    )


def load_lessons(path: Path | None = None) -> list[dict]:
    p = path or LESSONS
    if not p.is_file():
        return []
    out: list[dict] = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def similar_lessons(goal: str, stored: Iterable[dict], limit: int = 5) -> list[dict]:
    goal_toks = set(tokens(goal))
    if not goal_toks:
        return []
    scored: list[tuple[int, dict]] = []
    for row in stored:
        blob = set(tokens(str(row.get("goal", ""))))
        overlap = len(goal_toks & blob)
        if overlap:
            scored.append((overlap, row))
    scored.sort(key=lambda x: (-x[0], str(x[1].get("slug", ""))))
    return [r for _, r in scored[:limit]]


def boost_categories(prefer: list[str], goal: str, stored: Iterable[dict] | None = None) -> list[str]:
    """Closed loop: categories that worked on similar goals rise in the family."""
    lessons = similar_lessons(goal, stored if stored is not None else load_lessons())
    extra: list[str] = []
    seen = set(prefer)
    for row in lessons:
        if row.get("outcome", "pass") != "pass":
            continue
        for cat in row.get("categories") or []:
            if isinstance(cat, str) and cat and cat not in seen:
                extra.append(cat)
                seen.add(cat)
    if not extra:
        return prefer
    # Insert lesson cats after the first planning slot so they staff the middle.
    head = prefer[:1]
    rest = prefer[1:]
    return head + extra + rest


def record_lesson(
    goal: str,
    slug: str,
    hired: list[dict] | list[str],
    mode: str,
    *,
    outcome: str = "pass",
    path: Path | None = None,
) -> Path:
    p = path or LESSONS
    p.parent.mkdir(parents=True, exist_ok=True)
    names: list[str] = []
    cats: list[str] = []
    for h in hired:
        if isinstance(h, dict):
            names.append(str(h.get("name", "")))
            cat = str(h.get("category", "") or "")
            if cat and cat not in cats:
                cats.append(cat)
        else:
            names.append(str(h))
    row = {
        "goal": goal,
        "slug": slug,
        "mode": mode,
        "hired": [n for n in names if n],
        "categories": cats,
        "outcome": outcome,
    }
    with p.open("a") as fh:
        fh.write(json.dumps(row, separators=(",", ":")) + "\n")
    return p


def package_ok(root: Path) -> dict:
    """Fail-closed package-law check: artifacts present AND validate_graph."""
    from .validate import validate_graph

    slug = root.name
    binary = root / "bin" / f"opgrok-{slug}"
    required = {
        "readme": root / "README.md",
        "wc": root / "WINNING_CONDITION.md",
        "graph": root / "graph.json",
        "binary": binary,
    }
    missing = [k for k, path in required.items() if not path.exists()]
    graph_nodes = 0
    errors: list[str] = []
    warnings: list[str] = []
    graph = None
    if required["graph"].is_file():
        try:
            graph = json.loads(required["graph"].read_text())
            graph_nodes = len(graph.get("nodes") or [])
        except json.JSONDecodeError:
            missing.append("graph_parse")
    if graph is not None:
        reg_path = root.parent / "registry.json"
        registry = None
        if reg_path.is_file():
            try:
                registry = json.loads(reg_path.read_text())
            except json.JSONDecodeError:
                errors.append("registry_parse")
        vr = validate_graph(graph, registry, repo_root=ROOT)
        errors.extend(vr.errors)
        warnings.extend(vr.warnings)
    win = not missing and graph_nodes >= 2 and not errors
    return {
        "ok": win,
        "slug": slug,
        "missing": missing,
        "errors": errors,
        "warnings": warnings,
        "nodes": graph_nodes,
        "paths": {k: str(v) for k, v in required.items()},
    }


def wave_edges(node_ids: list[str], fan: int = 2) -> list[dict]:
    """Scout → k parallel crafts → join → serial seal. Linear when N<4."""
    n = len(node_ids)
    if n < 2:
        return []
    if n < 4:
        return [
            {"from": node_ids[i], "to": node_ids[i + 1], "key": f"{node_ids[i]}.output"}
            for i in range(n - 1)
        ]
    k = max(1, min(int(fan), n - 2))
    edges: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(frm: str, to: str) -> None:
        pair = (frm, to)
        if pair in seen:
            return
        seen.add(pair)
        edges.append({"from": frm, "to": to, "key": f"{frm}.output"})

    scout = node_ids[0]
    crafts = node_ids[1 : 1 + k]
    join = node_ids[1 + k]
    rest = node_ids[2 + k :]
    for c in crafts:
        add(scout, c)
        add(c, join)
    prev = join
    for nxt in rest:
        add(prev, nxt)
        prev = nxt
    return edges


def prior_input(node_ids: list[str], index: int) -> str:
    """Primary blackboard key a node should read, matching wave_edges."""
    keys = incoming_keys(node_ids, index)
    return keys[0] if keys else "goal"


def incoming_keys(node_ids: list[str], index: int) -> list[str]:
    """All in-edge keys for node_ids[index] (plus empty → caller adds goal)."""
    if index <= 0 or index >= len(node_ids):
        return []
    nid = node_ids[index]
    return [e["key"] for e in wave_edges(node_ids) if e.get("to") == nid]

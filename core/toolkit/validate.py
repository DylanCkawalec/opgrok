"""Graph schema validator — I7 + H1–H12 (v1.0.0 package-law seal).

H6 (detect_mode purity) is a static property of apex.detect_mode (goal string only).
H5 (slug injectivity) is enforced at craft time, not here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STANDARD_ROLES = frozenset({"forge", "smith", "scout", "seal", "trace", "audit"})
JUDGE_CATS = frozenset({"eval", "crit", "review"})
TIERS = frozenset({"fast", "strong", "judge"})
SEED_KEYS = frozenset({"goal", "vision_refs"})


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _name(node: dict) -> str:
    return str(node.get("name") or node.get("sg_name") or "")


def _is_judge(node: dict) -> bool:
    if node.get("judge"):
        return True
    return (node.get("category") or "").lower() in JUDGE_CATS


def _reach_self(ids: list[str], edges: list[dict]) -> bool:
    succ: dict[str, set[str]] = {i: set() for i in ids}
    for e in edges:
        frm, to = e.get("from"), e.get("to")
        if frm in succ and to in succ:
            succ[frm].add(to)
    for start in ids:
        seen: set[str] = set()
        stack = list(succ.get(start, ()))
        while stack:
            cur = stack.pop()
            if cur == start:
                return True
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(succ.get(cur, ()))
    return False


def validate_graph(
    graph: dict[str, Any],
    registry: dict[str, Any] | None = None,
    repo_root: Path | None = None,
) -> ValidationResult:
    """Return named errors for I7 / H1–H12 violations."""
    errors: list[str] = []
    warnings: list[str] = []
    repo = repo_root or ROOT
    nodes = list(graph.get("nodes") or [])
    edges = list(graph.get("edges") or [])
    ids = [n.get("id") for n in nodes]

    if not nodes or len(nodes) < 2 or len(nodes) > 25:
        errors.append("nodes: need 2..25 nodes")

    for n in nodes:
        nid = n.get("id")
        missing = []
        if not n.get("sg_id"):
            missing.append("sg_id")
        if not n.get("binary_id"):
            missing.append("binary_id")
        if not n.get("skill_path"):
            missing.append("skill_path")
        if not n.get("category"):
            missing.append("category")
        if not n.get("role"):
            missing.append("role")
        if not _name(n):
            missing.append("name")
        if missing:
            errors.append(f"anonymous: {nid} missing {','.join(missing)}")
        sp = n.get("skill_path") or ""
        if sp:
            p = (repo / sp).resolve()
            try:
                p.relative_to(repo.resolve())
                if not p.is_file():
                    errors.append(f"skill_path: {nid} {sp} not found")
            except ValueError:
                errors.append(f"skill_path: {nid} escapes repo")
        kind = n.get("kind")
        role = (n.get("role") or "").lower()
        if not _is_judge(n):
            if kind is not None and kind != "supergrok":
                errors.append(f"kind: {nid} must be supergrok")
            if role and role not in STANDARD_ROLES:
                errors.append(f"role: {nid} {role} not in standard roles")
        tier = n.get("model_tier")
        if tier is not None and tier not in TIERS:
            errors.append(f"model_tier: {nid} {tier}")
        if nid in SEED_KEYS or (isinstance(nid, str) and nid.startswith("memory.")):
            errors.append(f"reserved_key: {nid}")

    sinks = [n for n in nodes if n.get("sink")]
    if len(sinks) != 1:
        errors.append("sink: need exactly one sink:true")
    elif nodes and sinks[0] is not nodes[-1]:
        errors.append("sink: sink must be the last node")
    elif nodes and not _is_judge(nodes[-1]):
        errors.append("sink: last node must be a judge")

    judges = [n for n in nodes if _is_judge(n)]
    if nodes and nodes[-1] not in judges:
        errors.append("sink: Sink must be in Judges (I7)")

    if nodes and _reach_self([i for i in ids if isinstance(i, str)], edges):
        errors.append("cycle: Precede is cyclic")

    idset = {i for i in ids if isinstance(i, str)}
    for e in edges:
        frm, to, key = e.get("from"), e.get("to"), e.get("key")
        if frm not in idset:
            errors.append(f"edge_source: {frm}")
        if to not in idset:
            errors.append(f"edge_target: {to}")
        if frm in idset and key != f"{frm}.output":
            errors.append(f"edge_key: {frm}->{to} key must be {frm}.output")

    incoming: dict[str, set[str]] = {i: set() for i in idset}
    for e in edges:
        to, key = e.get("to"), e.get("key")
        if to in incoming and isinstance(key, str):
            incoming[to].add(key)
    for n in nodes:
        nid = n.get("id")
        if nid not in incoming:
            continue
        declared = set((n.get("ipo") or {}).get("inputs") or [])
        extra = incoming[nid] - declared
        if extra:
            errors.append(f"ipo_inputs: {nid} missing in-edge keys {sorted(extra)}")

    apex = graph.get("apex") or {}
    family = apex.get("family")
    if family is None:
        warnings.append("apex: family missing (H7)")
    elif not isinstance(family, list) or not family:
        errors.append("apex: family must be a non-empty list (H7)")

    if registry is not None:
        slug = graph.get("slug")
        entries = (registry.get("harnesses") or []) if isinstance(registry, dict) else []
        hit = next((h for h in entries if h.get("slug") == slug), None)
        if not hit:
            warnings.append("registry: no entry for slug")
        else:
            names = {_name(n) for n in nodes}
            hired = set(hit.get("hired") or [])
            extra = hired - names
            if extra:
                errors.append(f"registry: hired not subset of nodes {sorted(extra)}")

    return ValidationResult(ok=not errors, errors=errors, warnings=warnings)

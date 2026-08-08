"""Judge sink — final SuperGrok eval/crit node for harness quality."""
from __future__ import annotations

from typing import Any


JUDGE_CATS = {"eval", "crit", "review"}


def is_judge_category(cat: str) -> bool:
    return (cat or "").lower() in JUDGE_CATS


def ensure_judge_node(graph: dict[str, Any], registry_skills: list[dict] | None = None) -> dict[str, Any]:
    """Append a judge sink if missing. Mutates and returns graph."""
    nodes = graph.setdefault("nodes", [])
    edges = graph.setdefault("edges", [])
    if any(n.get("judge") or is_judge_category(n.get("category", "")) for n in nodes):
        # ensure last is sink
        for n in nodes:
            n["sink"] = False
        nodes[-1]["sink"] = True
        return graph

    # pick review-audit or eval-prism from registry if available
    pick = None
    if registry_skills:
        for prefer in ("review-audit", "eval-prism", "crit-mirror", "review-seal"):
            for sk in registry_skills:
                if sk.get("name") == prefer:
                    pick = sk
                    break
            if pick:
                break
        if not pick:
            for sk in registry_skills:
                if sk.get("category") in JUDGE_CATS:
                    pick = sk
                    break

    if pick:
        sg_name = pick["name"]
        sg_id = pick.get("sg_id", "")
        binary_id = pick.get("binary_id", f"opgrok.sg.{sg_name}")
        skill_path = pick.get("path", "")
        category = pick.get("category", "review")
        role = pick.get("role", "audit")
        intent = pick.get("intent", "Judge harness outputs")
        purpose = pick.get("purpose", "Evaluate completeness against the goal")
    else:
        sg_name = "review-audit"
        sg_id = "sg-judge"
        binary_id = "opgrok.sg.review-audit"
        skill_path = "core/skills/review/audit/SKILL.md"
        category = "review"
        role = "audit"
        intent = "Judge harness outputs against the goal"
        purpose = "Score completeness, correctness, and flag gaps"

    # clear prior sinks
    for n in nodes:
        n["sink"] = False
    prev_id = nodes[-1]["id"] if nodes else "n00"
    # next id
    n = len(nodes) + 1
    nid = f"n{n:02d}"
    nodes.append(
        {
            "id": nid,
            "sg_name": sg_name,
            "sg_id": sg_id,
            "binary_id": binary_id,
            "skill_path": skill_path,
            "category": category,
            "role": role,
            "intent": intent,
            "purpose": purpose,
            "sink": True,
            "judge": True,
            "model_tier": "judge",
            "ipo": {
                "inputs": [f"{prev_id}.output", "goal"],
                "process": "Judge all prior outputs against the goal; emit win PASS/FAIL + gaps",
                "outputs": [f"{nid}.output"],
            },
            "ooda": {
                "observe": "Read full thrift blackboard",
                "orient": "Map to acceptance criteria",
                "decide": "Score and list gaps",
                "act": "Return JSON win + summary + gaps",
            },
        }
    )
    if nodes and len(nodes) > 1:
        edges.append({"from": prev_id, "to": nid, "key": f"{prev_id}.output"})
    return graph

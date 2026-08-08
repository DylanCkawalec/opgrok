"""Multi-model routing — Grok strong vs fast vs judge."""
from __future__ import annotations

from enum import Enum
from typing import Any


class ModelTier(str, Enum):
    FAST = "fast"
    STRONG = "strong"
    JUDGE = "judge"


# Categories that usually need deep reasoning
STRONG_CATS = {
    "code",
    "rust",
    "python",
    "security",
    "math",
    "systems",
    "ml",
    "agent",
    "plan",
    "debug",
    "binary",
    "web",
    "ui",
}
# Cheap / thrift nodes
FAST_CATS = {
    "docs",
    "scribe",  # role fallback via name
    "chat",
    "search",
    "extract",
    "polish",
    "product",
}
JUDGE_CATS = {"eval", "crit", "review", "security"}
STRONG_ROLES = {"anvil", "crux", "forge", "radix", "vertex", "aegis", "guard"}
FAST_ROLES = {"scribe", "scout", "pulse", "lens", "glyph"}


def pick_model(node: dict[str, Any], flags: dict[str, Any]) -> tuple[str, ModelTier]:
    """Return (model_id, tier) for a SuperGrok node."""
    cat = (node.get("category") or "").lower()
    role = (node.get("role") or "").lower()
    name = (node.get("sg_name") or node.get("name") or "").lower()

    # Explicit node override
    if node.get("model"):
        return str(node["model"]), ModelTier.STRONG
    if node.get("model_tier") == "fast":
        return flags["model_fast"], ModelTier.FAST
    if node.get("model_tier") == "judge":
        return flags["model_judge"], ModelTier.JUDGE

    if cat in JUDGE_CATS or node.get("judge") or name.endswith("-audit"):
        return flags["model_judge"], ModelTier.JUDGE
    if cat in FAST_CATS or role in FAST_ROLES:
        return flags["model_fast"], ModelTier.FAST
    if cat in STRONG_CATS or role in STRONG_ROLES:
        return flags["model"], ModelTier.STRONG
    # default strong for unknown
    return flags["model"], ModelTier.STRONG

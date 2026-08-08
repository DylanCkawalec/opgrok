"""Content-addressable agent identity index for the OpGrok multi-agent runtime.

Loads `core/registry/named-hashes.json` once and exposes O(1) resolve by:
  - short token  (Name-HashPrefix12)
  - full token   (Name-FullHash64)
  - full hash
  - human name
  - skill path

See core/registry/ARCHITECTURE.md.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "core" / "registry" / "named-hashes.json"

TOKEN_RE = re.compile(
    r"^([A-Za-z][A-Za-z'-]*)-([0-9a-fA-F]{12,64})$"
)


@dataclass(frozen=True)
class AgentRef:
    name: str
    full_hash: str
    short_token: str
    full_token: str
    path: str
    timestamp: str = ""

    @property
    def skill_path(self) -> Path:
        return ROOT / self.path

    def load_skill_markdown(self) -> str:
        return self.skill_path.read_text(encoding="utf-8")


class IdentityIndex:
    """In-memory O(1) name ↔ hash ↔ path map."""

    def __init__(self, payload: dict, registry_path: Path | None = None):
        self.registry_path = registry_path or DEFAULT_REGISTRY
        self.version = payload.get("version", "")
        self.algorithm = payload.get("algorithm", "")
        self.updated_at = payload.get("updated_at", "")
        self.count = int(payload.get("count") or 0)
        self._by_short: dict[str, AgentRef] = {}
        self._by_full: dict[str, AgentRef] = {}
        self._by_hash: dict[str, AgentRef] = {}
        self._by_name: dict[str, AgentRef] = {}
        self._by_path: dict[str, AgentRef] = {}
        self._by_name_ci: dict[str, AgentRef] = {}

        for e in payload.get("agents") or []:
            ref = AgentRef(
                name=e["name"],
                full_hash=e["full_hash"].lower(),
                short_token=e["short_token"],
                full_token=e.get("full_token") or f"{e['name']}-{e['full_hash']}",
                path=e["path"],
                timestamp=e.get("timestamp", ""),
            )
            self._by_short[ref.short_token] = ref
            self._by_full[ref.full_token] = ref
            self._by_hash[ref.full_hash] = ref
            self._by_name[ref.name] = ref
            self._by_name_ci[ref.name.lower()] = ref
            self._by_path[ref.path] = ref
            # also index path without leading core/skills variants
            self._by_path[ref.path.lstrip("./")] = ref

    @classmethod
    def load(cls, registry_path: Path | str | None = None) -> "IdentityIndex":
        path = Path(registry_path) if registry_path else DEFAULT_REGISTRY
        if not path.is_file():
            raise FileNotFoundError(
                f"Identity registry missing: {path}. "
                "Run: python3 core/tools/assign_agent_identities.py"
            )
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(payload, registry_path=path)

    def resolve(self, token: str) -> AgentRef | None:
        """Resolve short token, full token, bare name, or raw hash."""
        if not token:
            return None
        t = token.strip()
        # strip optional backticks or surrounding quotes
        t = t.strip("`\"'")
        if t in self._by_short:
            return self._by_short[t]
        if t in self._by_full:
            return self._by_full[t]
        if re.fullmatch(r"[0-9a-fA-F]{64}", t):
            return self._by_hash.get(t.lower())
        if re.fullmatch(r"[0-9a-fA-F]{12}", t):
            # ambiguous hash prefix — match unique short suffix
            matches = [r for r in self._by_short.values() if r.full_hash.startswith(t.lower())]
            return matches[0] if len(matches) == 1 else None
        m = TOKEN_RE.match(t)
        if m:
            name, hx = m.group(1), m.group(2).lower()
            if len(hx) == 64:
                ref = self._by_full.get(f"{name}-{hx}")
                if ref:
                    return ref
                # name mismatch tolerance: resolve by hash only
                return self._by_hash.get(hx)
            # short form
            ref = self._by_short.get(f"{name}-{hx[:12]}")
            if ref:
                return ref
            # try name alone if hash prefix unique under that name
            by_name = self._by_name_ci.get(name.lower())
            if by_name and by_name.full_hash.startswith(hx):
                return by_name
        return self._by_name_ci.get(t.lower()) or self._by_name.get(t)

    def resolve_hash(self, full_hash: str) -> AgentRef | None:
        return self._by_hash.get(full_hash.lower())

    def resolve_name(self, name: str) -> AgentRef | None:
        return self._by_name_ci.get(name.lower())

    def resolve_path(self, path: str | Path) -> AgentRef | None:
        p = str(path).replace("\\", "/")
        if p in self._by_path:
            return self._by_path[p]
        # relativize if absolute under ROOT
        try:
            rel = Path(p).resolve().relative_to(ROOT).as_posix()
            return self._by_path.get(rel)
        except Exception:
            return None

    def self_token(self, current_path: str | Path, short: bool = True) -> str | None:
        ref = self.resolve_path(current_path)
        if not ref:
            return None
        return ref.short_token if short else ref.full_token

    def peers(self, short: bool = True) -> list[str]:
        refs = sorted(self._by_short.values(), key=lambda r: r.name.lower())
        return [r.short_token if short else r.full_token for r in refs]

    def path_for(self, token: str) -> str | None:
        ref = self.resolve(token)
        return ref.path if ref else None

    def all_refs(self) -> Iterable[AgentRef]:
        return sorted(self._by_short.values(), key=lambda r: r.name.lower())

    def prompt_addon(self, max_peers: int = 0) -> str:
        """Tiny context snippet: self-resolution instructions + optional peer sample."""
        lines = [
            "Agent identity protocol: peers are addressed as Name-HashPrefix (12 hex).",
            f"Registry: {self.registry_path.relative_to(ROOT)} ({self.count} agents).",
            "Resolve tokens via IdentityIndex; do not invent names or hashes.",
        ]
        if max_peers > 0:
            sample = self.peers()[:max_peers]
            lines.append("Sample peers: " + ", ".join(sample))
        return "\n".join(lines)


@lru_cache(maxsize=1)
def default_index() -> IdentityIndex:
    return IdentityIndex.load()


def resolve(token: str) -> AgentRef | None:
    return default_index().resolve(token)

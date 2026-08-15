"""General product harvest + compile. Domain-agnostic.

Live SuperGroks write source as artifacts. This module:
  - maps artifact names onto a path-contained product/ tree
  - cargo-builds when Rust sources exist (via build_harness / rust_opt)
  - prepares one compile-repair prompt so rustc errors can go back to a forge

Does not author product code. Does not embed domain templates.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

MAX_FILE_BYTES = 512_000
SOURCE_SUFFIXES = frozenset(
    {".rs", ".toml", ".py", ".ts", ".js", ".c", ".h", ".hpp", ".cc", ".go"}
)
PRODUCER_ROLES = frozenset({"forge", "smith", "seal"})
REPAIR_PREFER = (
    "rust-forge",
    "binary-forge",
    "code-forge",
    "rust-smith",
    "code-smith",
    "python-forge",
)


def crate_ident(slug: str) -> str:
    """Cargo package/bin name: [a-zA-Z][a-zA-Z0-9_-]*. Dots in slugs become hyphens."""
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", slug or "").strip("-").lower()
    if not s:
        s = "bin"
    if s[0].isdigit():
        s = f"p-{s}"
    return f"opgrok-{s}"


def dest_rel_for_name(name: str) -> str | None:
    """Map an artifact name to a product/-relative path, or None if not source.

    Rejects `..` and absolute paths. Cargo.toml stays at product root.
    Other sources land under product/src/ (preserving src/ subdirs).
    """
    if not name or not isinstance(name, str):
        return None
    rel = name.replace("\\", "/").lstrip("/")
    if not rel or rel.startswith("/") or ":" in rel.split("/")[0]:
        return None
    parts = [p for p in rel.split("/") if p and p != "."]
    if not parts or ".." in parts:
        return None
    rel = "/".join(parts)
    low = rel.lower()
    if low.endswith("cargo.toml") and Path(low).name == "cargo.toml":
        return "Cargo.toml"
    suffix = Path(low).suffix
    if suffix not in SOURCE_SUFFIXES:
        return None
    if suffix == ".toml" and Path(low).name != "cargo.toml":
        return None
    if low.startswith("src/"):
        rest = rel[4:]
        if not rest or ".." in rest.split("/"):
            return None
        return "src/" + rest
    if "/src/" in f"/{low}":
        idx = low.find("src/")
        rest = rel[idx + 4 :]
        if not rest or ".." in rest.split("/"):
            return None
        return "src/" + rest
    return "src/" + Path(rel).name


def safe_dest_path(dest_root: Path, rel: str) -> Path | None:
    """Resolve dest_root/rel and require it stay inside dest_root."""
    mapped = dest_rel_for_name(rel)
    if mapped is None:
        return None
    dest_root = dest_root.resolve()
    out = (dest_root / mapped).resolve()
    try:
        out.relative_to(dest_root)
    except ValueError:
        return None
    return out


def extract_json_object(text: str) -> str | None:
    """Brace-match the first JSON object, ignoring braces inside strings."""
    if not text:
        return None
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i, ch in enumerate(text[start:], start):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def node_max_tokens(node: dict[str, Any] | None, flags: dict[str, Any]) -> int:
    """Producers get a higher completion budget so they can emit full files."""
    base = int(flags.get("max_tokens") or 4096)
    prod = int(flags.get("max_tokens_producer") or 8192)
    node = node or {}
    role = str(node.get("role") or "")
    cat = str(node.get("category") or "")
    name = str(node.get("sg_name") or "")
    if role in PRODUCER_ROLES or cat in {"rust", "code", "binary", "python"}:
        return max(base, prod)
    if any(name.endswith(s) for s in ("-forge", "-smith", "-seal")):
        return max(base, prod)
    return base


def has_rust_sources(harvest: dict[str, Any] | None) -> bool:
    files = (harvest or {}).get("files") or []
    return any(str(f).endswith(".rs") for f in files)


def pick_repair_node(nodes: list[dict[str, Any]]) -> dict[str, Any] | None:
    by_name = {n.get("sg_name"): n for n in nodes}
    for name in REPAIR_PREFER:
        if name in by_name:
            return by_name[name]
    for n in reversed(nodes):
        if n.get("role") in {"forge", "smith"}:
            return n
    return None


def product_source_dump(product_dir: str | Path, files: list[str], cap_each: int = 8000, cap_total: int = 28000) -> str:
    """Inline harvested sources so compile-repair can fix them without tools."""
    root = Path(product_dir)
    chunks: list[str] = []
    total = 0
    for f in files:
        p = root / f
        if not p.is_file():
            continue
        body = p.read_text(encoding="utf-8", errors="ignore")[:cap_each]
        chunk = f"----- {f} -----\n{body}\n"
        if total + len(chunk) > cap_total:
            break
        chunks.append(chunk)
        total += len(chunk)
    return "\n".join(chunks) if chunks else "(no file bodies readable)"


def compile_repair_user(goal: str, cargo_err: str, files: list[str], product_dir: str) -> str:
    listing = "\n".join(f"- {f}" for f in files) or "- (none harvested)"
    err = (cargo_err or "")[-2500:]
    bodies = product_source_dump(product_dir, files)
    return f"""COMPILE REPAIR. cargo failed on harvested SuperGrok sources.

GOAL:
{goal}

PRODUCT DIR: {product_dir}
PRODUCT FILES:
{listing}

CURRENT SOURCES:
{bodies}

CARGO/RUSTC ERROR (tail):
{err}

Return a single JSON object with keys summary, artifacts, win.
artifacts MUST be the FULL corrected files, not a patch description:
  {{"name":"src/main.rs","content":"<entire file>","kind":"rust"}}
  plus any other src/*.rs or Cargo.toml that must change.
win=PASS only if you believe the crate now compiles. Do not describe the fix without writing the files.
"""


def _last_json_line(text: str) -> dict[str, Any] | None:
    for line in reversed((text or "").splitlines()):
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                v = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(v, dict):
                return v
    return None


def compile_product(repo: Path, slug: str) -> dict[str, Any]:
    """Cargo-release only. A Python-runner fallback is a FAIL, not a product."""
    runner = Path(repo) / "core/tools/build_harness.py"
    r = subprocess.run(
        [sys.executable, str(runner), slug, "--require-cargo"],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    meta = _last_json_line(r.stdout or "") or {}
    method = str(meta.get("method") or "")
    ok = r.returncode == 0 and method == "cargo-release"
    return {
        "rc": r.returncode,
        "ok": ok,
        "method": method or ("cargo-release" if ok else "cargo-required-fail"),
        "binary": meta.get("binary"),
        "stdout_tail": (r.stdout or "")[-2000:],
        "stderr_tail": (r.stderr or "")[-2000:],
    }

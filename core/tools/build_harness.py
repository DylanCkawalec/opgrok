#!/usr/bin/env python3
"""Build + install an OPGROK harness binary.

Steps:
1. Ensure skills_cache/ filled from graph
2. Prefer cargo build --release of core/binaries/<slug>/crate
3. Else package Python live runner as bin/opgrok-<slug>
4. Optional: install to ~/.opgrok/bin

Usage:
  python3 core/tools/build_harness.py <slug> [--install] [--force-python] [--require-cargo]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def cache_skills(slug: str) -> int:
    root = ROOT / "core/binaries" / slug
    graph = json.loads((root / "graph.json").read_text())
    cache = root / "skills_cache"
    cache.mkdir(parents=True, exist_ok=True)
    n = 0
    for node in graph.get("nodes") or []:
        sp = node.get("skill_path") or ""
        name = node.get("sg_name") or "unknown"
        src = ROOT / sp
        dst = cache / f"{name}.md"
        if src.is_file():
            text = src.read_text(encoding="utf-8", errors="ignore")
            # thrift store
            if len(text) > 8000:
                keep = []
                for sec in ("## Intent", "## Purpose", "## Call", "## Win", "## Do"):
                    if sec in text:
                        i = text.find(sec)
                        j = text.find("\n## ", i + 4)
                        keep.append(text[i : (j if j > 0 else i + 1500)])
                text = "\n\n".join(keep) if keep else text[:8000]
            dst.write_text(text, encoding="utf-8")
            n += 1
        elif not dst.is_file():
            dst.write_text(
                f"# {name}\n\nIntent: {node.get('intent')}\n\nPurpose: {node.get('purpose')}\n",
                encoding="utf-8",
            )
            n += 1
    return n


def write_python_bin(slug: str) -> Path:
    """Ship a portable entrypoint that calls the live runner."""
    root = ROOT / "core/binaries" / slug
    bin_dir = root / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    target = bin_dir / f"opgrok-{slug}"
    runner = ROOT / "core/tools/run_harness.py"
    script = f"""#!/usr/bin/env bash
set -euo pipefail
# OPGROK harness entrypoint — live Grok API via run_harness.py (loads .env itself)
REPO_ROOT="{ROOT}"
SLUG="{slug}"
GOAL=""
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --goal) GOAL="$2"; shift 2 ;;
    --dry-run) ARGS+=(--dry-run); shift ;;
    --max-tokens) ARGS+=(--max-tokens "$2"); shift 2 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done
if [[ -z "${{GOAL}}" ]]; then
  GOAL=$(python3 -c "import json;print(json.load(open('${{REPO_ROOT}}/core/binaries/${{SLUG}}/graph.json')).get('goal',''))")
fi
exec python3 "{runner}" "${{SLUG}}" --repo "${{REPO_ROOT}}" --goal "${{GOAL}}" "${{ARGS[@]}}"
"""
    target.write_text(script)
    target.chmod(target.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return target


def cargo_available() -> bool:
    return shutil.which("cargo") is not None


def build_cargo(slug: str) -> Path | None:
    crate = ROOT / "core/binaries" / slug / "crate"
    if not cargo_available():
        return None
    # rust specialists upgrade the crate BEFORE cargo is allowed to build
    try:
        ensure_full_crate(slug)
    except Exception as e:  # noqa: BLE001
        print(f"rust_opt failed: {e}", file=sys.stderr)
        return None
    if not (crate / "Cargo.toml").is_file():
        return None
    env = os.environ.copy()
    # isolate from workspace parent if needed — use --manifest-path
    cmd = [
        "cargo",
        "build",
        "--release",
        "--manifest-path",
        str(crate / "Cargo.toml"),
        "--target-dir",
        str(crate / "target"),
    ]
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd, cwd=str(crate), env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:] if r.stdout else "")
        print(r.stderr[-3000:] if r.stderr else "", file=sys.stderr)
        return None
    sys.path.insert(0, str(ROOT / "core"))
    from toolkit.product import crate_ident

    dest_name = f"opgrok-{slug}"
    want = [dest_name, crate_ident(slug)]
    release = crate / "target" / "release"
    candidates: list[Path] = []
    for name in want:
        candidates.extend(release.glob(name))
        candidates.extend(release.glob(f"{name}.exe"))
    candidates = [c for c in candidates if c.is_file()]
    if not candidates:
        print("cargo succeeded but binary not found", file=sys.stderr)
        return None
    dest_dir = ROOT / "core/binaries" / slug / "bin"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / dest_name
    shutil.copy2(candidates[0], dest)
    dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
    return dest


def ensure_full_crate(slug: str) -> None:
    """Generate crate sources, then run the rust-specialist optimize panel.

    Cargo must not run until rust_opt.optimize_crate has rewritten the crate.
    """
    sys.path.insert(0, str(ROOT / "core"))
    from toolkit.rust_opt import optimize_crate

    report = optimize_crate(slug, ROOT)
    print(
        "rust specialists:",
        ", ".join(p["sg"] for p in report.get("passes") or []),
    )
    return


def install_global(slug: str, binary: Path) -> Path:
    home = Path.home() / ".opgrok" / "bin"
    home.mkdir(parents=True, exist_ok=True)
    dest = home / f"opgrok-{slug}"
    shutil.copy2(binary, dest)
    dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
    # also short alias if reasonable
    meta = home.parent / "binaries.json"
    data = {"binaries": []}
    if meta.is_file():
        try:
            data = json.loads(meta.read_text())
        except Exception:
            pass
    data.setdefault("binaries", [])
    data["binaries"] = [b for b in data["binaries"] if b.get("slug") != slug]
    data["binaries"].append(
        {
            "slug": slug,
            "path": str(dest),
            "source": str(binary),
        }
    )
    meta.write_text(json.dumps(data, indent=2) + "\n")
    return dest


def update_registry_built(slug: str, binary: Path, method: str) -> None:
    reg_path = ROOT / "core/binaries/registry.json"
    reg = json.loads(reg_path.read_text()) if reg_path.is_file() else {"harnesses": []}
    for h in reg.get("harnesses") or []:
        if h.get("slug") == slug:
            h["binary"] = str(binary.relative_to(ROOT)) if str(binary).startswith(str(ROOT)) else str(binary)
            h["build_method"] = method
            h["built"] = True
    reg_path.write_text(json.dumps(reg, indent=2) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--install", action="store_true", help="Install to ~/.opgrok/bin")
    ap.add_argument("--force-python", action="store_true", help="Skip cargo; use Python runner")
    ap.add_argument(
        "--require-cargo",
        action="store_true",
        help="FAIL instead of falling back to a Python wrapper (product compiles)",
    )
    args = ap.parse_args()
    slug = args.slug
    root = ROOT / "core/binaries" / slug
    if not (root / "graph.json").is_file():
        print(f"FAIL: missing harness {slug}", file=sys.stderr)
        return 1

    n = cache_skills(slug)
    print(f"skills_cache: {n} skills")

    binary = None
    method = "python"
    if not args.force_python:
        binary = build_cargo(slug)
        if binary:
            method = "cargo-release"
            print(f"cargo binary: {binary}")
    if binary is None:
        if args.require_cargo:
            print(
                json.dumps(
                    {
                        "win": "FAIL",
                        "slug": slug,
                        "error": "cargo_required",
                        "method": "none",
                    }
                )
            )
            return 1
        ensure_full_crate(slug)
        binary = write_python_bin(slug)
        method = "python-runner"
        print(f"python entrypoint: {binary}")

    update_registry_built(slug, binary, method)
    if args.install:
        dest = install_global(slug, binary)
        print(f"installed: {dest}")
        print(f"PATH hint: export PATH=\"$HOME/.opgrok/bin:$PATH\"")

    print(json.dumps({"win": "PASS", "slug": slug, "binary": str(binary), "method": method}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

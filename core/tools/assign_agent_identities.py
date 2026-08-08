#!/usr/bin/env python3
"""Assign cryptographic human-named identities to every core/skills agent.

Implements the fixed-width self-hash construction (see core/registry/ARCHITECTURE.md):

  1. Strip prior identity lines; normalize SKILL.md
  2. Insert **Agent Identity**: Name-<64 zeros> after first H1 title
  3. H = SHA256(canonical form with zeroed hash field)
  4. Rewrite identity with Name-H; write IDENTITY.txt
  5. Emit named-hashes.{txt,json} + named-hashes.sha256
  6. Verify uniqueness of names, full hashes, short tokens; fail hard on collision

Usage:
  python3 core/tools/assign_agent_identities.py
  python3 core/tools/assign_agent_identities.py --verify-only
  python3 core/tools/assign_agent_identities.py --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "core" / "skills"
REGISTRY_DIR = ROOT / "core" / "registry"
NAME_POOL = REGISTRY_DIR / "name-pool.txt"
ASSIGNMENTS = REGISTRY_DIR / "name-assignments.json"
NAMED_TXT = REGISTRY_DIR / "named-hashes.txt"
NAMED_JSON = REGISTRY_DIR / "named-hashes.json"
NAMED_SHA = REGISTRY_DIR / "named-hashes.sha256"

HASH_HEX_LEN = 64
SHORT_PREFIX_LEN = 12
ZERO_HASH = "0" * HASH_HEX_LEN

# Use [ \t]* not \s* before $ — \s matches newlines and collapses blank lines after the identity.
IDENTITY_LINE_RE = re.compile(
    r"^\*\*Agent Identity\*\*:[ \t]*([A-Za-z][A-Za-z'-]*)-([0-9a-fA-F]{64})[ \t]*$",
    re.M,
)
IDENTITY_LINE_ANY_RE = re.compile(
    r"^\*\*Agent Identity\*\*:.*$",
    re.M,
)
H1_RE = re.compile(r"^#\s+.+$", re.M)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_name_pool() -> list[str]:
    if not NAME_POOL.is_file():
        raise SystemExit(f"FAIL: name pool missing: {NAME_POOL}")
    names: list[str] = []
    seen: set[str] = set()
    for line in NAME_POOL.read_text(encoding="utf-8").splitlines():
        n = line.strip()
        if not n or n.startswith("#"):
            continue
        key = n.lower()
        if key in seen:
            continue
        seen.add(key)
        names.append(n)
    if len(names) < 200:
        raise SystemExit(f"FAIL: name pool too small ({len(names)})")
    return names


def load_assignments() -> dict[str, str]:
    if not ASSIGNMENTS.is_file():
        return {}
    data = json.loads(ASSIGNMENTS.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "assignments" in data:
        return {str(k): str(v) for k, v in data["assignments"].items()}
    if isinstance(data, dict):
        return {str(k): str(v) for k, v in data.items() if not str(k).startswith("_")}
    return {}


def save_assignments(path_to_name: dict[str, str]) -> None:
    payload = {
        "version": "1.0.0",
        "updated_at": utc_now(),
        "count": len(path_to_name),
        "assignments": dict(sorted(path_to_name.items())),
    }
    ASSIGNMENTS.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def enumerate_skills() -> list[Path]:
    return sorted(
        p for p in SKILLS.rglob("SKILL.md") if "_framework" not in p.parts
    )


def rel_skill_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalize_text(text: str) -> str:
    """LF newlines, strip trailing whitespace per line, single trailing newline."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    # drop trailing empty lines then add one final newline
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def strip_identity_lines(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        if IDENTITY_LINE_ANY_RE.match(lines[i].strip() if lines[i].startswith("**") else lines[i]):
            # also drop a single blank line immediately after identity if present
            i += 1
            if i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        # match even with leading/trailing spaces
        if re.match(r"^\*\*Agent Identity\*\*:", lines[i].strip()):
            i += 1
            if i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def insert_identity_after_title(text: str, name: str, hash_hex: str) -> str:
    """Insert identity line immediately after the first H1 title."""
    text = strip_identity_lines(text)
    m = H1_RE.search(text)
    if not m:
        # prepend a synthetic title block if missing (should not happen)
        identity = f"**Agent Identity**: {name}-{hash_hex}\n\n"
        return identity + text
    end = m.end()
    # skip single blank after title if present; we re-add clean spacing
    rest = text[end:]
    if rest.startswith("\n"):
        rest = rest[1:]
    if rest.startswith("\n"):
        rest = rest[1:]
    identity_block = f"\n\n**Agent Identity**: {name}-{hash_hex}\n\n"
    return text[:end] + identity_block + rest


def zero_identity_hash_field(text: str) -> str:
    """Replace the 64-hex field of the Agent Identity line with zeros."""

    def repl(m: re.Match[str]) -> str:
        return f"**Agent Identity**: {m.group(1)}-{ZERO_HASH}"

    return IDENTITY_LINE_RE.sub(repl, text)


def extract_identity(text: str) -> tuple[str, str] | None:
    m = IDENTITY_LINE_RE.search(text)
    if not m:
        return None
    return m.group(1), m.group(2).lower()


def canonical_hash(text_with_identity: str) -> str:
    """SHA-256 of normalized text with identity hash field zeroed."""
    zeroed = zero_identity_hash_field(text_with_identity)
    canon = normalize_text(zeroed)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def short_token(name: str, full_hash: str) -> str:
    return f"{name}-{full_hash[:SHORT_PREFIX_LEN]}"


def full_token(name: str, full_hash: str) -> str:
    return f"{name}-{full_hash}"


def assign_names(skill_paths: list[Path], pool: list[str], sticky: dict[str, str]) -> dict[str, str]:
    """Return rel_path -> name, preserving sticky bindings; assign new names by sorted path."""
    used: set[str] = set()
    # keep sticky only for paths that still exist
    existing_rels = {rel_skill_path(p) for p in skill_paths}
    result: dict[str, str] = {}
    for rel, name in sticky.items():
        if rel in existing_rels:
            key = name.lower()
            if key in used:
                raise SystemExit(f"FAIL: sticky name collision on {name!r} for {rel}")
            used.add(key)
            result[rel] = name

    pool_iter = iter(pool)
    for path in skill_paths:
        rel = rel_skill_path(path)
        if rel in result:
            continue
        # next free name
        while True:
            try:
                candidate = next(pool_iter)
            except StopIteration:
                raise SystemExit(
                    f"FAIL: name pool exhausted at {rel} "
                    f"(need {len(skill_paths)}, pool={len(pool)}, sticky={len(result)})"
                )
            if candidate.lower() not in used:
                # also skip if name already taken by sticky that we haven't consumed from pool
                used.add(candidate.lower())
                result[rel] = candidate
                break
    # ensure sticky names that were already used don't conflict with pool walk:
    # (handled above)
    return result


def write_identity_txt(skill_dir: Path, name: str, full_hash: str, path_rel: str, ts: str) -> None:
    st = short_token(name, full_hash)
    ft = full_token(name, full_hash)
    body = (
        f"name: {name}\n"
        f"full_hash: {full_hash}\n"
        f"short_token: {st}\n"
        f"full_token: {ft}\n"
        f"path: {path_rel}\n"
        f"timestamp: {ts}\n"
        f"algorithm: sha256-fixed-width-identity-v1\n"
    )
    (skill_dir / "IDENTITY.txt").write_text(body, encoding="utf-8")


def process_skill(path: Path, name: str, ts: str, dry_run: bool) -> dict:
    raw = path.read_text(encoding="utf-8")
    body = normalize_text(strip_identity_lines(raw))
    # provisional with zeros
    provisional = insert_identity_after_title(body, name, ZERO_HASH)
    provisional = normalize_text(provisional)
    h = hashlib.sha256(provisional.encode("utf-8")).hexdigest()
    final_text = insert_identity_after_title(body, name, h)
    final_text = normalize_text(final_text)
    # sanity: recomputed canonical hash must equal h
    recomputed = canonical_hash(final_text)
    if recomputed != h:
        raise SystemExit(f"FAIL: hash mismatch after embed for {path}: {recomputed} != {h}")

    path_rel = rel_skill_path(path)
    if not dry_run:
        path.write_text(final_text, encoding="utf-8")
        write_identity_txt(path.parent, name, h, path_rel, ts)

    return {
        "name": name,
        "full_hash": h,
        "short_token": short_token(name, h),
        "full_token": full_token(name, h),
        "path": path_rel,
        "timestamp": ts,
    }


def emit_registry(entries: list[dict], dry_run: bool) -> None:
    entries_sorted = sorted(entries, key=lambda e: e["name"].lower())
    # text
    lines = [
        "# OPGROK named-hashes — authoritative agent identity registry",
        f"# version: 1.0.0",
        f"# updated_at: {entries_sorted[0]['timestamp'] if entries_sorted else utc_now()}",
        f"# count: {len(entries_sorted)}",
        f"# algorithm: sha256-fixed-width-identity-v1",
        "# columns: Name FullHash ShortToken Path Timestamp",
        "#",
    ]
    for e in entries_sorted:
        lines.append(
            f"{e['name']}\t{e['full_hash']}\t{e['short_token']}\t{e['path']}\t{e['timestamp']}"
        )
    txt = "\n".join(lines) + "\n"

    by_short = {e["short_token"]: e for e in entries_sorted}
    by_full = {e["full_token"]: e for e in entries_sorted}
    by_hash = {e["full_hash"]: e for e in entries_sorted}
    by_name = {e["name"]: e for e in entries_sorted}
    by_path = {e["path"]: e for e in entries_sorted}

    payload = {
        "version": "1.0.0",
        "algorithm": "sha256-fixed-width-identity-v1",
        "updated_at": entries_sorted[0]["timestamp"] if entries_sorted else utc_now(),
        "count": len(entries_sorted),
        "short_prefix_len": SHORT_PREFIX_LEN,
        "agents": entries_sorted,
        "index": {
            "by_short_token": {k: v["path"] for k, v in by_short.items()},
            "by_full_token": {k: v["path"] for k, v in by_full.items()},
            "by_hash": {k: v["path"] for k, v in by_hash.items()},
            "by_name": {k: v["path"] for k, v in by_name.items()},
            "by_path": {k: v["short_token"] for k, v in by_path.items()},
        },
    }
    js = json.dumps(payload, indent=2) + "\n"
    reg_hash = hashlib.sha256(js.encode("utf-8")).hexdigest()

    if dry_run:
        print(f"[dry-run] would write {len(entries_sorted)} agents to registry")
        return

    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    NAMED_TXT.write_text(txt, encoding="utf-8")
    NAMED_JSON.write_text(js, encoding="utf-8")
    NAMED_SHA.write_text(reg_hash + "\n", encoding="utf-8")


def verify_all(skill_paths: list[Path] | None = None) -> list[str]:
    """Hard verification. Returns list of error strings (empty = PASS)."""
    errs: list[str] = []
    if not NAMED_JSON.is_file():
        return ["named-hashes.json missing"]
    data = json.loads(NAMED_JSON.read_text(encoding="utf-8"))
    agents = data.get("agents") or []
    if not agents:
        return ["registry empty"]

    names: dict[str, str] = {}
    hashes: dict[str, str] = {}
    shorts: dict[str, str] = {}

    for e in agents:
        name = e["name"]
        fh = e["full_hash"].lower()
        st = e["short_token"]
        path = e["path"]
        if name.lower() in names:
            errs.append(f"name collision: {name} ({names[name.lower()]} vs {path})")
        names[name.lower()] = path
        if fh in hashes:
            errs.append(f"hash collision: {fh[:16]}… ({hashes[fh]} vs {path})")
        hashes[fh] = path
        if st in shorts:
            errs.append(f"short token collision: {st} ({shorts[st]} vs {path})")
        shorts[st] = path

        abs_path = ROOT / path
        if not abs_path.is_file():
            errs.append(f"path missing: {path}")
            continue
        text = abs_path.read_text(encoding="utf-8")
        extracted = extract_identity(text)
        if not extracted:
            errs.append(f"missing identity line: {path}")
            continue
        ename, ehash = extracted
        if ename != name:
            errs.append(f"name mismatch embed vs registry: {path} ({ename} != {name})")
        if ehash != fh:
            errs.append(f"hash mismatch embed vs registry: {path}")
        recomputed = canonical_hash(text)
        if recomputed != ehash:
            errs.append(
                f"hash verify fail: {path} embedded={ehash[:16]}… recomputed={recomputed[:16]}…"
            )
        id_txt = abs_path.parent / "IDENTITY.txt"
        if not id_txt.is_file():
            errs.append(f"IDENTITY.txt missing: {abs_path.parent}")
        else:
            id_body = id_txt.read_text(encoding="utf-8")
            if fh not in id_body or name not in id_body:
                errs.append(f"IDENTITY.txt incomplete: {id_txt}")

    # ensure every skill on disk is in registry
    disk = skill_paths if skill_paths is not None else enumerate_skills()
    reg_paths = {e["path"] for e in agents}
    for p in disk:
        rel = rel_skill_path(p)
        if rel not in reg_paths:
            errs.append(f"skill not in registry: {rel}")

    # registry self-hash
    if NAMED_SHA.is_file():
        claimed = NAMED_SHA.read_text(encoding="utf-8").strip().split()[0]
        actual = hashlib.sha256(NAMED_JSON.read_bytes()).hexdigest()
        if claimed != actual:
            errs.append("named-hashes.sha256 does not match named-hashes.json")

    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Assign / verify agent identities")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if args.verify_only:
        errs = verify_all()
        if errs:
            print(f"IDENTITY GATE: FAIL ({len(errs)} issues)")
            for e in errs[:50]:
                print(f"  - {e}")
            if len(errs) > 50:
                print(f"  … and {len(errs) - 50} more")
            return 1
        data = json.loads(NAMED_JSON.read_text(encoding="utf-8"))
        print(f"IDENTITY GATE: PASS — {data.get('count')} agents")
        return 0

    pool = load_name_pool()
    sticky = load_assignments()
    skills = enumerate_skills()
    print(f"Enumerated {len(skills)} skills; name pool={len(pool)}; sticky={len(sticky)}")

    path_to_name = assign_names(skills, pool, sticky)
    ts = utc_now()
    entries: list[dict] = []
    for path in skills:
        rel = rel_skill_path(path)
        name = path_to_name[rel]
        entries.append(process_skill(path, name, ts, dry_run=args.dry_run))

    if not args.dry_run:
        save_assignments(path_to_name)
    emit_registry(entries, dry_run=args.dry_run)

    if args.dry_run:
        print("dry-run complete (no files written)")
        return 0

    errs = verify_all(skills)
    if errs:
        print(f"IDENTITY GATE: FAIL ({len(errs)} issues)")
        for e in errs[:40]:
            print(f"  - {e}")
        return 1

    print(f"IDENTITY GATE: PASS — {len(entries)} agents")
    print(f"  registry: {NAMED_JSON.relative_to(ROOT)}")
    print(f"  text:     {NAMED_TXT.relative_to(ROOT)}")
    print(f"  digest:   {NAMED_SHA.relative_to(ROOT)}")
    # sample
    sample = entries[0]
    print(f"  sample:   {sample['short_token']} → {sample['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

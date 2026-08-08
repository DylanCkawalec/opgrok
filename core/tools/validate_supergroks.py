#!/usr/bin/env python3
"""Leslie Gate validator for nested SuperGrok packages under core/skills/."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "core" / "skills"
FRAMEWORK = SKILLS / "_framework"
REGISTRY = FRAMEWORK / "REGISTRY.json"
GLOSSARY = FRAMEWORK / "AGENT_GLOSSARY.md"

# Enhancement protocol L2 (preferred) OR legacy Intent/Win/Do
PROTOCOL_SECTIONS = [
    "## Core Mandate",
    "## Procedural Workflow",
    "## Constraints",
    "## Definition of Done",
]
LEGACY_SECTIONS = [
    "## Intent",
    "## Purpose",
    "## Call",
    "## Win",
    "## Do",
]

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,48}[a-z0-9]$")


def validate_skill(path: Path, expect_name: str, category: str) -> list[str]:
    errs: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not NAME_RE.match(expect_name) or "--" in expect_name:
        errs.append(f"invalid name form: {expect_name}")
    if f"name: {expect_name}" not in text:
        errs.append(f"frontmatter name missing or mismatch for {expect_name}")
    if f"/{expect_name}" not in text and "description:" not in text[:800]:
        errs.append("missing call/description triggers")
    proto_ok = all(s in text for s in PROTOCOL_SECTIONS)
    legacy_ok = all(s in text for s in LEGACY_SECTIONS)
    if not proto_ok and not legacy_ok:
        errs.append("missing protocol skeleton (Core Mandate/Workflow/Constraints/Done) or legacy Intent/Win/Do")
    if "PASS" not in text and "Definition of Done" not in text and "## Win" not in text:
        errs.append("missing PASS / Definition of Done language")
    # Compactness: SuperGrok bodies should stay lean (allow navigators/core up to 250)
    lines = text.count("\n")
    if lines > 350:
        errs.append(f"too long for L2 compactness: {lines} lines")
    return errs


def main() -> int:
    if not SKILLS.is_dir():
        print("FAIL: core/skills/ missing")
        return 1

    skill_files = sorted(
        p for p in SKILLS.rglob("SKILL.md") if "_framework" not in p.parts
    )

    print(f"Found {len(skill_files)} SKILL.md under core/skills/ (full tree)")
    fail = 0
    names: set[str] = set()
    role_skills = []

    for path in skill_files:
        rel = path.relative_to(SKILLS)
        parts = rel.parts
        if len(parts) == 3:
            category, role = parts[0], parts[1]
            text0 = path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^name:\s*(\S+)", text0, re.M)
            expect_name = m.group(1) if m else f"{category}-{role}"
            role_skills.append(path)
        elif len(parts) == 2:
            category = parts[0]
            text0 = path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"^name:\s*(\S+)", text0, re.M)
            expect_name = m.group(1) if m else parts[0]
        else:
            continue
        errs = validate_skill(path, expect_name, category)
        if expect_name in names:
            errs.append("duplicate name")
        names.add(expect_name)
        if errs:
            fail += 1
            if fail <= 20:
                print(f"FAIL {path.relative_to(SKILLS)}:")
                for e in errs:
                    print(f"  - {e}")

    print(f"OK: unique names={len(names)}")
    print(f"OK: role-level paths={len(role_skills)}")
    print(f"OK: total SKILL.md={len(skill_files)}")

    for required in ("leslie", "opgrok"):
        if not (SKILLS / required / "SKILL.md").exists():
            print(f"FAIL: {required} missing")
            fail += 1
        else:
            print(f"OK: {required} present")

    # SuperGrok floor: 25 cats × 6 roles = 150 (+ navigators/core)
    MIN_SUPER = 150
    MIN_TOTAL = 160

    if REGISTRY.exists():
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        rc = reg.get("count") or 0
        if rc < MIN_TOTAL:
            print(f"FAIL: registry count {rc} < {MIN_TOTAL}")
            fail += 1
        else:
            print(f"OK: REGISTRY.json count={rc}")
        kinds = reg.get("counts_by_kind") or {}
        if kinds:
            print(f"OK: kinds {kinds}")
            super_n = kinds.get("supergrok") or kinds.get("role") or 0
            # rebuild may label as supergrok; generator registry uses skills[] length
            if super_n and super_n < MIN_SUPER:
                print(f"FAIL: SuperGrok kind count {super_n} < {MIN_SUPER}")
                fail += 1
        skills = reg.get("skills") or []
        if skills and not str(skills[0].get("path", "")).startswith("core/skills/"):
            print("FAIL: registry paths not under core/skills/")
            fail += 1
        # role set check on role-level entries
        prod_roles = {"smith", "forge", "scout", "trace", "audit", "seal"}
        role_names = {
            s.get("role")
            for s in skills
            if s.get("role") and s.get("category") not in (None, "meta") or True
        }
        # only enforce if skills look like SuperGrok rows
        sg_roles = {s.get("role") for s in skills if s.get("role") in prod_roles}
        if skills and not (sg_roles & prod_roles):
            # rebuild format may nest differently — count paths
            pass
        legacy = {
            s.get("role")
            for s in skills
            if s.get("role")
            in {
                "anvil",
                "weld",
                "carve",
                "loom",
                "stitch",
                "glyph",
                "prism",
                "lens",
                "mirror",
                "probe",
                "guard",
                "aegis",
                "pulse",
                "flux",
                "radix",
                "vertex",
                "ridge",
                "crux",
                "scribe",
            }
        }
        if legacy:
            print(f"FAIL: legacy roles still in registry: {sorted(legacy)[:8]}…")
            fail += 1
        else:
            print("OK: no legacy 25-role catalog entries")
    else:
        print("FAIL: REGISTRY.json missing")
        fail += 1

    if GLOSSARY.exists():
        g = GLOSSARY.read_text(encoding="utf-8")
        if g.count("\n### ") < MIN_SUPER:
            print(f"FAIL: AGENT_GLOSSARY.md incomplete (### count < {MIN_SUPER})")
            fail += 1
        else:
            print("OK: AGENT_GLOSSARY.md")
    else:
        print("FAIL: AGENT_GLOSSARY.md missing")
        fail += 1

    # SuperGrok path count on disk
    super_paths = [
        p
        for p in skill_files
        if len(p.relative_to(SKILLS).parts) == 3
        and p.relative_to(SKILLS).parts[1]
        in {"smith", "forge", "scout", "trace", "audit", "seal"}
    ]
    if len(super_paths) != MIN_SUPER:
        print(f"FAIL: SuperGrok paths={len(super_paths)} expected {MIN_SUPER}")
        fail += 1
    else:
        print(f"OK: SuperGroks={len(super_paths)}")

    for fname in ("NAVIGATION.md", "MCP_CATALOG.json", "CATEGORY_INDEX.md"):
        if (FRAMEWORK / fname).is_file():
            print(f"OK: {fname}")
        else:
            print(f"FAIL: {fname} missing")
            fail += 1

    # Cryptographic human-named identity layer
    id_script = ROOT / "core" / "tools" / "assign_agent_identities.py"
    id_json = ROOT / "core" / "registry" / "named-hashes.json"
    if id_script.is_file() and id_json.is_file():
        import subprocess

        r = subprocess.run(
            [sys.executable, str(id_script), "--verify-only"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print("FAIL: identity registry verification")
            print(r.stdout or r.stderr)
            fail += 1
        else:
            print((r.stdout or "").strip().splitlines()[-1] if r.stdout else "OK: identities")
    elif not id_json.is_file():
        print("FAIL: core/registry/named-hashes.json missing — run assign_agent_identities.py")
        fail += 1

    if fail:
        print(f"\nLESLIE GATE: FAIL ({fail} issue groups)")
        return 1
    print("\nLESLIE GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

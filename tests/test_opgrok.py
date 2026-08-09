#!/usr/bin/env python3
"""OPGROK self-tests — harness craft/run, toolkit, web controllers.

Run: python3 tests/test_opgrok.py
Exit 0 = all pass, 1 = any fail.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "core" / "tools"))
sys.path.insert(0, str(ROOT / "apps" / "web"))

os.environ.setdefault("XAI_API_KEY", "test-key-for-dry-run")

PASS = 0
FAIL = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  PASS: {label}")
    else:
        FAIL += 1
        print(f"  FAIL: {label} {detail}")


# ── Harness craft ──────────────────────────────────────────────

def test_craft_harness() -> None:
    print("\n[harness craft]")
    from craft_harness import craft, slugify, route

    slug = slugify("test harness for unit checks")
    check("slugify produces clean slug", bool(slug) and "--" not in slug, slug)

    hired = route("build a landing page", 4)
    check("route returns >=2 skills", len(hired) >= 2, f"got {len(hired)}")
    check("route respects limit", len(hired) <= 4)
    check("routed skills have names", all(s.get("name") for s in hired))

    pkg = craft("test harness for unit checks", hire_limit=4)
    check("craft returns package path", pkg.is_dir(), str(pkg))
    check("graph.json exists", (pkg / "graph.json").is_file())
    check("README.md exists", (pkg / "README.md").is_file())
    check("WINNING_CONDITION.md exists", (pkg / "WINNING_CONDITION.md").is_file())
    check("bin entrypoint exists", (pkg / "bin").is_dir())

    graph = json.loads((pkg / "graph.json").read_text())
    check("graph has nodes", len(graph.get("nodes", [])) >= 2)
    check("graph has edges", len(graph.get("edges", [])) >= 1)
    check("graph has goal", bool(graph.get("goal")))
    check("graph has slug", graph.get("slug") == slug)
    check("nodes have sg_name", all(n.get("sg_name") for n in graph["nodes"]))
    check("last node is sink", graph["nodes"][-1].get("sink") is True)


# ── Harness dry-run ────────────────────────────────────────────

def test_run_harness_dry() -> None:
    print("\n[harness dry-run]")
    from run_harness import run_harness

    result = run_harness("test-harness-for-unit-checks", dry_run=True)
    check("dry-run seals DRY (I2 DryHonesty)", result.get("win") == "DRY", result.get("win", "?"))
    check("dry-run has node_results", len(result.get("node_results", [])) >= 1)
    check("dry-run has no failed nodes", len(result.get("failed_nodes", [])) == 0,
          str(result.get("failed_nodes")))
    check("dry-run marks dry_run=True", result.get("dry_run") is True)
    check("dry-run has run_id", bool(result.get("run_id")))


# ── Harness build ──────────────────────────────────────────────

def test_build_harness() -> None:
    print("\n[harness build]")
    from build_harness import cache_skills, write_python_bin

    n = cache_skills("test-harness-for-unit-checks")
    check("cache_skills returns >0", n > 0, f"cached {n}")

    bin_path = write_python_bin("test-harness-for-unit-checks")
    check("python bin written", bin_path.is_file(), str(bin_path))
    check("python bin is executable", os.access(bin_path, os.X_OK))


# ── Toolkit ────────────────────────────────────────────────────

def test_toolkit() -> None:
    print("\n[toolkit]")
    from toolkit import (
        pick_model, toolkit_flags, MemoryStore, TokenLedger,
        RunJournal, ArtifactVault, should_retry, repair_prompt,
        topo_layers, ready_wave,
    )

    flags = toolkit_flags()
    check("toolkit_flags is dict", isinstance(flags, dict))
    check("toolkit_flags has max_tokens", "max_tokens" in flags)

    model, tier = pick_model({"category": "code", "role": "forge"}, flags)
    check("pick_model returns model str", isinstance(model, str))
    check("pick_model returns tier", tier is not None)

    model_f, _ = pick_model({"category": "docs", "role": "scout"}, flags)
    check("pick_model fast for docs", isinstance(model_f, str))

    model_j, _ = pick_model({"category": "review", "role": "audit"}, flags)
    check("pick_model judge for review", isinstance(model_j, str))

    ms = MemoryStore(Path("/tmp/opgrok-test-mem"))
    ms.remember_from_run("test goal", {"summary": "ok"}, [])
    check("MemoryStore persists", ms.path.is_file())

    tl = TokenLedger(Path("/tmp/opgrok-test-ledger"))
    tl.record("n01", "test-sg", "grok-4", {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30})
    check("TokenLedger records", tl.totals["total_tokens"] >= 30)

    rj = RunJournal(Path("/tmp/opgrok-test-jr"))
    rj.event("test", detail="ok")
    check("RunJournal logs without error", rj.path.is_file())

    av = ArtifactVault(Path("/tmp/opgrok-test-art"))
    av.write("n01", "test.md", "hello")
    check("ArtifactVault writes", len(av.index) >= 1)

    check("should_retry True on error", should_retry({"error": "x"}, 0, 1) is True)
    check("should_retry False over limit", should_retry({"error": "x"}, 1, 1) is False)
    check("should_retry False on PASS",
          should_retry({"parsed": {"summary": "s", "artifacts": [], "win": "PASS"}}, 0, 1) is False)
    rp = repair_prompt("goal", {"sg_name": "test", "purpose": "test"}, {"error": "bad"}, 0)
    check("repair_prompt returns string", isinstance(rp, str))

    layers = topo_layers(
        nodes=[{"id": "n1"}, {"id": "n2"}],
        edges=[{"from": "n1", "to": "n2"}],
    )
    check("topo_layers returns list", isinstance(layers, list))
    check("topo_layers has >=1 layer", len(layers) >= 1)

    wave = ready_wave(
        layer_ids=["n1"],
        run_one=lambda nid: {"win": "PASS"},
        parallel=False,
    )
    check("ready_wave returns results", wave.get("n1", {}).get("win") == "PASS")


# ── Validator ──────────────────────────────────────────────────

def test_validator() -> None:
    print("\n[validator]")
    import subprocess
    r = subprocess.run(
        [sys.executable, str(ROOT / "core/tools/validate_supergroks.py")],
        cwd=str(ROOT), capture_output=True, text=True, timeout=30,
    )
    check("validator exits 0", r.returncode == 0, f"rc={r.returncode}")
    check("validator prints LESLIE GATE: PASS", "LESLIE GATE: PASS" in (r.stdout or ""),
          (r.stdout or "")[-200:])


# ── Web controllers ────────────────────────────────────────────

def test_web_controllers() -> None:
    print("\n[web controllers]")
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)

    r = client.get("/api/health")
    check("GET /api/health → 200", r.status_code == 200, str(r.status_code))
    body = r.json()
    check("health has xai_key_present", "xai_key_present" in body, str(body.keys()))

    r = client.get("/api/models")
    check("GET /api/models → 200", r.status_code == 200, str(r.status_code))
    check("models returns list", isinstance(r.json().get("models"), list))

    r = client.get("/api/harnesses")
    check("GET /api/harnesses → 200", r.status_code == 200, str(r.status_code))

    r = client.get("/")
    check("GET / → 200 (HTML)", r.status_code == 200, str(r.status_code))

    r = client.get("/harnesses")
    check("GET /harnesses → 200 (HTML)", r.status_code == 200, str(r.status_code))

    r = client.get("/mcp/tools")
    check("GET /mcp/tools → 200", r.status_code == 200, str(r.status_code))

    # craft via API
    r = client.post("/api/harnesses/craft", json={"goal": "test api craft", "hire": 3})
    check("POST /api/harnesses/craft → 200", r.status_code == 200, str(r.status_code))
    if r.status_code == 200:
        body = r.json()
        check("craft returns ok=true", body.get("ok") is True, str(body.get("ok")))
        check("craft has stdout", bool(body.get("stdout")), "no stdout")


# ── Main ───────────────────────────────────────────────────────

def main() -> int:
    print("OPGROK self-tests")
    print("=" * 50)
    test_craft_harness()
    test_run_harness_dry()
    test_build_harness()
    test_toolkit()
    test_validator()
    test_web_controllers()
    print("\n" + "=" * 50)
    print(f"Results: {PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

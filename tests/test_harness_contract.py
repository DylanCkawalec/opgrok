#!/usr/bin/env python3
"""WC contract checks: the aria-math-v2 counterexample must never seal PASS again.

Run: python3 tests/test_harness_contract.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core/tools"))
sys.path.insert(0, str(ROOT / "core"))

from run_harness import contract_ok  # noqa: E402
from toolkit.repair import should_retry  # noqa: E402

# 1. Contract acceptance/rejection
good = {"parsed": {"summary": "s", "artifacts": [], "win": "PASS"}}
assert contract_ok(good), "valid contract output must pass"
assert not contract_ok({"error": "http_400", "parsed": good["parsed"]}), "error output must fail"
assert not contract_ok({"parsed": None, "content": "prose one-liner"}), "non-JSON junk must fail"
assert not contract_ok({"parsed": {"summary": "only summary"}}), "missing keys must fail"

# 2. Repair pressure: junk and hollow outputs are retryable
assert should_retry({"parsed": None}, 0, 1), "non-JSON must retry"
assert should_retry({"parsed": {"summary": "x"}}, 0, 1), "missing keys must retry"
assert should_retry({"parsed": {"summary": "s", "artifacts": [], "win": "FAIL"}}, 0, 1)
assert not should_retry(good, 0, 1), "valid PASS must not retry"
assert not should_retry({"parsed": None}, 1, 1), "retry budget respected"

# 3. Replay the actual v2 counterexample receipt: every node was contract-invalid,
#    so the old vacuous PASS is unreachable now.
receipt = ROOT / "core/binaries/aria-math-v2/artifacts/live_run_stdout.json"
if receipt.is_file():
    d = json.loads(receipt.read_text())
    nodes = d.get("node_results", [])
    assert nodes, "receipt has nodes"
    assert all(not contract_ok(n.get("output")) for n in nodes), (
        "v2 counterexample nodes must all fail the contract"
    )

print("PASS: harness contract checks")

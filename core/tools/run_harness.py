#!/usr/bin/env python3
"""Live OPGROK harness runner with Grok-native toolkit.

Capabilities: multi-model routing, memory, artifacts, repair, parallel DAG,
toolbelt, judge sink support, ledger, journal, vision refs.

Usage:
  python3 core/tools/run_harness.py <slug> [--goal "..."] [--dry-run]
      [--max-tokens 1200] [--serial] [--no-memory] [--no-tools]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "core"))

from toolkit import (  # noqa: E402
    ArtifactVault,
    MemoryStore,
    RunJournal,
    TokenLedger,
    Toolbelt,
    collect_vision_refs,
    load_repo_env,
    pick_model,
    repair_prompt,
    should_retry,
    toolkit_flags,
    topo_layers,
    vision_system_addon,
)
from toolkit.parallel import ready_wave  # noqa: E402


def read_skill(repo: Path, skill_path: str, cache_dir: Path, sg_name: str, max_chars: int = 6000) -> str:
    cache_file = cache_dir / f"{sg_name}.md"
    if cache_file.is_file():
        text = cache_file.read_text(encoding="utf-8", errors="ignore")
    else:
        p = repo / skill_path if skill_path else None
        if not p or not p.is_file():
            return ""
        text = p.read_text(encoding="utf-8", errors="ignore")
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(text[: max_chars * 2], encoding="utf-8")
        except Exception:
            pass
    if len(text) > max_chars:
        parts = []
        for sec in ("## Intent", "## Purpose", "## Call", "## Win", "## Do", "## Contract"):
            if sec in text:
                i = text.find(sec)
                j = text.find("\n## ", i + 4)
                parts.append(text[i : j if j > 0 else i + 1200])
        text = "\n\n".join(parts) if parts else text[:max_chars]
        text = text[:max_chars]
    return text


def try_parse_json(text: str):
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
    return None


CONTRACT_KEYS = ("summary", "artifacts", "win")


def contract_ok(out: dict) -> bool:
    """WC gate 2: error-free output whose parsed JSON carries the contract keys."""
    if not isinstance(out, dict) or out.get("error"):
        return False
    p = out.get("parsed")
    return isinstance(p, dict) and all(k in p for k in CONTRACT_KEYS)


def call_grok(
    prompt: str,
    system: str,
    model: str,
    api_key: str,
    max_tokens: int,
    reasoning_effort: str | None = None,
    timeout_s: int | None = None,
) -> dict:
    """Chat Completions call. Grok 4.5: reasoning_effort in {low,medium,high} (default high)."""
    body: dict = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
    }
    # Reasoning models (grok-4.5): effort high|medium|low; avoid unsupported penalties
    effort = (reasoning_effort or os.environ.get("OPGROK_REASONING_EFFORT") or "").strip().lower()
    if effort in {"low", "medium", "high"}:
        body["reasoning_effort"] = effort
    elif model.startswith("grok-4.5") or model == "grok-4.5":
        body["reasoning_effort"] = "high"
    else:
        body["temperature"] = 0.2

    timeout = timeout_s or int(os.environ.get("OPGROK_HTTP_TIMEOUT", "600"))
    req = urllib.request.Request(
        "https://api.x.ai/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "opgrok-harness/3.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        return {"error": f"http_{e.code}", "detail": err[:2000]}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)}

    try:
        msg = data["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning_content") or msg.get("reasoning")
    except Exception:  # noqa: BLE001
        return {"error": "bad_response", "raw": data}

    return {
        "content": content,
        "reasoning_content": reasoning,
        "reasoning_effort": body.get("reasoning_effort"),
        "parsed": try_parse_json(content),
        "usage": data.get("usage"),
        "model": data.get("model") or model,
    }


def thrift_bb(blackboard: dict) -> dict:
    slim = {}
    for k, v in blackboard.items():
        if k.startswith("memory.") or k in {"goal", "vision_refs"}:
            slim[k] = v
            continue
        if not (k == "goal" or k.endswith(".output")):
            continue
        if isinstance(v, dict) and "content" in v and isinstance(v.get("content"), str):
            slim[k] = {
                "summary": (v.get("parsed") or {}).get("summary")
                if isinstance(v.get("parsed"), dict)
                else None,
                "content_preview": v["content"][:1200],
                "win": (v.get("parsed") or {}).get("win")
                if isinstance(v.get("parsed"), dict)
                else None,
                "artifacts": (v.get("parsed") or {}).get("artifacts")
                if isinstance(v.get("parsed"), dict)
                else None,
            }
        else:
            slim[k] = v
    return slim


def build_system(node: dict, skill_text: str, vision_refs: list[str], tools_on: bool) -> str:
    tool_hint = ""
    if tools_on:
        tool_hint = """
Optional tools (return in JSON as tool_calls array when needed):
  {"tool":"read_file","args":{"path":"relative/to/repo"}}
  {"tool":"grep","args":{"pattern":"regex","path":"."}}
  {"tool":"web_fetch","args":{"url":"https://..."}}
  {"tool":"write_artifact","args":{"name":"file.md","content":"..."}}
After tool_calls, still return summary/artifacts/win for this step.
"""
    identity_line = ""
    try:
        from toolkit.identity import IdentityIndex  # type: ignore

        idx = IdentityIndex.load()
        sp = node.get("skill_path") or ""
        ref = idx.resolve_path(sp) if sp else None
        if ref:
            identity_line = (
                f"Agent identity: `{ref.short_token}` (full: `{ref.full_token}`).\n"
                f"Address other SuperGroks by short token Name-HashPrefix; "
                f"registry `core/registry/named-hashes.json` resolves O(1).\n"
            )
    except Exception:
        identity_line = ""

    return f"""You are SuperGrok `{node.get('sg_name')}` (binary_id={node.get('binary_id')}).
Category/role: {node.get('category')}/{node.get('role')}
Intent: {node.get('intent')}
Purpose: {node.get('purpose')}
Tier: {node.get('model_tier') or 'auto'}
{identity_line}
You are one node in an OPGROK harness. Do only this node's job.
Return a single JSON object with keys:
  - summary (string — your actual analysis, not a restatement of this prompt)
  - artifacts (array of {{name, content, kind}} holding the REAL deliverable: code, spec text,
    patches, configs. Empty [] only for pure-analysis nodes, and then summary must carry the
    full analysis. Producer roles (forge/smith/seal) must attach at least one artifact.)
  - next_hints (array of strings)
  - win ("PASS" only if you fully produced this node's deliverable; otherwise "FAIL" — the
    harness will repair-retry you. A hollow PASS is a contract violation.)
  - tool_calls (optional array)
{tool_hint}
{vision_system_addon(vision_refs) if (node.get('category') == 'vision' or vision_refs) else ''}
SKILL CONTRACT:
{skill_text or '(skill body unavailable — use intent/purpose only)'}
"""


def build_user(goal: str, node: dict, blackboard: dict) -> str:
    return f"""GOAL:
{goal}

NODE: {node.get('id')} ({node.get('sg_name')})
PROCESS: {node.get('ipo', {}).get('process')}
OODA.ACT: {node.get('ooda', {}).get('act')}
INPUT KEYS: {node.get('ipo', {}).get('inputs')}

BLACKBOARD (thrift):
{json.dumps(thrift_bb(blackboard), indent=2)[:14000]}

Produce the JSON result for this node only.
"""


def run_harness(
    slug: str,
    goal: str = "",
    dry_run: bool = False,
    max_tokens: int | None = None,
    repo: Path | None = None,
    serial: bool = False,
    no_memory: bool = False,
    no_tools: bool = False,
) -> dict:
    repo = repo or ROOT
    load_repo_env(repo)
    flags = toolkit_flags()
    if max_tokens is not None:
        flags["max_tokens"] = max_tokens
    if serial:
        flags["parallel"] = False
    if no_memory:
        flags["memory"] = False
    if no_tools:
        flags["tools"] = False

    harness_root = repo / "core/binaries" / slug
    gpath = harness_root / "graph.json"
    if not gpath.is_file():
        return {"win": "FAIL", "error": f"missing {gpath}"}

    graph = json.loads(gpath.read_text(encoding="utf-8"))
    goal = goal or graph.get("goal") or ""
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []
    by_id = {n["id"]: n for n in nodes}

    api_key = (os.environ.get("XAI_API_KEY") or os.environ.get("xai_api_key") or "").strip()
    require_live = os.environ.get("OPGROK_REQUIRE_LIVE", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    dry = dry_run or not api_key
    if dry and not dry_run and not api_key:
        print(
            "WARN: XAI_API_KEY missing/empty after load_repo_env — forcing dry-run. "
            "Set a live key in monorepo .env or export XAI_API_KEY. "
            "Use OPGROK_REQUIRE_LIVE=1 to fail instead of silent dry.",
            file=sys.stderr,
        )
    if require_live and dry:
        return {
            "win": "FAIL",
            "error": "OPGROK_REQUIRE_LIVE=1 but run would be dry "
            f"(dry_run={dry_run}, api_key_present={bool(api_key)}). "
            "Refuse silent dry-run.",
            "slug": slug,
            "dry_run": True,
            "api_key_present": bool(api_key),
        }

    journal = RunJournal(harness_root)
    ledger = TokenLedger(harness_root)
    vault = ArtifactVault(harness_root)
    memory = MemoryStore(harness_root, enabled=flags["memory"])
    tools = Toolbelt(
        repo,
        harness_root,
        allow_net=flags["allow_net"],
        allow_shell=flags["allow_shell"],
    )

    blackboard: dict = {"goal": goal}
    memory.load_into(blackboard)
    vision_refs = collect_vision_refs(goal, repo, blackboard)
    if vision_refs:
        blackboard["vision_refs"] = vision_refs

    journal.event("start", slug=slug, goal=goal, dry=dry, nodes=len(nodes), flags=flags)
    skills_cache = harness_root / "skills_cache"
    node_results_map: dict[str, dict] = {}

    def run_one(nid: str) -> dict:
        node = by_id[nid]
        skill_text = read_skill(
            repo, node.get("skill_path") or "", skills_cache, node.get("sg_name") or "x"
        )
        model, tier = pick_model(node, flags)
        system = build_system(node, skill_text, vision_refs, flags["tools"])
        user = build_user(goal, node, blackboard)

        attempt = 0
        out: dict = {}
        while True:
            if dry:
                out = {
                    "mode": "dry_run",
                    "sg": node.get("sg_name"),
                    "model": model,
                    "model_tier": tier.value,
                    "skill_chars": len(skill_text),
                    "system_preview": system[:400],
                    "prompt_preview": user[:500],
                    "parsed": {
                        "summary": f"[dry] {node.get('sg_name')} ({tier.value}/{model})",
                        "artifacts": [],
                        "win": "PASS",
                    },
                }
                ledger.record(nid, node.get("sg_name") or "", model, None)
                break

            out = call_grok(
                user if attempt == 0 else repair_prompt(goal, node, out, attempt),
                system,
                model,
                api_key,
                flags["max_tokens"],
                reasoning_effort=flags.get("reasoning_effort") or "high",
                timeout_s=flags.get("http_timeout") or 600,
            )
            out["mode"] = "live" if attempt == 0 else f"repair_{attempt}"
            out["sg"] = node.get("sg_name")
            out["model"] = model
            out["model_tier"] = tier.value
            out["skill_chars"] = len(skill_text)
            out["reasoning_effort"] = out.get("reasoning_effort") or flags.get("reasoning_effort")
            ledger.record(
                nid,
                node.get("sg_name") or "",
                model,
                out.get("usage") if isinstance(out.get("usage"), dict) else None,
                error=out.get("error"),
            )

            # toolbelt pass
            if flags["tools"] and isinstance(out.get("parsed"), dict):
                tool_results = tools.run_requested(out["parsed"])
                if tool_results:
                    out["tool_results"] = tool_results
                    # one follow-up with tool results (not counted as repair)
                    follow = (
                        user
                        + "\n\nTOOL RESULTS:\n"
                        + json.dumps(tool_results)[:8000]
                        + "\n\nIntegrate tool results and return final JSON for this node."
                    )
                    out2 = call_grok(
                        follow,
                        system,
                        model,
                        api_key,
                        flags["max_tokens"],
                        reasoning_effort=flags.get("reasoning_effort") or "high",
                        timeout_s=flags.get("http_timeout") or 600,
                    )
                    out2["mode"] = "tool_followup"
                    out2["sg"] = node.get("sg_name")
                    out2["model"] = model
                    out2["tool_results"] = tool_results
                    out2["skill_chars"] = len(skill_text)
                    ledger.record(
                        nid,
                        node.get("sg_name") or "",
                        model,
                        out2.get("usage") if isinstance(out2.get("usage"), dict) else None,
                        error=out2.get("error"),
                    )
                    if not out2.get("error"):
                        out = out2

            # materialize artifacts
            if isinstance(out.get("parsed"), dict):
                written = vault.materialize_from_parsed(nid, out["parsed"])
                if written:
                    out["artifacts_written"] = written

            if should_retry(out, attempt, flags["max_retries"]):
                attempt += 1
                journal.event("retry", node_id=nid, attempt=attempt, error=out.get("error"))
                continue
            break

        journal.event(
            "node_done",
            node_id=nid,
            sg=node.get("sg_name"),
            model=model,
            tier=tier.value,
            error=out.get("error"),
            win=(out.get("parsed") or {}).get("win") if isinstance(out.get("parsed"), dict) else None,
        )
        return {
            "id": nid,
            "sg_name": node.get("sg_name"),
            "binary_id": node.get("binary_id"),
            "model": model,
            "model_tier": tier.value,
            "output": out,
        }

    # Schedule
    layers = topo_layers(nodes, edges)
    # If edges empty (linear craft), force serial order of node ids
    if not edges and nodes:
        layers = [[n["id"]] for n in nodes]

    for layer in layers:
        wave = ready_wave(layer, run_one, parallel=bool(flags["parallel"]) and not dry)
        for nid, result in wave.items():
            node_results_map[nid] = result
            blackboard[f"{nid}.output"] = result["output"]

    # preserve graph order in results
    node_results = [node_results_map[n["id"]] for n in nodes if n["id"] in node_results_map]
    sink = node_results[-1] if node_results else None
    final = None
    if sink and isinstance(sink.get("output"), dict):
        final = sink["output"].get("parsed") or sink["output"].get("content") or sink["output"]

    fails = [n for n in node_results if not contract_ok(n.get("output"))]
    fails += [
        n
        for n in node_results
        if n not in fails
        and str((n["output"].get("parsed") or {}).get("win", "")).upper() == "FAIL"
    ]
    artifacts_written = sum(
        len(n["output"].get("artifacts_written") or [])
        for n in node_results
        if isinstance(n.get("output"), dict)
    )
    # Decisive node: last judge-flavored node, else sink (WC gate 4)
    decisive = sink
    for n in reversed(node_results):
        nid_node = by_id.get(n["id"], {})
        if nid_node.get("judge") or (nid_node.get("category") or "").lower() in {"eval", "crit", "review"}:
            decisive = n
            break
    decisive_win = None
    if decisive and isinstance(decisive.get("output"), dict):
        p = decisive["output"].get("parsed")
        if isinstance(p, dict):
            decisive_win = str(p.get("win", "")).upper() or None
    if dry:
        win = "DRY"
    else:
        win = "PASS" if (not fails and decisive_win == "PASS") else "FAIL"
    error_hint = None
    if fails:
        fo = fails[0].get("output") or {}
        error_hint = fo.get("detail") or fo.get("error")
        if isinstance(error_hint, str) and "disabled" in error_hint.lower():
            error_hint = (
                "XAI_API_KEY is disabled at console.x.ai — enable or replace the key in .env. "
                "Dry-run confirms the toolkit pipeline."
            )

    memory.remember_from_run(goal, final, node_results)
    ledger_payload = ledger.flush()
    journal.event("end", win=win, failed=[f["id"] for f in fails])

    return {
        "win": win,
        "slug": slug,
        "goal": goal,
        "dry_run": dry,
        "run_id": journal.run_id,
        "nodes": len(node_results),
        "node_results": node_results,
        "result": final,
        "failed_nodes": [f["id"] for f in fails],
        "decisive_node": decisive["id"] if decisive else None,
        "decisive_win": decisive_win,
        "artifacts_written": artifacts_written,
        "error_hint": error_hint,
        "api_key_present": bool(api_key),
        "ledger": ledger_payload["totals"],
        "artifacts_index": str((harness_root / "artifacts" / "index.json").relative_to(repo))
        if (harness_root / "artifacts" / "index.json").is_file()
        else None,
        "journal": str(journal.path.relative_to(repo)),
        "memory": str((harness_root / "memory" / "blackboard.json").relative_to(repo))
        if flags["memory"]
        else None,
        "toolkit": {
            "parallel": flags["parallel"],
            "memory": flags["memory"],
            "tools": flags["tools"],
            "max_retries": flags["max_retries"],
            "models": {
                "strong": flags["model"],
                "fast": flags["model_fast"],
                "judge": flags["model_judge"],
            },
        },
        "blackboard_keys": list(blackboard.keys()),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Run OPGROK harness (toolkit-enabled)")
    ap.add_argument("slug")
    ap.add_argument("--goal", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-tokens", type=int, default=None)
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--serial", action="store_true", help="Disable parallel layers")
    ap.add_argument("--no-memory", action="store_true")
    ap.add_argument("--no-tools", action="store_true")
    args = ap.parse_args()
    payload = run_harness(
        args.slug,
        goal=args.goal,
        dry_run=args.dry_run,
        max_tokens=args.max_tokens,
        repo=Path(args.repo),
        serial=args.serial,
        no_memory=args.no_memory,
        no_tools=args.no_tools,
    )
    print(json.dumps(payload, indent=2))
    return 0 if payload.get("win") in {"PASS", "DRY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

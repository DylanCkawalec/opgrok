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
import copy
import json
import os
import re
import signal
import sys
import time
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
from toolkit.live_ui import LiveBoard  # noqa: E402
from toolkit.product import (  # noqa: E402
    compile_product,
    compile_repair_user,
    extract_json_object,
    has_rust_sources,
    node_max_tokens,
    pick_repair_node,
)
from toolkit.tools import redact  # noqa: E402

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def emit_progress(harness_root: Path | None, slug: str, stage: str, **kw) -> None:
    """Always-on stage line so a live run is never silent.

    Writes stderr (flushed) + core/binaries/<slug>/progress.jsonl + STATUS.
    """
    bits = [f"OPGROK[{slug}]", stage]
    for k, v in kw.items():
        if v is None or v == "":
            continue
        bits.append(f"{k}={v}")
    line = " ".join(str(b) for b in bits)
    print(line, file=sys.stderr, flush=True)
    if harness_root is None:
        return
    rec = {"ts": time.time(), "slug": slug, "stage": stage, **kw}
    try:
        prog = harness_root / "progress.jsonl"
        with prog.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, default=str) + "\n")
            fh.flush()
        (harness_root / "STATUS").write_text(line + "\n", encoding="utf-8")
    except Exception:
        pass


def _retry_why(out: dict | None) -> str:
    if not isinstance(out, dict):
        return "empty_output"
    if out.get("error"):
        return f"api_error:{out.get('error')}"
    fr = str(out.get("finish_reason") or "")
    if fr in {"length", "max_tokens"}:
        return "truncated"
    p = out.get("parsed")
    if not isinstance(p, dict):
        return "reply_not_json"
    missing = [k for k in CONTRACT_KEYS if k not in p]
    if missing:
        return "missing_keys:" + ",".join(missing)
    w = win_norm(out)
    if w != "PASS":
        return f"win={w or 'empty'}"
    return "contract_retry"


def classify_error(fails: list, ledger: dict | None = None) -> str:
    """Class-coded error_hint — no raw bodies, no key state."""
    if any((n.get("status") == "RetryExhausted") for n in fails):
        return "retry_exhausted"
    for n in fails:
        out = n.get("output") or {}
        err = str(out.get("error") or "")
        if err.startswith("http_401") or err.startswith("http_403"):
            return "api_key_unauthorized"
        if err.startswith("http_429"):
            return "rate_limited"
        if "timeout" in err.lower():
            return "timeout"
        if not contract_ok(out):
            return "contract_violation"
    return "run_failed"


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
        pass
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        inner = fence.group(1).strip()
        try:
            return json.loads(inner)
        except Exception:
            blob = extract_json_object(inner)
            if blob:
                try:
                    return json.loads(blob)
                except Exception:
                    pass
    blob = extract_json_object(text)
    if blob:
        try:
            return json.loads(blob)
        except Exception:
            return None
    return None


CONTRACT_KEYS = ("summary", "artifacts", "win")
GOAL_STOPWORDS = frozenset(
    {"the", "a", "an", "for", "with", "and", "or", "of", "to", "in", "is", "on", "at", "by"}
)
PRODUCER_ROLES = frozenset({"forge", "smith", "seal"})
JUDGE_CATS = frozenset({"eval", "crit", "review"})


def contract_ok(out: dict | None) -> bool:
    """WC gate 2 structural base: error-free output with summary/artifacts/win keys."""
    if not isinstance(out, dict) or out.get("error"):
        return False
    p = out.get("parsed")
    return isinstance(p, dict) and all(k in p for k in CONTRACT_KEYS)


def _parsed(out: dict | None) -> dict | None:
    if not isinstance(out, dict):
        return None
    p = out.get("parsed")
    return p if isinstance(p, dict) else None


def win_norm(out: dict | None) -> str:
    """Normalize parsed.win: non-string/empty ⇒ ''."""
    p = _parsed(out)
    if p is None:
        return ""
    w = p.get("win")
    if not isinstance(w, str):
        return ""
    return w.strip().upper()


def win_pass(out: dict | None) -> bool:
    return win_norm(out) == "PASS"


def win_fail(out: dict | None) -> bool:
    return win_norm(out) == "FAIL"


def goal_tokens(text: str) -> set[str]:
    return {
        t
        for t in re.split(r"[^a-z0-9\-]+", (text or "").lower())
        if len(t) > 2 and t not in GOAL_STOPWORDS
    }


def _is_producer(node: dict, parsed: dict | None) -> bool:
    role = (node.get("role") or "").lower()
    if role in PRODUCER_ROLES:
        return True
    arts = (parsed or {}).get("artifacts") if parsed else None
    return isinstance(arts, list) and len(arts) > 0


def _is_judge_flavored(node: dict) -> bool:
    if node.get("judge"):
        return True
    return (node.get("category") or "").lower() in JUDGE_CATS


def _has_materialized(out: dict | None) -> bool:
    if not isinstance(out, dict):
        return False
    written = out.get("artifacts_written") or []
    if not isinstance(written, list):
        return False
    for w in written:
        if isinstance(w, dict) and int(w.get("bytes") or 0) > 0:
            return True
    return False


def is_dry(out: dict | None) -> bool:
    """PassBody IsDry: produced without a live API call."""
    if not isinstance(out, dict):
        return False
    return out.get("mode") == "dry_run"


def producer_artifact(out: dict | None, node: dict | None) -> bool:
    """Gate 3: non-decisive producer with declared artifacts and bytes>0 on disk."""
    parsed = _parsed(out)
    node = node or {}
    if not _is_producer(node, parsed):
        return False
    arts = parsed.get("artifacts") if parsed else None
    if not isinstance(arts, list) or len(arts) == 0:
        return False
    return _has_materialized(out)


def substantive_contract(out: dict | None, node: dict | None, goal: str) -> bool:
    """PassBody Substantive + ContractOK + WinPass for this node's role."""
    if not contract_ok(out):
        return False
    if not win_pass(out):
        return False
    parsed = _parsed(out)
    node = node or {}
    if _is_producer(node, parsed):
        arts = parsed.get("artifacts") if parsed else None
        if not isinstance(arts, list) or len(arts) == 0:
            return False
        if not _has_materialized(out):
            return False
    if _is_judge_flavored(node) or node.get("decisive"):
        summary = str((parsed or {}).get("summary") or "")
        if not (goal_tokens(summary) & goal_tokens(goal or "")):
            return False
    return True


def pick_decisive(node_results: list, by_id: dict) -> dict | None:
    """Last judge-flavored node in declared order, else sink (positional last)."""
    if not node_results:
        return None
    decisive = node_results[-1]
    for n in reversed(node_results):
        if _is_judge_flavored(by_id.get(n["id"], {})):
            return n
    return decisive


def seal_verdict(
    node_results: list,
    by_id: dict,
    goal: str,
    dry: bool,
    ledger_totals: dict | None,
) -> dict:
    """Shipped PassBody seal. Dry short-circuits to DRY before live gates."""
    decisive = pick_decisive(node_results, by_id)
    fails = [n for n in node_results if not contract_ok(n.get("output"))]
    fails += [n for n in node_results if n not in fails and win_fail(n.get("output"))]
    fails += [n for n in node_results if n not in fails and not win_pass(n.get("output"))]
    # Gate 3: TLA Substantive — hollow analysis nodes are not producers (H ∉ SubstantiveOuts)
    has_producer_artifact = any(
        producer_artifact(n.get("output"), by_id.get(n["id"], {}))
        and decisive is not None
        and n["id"] != decisive["id"]
        for n in node_results
    )
    has_tokens = int((ledger_totals or {}).get("total_tokens") or 0) > 0
    decisive_win = win_norm(decisive.get("output") if decisive else None) or None
    dry_contaminated = (not dry) and any(is_dry(n.get("output")) for n in node_results)
    all_substantive = all(
        substantive_contract(n.get("output"), by_id.get(n["id"], {}), goal)
        for n in node_results
    )
    if dry:
        win = "DRY"
    elif fails or decisive_win != "PASS":
        win = "FAIL"
    elif dry_contaminated:
        win = "FAIL"
    elif not all_substantive:
        win = "FAIL"
    elif not has_producer_artifact:
        win = "FAIL"
    elif not has_tokens:
        win = "FAIL"
    elif not substantive_contract(
        decisive.get("output") if decisive else None,
        by_id.get(decisive["id"], {}) if decisive else {},
        goal,
    ):
        win = "FAIL"
    else:
        win = "PASS"
    return {
        "win": win,
        "fails": fails,
        "decisive": decisive,
        "decisive_win": decisive_win,
        "has_producer_artifact": has_producer_artifact,
        "has_tokens": has_tokens,
    }


def call_grok(
    prompt: str,
    system: str,
    model: str,
    api_key: str,
    max_tokens: int,
    reasoning_effort: str | None = None,
    timeout_s: int | None = None,
    on_delta=None,
    stream: bool = True,
) -> dict:
    """Chat Completions. Streams by default so STATUS can show live char counts."""
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
    if stream:
        body["stream"] = True
        body["stream_options"] = {"include_usage": True}

    timeout = timeout_s or int(os.environ.get("OPGROK_HTTP_TIMEOUT", "600"))
    req_id = ""
    req = urllib.request.Request(
        "https://api.x.ai/v1/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "opgrok-harness/3.0",
            "Accept": "text/event-stream" if stream else "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            req_id = resp.headers.get("x-request-id") or resp.headers.get("X-Request-Id") or ""
            if stream:
                out = _read_sse(resp, body, on_delta)
                if req_id:
                    out["request_id"] = req_id
                return out
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
        "request_id": req_id,
    }


def _read_sse(resp, body: dict, on_delta) -> dict:
    content_parts: list[str] = []
    reason_parts: list[str] = []
    usage = None
    finish_reason = None
    model = body.get("model")
    buf = ""
    while True:
        chunk = resp.read(2048)
        if not chunk:
            break
        buf += chunk.decode("utf-8", errors="ignore")
        while "\n" in buf:
            line, buf = buf.split("\n", 1)
            line = line.strip()
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                continue
            try:
                ev = json.loads(payload)
            except json.JSONDecodeError:
                continue
            if ev.get("usage"):
                usage = ev["usage"]
            if ev.get("model"):
                model = ev.get("model")
            chs = ev.get("choices") or []
            if not chs:
                continue
            fr = chs[0].get("finish_reason")
            if fr:
                finish_reason = fr
            delta = chs[0].get("delta") or {}
            c = delta.get("content") or ""
            r = delta.get("reasoning_content") or delta.get("reasoning") or ""
            if c:
                content_parts.append(c)
                if on_delta:
                    on_delta("content", c)
            if r:
                reason_parts.append(r)
                if on_delta:
                    on_delta("reason", r)
    content = "".join(content_parts)
    reasoning = "".join(reason_parts) or None
    return {
        "content": content,
        "reasoning_content": reasoning,
        "reasoning_effort": body.get("reasoning_effort"),
        "parsed": try_parse_json(content),
        "usage": usage,
        "model": model,
        "streamed": True,
        "stream_chars": len(content),
        "finish_reason": finish_reason,
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
            parsed = v.get("parsed") if isinstance(v.get("parsed"), dict) else {}
            arts = parsed.get("artifacts") if parsed else None
            names = []
            if isinstance(arts, list):
                for a in arts[:24]:
                    if isinstance(a, dict):
                        names.append(
                            {
                                "name": a.get("name") or a.get("path"),
                                "bytes": len(str(a.get("content") or "")),
                            }
                        )
            written = v.get("artifacts_written") or []
            slim[k] = {
                "summary": parsed.get("summary") if parsed else None,
                "content_preview": v["content"][:1200],
                "win": parsed.get("win") if parsed else None,
                "artifact_names": names,
                "artifacts_on_disk": [
                    {"name": w.get("name"), "path": w.get("path"), "bytes": w.get("bytes")}
                    for w in written
                    if isinstance(w, dict)
                ][:24],
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
Do not request a shell tool.

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
  - artifacts (array of {{name, content, kind}} holding the REAL deliverable. Empty [] only
    for pure-analysis nodes. Producer roles (forge/smith/seal) must attach at least one
    artifact with real content — not a filename stub.
    If the goal is to ship a program, write COMPILABLE files, not descriptions:
      {{"name":"src/main.rs","content":"<full rust source>","kind":"rust"}}
      {{"name":"src/lib.rs","content":"...","kind":"rust"}}
      {{"name":"Cargo.toml","content":"...","kind":"toml"}}
    The harness harvests those names into product/ and cargo-builds them. Do not
    describe the program instead of writing it. Do not ask for a template.)
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
    catalog = blackboard.get("artifacts_catalog") or []
    cat_block = ""
    if catalog:
        cat_block = (
            "\nPRIOR ARTIFACTS ON DISK (read_file these paths; do not restate):\n"
            + json.dumps(catalog, indent=2)[:4000]
            + "\n"
        )
    return f"""GOAL:
{goal}

NODE: {node.get('id')} ({node.get('sg_name')})
PROCESS: {node.get('ipo', {}).get('process')}
OODA.ACT: {node.get('ooda', {}).get('act')}
INPUT KEYS: {node.get('ipo', {}).get('inputs')}
{cat_block}
BLACKBOARD (thrift):
{json.dumps(thrift_bb(blackboard), indent=2)[:14000]}

If this node ships a program, artifacts must be full files named src/main.rs, src/*.rs, Cargo.toml.
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
    _crash_after: int | None = None,
) -> dict:
    repo = repo or ROOT
    if not SLUG_RE.match(slug or ""):
        return {
            "win": "FAIL",
            "error": "invalid_slug",
            "slug": slug,
            "dry_run": True,
            "api_key_present": False,
        }
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
            "WARN: API key missing/empty after load_repo_env — forcing dry-run. "
            "Set a live key in monorepo .env. "
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
    vault = ArtifactVault(harness_root, run_id=journal.run_id)
    memory = MemoryStore(harness_root, enabled=flags["memory"])
    tools = Toolbelt(
        repo,
        harness_root,
        allow_net=flags["allow_net"],
        allow_shell=False,
        redact_key=api_key or None,
    )

    blackboard: dict = {"goal": goal, "artifacts_catalog": []}
    memory.load_into(blackboard, goal=goal)
    if memory.schema_warning:
        journal.event("memory_schema", warning="unknown_or_corrupt")
    vision_refs = collect_vision_refs(goal, repo, blackboard)
    if vision_refs:
        blackboard["vision_refs"] = vision_refs

    journal.event("start", slug=slug, goal=goal, dry=dry, nodes=len(nodes), flags=flags)
    board = LiveBoard(harness_root, slug, nodes)
    prev_sig = None
    try:
        prev_sig = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
    except Exception:
        prev_sig = None
    board.begin(journal.run_id, str(flags.get("model") or ""), dry)
    skills_cache = harness_root / "skills_cache"
    node_results_map: dict[str, dict] = {}

    def run_one(nid: str, bb_view: dict | None = None) -> dict:
        if _crash_after is not None and len(node_results_map) >= _crash_after:
            raise RuntimeError("test_crash")
        node = by_id[nid]
        skill_text = read_skill(
            repo, node.get("skill_path") or "", skills_cache, node.get("sg_name") or "x"
        )
        model, tier = pick_model(node, flags)
        system = build_system(node, skill_text, vision_refs, flags["tools"])
        user = build_user(goal, node, bb_view if bb_view is not None else blackboard)

        attempt = 0
        out: dict = {}
        job = re.sub(r"\s+", "-", (node.get("intent") or node.get("purpose") or node.get("sg_name") or "")[:56])
        budget = node_max_tokens(node, flags)
        board.node_begin(nid, node.get("sg_name") or "", job, model, budget)
        journal.event("node_start", node_id=nid, sg=node.get("sg_name"), model=model)
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
                ledger.record(nid, node.get("sg_name") or "", model, None, phase="dry", dry=True)
                break

            out = call_grok(
                user if attempt == 0 else repair_prompt(goal, node, out, attempt),
                system,
                model,
                api_key,
                budget,
                reasoning_effort=flags.get("reasoning_effort") or "high",
                timeout_s=flags.get("http_timeout") or 600,
                on_delta=board.on_delta,
            )
            out["mode"] = "live" if attempt == 0 else f"repair_{attempt}"
            out["sg"] = node.get("sg_name")
            out["model"] = model
            out["model_tier"] = tier.value
            out["skill_chars"] = len(skill_text)
            out["reasoning_effort"] = out.get("reasoning_effort") or flags.get("reasoning_effort")
            usage = out.get("usage") if isinstance(out.get("usage"), dict) else None
            ledger.record(
                nid,
                node.get("sg_name") or "",
                model,
                usage,
                error=redact(out.get("error"), api_key),
                phase="initial" if attempt == 0 else f"repair_{attempt}",
            )
            board.node_api_done(
                nid,
                node.get("sg_name") or "",
                tokens=(usage or {}).get("total_tokens"),
                win=win_norm(out) or None,
                why=_retry_why(out) if not win_pass(out) else "ok",
                finish=out.get("finish_reason"),
                arts=len(out.get("artifacts_written") or []) if isinstance(out.get("artifacts_written"), list) else 0,
                req=out.get("request_id"),
            )
            ledger.flush()

            # toolbelt pass
            if flags["tools"] and isinstance(out.get("parsed"), dict):
                tool_results = tools.run_requested(
                    out["parsed"],
                    node_id=nid,
                    vault=vault,
                    run_id=journal.run_id,
                )
                if tool_results:
                    out["tool_results"] = redact(tool_results, api_key)
                    # one follow-up with tool results (not counted as repair)
                    follow = (
                        user
                        + "\n\nTOOL RESULTS:\n"
                        + json.dumps(tool_results)[:8000]
                        + "\n\nIntegrate tool results and return final JSON for this node."
                    )
                    board.event("tool_followup", node=nid, sg=node.get("sg_name"))
                    out2 = call_grok(
                        follow,
                        system,
                        model,
                        api_key,
                        budget,
                        reasoning_effort=flags.get("reasoning_effort") or "high",
                        timeout_s=flags.get("http_timeout") or 600,
                        on_delta=board.on_delta,
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
                        error=redact(out2.get("error"), api_key),
                        phase="tool_followup",
                    )
                    if not out2.get("error"):
                        out = out2

            # materialize artifacts
            if isinstance(out.get("parsed"), dict):
                discarded = should_retry(out, attempt, flags["max_retries"])
                written = vault.materialize_from_parsed(
                    nid,
                    out["parsed"],
                    attempt=attempt,
                    discarded=discarded,
                    run_id=journal.run_id,
                )
                if written:
                    out["artifacts_written"] = written

            if should_retry(out, attempt, flags["max_retries"]):
                attempt += 1
                why = _retry_why(out)
                if why in {"truncated", "reply_not_json"} or why.startswith("missing_keys"):
                    budget = min(max(budget * 2, budget + 8192), 65536)
                journal.event("retry", node_id=nid, attempt=attempt, error=out.get("error"))
                board.retry(nid, attempt, why, budget)
                continue
            break

        repair_good = contract_ok(out) and not win_fail(out)
        if dry or repair_good:
            node_status = "Valid"
        elif attempt >= flags["max_retries"]:
            node_status = "RetryExhausted"
        else:
            node_status = "Invalid"

        journal.event(
            "node_done",
            node_id=nid,
            sg=node.get("sg_name"),
            model=model,
            tier=tier.value,
            error=out.get("error"),
            status=node_status,
            win=win_norm(out) or None,
        )
        board.node_end(
            nid,
            node_status,
            win_norm(out) or None,
            len(out.get("artifacts_written") or []) if isinstance(out, dict) else 0,
        )
        ledger.flush()
        result = {
            "id": nid,
            "sg_name": node.get("sg_name"),
            "binary_id": node.get("binary_id"),
            "model": model,
            "model_tier": tier.value,
            "status": node_status,
            "output": out,
        }
        node_results_map[nid] = result
        return result

    # Schedule
    layers = topo_layers(nodes, edges)
    # If edges empty (linear craft), force serial order of node ids
    if not edges and nodes:
        layers = [[n["id"]] for n in nodes]

    try:
        for layer in layers:
            board.event(
                "wave",
                nodes=",".join(layer),
                parallel=bool(flags["parallel"]) and not dry and len(layer) > 1,
            )
            snap = copy.deepcopy(blackboard)
            wave = ready_wave(
                layer,
                lambda nid, s=snap: run_one(nid, s),
                parallel=bool(flags["parallel"]) and not dry,
            )
            for nid, result in wave.items():
                node_results_map[nid] = result
                blackboard[f"{nid}.output"] = result["output"]
                cat = blackboard.setdefault("artifacts_catalog", [])
                out = result.get("output") if isinstance(result.get("output"), dict) else {}
                for w in out.get("artifacts_written") or []:
                    if isinstance(w, dict):
                        cat.append(
                            {
                                "node": nid,
                                "name": w.get("name"),
                                "path": w.get("path"),
                                "bytes": w.get("bytes"),
                            }
                        )
    except KeyboardInterrupt:
        ledger_payload = ledger.flush()
        journal.event("end", win="FAIL", error="cancelled")
        board.cancel()
        return {
            "win": "FAIL",
            "error": "cancelled",
            "slug": slug,
            "goal": goal,
            "dry_run": dry,
            "run_id": journal.run_id,
            "nodes": len(node_results_map),
            "api_key_present": bool(api_key),
            "ledger": ledger_payload["totals"],
        }
    except Exception as exc:  # noqa: BLE001
        ledger_payload = ledger.flush()
        journal.event("end", win="FAIL", error=redact(str(exc), api_key), partial=True)
        board.event("fail", error="partial_run")
        board.stop()
        return {
            "win": "FAIL",
            "error": "partial_run",
            "slug": slug,
            "goal": goal,
            "dry_run": dry,
            "run_id": journal.run_id,
            "partial_node_results": [
                node_results_map[n["id"]] for n in nodes if n["id"] in node_results_map
            ],
            "nodes": len(node_results_map),
            "failed_nodes": list(node_results_map.keys()),
            "api_key_present": bool(api_key),
            "ledger": ledger_payload["totals"],
        }

    # preserve graph order in results
    node_results = [node_results_map[n["id"]] for n in nodes if n["id"] in node_results_map]
    sink = node_results[-1] if node_results else None
    final = None
    if sink and isinstance(sink.get("output"), dict):
        final = sink["output"].get("parsed") or sink["output"].get("content") or sink["output"]

    artifacts_written = sum(
        len(n["output"].get("artifacts_written") or [])
        for n in node_results
        if isinstance(n.get("output"), dict)
    )
    ledger_payload = ledger.flush()
    sealed = seal_verdict(node_results, by_id, goal, dry, ledger_payload["totals"])
    win = sealed["win"]
    fails = sealed["fails"]
    decisive = sealed["decisive"]
    decisive_win = sealed["decisive_win"]
    exhausted_nodes = [n["id"] for n in node_results if n.get("status") == "RetryExhausted"]
    error_hint = classify_error(fails or node_results, ledger_payload["totals"]) if (fails or win == "FAIL") else None
    if error_hint:
        error_hint = redact(error_hint, api_key)

    memory.remember_from_run(goal, final, node_results, verdict=win, run_id=journal.run_id)
    journal.event("end", win=win, failed=[f["id"] for f in fails], exhausted=exhausted_nodes)
    board.seal(win, int((ledger_payload.get("totals") or {}).get("total_tokens") or 0), artifacts_written)

    harvest = {"product": None, "files": [], "count": 0}
    product_build = None
    compile_repair = None
    if not dry:
        harvest = vault.harvest_product(harness_root / "product", run_id=journal.run_id)
        board.harvest(list(harvest.get("files") or []))
        if win != "FAIL" and has_rust_sources(harvest):
            product_build = compile_product(repo, slug)
            board.compile(
                product_build.get("ok"),
                product_build.get("method"),
                product_build.get("rc"),
            )
            journal.event("product_build", rc=product_build.get("rc"), files=harvest.get("count"))
            repairs_left = int(flags.get("compile_repairs") or 0)
            repair_node = pick_repair_node(nodes)
            while (
                repairs_left > 0
                and product_build
                and not product_build.get("ok")
                and repair_node
                and api_key
            ):
                repairs_left -= 1
                model, _tier = pick_model(repair_node, flags)
                system = build_system(repair_node, "", vision_refs, False)
                user = compile_repair_user(
                    goal,
                    (product_build.get("stderr_tail") or "") + "\n" + (product_build.get("stdout_tail") or ""),
                    list(harvest.get("files") or []),
                    str(harness_root / "product"),
                )
                board.event("compile_repair", sg=repair_node.get("sg_name"), left=repairs_left)
                repaired = call_grok(
                    user,
                    system,
                    model,
                    api_key,
                    node_max_tokens(repair_node, flags),
                    reasoning_effort=flags.get("reasoning_effort") or "high",
                    timeout_s=flags.get("http_timeout") or 600,
                    on_delta=board.on_delta,
                )
                written = []
                if isinstance(repaired.get("parsed"), dict):
                    written = vault.materialize_from_parsed(
                        repair_node.get("id") or "repair",
                        repaired["parsed"],
                        attempt=0,
                        discarded=False,
                        run_id=journal.run_id,
                    )
                harvest = vault.harvest_product(harness_root / "product", run_id=journal.run_id)
                product_build = compile_product(repo, slug)
                compile_repair = {
                    "sg": repair_node.get("sg_name"),
                    "node_id": repair_node.get("id"),
                    "artifacts_written": len(written),
                    "rc": product_build.get("rc"),
                    "ok": product_build.get("ok"),
                }
                ledger.record(
                    repair_node.get("id") or "repair",
                    repair_node.get("sg_name") or "compile-repair",
                    model,
                    repaired.get("usage") if isinstance(repaired.get("usage"), dict) else None,
                    error=redact(repaired.get("error"), api_key),
                    phase="compile_repair",
                )
                journal.event(
                    "compile_repair",
                    sg=repair_node.get("sg_name"),
                    rc=product_build.get("rc"),
                    files=harvest.get("count"),
                )
                if product_build.get("ok"):
                    break
        if compile_repair is not None:
            ledger_payload = ledger.flush()

    payload = {
        "win": win,
        "slug": slug,
        "goal": goal,
        "dry_run": dry,
        "run_id": journal.run_id,
        "nodes": len(node_results),
        "node_results": node_results,
        "result": final,
        "failed_nodes": [f["id"] for f in fails],
        "exhausted_nodes": exhausted_nodes,
        "decisive_node": decisive["id"] if decisive else None,
        "decisive_win": decisive_win,
        "artifacts_written": artifacts_written,
        "product_harvest": harvest,
        "product_build": product_build,
        "compile_repair": compile_repair,
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
    board.stop()
    return payload


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
    try:
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
    except KeyboardInterrupt:
        print("OPGROK cancelled", file=sys.stderr, flush=True)
        return 130
    key = (os.environ.get("XAI_API_KEY") or os.environ.get("xai_api_key") or "").strip()
    print(json.dumps(redact(payload, key or None), indent=2))
    return 0 if payload.get("win") in {"PASS", "DRY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

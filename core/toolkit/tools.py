"""Node toolbelt — safe defaults for Grok SuperGrok nodes."""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class Toolbelt:
    def __init__(self, repo: Path, harness_root: Path, allow_net: bool = True, allow_shell: bool = False):
        self.repo = repo
        self.harness_root = harness_root
        self.allow_net = allow_net
        self.allow_shell = allow_shell
        self.artifacts = harness_root / "artifacts"
        self.artifacts.mkdir(parents=True, exist_ok=True)

    def run_requested(self, parsed: Any) -> list[dict[str, Any]]:
        """Execute optional tool_calls from model JSON: [{tool, args}]."""
        if not isinstance(parsed, dict):
            return []
        calls = parsed.get("tool_calls") or parsed.get("tools") or []
        if not isinstance(calls, list):
            return []
        results = []
        for c in calls[:8]:  # thrift
            if not isinstance(c, dict):
                continue
            tool = (c.get("tool") or c.get("name") or "").lower()
            args = c.get("args") or c.get("arguments") or {}
            try:
                if tool in {"read_file", "read"}:
                    results.append({"tool": tool, "ok": True, "result": self.read_file(str(args.get("path", "")))})
                elif tool in {"grep", "search"}:
                    results.append(
                        {
                            "tool": tool,
                            "ok": True,
                            "result": self.grep(str(args.get("pattern", "")), str(args.get("path", "."))),
                        }
                    )
                elif tool in {"web_fetch", "fetch", "http_get"}:
                    results.append(
                        {
                            "tool": tool,
                            "ok": True,
                            "result": self.web_fetch(str(args.get("url", ""))),
                        }
                    )
                elif tool in {"write_artifact", "write"}:
                    results.append(
                        {
                            "tool": tool,
                            "ok": True,
                            "result": self.write_artifact(
                                str(args.get("name", "out.txt")),
                                str(args.get("content", "")),
                            ),
                        }
                    )
                elif tool == "shell" and self.allow_shell:
                    results.append(
                        {
                            "tool": tool,
                            "ok": True,
                            "result": self.shell(str(args.get("cmd", "echo blocked"))),
                        }
                    )
                else:
                    results.append({"tool": tool, "ok": False, "error": "unknown_or_denied"})
            except Exception as e:  # noqa: BLE001
                results.append({"tool": tool, "ok": False, "error": str(e)})
        return results

    def read_file(self, rel: str, max_chars: int = 8000) -> dict[str, Any]:
        p = (self.repo / rel).resolve()
        if not str(p).startswith(str(self.repo.resolve())):
            return {"error": "path_escape"}
        if not p.is_file():
            return {"error": "not_found", "path": rel}
        text = p.read_text(encoding="utf-8", errors="ignore")
        return {"path": rel, "content": text[:max_chars], "truncated": len(text) > max_chars}

    def grep(self, pattern: str, rel: str = ".", max_hits: int = 30) -> dict[str, Any]:
        root = (self.repo / rel).resolve()
        if not str(root).startswith(str(self.repo.resolve())):
            return {"error": "path_escape"}
        try:
            rx = re.compile(pattern)
        except re.error as e:
            return {"error": f"bad_regex: {e}"}
        hits = []
        paths = [root] if root.is_file() else root.rglob("*")
        for p in paths:
            if not p.is_file():
                continue
            if any(x in p.parts for x in {".git", "node_modules", "target", ".venv", "__pycache__"}):
                continue
            try:
                for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if rx.search(line):
                        hits.append(
                            {
                                "path": str(p.relative_to(self.repo)),
                                "line": i,
                                "text": line[:200],
                            }
                        )
                        if len(hits) >= max_hits:
                            return {"hits": hits, "truncated": True}
            except Exception:
                continue
        return {"hits": hits, "truncated": False}

    def web_fetch(self, url: str, max_chars: int = 12000) -> dict[str, Any]:
        if not self.allow_net:
            return {"error": "net_disabled"}
        if not url.startswith("http://") and not url.startswith("https://"):
            return {"error": "bad_url"}
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "opgrok-toolkit/1.0"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="ignore")
                return {
                    "url": url,
                    "status": getattr(resp, "status", 200),
                    "content": raw[:max_chars],
                    "truncated": len(raw) > max_chars,
                }
        except urllib.error.HTTPError as e:
            return {"error": f"http_{e.code}", "url": url}
        except Exception as e:  # noqa: BLE001
            return {"error": str(e), "url": url}

    def write_artifact(self, name: str, content: str) -> dict[str, Any]:
        safe = re.sub(r"[^a-zA-Z0-9._\-]+", "-", name).strip("-")[:80] or "out.txt"
        path = self.artifacts / safe
        path.write_text(content, encoding="utf-8")
        return {"path": str(path.relative_to(self.harness_root)), "bytes": path.stat().st_size}

    def shell(self, cmd: str) -> dict[str, Any]:
        if not self.allow_shell:
            return {"error": "shell_disabled"}
        import subprocess

        # hard deny patterns
        if re.search(r"rm\s+-rf|mkfs|dd\s+if=|:(){:|:&};:", cmd):
            return {"error": "denied_pattern"}
        r = subprocess.run(
            cmd,
            shell=True,
            cwd=str(self.repo),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "code": r.returncode,
            "stdout": r.stdout[:8000],
            "stderr": r.stderr[:4000],
        }

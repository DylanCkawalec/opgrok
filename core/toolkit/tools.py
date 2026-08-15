"""Node toolbelt — safe defaults for Grok SuperGrok nodes."""
from __future__ import annotations

import ipaddress
import json
import re
import socket
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SENSITIVE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_ed25519",
}
SENSITIVE_SUFFIXES = (".pem", ".key")


def redact(text: Any, key: str | None) -> Any:
    """Replace every occurrence of the live key with [REDACTED]."""
    if not key:
        return text
    if isinstance(text, str):
        return text.replace(key, "[REDACTED]")
    if isinstance(text, list):
        return [redact(x, key) for x in text]
    if isinstance(text, dict):
        return {k: redact(v, key) for k, v in text.items()}
    return text


def contained(p: Path, root: Path) -> bool:
    try:
        p.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def is_sensitive_path(p: Path) -> bool:
    name = p.name
    if name in SENSITIVE_NAMES:
        return True
    if name.endswith(SENSITIVE_SUFFIXES):
        return True
    return False


def _blocked_ip(ip: str) -> bool:
    addr = ipaddress.ip_address(ip)
    return bool(
        addr.is_loopback
        or addr.is_private
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )


def url_blocked(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return True
    host = parsed.hostname
    if not host:
        return True
    try:
        ipaddress.ip_address(host)
        return _blocked_ip(host)
    except ValueError:
        pass
    try:
        infos = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))
    except OSError:
        return True
    for info in infos:
        ip = info[4][0]
        try:
            if _blocked_ip(ip):
                return True
        except ValueError:
            return True
    return False


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if url_blocked(newurl):
            raise urllib.error.URLError("ssrf_denied")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Toolbelt:
    def __init__(
        self,
        repo: Path,
        harness_root: Path,
        allow_net: bool = True,
        allow_shell: bool = False,
        redact_key: str | None = None,
    ):
        self.repo = repo
        self.harness_root = harness_root
        self.allow_net = allow_net
        self.allow_shell = allow_shell
        self.redact_key = redact_key
        self.artifacts = harness_root / "artifacts"
        self.artifacts.mkdir(parents=True, exist_ok=True)

    def run_requested(
        self,
        parsed: Any,
        node_id: str | None = None,
        vault: Any = None,
        run_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Execute optional tool_calls from model JSON: [{tool, args}]."""
        if not isinstance(parsed, dict):
            return []
        calls = parsed.get("tool_calls") or parsed.get("tools") or []
        if not isinstance(calls, list):
            return []
        results = []
        for c in calls[:8]:
            if not isinstance(c, dict):
                continue
            tool = (c.get("tool") or c.get("name") or "").lower()
            args = c.get("args") or c.get("arguments") or {}
            try:
                if tool in {"read_file", "read"}:
                    results.append({"tool": tool, **self.read_file(str(args.get("path", "")))})
                elif tool in {"grep", "search"}:
                    results.append(
                        {"tool": tool, **self.grep(str(args.get("pattern", "")), str(args.get("path", ".")))}
                    )
                elif tool in {"web_fetch", "fetch", "http_get"}:
                    results.append({"tool": tool, **self.web_fetch(str(args.get("url", "")))})
                elif tool in {"write_artifact", "write"}:
                    name = str(args.get("name") or args.get("path") or "out.txt")
                    content = str(args.get("content", ""))
                    if vault is not None and node_id:
                        meta = vault.write(node_id, name, content, kind="text", run_id=run_id)
                        results.append(
                            {
                                "tool": tool,
                                "ok": True,
                                "name": name,
                                "path": meta.get("path"),
                                "bytes": meta.get("bytes"),
                            }
                        )
                    else:
                        results.append({"tool": tool, **self.write_artifact(name, content)})
                elif tool == "shell":
                    results.append({"tool": tool, "ok": False, "error": "shell_disabled"})
                else:
                    results.append({"tool": tool, "ok": False, "error": "unknown_or_denied"})
            except Exception as e:  # noqa: BLE001
                results.append({"tool": tool, "ok": False, "error": redact(str(e), self.redact_key)})
        return redact(results, self.redact_key)

    def read_file(self, rel: str, max_chars: int | None = None) -> dict[str, Any]:
        p = (self.repo / rel)
        if not contained(p, self.repo):
            return {"ok": False, "error": "path_escape"}
        p = p.resolve()
        if is_sensitive_path(p):
            return {"ok": False, "error": "sensitive_file"}
        if not p.is_file():
            return {"ok": False, "error": "not_found", "path": rel}
        if max_chars is None:
            max_chars = 24000 if p.suffix.lower() in {".rs", ".toml", ".py", ".ts", ".c", ".h", ".go"} else 8000
        text = p.read_text(encoding="utf-8", errors="ignore")
        text = redact(text, self.redact_key)
        return {
            "ok": True,
            "path": rel,
            "content": text[:max_chars],
            "truncated": len(text) > max_chars,
        }

    def grep(self, pattern: str, rel: str = ".", max_hits: int = 30) -> dict[str, Any]:
        root = self.repo / rel
        if not contained(root, self.repo):
            return {"ok": False, "error": "path_escape"}
        root = root.resolve()
        if is_sensitive_path(root):
            return {"ok": False, "error": "sensitive_file"}
        if len(pattern) > 256:
            return {"ok": False, "error": "pattern_too_long"}
        try:
            rx = re.compile(pattern)
        except re.error as e:
            return {"ok": False, "error": f"bad_regex: {e}"}
        hits = []
        paths = [root] if root.is_file() else root.rglob("*")
        for p in paths:
            if not p.is_file():
                continue
            if any(x in p.parts for x in {".git", "node_modules", "target", ".venv", "__pycache__"}):
                continue
            if is_sensitive_path(p):
                continue
            try:
                for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if rx.search(line):
                        hits.append(
                            {
                                "path": str(p.relative_to(self.repo)),
                                "line": i,
                                "text": redact(line[:200], self.redact_key),
                            }
                        )
                        if len(hits) >= max_hits:
                            return {"ok": True, "hits": hits, "truncated": True}
            except Exception:
                continue
        return {"ok": True, "hits": hits, "truncated": False}

    def web_fetch(self, url: str, max_chars: int = 12000) -> dict[str, Any]:
        if not self.allow_net:
            return {"ok": False, "error": "net_disabled"}
        if url_blocked(url):
            return {"ok": False, "error": "ssrf_denied", "url": url}
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "opgrok-toolkit/1.0"},
            method="GET",
        )
        opener = urllib.request.build_opener(_SafeRedirect)
        try:
            with opener.open(req, timeout=30) as resp:
                chunks: list[bytes] = []
                n = 0
                while n < max_chars:
                    buf = resp.read(min(4096, max_chars - n))
                    if not buf:
                        break
                    chunks.append(buf)
                    n += len(buf)
                raw = b"".join(chunks).decode("utf-8", errors="ignore")
                return {
                    "ok": True,
                    "url": url,
                    "status": getattr(resp, "status", 200),
                    "content": redact(raw[:max_chars], self.redact_key),
                    "truncated": n >= max_chars,
                }
        except urllib.error.HTTPError as e:
            return {"ok": False, "error": f"http_{e.code}", "url": url}
        except urllib.error.URLError as e:
            reason = str(getattr(e, "reason", e))
            if "ssrf_denied" in reason:
                return {"ok": False, "error": "ssrf_denied", "url": url}
            return {"ok": False, "error": redact(reason, self.redact_key), "url": url}
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "error": redact(str(e), self.redact_key), "url": url}

    def write_artifact(self, name: str, content: str) -> dict[str, Any]:
        safe = re.sub(r"[^a-zA-Z0-9._\-]+", "-", name).strip("-")[:80] or "out.txt"
        path = self.artifacts / safe
        if not contained(path, self.harness_root):
            return {"ok": False, "error": "path_escape"}
        path.write_text(redact(content, self.redact_key), encoding="utf-8")
        return {"ok": True, "path": str(path.relative_to(self.harness_root)), "bytes": path.stat().st_size}

    def shell(self, cmd: str) -> dict[str, Any]:
        # Host shell is not an admissible tool. Regex is not the boundary.
        return {"ok": False, "error": "shell_disabled"}

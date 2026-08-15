"""Frontier live-await UI for OPGROK harness runs.

TTY: in-place spinner + stream snippet (Claude/Grok-Build style).
Non-TTY / tests: one line per committed event only.
STATUS file is always a small dashboard (overwrite).
progress.jsonl gets events, not spinner frames.
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
from pathlib import Path
from typing import Any

SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
FILE_RE = re.compile(r'"name"\s*:\s*"(src/[^"\n]+|Cargo\.toml)"')
DIM, BOLD, GREEN, YELLOW, RED, CYAN, RESET = (
    "\033[2m",
    "\033[1m",
    "\033[32m",
    "\033[33m",
    "\033[31m",
    "\033[36m",
    "\033[0m",
)


def _use_color() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("OPGROK_NO_COLOR"):
        return False
    return bool(sys.stderr.isatty())


def _use_tty() -> bool:
    if os.environ.get("OPGROK_NO_SPINNER"):
        return False
    return bool(sys.stderr.isatty())


def _snip(text: str, n: int = 88) -> str:
    s = re.sub(r"\s+", " ", text or "").strip()
    if len(s) > n:
        s = "…" + s[-n:]
    return s


def _ago(seconds: float) -> str:
    s = max(0, int(seconds))
    if s < 60:
        return f"{s}s"
    return f"{s // 60}m{s % 60:02d}s"


class LiveBoard:
    """One board per harness run."""

    def __init__(self, harness_root: Path, slug: str, nodes: list[dict[str, Any]]):
        self.root = harness_root
        self.slug = slug
        self.color = _use_color()
        self.tty = _use_tty()
        self.lock = threading.Lock()
        self.t0 = time.time()
        self.run_id = ""
        self.model = ""
        self.dry = False
        self.spin_i = 0
        self._live_lines = 0
        self._stop = threading.Event()
        self._thr: threading.Thread | None = None
        self.rows: list[dict[str, Any]] = []
        for n in nodes:
            self.rows.append(
                {
                    "id": n.get("id"),
                    "sg": n.get("sg_name") or n.get("name"),
                    "role": n.get("role"),
                    "state": "queued",
                    "tokens": 0,
                    "arts": 0,
                    "why": "",
                    "job": "",
                }
            )
        self.active: dict[str, Any] = {
            "id": None,
            "phase": "idle",
            "out": 0,
            "think": 0,
            "tail": "",
            "file": "",
            "budget": 0,
            "req": "",
        }

    def _c(self, code: str, text: str) -> str:
        return f"{code}{text}{RESET}" if self.color else text

    def begin(self, run_id: str, model: str, dry: bool) -> None:
        self.run_id = run_id
        self.model = model
        self.dry = dry
        self.event(
            "start",
            run_id=run_id,
            nodes=len(self.rows),
            dry=dry,
            model=model,
        )
        if self.tty:
            self._thr = threading.Thread(target=self._spin, name="opgrok-ui", daemon=True)
            self._thr.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thr:
            self._thr.join(timeout=0.4)
        self._clear_live()

    def node_begin(self, nid: str, sg: str, job: str, model: str, budget: int) -> None:
        with self.lock:
            for r in self.rows:
                if r["id"] == nid:
                    r["state"] = "running"
                    r["job"] = job
            self.active = {
                "id": nid,
                "phase": "connecting",
                "out": 0,
                "think": 0,
                "tail": "",
                "file": "",
                "budget": budget,
                "req": "",
            }
        self.event("node_start", node=nid, sg=sg, job=job, model=model, budget=budget)
        self._paint()

    def on_delta(self, kind: str, text: str) -> None:
        piece = text or ""
        with self.lock:
            if kind == "content":
                self.active["out"] = int(self.active["out"]) + len(piece)
                if self.active["phase"] in {"connecting", "thinking"}:
                    self.active["phase"] = "writing"
            else:
                self.active["think"] = int(self.active["think"]) + len(piece)
                if self.active["phase"] == "connecting":
                    self.active["phase"] = "thinking"
            if piece:
                self.active["tail"] = (str(self.active["tail"]) + piece)[-240:]
            hit = FILE_RE.search(str(self.active["tail"]))
            if hit:
                self.active["file"] = hit.group(1)
                self.active["phase"] = "emitting"

    def node_api_done(
        self,
        nid: str,
        sg: str,
        *,
        tokens: int | None,
        win: str | None,
        why: str,
        finish: str | None,
        arts: int,
        req: str | None = None,
    ) -> None:
        with self.lock:
            for r in self.rows:
                if r["id"] == nid:
                    r["tokens"] = int(tokens or 0)
                    r["arts"] = int(arts or 0)
                    r["why"] = why
            self.active["req"] = req or ""
            if why and why != "ok":
                self.active["phase"] = "retry" if why else "done"
        self.event(
            "api_done",
            node=nid,
            sg=sg,
            tokens=tokens,
            win=win,
            why=why,
            finish=finish,
            arts=arts,
            req=req,
            think=self.active.get("think"),
            out=self.active.get("out"),
        )
        self._paint()

    def retry(self, nid: str, attempt: int, why: str, budget: int) -> None:
        with self.lock:
            for r in self.rows:
                if r["id"] == nid:
                    r["state"] = "retry"
            self.active["phase"] = "retry"
            self.active["budget"] = budget
            self.active["out"] = 0
            self.active["think"] = 0
            self.active["tail"] = ""
            self.active["file"] = ""
        self.event("retry", node=nid, attempt=attempt, why=why, budget=budget)
        self._paint()

    def node_end(self, nid: str, status: str, win: str | None, arts: int) -> None:
        ok = status == "Valid" and (win or "").upper() == "PASS"
        with self.lock:
            for r in self.rows:
                if r["id"] == nid:
                    r["state"] = "ok" if ok else "fail"
                    r["arts"] = arts
            self.active["phase"] = "idle"
            self.active["id"] = None
        self.event("node_done", node=nid, status=status, win=win, arts=arts)
        self._paint()

    def harvest(self, files: list[str]) -> None:
        self.event("harvest", files=len(files), names=",".join(files)[:180])
        self._paint()

    def compile(self, ok: bool | None, method: str | None, rc: int | None) -> None:
        self.event("compile", ok=ok, method=method, rc=rc)
        self._paint()

    def seal(self, win: str, tokens: int, arts: int) -> None:
        self.event("seal", win=win, tokens=tokens, artifacts_written=arts)
        self._paint()

    def cancel(self) -> None:
        self.event("cancel")
        self.stop()

    def event(self, stage: str, **kw: Any) -> None:
        rec = {"ts": time.time(), "slug": self.slug, "stage": stage, **kw}
        try:
            with (self.root / "progress.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, default=str) + "\n")
                fh.flush()
        except Exception:
            pass
        bits = [f"OPGROK[{self.slug}]", stage]
        for k, v in kw.items():
            if v is None or v == "":
                continue
            bits.append(f"{k}={v}")
        line = " ".join(str(b) for b in bits)
        with self.lock:
            self._clear_live()
            print(line, file=sys.stderr, flush=True)
            self._draw_live_unlocked()

    def _spin(self) -> None:
        while not self._stop.wait(0.08):
            with self.lock:
                self.spin_i += 1
                self._draw_live_unlocked()

    def _clear_live(self) -> None:
        if self.tty and self._live_lines:
            sys.stderr.write(f"\x1b[{self._live_lines}A\x1b[J")
            sys.stderr.flush()
            self._live_lines = 0

    def _draw_live_unlocked(self) -> None:
        frame = self._frame()
        try:
            (self.root / "STATUS").write_text(frame, encoding="utf-8")
        except Exception:
            pass
        if not self.tty:
            return
        sys.stderr.write(frame)
        if not frame.endswith("\n"):
            sys.stderr.write("\n")
        sys.stderr.flush()
        self._live_lines = frame.count("\n") + (0 if frame.endswith("\n") else 1)

    def _paint(self) -> None:
        with self.lock:
            self._draw_live_unlocked()

    def _frame(self) -> str:
        spin = SPIN[self.spin_i % len(SPIN)]
        elapsed = _ago(time.time() - self.t0)
        mode = "DRY" if self.dry else "LIVE"
        head = f"{self.slug}  {mode}  {self.model}  {elapsed}  {self.run_id}"
        lines = [self._c(BOLD, head)]
        done = sum(1 for r in self.rows if r["state"] in {"ok", "fail"})
        lines.append(self._c(DIM, f"{done}/{len(self.rows)} nodes"))
        act = self.active
        if act.get("id"):
            phase = act.get("phase") or "running"
            glyph = spin if phase not in {"idle", "ok", "fail"} else "·"
            file_bit = f"  → {act['file']}" if act.get("file") else ""
            bud = int(act.get("budget") or 0)
            used = int(act.get("think") or 0) + int(act.get("out") or 0)
            meter = ""
            if bud:
                pct = min(99, int(100 * used / max(bud, 1)))
                meter = f"  ~{pct}% of {bud} tok-cap"
            lines.append(
                f"{glyph} {act['id']} {phase}  think {act.get('think', 0)}  out {act.get('out', 0)}{file_bit}{meter}"
            )
            snip = _snip(str(act.get("tail") or ""))
            if snip:
                lines.append(self._c(CYAN, f"  {snip}"))
        for r in self.rows:
            mark = {
                "queued": "·",
                "running": spin,
                "retry": "↻",
                "ok": "✓",
                "fail": "✗",
            }.get(r["state"], "·")
            extra = ""
            if r["tokens"]:
                extra += f"  {r['tokens']} tok"
            if r["arts"]:
                extra += f"  {r['arts']} files"
            if r["state"] == "fail" and r.get("why"):
                extra += f"  {r['why']}"
            col = {"ok": GREEN, "fail": RED, "retry": YELLOW, "running": CYAN}.get(r["state"], DIM)
            lines.append(self._c(col, f"  {mark} {r['id']} {r['sg']}  {r['state']}{extra}"))
        return "\n".join(lines) + "\n"

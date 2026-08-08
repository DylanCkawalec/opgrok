"""Self-repair retries — Grok's strength at fixing failures."""
from __future__ import annotations

from typing import Any


def should_retry(output: dict[str, Any], attempt: int, max_retries: int) -> bool:
    if attempt >= max_retries:
        return False
    if output.get("error"):
        return True
    parsed = output.get("parsed")
    if isinstance(parsed, dict) and str(parsed.get("win", "")).upper() == "FAIL":
        return True
    return False


def repair_prompt(
    goal: str,
    node: dict[str, Any],
    previous_output: dict[str, Any],
    attempt: int,
) -> str:
    err = previous_output.get("error") or previous_output.get("detail") or ""
    parsed = previous_output.get("parsed")
    prev_content = previous_output.get("content") or ""
    if isinstance(parsed, dict):
        why = parsed.get("summary") or parsed.get("error") or ""
    else:
        why = str(prev_content)[:800]
    return f"""REPAIR ATTEMPT {attempt + 1} for SuperGrok `{node.get('sg_name')}`.

Original goal:
{goal}

Your previous attempt failed or returned win=FAIL.
Error/detail: {err}
Previous summary/body: {why}

Requirements:
1. Fix the failure class, not symptoms only.
2. Return valid JSON with keys: summary, artifacts, next_hints, win (PASS|FAIL).
3. If you need tools, include tool_calls: [{{"tool":"read_file|grep|web_fetch|write_artifact","args":{{...}}}}]
4. Stay inside this SuperGrok's purpose: {node.get('purpose')}
"""

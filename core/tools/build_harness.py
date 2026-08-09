#!/usr/bin/env python3
"""Build + install an OPGROK harness binary.

Steps:
1. Ensure skills_cache/ filled from graph
2. Prefer cargo build --release of core/binaries/<slug>/crate
3. Else package Python live runner as bin/opgrok-<slug>
4. Optional: install to ~/.opgrok/bin

Usage:
  python3 core/tools/build_harness.py <slug> [--install] [--force-python]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def cache_skills(slug: str) -> int:
    root = ROOT / "core/binaries" / slug
    graph = json.loads((root / "graph.json").read_text())
    cache = root / "skills_cache"
    cache.mkdir(parents=True, exist_ok=True)
    n = 0
    for node in graph.get("nodes") or []:
        sp = node.get("skill_path") or ""
        name = node.get("sg_name") or "unknown"
        src = ROOT / sp
        dst = cache / f"{name}.md"
        if src.is_file():
            text = src.read_text(encoding="utf-8", errors="ignore")
            # thrift store
            if len(text) > 8000:
                keep = []
                for sec in ("## Intent", "## Purpose", "## Call", "## Win", "## Do"):
                    if sec in text:
                        i = text.find(sec)
                        j = text.find("\n## ", i + 4)
                        keep.append(text[i : (j if j > 0 else i + 1500)])
                text = "\n\n".join(keep) if keep else text[:8000]
            dst.write_text(text, encoding="utf-8")
            n += 1
        elif not dst.is_file():
            dst.write_text(
                f"# {name}\n\nIntent: {node.get('intent')}\n\nPurpose: {node.get('purpose')}\n",
                encoding="utf-8",
            )
            n += 1
    return n


def write_python_bin(slug: str) -> Path:
    """Ship a portable entrypoint that calls the live runner."""
    root = ROOT / "core/binaries" / slug
    bin_dir = root / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    target = bin_dir / f"opgrok-{slug}"
    runner = ROOT / "core/tools/run_harness.py"
    script = f"""#!/usr/bin/env bash
set -euo pipefail
# OPGROK harness entrypoint — live Grok API via run_harness.py (loads .env itself)
REPO_ROOT="{ROOT}"
SLUG="{slug}"
GOAL=""
ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --goal) GOAL="$2"; shift 2 ;;
    --dry-run) ARGS+=(--dry-run); shift ;;
    --max-tokens) ARGS+=(--max-tokens "$2"); shift 2 ;;
    *) ARGS+=("$1"); shift ;;
  esac
done
if [[ -z "${{GOAL}}" ]]; then
  GOAL=$(python3 -c "import json;print(json.load(open('${{REPO_ROOT}}/core/binaries/${{SLUG}}/graph.json')).get('goal',''))")
fi
exec python3 "{runner}" "${{SLUG}}" --repo "${{REPO_ROOT}}" --goal "${{GOAL}}" "${{ARGS[@]}}"
"""
    target.write_text(script)
    target.chmod(target.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    return target


def cargo_available() -> bool:
    return shutil.which("cargo") is not None


def build_cargo(slug: str) -> Path | None:
    crate = ROOT / "core/binaries" / slug / "crate"
    if not (crate / "Cargo.toml").is_file():
        return None
    if not cargo_available():
        return None
    # ensure full main.rs from template exists
    ensure_full_crate(slug)
    env = os.environ.copy()
    # isolate from workspace parent if needed — use --manifest-path
    cmd = [
        "cargo",
        "build",
        "--release",
        "--manifest-path",
        str(crate / "Cargo.toml"),
        "--target-dir",
        str(crate / "target"),
    ]
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd, cwd=str(crate), env=env, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:] if r.stdout else "")
        print(r.stderr[-3000:] if r.stderr else "", file=sys.stderr)
        return None
    # find binary
    bin_name = f"opgrok-{slug}"
    candidates = list((crate / "target" / "release").glob(bin_name))
    if not candidates:
        # windows or renamed
        candidates = list((crate / "target" / "release").glob(f"{bin_name}*"))
    if not candidates:
        print("cargo succeeded but binary not found", file=sys.stderr)
        return None
    dest_dir = ROOT / "core/binaries" / slug / "bin"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / bin_name
    shutil.copy2(candidates[0], dest)
    dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
    return dest


def ensure_full_crate(slug: str) -> None:
    """Write a complete standalone harness crate with embedded graph + skill runner via subprocess python or curl."""
    crate = ROOT / "core/binaries" / slug / "crate"
    crate.mkdir(parents=True, exist_ok=True)
    (crate / "src").mkdir(exist_ok=True)
    graph_src = ROOT / "core/binaries" / slug / "graph.json"
    if graph_src.is_file():
        shutil.copy2(graph_src, crate / "graph.json")

    # Copy skills_cache into crate for portability
    cache = ROOT / "core/binaries" / slug / "skills_cache"
    crate_cache = crate / "skills_cache"
    if cache.is_dir():
        if crate_cache.exists():
            shutil.rmtree(crate_cache)
        shutil.copytree(cache, crate_cache)

    pkg = f"opgrok-{slug}"
    (crate / "Cargo.toml").write_text(
        f"""[package]
name = "{pkg}"
version = "0.1.0"
edition = "2021"
description = "OPGROK SuperGrok harness binary"

[[bin]]
name = "opgrok-{slug}"
path = "src/main.rs"

[dependencies]
serde = {{ version = "1", features = ["derive"] }}
serde_json = "1"
clap = {{ version = "4", features = ["derive"] }}
"""
    )

    main_rs = r'''//! OPGROK harness binary — loads graph, injects skills, calls Grok API.
use clap::Parser;
use serde_json::{json, Value};
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::Duration;

#[derive(Parser, Debug)]
struct Cli {
    #[arg(long)]
    goal: Option<String>,
    #[arg(long, default_value_t = false)]
    dry_run: bool,
    #[arg(long)]
    graph: Option<PathBuf>,
}

fn main() {
    let cli = Cli::parse();
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let graph_path = cli
        .graph
        .unwrap_or_else(|| manifest.join("graph.json"));
    let raw = fs::read_to_string(&graph_path).expect("read graph.json");
    let graph: Value = serde_json::from_str(&raw).expect("parse graph");
    let goal = cli
        .goal
        .or_else(|| graph["goal"].as_str().map(|s| s.to_string()))
        .unwrap_or_default();
    let nodes = graph["nodes"].as_array().cloned().unwrap_or_default();
    let api_key = env::var("XAI_API_KEY").ok();
    let model = env::var("OPGROK_MODEL").unwrap_or_else(|_| "grok-4".into());
    let dry = cli.dry_run || api_key.is_none();

    let mut blackboard: BTreeMap<String, Value> = BTreeMap::new();
    blackboard.insert("goal".into(), json!(goal));
    let mut node_results = Vec::new();

    for node in &nodes {
        let id = node["id"].as_str().unwrap_or("?");
        let sg = node["sg_name"].as_str().unwrap_or("?");
        let skill = load_skill(&manifest, sg, node);
        let system = format!(
            "You are SuperGrok `{sg}` (binary_id={bin}).\nIntent: {intent}\nPurpose: {purpose}\nReturn JSON with keys summary, artifacts, next_hints, win (PASS|FAIL).\n\nSKILL:\n{skill}",
            sg = sg,
            bin = node["binary_id"].as_str().unwrap_or(""),
            intent = node["intent"].as_str().unwrap_or(""),
            purpose = node["purpose"].as_str().unwrap_or(""),
            skill = skill.chars().take(6000).collect::<String>(),
        );
        let bb = serde_json::to_string(&thrift_bb(&blackboard)).unwrap_or_else(|_| "{}".into());
        let user = format!(
            "GOAL:\n{goal}\n\nNODE: {id} ({sg})\nPROCESS: {proc}\n\nBLACKBOARD:\n{bb}\n\nReturn JSON only for this node.",
            goal = goal,
            id = id,
            sg = sg,
            proc = node["ipo"]["process"].as_str().unwrap_or(""),
            bb = bb.chars().take(12000).collect::<String>(),
        );

        let output = if dry {
            json!({
                "mode": "dry_run",
                "sg": sg,
                "skill_chars": skill.len(),
                "prompt_preview": user.chars().take(400).collect::<String>(),
                "parsed": {"summary": format!("[dry] {sg}"), "win": "PASS", "artifacts": []}
            })
        } else {
            match call_grok(api_key.as_deref().unwrap(), &model, &system, &user) {
                Ok(v) => v,
                Err(e) => json!({"error": e, "sg": sg}),
            }
        };
        blackboard.insert(format!("{id}.output"), output.clone());
        node_results.push(json!({"id": id, "sg_name": sg, "output": output}));
    }

    let fails = node_results
        .iter()
        .filter(|n| {
            let o = &n["output"];
            if o.get("error").is_some() {
                return true;
            }
            let p = &o["parsed"];
            let ok = p.is_object() && p.get("summary").is_some() && p.get("win").is_some();
            if !ok {
                return true;
            }
            p["win"].as_str() == Some("FAIL")
        })
        .count();
    let win = if dry {
        "DRY"
    } else if fails == 0 {
        "PASS"
    } else {
        "FAIL"
    };
    let sink = node_results.last().cloned().unwrap_or(json!(null));
    let result = json!({
        "win": win,
        "slug": graph["slug"],
        "goal": goal,
        "dry_run": dry,
        "model": if dry { Value::Null } else { json!(model) },
        "nodes": node_results.len(),
        "node_results": node_results,
        "result": sink.get("output").cloned().unwrap_or(sink),
    });
    println!("{}", serde_json::to_string_pretty(&result).unwrap());
}

fn thrift_bb(bb: &BTreeMap<String, Value>) -> BTreeMap<String, Value> {
    let mut out = BTreeMap::new();
    for (k, v) in bb {
        if k == "goal" || k.ends_with(".output") {
            if let Some(obj) = v.as_object() {
                if let Some(c) = obj.get("content").and_then(|x| x.as_str()) {
                    out.insert(
                        k.clone(),
                        json!({
                            "content_preview": c.chars().take(1200).collect::<String>(),
                            "parsed": obj.get("parsed"),
                        }),
                    );
                    continue;
                }
            }
            out.insert(k.clone(), v.clone());
        }
    }
    out
}

fn load_skill(manifest: &Path, sg: &str, node: &Value) -> String {
    let p = manifest.join("skills_cache").join(format!("{sg}.md"));
    if p.is_file() {
        return fs::read_to_string(p).unwrap_or_default();
    }
    format!(
        "Intent: {}\nPurpose: {}\n",
        node["intent"].as_str().unwrap_or(""),
        node["purpose"].as_str().unwrap_or("")
    )
}

fn call_grok(api_key: &str, model: &str, system: &str, user: &str) -> Result<Value, String> {
    let body = json!({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": 0.2,
        "max_tokens": 1200
    });
    let tmp = env::temp_dir().join(format!("opgrok-body-{}.json", std::process::id()));
    fs::write(&tmp, body.to_string()).map_err(|e| e.to_string())?;
    let auth = format!("Authorization: Bearer {api_key}");
    let data = format!("@{}", tmp.display());
    let out = Command::new("curl")
        .args([
            "-sS",
            "--max-time",
            "120",
            "https://api.x.ai/v1/chat/completions",
            "-H",
            &auth,
            "-H",
            "Content-Type: application/json",
            "-d",
            &data,
        ])
        .output()
        .map_err(|e| e.to_string())?;
    let _ = fs::remove_file(&tmp);
    if !out.status.success() {
        return Err(String::from_utf8_lossy(&out.stderr).into());
    }
    let v: Value = serde_json::from_slice(&out.stdout).map_err(|e| e.to_string())?;
    let content = v["choices"][0]["message"]["content"]
        .as_str()
        .unwrap_or("")
        .to_string();
    let parsed = parse_jsonish(&content);
    Ok(json!({
        "mode": "live",
        "content": content,
        "parsed": parsed,
        "usage": v.get("usage"),
        "model": v.get("model"),
    }))
}

fn parse_jsonish(text: &str) -> Value {
    let t = text.trim();
    if let Ok(v) = serde_json::from_str::<Value>(t) {
        return v;
    }
    if let Some(start) = t.find('{') {
        if let Some(end) = t.rfind('}') {
            if let Ok(v) = serde_json::from_str::<Value>(&t[start..=end]) {
                return v;
            }
        }
    }
    json!({"summary": t.chars().take(500).collect::<String>()})
}
'''
    # fix unused imports warning in template
    main_rs = main_rs.replace("use std::time::Duration;\n", "")
    (crate / "src" / "main.rs").write_text(main_rs)


def install_global(slug: str, binary: Path) -> Path:
    home = Path.home() / ".opgrok" / "bin"
    home.mkdir(parents=True, exist_ok=True)
    dest = home / f"opgrok-{slug}"
    shutil.copy2(binary, dest)
    dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
    # also short alias if reasonable
    meta = home.parent / "binaries.json"
    data = {"binaries": []}
    if meta.is_file():
        try:
            data = json.loads(meta.read_text())
        except Exception:
            pass
    data.setdefault("binaries", [])
    data["binaries"] = [b for b in data["binaries"] if b.get("slug") != slug]
    data["binaries"].append(
        {
            "slug": slug,
            "path": str(dest),
            "source": str(binary),
        }
    )
    meta.write_text(json.dumps(data, indent=2) + "\n")
    return dest


def update_registry_built(slug: str, binary: Path, method: str) -> None:
    reg_path = ROOT / "core/binaries/registry.json"
    reg = json.loads(reg_path.read_text()) if reg_path.is_file() else {"harnesses": []}
    for h in reg.get("harnesses") or []:
        if h.get("slug") == slug:
            h["binary"] = str(binary.relative_to(ROOT)) if str(binary).startswith(str(ROOT)) else str(binary)
            h["build_method"] = method
            h["built"] = True
    reg_path.write_text(json.dumps(reg, indent=2) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--install", action="store_true", help="Install to ~/.opgrok/bin")
    ap.add_argument("--force-python", action="store_true", help="Skip cargo; use Python runner")
    args = ap.parse_args()
    slug = args.slug
    root = ROOT / "core/binaries" / slug
    if not (root / "graph.json").is_file():
        print(f"FAIL: missing harness {slug}", file=sys.stderr)
        return 1

    n = cache_skills(slug)
    print(f"skills_cache: {n} skills")

    binary = None
    method = "python"
    if not args.force_python:
        binary = build_cargo(slug)
        if binary:
            method = "cargo-release"
            print(f"cargo binary: {binary}")
    if binary is None:
        ensure_full_crate(slug)
        binary = write_python_bin(slug)
        method = "python-runner"
        print(f"python entrypoint: {binary}")

    update_registry_built(slug, binary, method)
    if args.install:
        dest = install_global(slug, binary)
        print(f"installed: {dest}")
        print(f"PATH hint: export PATH=\"$HOME/.opgrok/bin:$PATH\"")

    print(json.dumps({"win": "PASS", "slug": slug, "binary": str(binary), "method": method}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

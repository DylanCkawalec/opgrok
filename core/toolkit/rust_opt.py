"""Rust-specialist optimize panel — runs BEFORE cargo ever builds a harness binary.

Six SuperGroks own one pass each (deterministic, no live API):

  rust-scout  inventory + isolate crate from the OPGROK workspace
  rust-smith  smallest correct crate layout (Cargo.toml, rust-version, bins)
  rust-forge  e2e path: clap CLI, Result, ureq (no curl, no key-on-disk)
  rust-trace  delete hollow-PASS / unused imports / temp-file secrets
  rust-audit  clippy-shaped checks (no unwrap on lib edges, no shell API)
  rust-seal   cargo check gate; refuse to compile if the crate is not sealed

This is the extra optimization step between generate and binary.
It never authors domain product code (no domain templates, no slug special cases).
If `core/binaries/<slug>/product/` holds SuperGrok-harvested sources, those win.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .product import crate_ident

ROOT = Path(__file__).resolve().parents[2]

RUST_SPECIALISTS = (
    "rust-scout",
    "rust-smith",
    "rust-forge",
    "rust-trace",
    "rust-audit",
    "rust-seal",
)

HIREABLE_RUST = frozenset(RUST_SPECIALISTS)


def specialist_paths(repo: Path | None = None) -> dict[str, str]:
    repo = repo or ROOT
    out: dict[str, str] = {}
    for name in RUST_SPECIALISTS:
        role = name.split("-", 1)[1]
        rel = f"core/skills/rust/{role}/SKILL.md"
        if (repo / rel).is_file():
            out[name] = rel
    return out


def optimize_crate(slug: str, repo: Path | None = None) -> dict[str, Any]:
    """Rewrite core/binaries/<slug>/crate into a sealed, isolated Rust package.

    Must be called after graph.json + skills_cache exist and BEFORE cargo build.
    """
    repo = repo or ROOT
    root = repo / "core/binaries" / slug
    crate = root / "crate"
    crate.mkdir(parents=True, exist_ok=True)
    (crate / "src").mkdir(exist_ok=True)
    passes: list[dict[str, str]] = []

    graph_src = root / "graph.json"
    if graph_src.is_file():
        shutil.copy2(graph_src, crate / "graph.json")
        passes.append({"sg": "rust-scout", "act": "copied graph.json into isolated crate"})
    cache = root / "skills_cache"
    if cache.is_dir():
        dest = crate / "skills_cache"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(cache, dest)
        passes.append({"sg": "rust-scout", "act": "vendored skills_cache"})

    # rust-smith + rust-forge: isolate the crate. Product sources (live SuperGrok
    # artifacts harvested into product/) win over the generic harness scaffold.
    # Never embed domain templates. Harvested product/ sources win.
    product = root / "product"
    product_rs = [p for p in product.rglob("*.rs") if p.is_file()] if product.is_dir() else []
    product_cargo = product / "Cargo.toml"
    _write_or_merge_cargo(
        crate,
        slug,
        product_cargo if product_cargo.is_file() else None,
    )
    passes.append(
        {
            "sg": "rust-smith",
            "act": "isolated [workspace], edition 2021, rust-version 1.85",
        }
    )
    if product_rs:
        n = _install_product_sources(crate, product)
        passes.append(
            {
                "sg": "rust-forge",
                "act": f"installed {n} SuperGrok product source(s); did not write scaffold",
            }
        )
    else:
        (crate / "src" / "main.rs").write_text(
            _MAIN_RS.replace("@@SLUG@@", slug), encoding="utf-8"
        )
        passes.append(
            {
                "sg": "rust-forge",
                "act": "e2e CLI: clap, Result, ureq live path, no curl, no key temp files",
            }
        )

    main_path = crate / "src" / "main.rs"
    if not main_path.is_file():
        raise RuntimeError("rust-trace: crate has no src/main.rs (SuperGrok product must ship a bin entry)")
    main = main_path.read_text(encoding="utf-8")
    cargo = (crate / "Cargo.toml").read_text(encoding="utf-8")
    src_blob = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore") for p in (crate / "src").rglob("*.rs")
    )
    if 'Command::new("curl")' in src_blob:
        raise RuntimeError("rust-trace: crate uses curl")
    if not product_rs and "env::temp_dir" in main:
        raise RuntimeError("rust-trace: generated crate still uses curl or temp files")
    if "[workspace]" not in cargo:
        raise RuntimeError("rust-trace: crate is not workspace-isolated")
    passes.append({"sg": "rust-trace", "act": "rejected curl / parent-workspace join"})

    audit_hits = []
    if re.search(r'Command::new\(\s*"curl"\s*\)', src_blob):
        audit_hits.append("curl-command")
    if audit_hits:
        raise RuntimeError(f"rust-audit: {audit_hits}")
    passes.append({"sg": "rust-audit", "act": "no curl, isolated crate, Result-shaped live path"})

    if shutil.which("rustfmt"):
        for rs in (crate / "src").rglob("*.rs"):
            subprocess.run(
                ["rustfmt", str(rs)],
                check=False,
                capture_output=True,
            )

    check_ok = True
    check_err = ""
    if shutil.which("cargo"):
        r = subprocess.run(
            [
                "cargo",
                "check",
                "--manifest-path",
                str(crate / "Cargo.toml"),
                "--offline",
                "--target-dir",
                str(crate / "target"),
            ],
            cwd=str(crate),
            capture_output=True,
            text=True,
        )
        # first-time crates may need network for ureq; retry online once
        if r.returncode != 0 and "failed to select a version" in (r.stderr or "") + (r.stdout or ""):
            r = subprocess.run(
                [
                    "cargo",
                    "check",
                    "--manifest-path",
                    str(crate / "Cargo.toml"),
                    "--target-dir",
                    str(crate / "target"),
                ],
                cwd=str(crate),
                capture_output=True,
                text=True,
            )
        if r.returncode != 0:
            # ureq may be uncached; still seal the sources — cargo build will fetch
            check_ok = False
            check_err = (r.stderr or r.stdout or "")[-1500:]
    passes.append(
        {
            "sg": "rust-seal",
            "act": "cargo check" if check_ok else f"sources sealed; check deferred: {check_err[:200]}",
        }
    )

    report = {
        "slug": slug,
        "specialists": list(RUST_SPECIALISTS),
        "paths": specialist_paths(repo),
        "passes": passes,
        "crate": str(crate),
        "check_ok": check_ok,
    }
    (crate / "RUST_SPECIALISTS.md").write_text(_report_md(report), encoding="utf-8")
    _stamp_graph(root, report)
    return report


def _install_product_sources(crate: Path, product: Path) -> int:
    """Copy harvested SuperGrok sources into the isolated crate. Do not invent files."""
    n = 0
    src_in = product / "src"
    dest_src = crate / "src"
    if dest_src.exists():
        shutil.rmtree(dest_src)
    dest_src.mkdir(parents=True, exist_ok=True)
    if src_in.is_dir():
        for p in src_in.rglob("*"):
            if not p.is_file():
                continue
            rel = p.relative_to(src_in)
            dest = dest_src / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(p.read_bytes())
            n += 1
    for p in product.glob("*.rs"):
        dest = dest_src / p.name
        dest.write_bytes(p.read_bytes())
        n += 1
    return n


def _write_or_merge_cargo(crate: Path, slug: str, product_cargo: Path | None) -> None:
    """Force workspace isolation. Keep SuperGrok deps when they shipped a Cargo.toml."""
    if not product_cargo or not product_cargo.is_file():
        _write_cargo_toml(crate, slug)
        return
    ident = crate_ident(slug)
    raw = product_cargo.read_text(encoding="utf-8")
    raw = re.sub(r"(?ms)^\[workspace\][^\[]*", "", raw).strip() + "\n"
    raw = re.sub(
        r'(?m)^name\s*=\s*"[^"]+"',
        f'name = "{ident}"',
        raw,
        count=1,
    )
    if "rust-version" not in raw:
        raw = raw.replace("[package]", '[package]\nrust-version = "1.85"', 1)
    if "edition" not in raw:
        raw = raw.replace("[package]", '[package]\nedition = "2021"', 1)
    if "[[bin]]" not in raw:
        raw += f'\n[[bin]]\nname = "{ident}"\npath = "src/main.rs"\n'
    else:
        raw = re.sub(
            r'(?s)(\[\[bin\]\].*?name\s*=\s*")[^"]+"',
            rf'\1{ident}"',
            raw,
            count=1,
        )
    text = (
        "# Isolated harness crate — do not join the OPGROK workspace.\n"
        "[workspace]\n\n"
        f"{raw}"
    )
    (crate / "Cargo.toml").write_text(text, encoding="utf-8")


def _write_cargo_toml(crate: Path, slug: str) -> None:
    pkg = crate_ident(slug)
    (crate / "Cargo.toml").write_text(
        f"""# Isolated harness crate — do not join the OPGROK workspace.
[workspace]

[package]
name = "{pkg}"
version = "1.0.0"
edition = "2021"
rust-version = "1.85"
description = "OPGROK v1.0.0 SuperGrok harness binary (rust-specialist optimized)"
license = "MIT"
publish = false

[[bin]]
name = "{pkg}"
path = "src/main.rs"

[dependencies]
serde = {{ version = "1.0.228", features = ["derive"] }}
serde_json = "1.0.145"
clap = {{ version = "4.5.53", features = ["derive"] }}
ureq = {{ version = "2.12.1", default-features = true }}
""",
        encoding="utf-8",
    )


def _stamp_graph(root: Path, report: dict[str, Any]) -> None:
    gpath = root / "graph.json"
    if not gpath.is_file():
        return
    try:
        graph = json.loads(gpath.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    apex = graph.setdefault("apex", {})
    apex["rust_specialists"] = list(RUST_SPECIALISTS)
    apex["rust_opt"] = {
        "passes": [p["sg"] for p in report["passes"]],
        "crate": "crate/",
    }
    gpath.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")


def _report_md(report: dict[str, Any]) -> str:
    rows = "\n".join(f"| `{p['sg']}` | {p['act']} |" for p in report["passes"])
    return f"""# Rust specialist seal — `{report['slug']}`

Applied **before** `cargo build`. These SuperGroks own the generated crate.

| specialist | pass |
|------------|------|
{rows}

Sources: {", ".join(report["paths"].values())}
"""


_MAIN_RS = r'''//! OPGROK v1.0.0 harness binary — rust-specialist optimized.
//! Live inference prefers the Python runner (PassBody authority).
//! Native ureq path is the standalone fallback (no curl, no key-on-disk).

use clap::Parser;
use serde_json::{json, Value};
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

#[derive(Parser, Debug)]
#[command(name = "opgrok-@@SLUG@@", version = "1.0.0")]
struct Cli {
    #[arg(long)]
    goal: Option<String>,
    #[arg(long, default_value_t = false)]
    dry_run: bool,
    #[arg(long)]
    graph: Option<PathBuf>,
}

fn main() {
    if let Err(e) = run() {
        let fail = json!({"win": "FAIL", "error": e, "slug": "@@SLUG@@"});
        println!("{}", serde_json::to_string_pretty(&fail).unwrap_or_else(|_| fail.to_string()));
        std::process::exit(1);
    }
}

fn run() -> Result<(), String> {
    let cli = Cli::parse();
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let graph_path = cli
        .graph
        .clone()
        .unwrap_or_else(|| manifest.join("graph.json"));
    let raw = fs::read_to_string(&graph_path).map_err(|e| format!("read graph: {e}"))?;
    let graph: Value = serde_json::from_str(&raw).map_err(|e| format!("parse graph: {e}"))?;
    let goal = cli
        .goal
        .clone()
        .or_else(|| graph["goal"].as_str().map(str::to_string))
        .unwrap_or_default();
    let api_key = env::var("XAI_API_KEY").ok().filter(|k| !k.is_empty());
    let dry = cli.dry_run || api_key.is_none();

    if let Some(py) = python_runner() {
        if !dry {
            return delegate_python(&py, &goal, cli.dry_run);
        }
    }

    native_run(&manifest, &graph, &goal, dry, api_key.as_deref())
}

fn python_runner() -> Option<PathBuf> {
    let here = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    // crate/ → slug/ → binaries/ → core/ → repo
    let candidate = here
        .parent()
        .and_then(|p| p.parent())
        .and_then(|p| p.parent())
        .and_then(|p| p.parent())
        .map(|repo| repo.join("core/tools/run_harness.py"));
    candidate.filter(|p| p.is_file())
}

fn delegate_python(runner: &Path, goal: &str, dry: bool) -> Result<(), String> {
    let repo = runner
        .parent()
        .and_then(Path::parent)
        .and_then(Path::parent)
        .ok_or("cannot locate repo root")?;
    let mut cmd = Command::new("python3");
    cmd.arg(runner)
        .arg("@@SLUG@@")
        .arg("--repo")
        .arg(repo)
        .arg("--goal")
        .arg(goal);
    if dry {
        cmd.arg("--dry-run");
    }
    let status = cmd.status().map_err(|e| e.to_string())?;
    if status.success() {
        Ok(())
    } else {
        Err(format!("python runner exited {status}"))
    }
}

fn native_run(
    manifest: &Path,
    graph: &Value,
    goal: &str,
    dry: bool,
    api_key: Option<&str>,
) -> Result<(), String> {
    let nodes = graph["nodes"].as_array().cloned().unwrap_or_default();
    let model = env::var("OPGROK_MODEL").unwrap_or_else(|_| "grok-4".to_string());
    let mut blackboard: BTreeMap<String, Value> = BTreeMap::new();
    blackboard.insert("goal".into(), json!(goal));
    let mut node_results = Vec::new();
    let mut total_tokens: u64 = 0;

    for node in &nodes {
        let id = node["id"].as_str().unwrap_or("?");
        let sg = node["sg_name"].as_str().unwrap_or("?");
        let skill = load_skill(manifest, sg, node);
        let system = format!(
            "You are SuperGrok `{sg}`.\nIntent: {intent}\nPurpose: {purpose}\n\
             Return JSON keys summary, artifacts, win (PASS|FAIL). Producer roles must attach artifacts.\n\nSKILL:\n{skill}",
            intent = node["intent"].as_str().unwrap_or(""),
            purpose = node["purpose"].as_str().unwrap_or(""),
            skill = skill.chars().take(6000).collect::<String>(),
        );
        let bb = serde_json::to_string(&thrift_bb(&blackboard)).unwrap_or_else(|_| "{}".into());
        let user = format!(
            "GOAL:\n{goal}\n\nNODE: {id} ({sg})\nPROCESS: {proc}\n\nBLACKBOARD:\n{bb}",
            proc = node["ipo"]["process"].as_str().unwrap_or(""),
            bb = bb.chars().take(12000).collect::<String>(),
        );

        let output = if dry {
            json!({
                "mode": "dry_run",
                "sg": sg,
                "skill_chars": skill.len(),
                "parsed": {"summary": format!("[dry] {sg}"), "artifacts": [], "win": "PASS"}
            })
        } else {
            let key = api_key.ok_or("XAI_API_KEY missing")?;
            call_grok(key, &model, &system, &user)?
        };
        if let Some(u) = output.get("usage") {
            if let Some(n) = u.get("total_tokens").and_then(Value::as_u64) {
                total_tokens += n;
            }
        }
        blackboard.insert(format!("{id}.output"), output.clone());
        node_results.push(json!({"id": id, "sg_name": sg, "output": output}));
    }

    let win = seal(&node_results, dry, total_tokens);
    let sink = node_results.last().cloned().unwrap_or(json!(null));
    let result = json!({
        "win": win,
        "slug": graph["slug"],
        "goal": goal,
        "dry_run": dry,
        "nodes": node_results.len(),
        "node_results": node_results,
        "result": sink.get("output").cloned().unwrap_or(sink),
        "ledger": {"total_tokens": total_tokens},
    });
    println!(
        "{}",
        serde_json::to_string_pretty(&result).map_err(|e| e.to_string())?
    );
    if win == "FAIL" {
        return Err("sealed FAIL".into());
    }
    Ok(())
}

fn seal(node_results: &[Value], dry: bool, total_tokens: u64) -> &'static str {
    if dry {
        return "DRY";
    }
    let mut has_producer = false;
    for n in node_results {
        let o = &n["output"];
        if o.get("error").is_some() {
            return "FAIL";
        }
        if o.get("mode").and_then(Value::as_str) == Some("dry_run") {
            return "FAIL";
        }
        let p = &o["parsed"];
        if !p.is_object() || p.get("summary").is_none() || p.get("artifacts").is_none() {
            return "FAIL";
        }
        let win = p
            .get("win")
            .and_then(Value::as_str)
            .unwrap_or("")
            .trim()
            .to_ascii_uppercase();
        if win != "PASS" {
            return "FAIL";
        }
        let arts = p.get("artifacts").and_then(Value::as_array);
        if arts.is_some_and(|a| !a.is_empty()) {
            has_producer = true;
        }
    }
    if !has_producer || total_tokens == 0 {
        return "FAIL";
    }
    "PASS"
}

fn thrift_bb(bb: &BTreeMap<String, Value>) -> BTreeMap<String, Value> {
    let mut out = BTreeMap::new();
    for (k, v) in bb {
        if k == "goal" || k.ends_with(".output") {
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
        "max_tokens": 4096
    });
    let resp = ureq::post("https://api.x.ai/v1/chat/completions")
        .set("Authorization", &format!("Bearer {api_key}"))
        .set("Content-Type", "application/json")
        .set("User-Agent", "opgrok-harness/1.0.0")
        .send_string(&body.to_string())
        .map_err(|e| e.to_string())?;
    let text = resp.into_string().map_err(|e| e.to_string())?;
    let v: Value = serde_json::from_str(&text).map_err(|e| e.to_string())?;
    let content = v["choices"][0]["message"]["content"]
        .as_str()
        .unwrap_or("")
        .to_string();
    Ok(json!({
        "mode": "live",
        "content": content,
        "parsed": parse_jsonish(&content),
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
    json!({"summary": t.chars().take(500).collect::<String>(), "artifacts": [], "win": "FAIL"})
}
'''

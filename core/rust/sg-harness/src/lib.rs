//! OPGROK harness crafter.
//!
//! Turns a user goal into:
//! - SuperGrok hire list (intent route)
//! - n8n-style graph.json (IPO/OODA nodes)
//! - Leslie WINNING_CONDITION.md
//! - single README.md
//! - Rust crate sources under core/binaries/<slug>/crate
//! - registry entry
//!
//! Winning condition: exactly one binary package + one README (Leslie).

use anyhow::{bail, Context, Result};
use opgrok_sg_runtime::{SuperGrokIndex, SuperGrokMeta};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Ipo {
    pub inputs: Vec<String>,
    pub process: String,
    pub outputs: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Ooda {
    pub observe: String,
    pub orient: String,
    pub decide: String,
    pub act: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GraphNode {
    pub id: String,
    pub sg_name: String,
    pub sg_id: String,
    pub binary_id: String,
    pub skill_path: String,
    pub category: String,
    pub role: String,
    pub intent: String,
    pub purpose: String,
    pub sink: bool,
    pub ipo: Ipo,
    pub ooda: Ooda,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GraphEdge {
    pub from: String,
    pub to: String,
    #[serde(default)]
    pub key: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HarnessGraph {
    pub version: String,
    pub slug: String,
    pub goal: String,
    pub created_at: String,
    pub leslie_wc_path: String,
    pub nodes: Vec<GraphNode>,
    pub edges: Vec<GraphEdge>,
}

#[derive(Debug, Clone, Serialize)]
pub struct HarnessPackage {
    pub slug: String,
    pub root: PathBuf,
    pub readme: PathBuf,
    pub winning_condition: PathBuf,
    pub graph: PathBuf,
    pub crate_dir: PathBuf,
    pub binary_hint: PathBuf,
    pub hired: Vec<String>,
}

pub fn slugify(goal: &str) -> String {
    let mut s: String = goal
        .chars()
        .map(|c| {
            if c.is_ascii_alphanumeric() {
                c.to_ascii_lowercase()
            } else {
                '-'
            }
        })
        .collect();
    while s.contains("--") {
        s = s.replace("--", "-");
    }
    s = s.trim_matches('-').to_string();
    if s.is_empty() {
        s = format!(
            "harness-{}",
            SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .map(|d| d.as_secs())
                .unwrap_or(0)
        );
    }
    s.chars().take(48).collect()
}

pub fn hire(index: &SuperGrokIndex, goal: &str, limit: usize) -> Vec<SuperGrokMeta> {
    let limit = limit.clamp(2, 24);
    let mut hired: Vec<SuperGrokMeta> = index
        .route(goal, limit.saturating_mul(2))
        .into_iter()
        .map(|m| m.clone())
        .collect();

    // Ensure diversity: if route is thin, pull category anchors.
    let anchors = ["plan", "code", "web", "ui", "review", "test", "docs", "agent"];
    for cat in anchors {
        if hired.len() >= limit {
            break;
        }
        if hired.iter().any(|h| h.category == cat) {
            continue;
        }
        if let Some(m) = index.by_category(cat).into_iter().next() {
            hired.push(m.clone());
        }
    }

    hired.truncate(limit);
    if hired.len() < 2 {
        // last resort: first two registry entries
        if let Some(reg) = index.registry.as_ref() {
            for sk in reg.skills.iter().take(2) {
                if !hired.iter().any(|h| h.name == sk.name) {
                    hired.push(sk.clone());
                }
            }
        }
    }
    hired
}

pub fn build_graph(slug: &str, goal: &str, hired: &[SuperGrokMeta]) -> HarnessGraph {
    let mut nodes = Vec::new();
    let mut edges = Vec::new();
    let n = hired.len();

    for (i, sk) in hired.iter().enumerate() {
        let id = format!("n{:02}", i + 1);
        let prev_out = if i == 0 {
            "goal".to_string()
        } else {
            format!("n{:02}.output", i)
        };
        let sink = i + 1 == n;
        nodes.push(GraphNode {
            id: id.clone(),
            sg_name: sk.name.clone(),
            sg_id: sk.sg_id.clone(),
            binary_id: sk.binary_id.clone(),
            skill_path: sk.path.clone(),
            category: sk.category.clone(),
            role: sk.role.clone(),
            intent: sk.intent.clone(),
            purpose: sk.purpose.clone(),
            sink,
            ipo: Ipo {
                inputs: vec![prev_out.clone(), "goal".into()],
                process: format!(
                    "Execute SuperGrok {} ({}). Purpose: {}",
                    sk.name, sk.shorthand, sk.purpose
                ),
                outputs: vec![format!("{id}.output")],
            },
            ooda: Ooda {
                observe: format!("Read blackboard + skill {}", sk.path),
                orient: format!("Map goal facet to intent: {}", sk.intent),
                decide: "Choose minimal actions per skill Win/Do".into(),
                act: format!(
                    "Prompt-engineer for binary_id {} via Grok API; write {}.output",
                    sk.binary_id, id
                ),
            },
        });
        if i > 0 {
            edges.push(GraphEdge {
                from: format!("n{:02}", i),
                to: id,
                key: format!("n{:02}.output", i),
            });
        }
    }

    HarnessGraph {
        version: "1.0.0".into(),
        slug: slug.into(),
        goal: goal.into(),
        created_at: iso_now(),
        leslie_wc_path: format!("core/binaries/{slug}/WINNING_CONDITION.md"),
        nodes,
        edges,
    }
}

fn iso_now() -> String {
    // Keep deps minimal — unix timestamp string is enough for v1.
    format!(
        "unix:{}",
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0)
    )
}

fn write_readme(path: &Path, slug: &str, goal: &str, graph: &HarnessGraph) -> Result<()> {
    let mut agents = String::new();
    for n in &graph.nodes {
        agents.push_str(&format!(
            "| `{}` | `{}` | {} | {} |\n",
            n.sg_name, n.id, n.intent, n.purpose
        ));
    }
    let order: Vec<&str> = graph.nodes.iter().map(|n| n.sg_name.as_str()).collect();
    let body = format!(
        r#"# opgrok-{slug}

## What this binary does

Harness for goal:

> {goal}

It runs an n8n-style SuperGrok graph: each node loads a SuperGrok skill, prompt-engineers for that node's purpose, calls the Grok API, and writes to a run blackboard. The sink node surfaces `OPGROK_RESULT`.

## Winning condition (Leslie)

See `WINNING_CONDITION.md`. PASS = this package contains **one binary** + **this single README** + successful run observables.

## Hired SuperGroks

| name | node | intent | purpose |
|------|------|--------|---------|
{agents}

## Graph order

{order}

## Run

```bash
# from repo root
./core/binaries/{slug}/bin/opgrok-{slug} --goal "{goal}"
# or rebuild
cargo run -p opgrok-{slug} -- --goal "{goal}"
```

Requires `XAI_API_KEY` in environment for live inference. Without it, dry-run mode emits the planned node prompts only.

## Files

- `graph.json` — agent DAG
- `WINNING_CONDITION.md` — Leslie seal
- `crate/` — Rust sources
- `bin/opgrok-{slug}` — release binary (after compile)
"#,
        slug = slug,
        goal = goal.replace('"', "'"),
        agents = agents,
        order = order.join(" → "),
    );
    fs::write(path, body)?;
    Ok(())
}

fn write_wc(path: &Path, slug: &str, goal: &str, graph: &HarnessGraph) -> Result<()> {
    let mut rows = String::new();
    for n in &graph.nodes {
        rows.push_str(&format!(
            "| `{}` | {} | {} |\n",
            n.sg_name, n.intent, n.purpose
        ));
    }
    let order: Vec<&str> = graph.nodes.iter().map(|n| n.id.as_str()).collect();
    let body = format!(
        r#"# Winning Condition — opgrok-{slug}

**Leslie seal.** Governed by the master seal `docs/WINNING_CONDITION.md`
(module `HarnessRun`: I1 NoVacuousPass, I2 DryHonesty, I3 SingleVerdict).
Upstream protocol: https://github.com/DylanCkawalec/Leslie

## Goal

{goal}

## Non-goals

- Implementing the full user deliverable outside the harness graph
- Multiple competing binaries or READMEs for this slug
- Unverified claims of PASS without a run receipt

## Hired SuperGroks

| name | intent | purpose |
|------|--------|---------|
{rows}

## Graph invariants

- Topological order: {order}
- Blackboard always includes `goal`
- Each node writes `{{id}}.output`
- Exactly one sink node (last)
- Scheduler is serial topo for determinism unless graph says otherwise

## Falsifiable PASS

Running:

```bash
core/binaries/{slug}/bin/opgrok-{slug} --goal "..."
```

exits 0 and prints JSON where:

1. `win` is `PASS` only on a live run (`dry_run=false`); dry runs print `DRY` — package law only
2. every node output is error-free and parses to JSON with `summary`, `artifacts`, `win`
3. sink node `parsed.win` is `PASS` with a goal-specific summary
4. `slug` equals `{slug}`; `nodes` length equals {n}; `result` non-empty

## Builder checklist (for harness crafter — not Leslie)

1. Emit `graph.json` conforming to `core/harness/schema.json`
2. Emit single `README.md`
3. Emit `crate/` and compile binary to `bin/opgrok-{slug}`
4. Register entry in `core/binaries/registry.json`
5. Run binary; capture `OPGROK_RESULT`

## WIN

Leslie seals this WC as the only acceptance bar for package completeness.
"#,
        slug = slug,
        goal = goal,
        rows = rows,
        order = order.join(" → "),
        n = graph.nodes.len(),
    );
    fs::write(path, body)?;
    Ok(())
}


fn write_crate(crate_dir: &Path, slug: &str, goal: &str, graph: &HarnessGraph) -> Result<()> {
    fs::create_dir_all(crate_dir.join("src"))?;
    let pkg = format!("opgrok-{slug}");
    let graph_json = serde_json::to_string_pretty(graph)?;
    fs::write(crate_dir.join("graph.json"), &graph_json)?;

    let goal_esc = goal.replace('"', "'");
    let cargo = format!(
        r#"[package]
name = "{pkg}"
version = "0.1.0"
edition = "2021"
description = "OPGROK harness binary for: {goal_esc}"

[[bin]]
name = "opgrok-{slug}"
path = "src/main.rs"

[dependencies]
serde = {{ version = "1", features = ["derive"] }}
serde_json = "1"
clap = {{ version = "4", features = ["derive"] }}
"#,
        pkg = pkg,
        slug = slug,
        goal_esc = goal_esc,
    );
    fs::write(crate_dir.join("Cargo.toml"), cargo)?;

    // Template uses @@SLUG@@ placeholders — avoid format! brace wars.
    let main_rs = HARNESS_MAIN_RS.replace("@@SLUG@@", slug);
    fs::write(crate_dir.join("src/main.rs"), main_rs)?;
    Ok(())
}

const HARNESS_MAIN_RS: &str = r##"//! Auto-generated OPGROK harness: @@SLUG@@
//! Graph: n8n-style SuperGrok chain. Live Grok API when XAI_API_KEY set.

use clap::Parser;
use serde_json::{json, Value};
use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::Command;

#[derive(Parser, Debug)]
#[command(name = "opgrok-@@SLUG@@")]
struct Cli {
    #[arg(long)]
    goal: String,
    /// Skip Grok API; emit planned prompts only
    #[arg(long, default_value_t = false)]
    dry_run: bool,
    #[arg(long)]
    graph: Option<PathBuf>,
}

fn main() {
    let cli = Cli::parse();
    let graph_path = cli.graph.unwrap_or_else(|| {
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("graph.json")
    });
    let raw = fs::read_to_string(&graph_path).expect("graph.json");
    let graph: Value = serde_json::from_str(&raw).expect("graph parse");
    let nodes = graph["nodes"].as_array().cloned().unwrap_or_default();

    let mut blackboard: BTreeMap<String, Value> = BTreeMap::new();
    blackboard.insert("goal".into(), json!(cli.goal));

    let dry = cli.dry_run || env::var("XAI_API_KEY").is_err();
    let mut node_results = Vec::new();

    for node in &nodes {
        let id = node["id"].as_str().unwrap_or("?");
        let sg = node["sg_name"].as_str().unwrap_or("?");
        let purpose = node["purpose"].as_str().unwrap_or("");
        let skill_path = node["skill_path"].as_str().unwrap_or("");
        let process = node["ipo"]["process"].as_str().unwrap_or("");

        let bb = serde_json::to_string(&blackboard).unwrap_or_else(|_| "{}".into());
        let prompt = format!(
            "You are SuperGrok `{sg}`.\nPurpose: {purpose}\nProcess: {process}\nGoal: {goal}\nBlackboard: {bb}\nSkill path: {skill_path}\nReturn concise JSON with keys summary and artifacts.",
            sg = sg,
            purpose = purpose,
            process = process,
            goal = cli.goal,
            bb = bb,
            skill_path = skill_path,
        );

        let output = if dry {
            json!({
                "mode": "dry_run",
                "sg": sg,
                "prompt_preview": prompt.chars().take(500).collect::<String>(),
            })
        } else {
            match call_grok(&prompt) {
                Ok(v) => v,
                Err(e) => json!({"error": e}),
            }
        };

        let key = format!("{id}.output");
        blackboard.insert(key, output.clone());
        node_results.push(json!({
            "id": id,
            "sg_name": sg,
            "output": output,
        }));
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
                return !dry; // dry rows carry no parsed contract; live junk fails
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
        "slug": "@@SLUG@@",
        "goal": cli.goal,
        "dry_run": dry,
        "nodes": node_results.len(),
        "node_results": node_results,
        "result": sink,
        "blackboard_keys": blackboard.keys().cloned().collect::<Vec<_>>(),
    });
    println!("{}", serde_json::to_string_pretty(&result).unwrap());
}

fn call_grok(prompt: &str) -> Result<Value, String> {
    let key = env::var("XAI_API_KEY").map_err(|_| "XAI_API_KEY missing".to_string())?;
    let model = env::var("OPGROK_MODEL").unwrap_or_else(|_| "grok-4".into());
    let body = json!({
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a SuperGrok node in an OPGROK harness. Be concise. Prefer JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    });
    let tmp = env::temp_dir().join("opgrok-harness-body.json");
    fs::write(&tmp, body.to_string()).map_err(|e| e.to_string())?;
    let auth = format!("Authorization: Bearer {key}");
    let data_arg = format!("@{}", tmp.display());
    let out = Command::new("curl")
        .args([
            "-sS",
            "https://api.x.ai/v1/chat/completions",
            "-H",
            auth.as_str(),
            "-H",
            "Content-Type: application/json",
            "-d",
            data_arg.as_str(),
        ])
        .output()
        .map_err(|e| e.to_string())?;
    if !out.status.success() {
        return Err(String::from_utf8_lossy(&out.stderr).into());
    }
    let v: Value = serde_json::from_slice(&out.stdout).map_err(|e| e.to_string())?;
    Ok(v)
}
"##;

fn update_registry(repo: &Path, slug: &str, goal: &str, hired: &[String]) -> Result<()> {
    let path = repo.join("core/binaries/registry.json");
    let mut reg: Value = if path.exists() {
        serde_json::from_str(&fs::read_to_string(&path)?)?
    } else {
        json!({"version":"1.0.0","harnesses":[]})
    };
    let entry = json!({
        "slug": slug,
        "goal": goal,
        "path": format!("core/binaries/{slug}"),
        "binary": format!("core/binaries/{slug}/bin/opgrok-{slug}"),
        "readme": format!("core/binaries/{slug}/README.md"),
        "hired": hired,
        "updated_at": iso_now(),
    });
    let arr = reg
        .get_mut("harnesses")
        .and_then(|h| h.as_array_mut())
        .context("registry harnesses")?;
    arr.retain(|h| h.get("slug").and_then(|s| s.as_str()) != Some(slug));
    arr.push(entry);
    fs::write(path, serde_json::to_string_pretty(&reg)? + "\n")?;
    Ok(())
}


/// Craft a full harness package for `goal` under `repo_root/core/binaries/<slug>/`.
pub fn craft(repo_root: impl AsRef<Path>, goal: &str, hire_limit: usize) -> Result<HarnessPackage> {
    let repo = repo_root.as_ref();
    if goal.trim().is_empty() {
        bail!("goal must be non-empty");
    }
    let index = SuperGrokIndex::load_from_repo_root(repo)
        .map_err(|e| anyhow::anyhow!("{e}"))
        .context("load SuperGrok registry")?;
    let slug = slugify(goal);
    let hired_meta = hire(&index, goal, hire_limit);
    if hired_meta.len() < 2 {
        bail!("need at least 2 SuperGroks hired");
    }
    let hired_names: Vec<String> = hired_meta.iter().map(|m| m.name.clone()).collect();
    let graph = build_graph(&slug, goal, &hired_meta);

    let root = repo.join("core/binaries").join(&slug);
    let bin_dir = root.join("bin");
    let crate_dir = root.join("crate");
    fs::create_dir_all(&bin_dir)?;
    fs::create_dir_all(&crate_dir)?;

    let graph_path = root.join("graph.json");
    fs::write(&graph_path, serde_json::to_string_pretty(&graph)? + "\n")?;

    let readme = root.join("README.md");
    write_readme(&readme, &slug, goal, &graph)?;

    let wc = root.join("WINNING_CONDITION.md");
    write_wc(&wc, &slug, goal, &graph)?;

    write_crate(&crate_dir, &slug, goal, &graph)?;

    // Placeholder marker until cargo compile
    let binary_hint = bin_dir.join(format!("opgrok-{slug}"));
    let stub = format!(
        "#!/usr/bin/env bash\n# Stub until `cargo build --release` in crate/\nset -euo pipefail\nDIR=\"$(cd \"$(dirname \"$0\")/../crate\" && pwd)\"\nif command -v cargo >/dev/null 2>&1; then\n  cargo run --manifest-path \"$DIR/Cargo.toml\" -- --goal \"${{1:-{goal}}}\" \"${{@:2}}\"\nelse\n  echo '{{\"win\":\"FAIL\",\"error\":\"cargo not installed; open crate/ and build\"}}'\n  exit 1\nfi\n",
        goal = goal.replace('\'', ""),
        slug = slug,
    );
    fs::write(&binary_hint, stub)?;
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut perms = fs::metadata(&binary_hint)?.permissions();
        perms.set_mode(0o755);
        fs::set_permissions(&binary_hint, perms)?;
    }

    update_registry(repo, &slug, goal, &hired_names)?;

    Ok(HarnessPackage {
        slug,
        root,
        readme,
        winning_condition: wc,
        graph: graph_path,
        crate_dir,
        binary_hint,
        hired: hired_names,
    })
}

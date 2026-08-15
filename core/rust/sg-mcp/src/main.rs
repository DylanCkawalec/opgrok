//! SuperGrok MCP-facing process (prototype).
//!
//! Not a full MCP wire protocol yet — exposes the same capabilities the future
//! MCP server will: list, route, describe, load skill markdown.
//!
//! Usage:
//!   opgrok-sg-mcp --repo . list
//!   opgrok-sg-mcp --repo . route "fix rust borrow checker"
//!   opgrok-sg-mcp --repo . load rust-smith
//!   opgrok-sg-mcp --repo . tools-manifest

use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use opgrok_sg_runtime::SuperGrokIndex;
use serde_json::json;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(name = "opgrok-sg-mcp", about = "SuperGrok MCP tool surface (prototype)")]
struct Cli {
    /// Repo root containing core/skills/
    #[arg(long, default_value = ".")]
    repo: PathBuf,

    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// List skills (optional category filter)
    List {
        #[arg(long)]
        category: Option<String>,
        #[arg(long, default_value_t = 50)]
        limit: usize,
    },
    /// Intent → ranked SuperGroks
    Route {
        intent: String,
        #[arg(long, default_value_t = 8)]
        limit: usize,
    },
    /// Describe one skill by name or sg_id
    Describe { name: String },
    /// Load SKILL.md body
    Load { name: String },
    /// List categories + SuperGrok counts (from MCP_CATALOG or registry)
    Categories,
    /// Return category navigator skill record
    Nav { category: String },
    /// Emit MCP-style tools manifest JSON
    ToolsManifest,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    let idx = SuperGrokIndex::load_from_repo_root(&cli.repo)
        .with_context(|| format!("load registry under {}", cli.repo.display()))?;

    match cli.cmd {
        Cmd::List { category, limit } => {
            let items = if let Some(cat) = category {
                idx.by_category(&cat)
            } else {
                idx.mcp_descriptors()
                    .into_iter()
                    .filter_map(|d| idx.get(&d.name))
                    .collect()
            };
            let out: Vec<_> = items
                .into_iter()
                .take(limit)
                .map(|sk| {
                    json!({
                        "name": sk.name,
                        "sg_id": sk.sg_id,
                        "call": sk.call,
                        "category": sk.category,
                        "nest": sk.nest,
                        "intent": sk.intent,
                        "binary_id": sk.binary_id,
                    })
                })
                .collect();
            println!("{}", serde_json::to_string_pretty(&out)?);
        }
        Cmd::Route { intent, limit } => {
            let hits = idx.route(&intent, limit);
            let out: Vec<_> = hits
                .into_iter()
                .map(|sk| {
                    json!({
                        "name": sk.name,
                        "sg_id": sk.sg_id,
                        "call": sk.call,
                        "nest": sk.nest,
                        "intent": sk.intent,
                        "purpose": sk.purpose,
                        "binary_id": sk.binary_id,
                    })
                })
                .collect();
            println!("{}", serde_json::to_string_pretty(&out)?);
        }
        Cmd::Describe { name } => {
            let sk = idx
                .get(&name)
                .ok_or_else(|| anyhow::anyhow!("not found: {name}"))?;
            println!("{}", serde_json::to_string_pretty(sk)?);
        }
        Cmd::Load { name } => {
            let body = opgrok_sg_runtime::load_skill_markdown(&cli.repo, &idx, &name)
                .with_context(|| format!("load {name}"))?;
            print!("{body}");
        }
        Cmd::Categories => {
            let mut cats = idx.list_categories();
            cats.sort();
            let out: Vec<_> = cats
                .into_iter()
                .map(|c| {
                    json!({
                        "category": c,
                        "count": idx.by_category(&c).len(),
                        "navigator": format!("cat-{c}"),
                        "call": format!("/cat-{c}"),
                    })
                })
                .collect();
            println!("{}", serde_json::to_string_pretty(&out)?);
        }
        Cmd::Nav { category } => {
            let name = if category.starts_with("cat-") {
                category.clone()
            } else {
                format!("cat-{category}")
            };
            if let Some(sk) = idx.get(&name) {
                println!("{}", serde_json::to_string_pretty(sk)?);
            } else {
                // fallback: list roles in category
                let items: Vec<_> = idx
                    .by_category(&category)
                    .into_iter()
                    .map(|sk| {
                        json!({
                            "name": sk.name,
                            "call": sk.call,
                            "role": sk.role,
                            "intent": sk.intent,
                            "path": sk.path,
                        })
                    })
                    .collect();
                println!(
                    "{}",
                    serde_json::to_string_pretty(&json!({
                        "category": category,
                        "navigator_missing": true,
                        "roles": items,
                    }))?
                );
            }
        }
        Cmd::ToolsManifest => {
            let catalog = cli.repo.join("core/skills/_framework/MCP_CATALOG.json");
            let nav = cli.repo.join("core/skills/_framework/NAVIGATION.md");
            let manifest = json!({
                "name": "opgrok-supergrok",
                "version": "1.0.0",
                "description": "OPGROK v1.0.0 SuperGrok catalog + harness MCP (route, load, mode)",
                "skills_root": "core/skills",
                "registry": "core/skills/_framework/REGISTRY.json",
                "mcp_catalog": "core/skills/_framework/MCP_CATALOG.json",
                "navigation": "core/skills/_framework/NAVIGATION.md",
                "glossary": "core/skills/_framework/AGENT_GLOSSARY.json",
                "catalog_exists": catalog.is_file(),
                "navigation_exists": nav.is_file(),
                "traversal": [
                    "goal → /opgrok if multi-agent",
                    "else match category → /cat-<category>",
                    "pick /<category>-<role> by intent/purpose",
                    "sg_load path from REGISTRY"
                ],
                "tools": [
                    {
                        "name": "sg_categories",
                        "description": "List SuperGrok categories with counts and navigator calls",
                        "input_schema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "sg_nav",
                        "description": "Get category navigator (cat-<category>) or list roles",
                        "input_schema": {
                            "type": "object",
                            "required": ["category"],
                            "properties": {"category": {"type": "string"}}
                        }
                    },
                    {
                        "name": "sg_list",
                        "description": "List SuperGrok agents (optional category)",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "category": {"type": "string"},
                                "limit": {"type": "integer", "default": 50}
                            }
                        }
                    },
                    {
                        "name": "sg_route",
                        "description": "Route natural-language intent to SuperGroks",
                        "input_schema": {
                            "type": "object",
                            "required": ["intent"],
                            "properties": {
                                "intent": {"type": "string"},
                                "limit": {"type": "integer", "default": 8}
                            }
                        }
                    },
                    {
                        "name": "sg_describe",
                        "description": "Describe one SuperGrok by name or sg_id",
                        "input_schema": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {"name": {"type": "string"}}
                        }
                    },
                    {
                        "name": "sg_load",
                        "description": "Load SKILL.md for a SuperGrok",
                        "input_schema": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {"name": {"type": "string"}}
                        }
                    },
                    {
                        "name": "sg_run_binary",
                        "description": "Invoke SuperGrok binary_id (stubs until implemented)",
                        "input_schema": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {
                                "name": {"type": "string"},
                                "ctx_json": {"type": "string"}
                            }
                        }
                    }
                ]
            });
            println!("{}", serde_json::to_string_pretty(&manifest)?);
        }
    }

    Ok(())
}

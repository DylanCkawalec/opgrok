//! `opgrok-sg` — operator CLI for SuperGrok + harness craft.

use anyhow::{Context, Result};
use clap::{Parser, Subcommand};
use opgrok_sg_runtime::SuperGrokIndex;
use std::path::PathBuf;
use std::process::Command;

#[derive(Parser, Debug)]
#[command(
    name = "opgrok-sg",
    about = "SuperGrok control plane — route, craft harnesses (@opgrok)"
)]
struct Cli {
    #[arg(long, default_value = ".")]
    repo: PathBuf,
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Show SuperGrok registry summary
    Status,
    /// List categories
    Categories,
    /// List skills in a category
    List { category: String },
    /// Route intent text to SuperGroks
    Route {
        intent: String,
        #[arg(long, default_value_t = 8)]
        limit: usize,
    },
    /// Print skill path + intent/purpose
    Show { name: String },
    /// Print full SKILL.md
    Load { name: String },
    /// @opgrok craft: hire SuperGroks, Leslie WC, graph, README, crate → core/binaries/
    Craft {
        /// User goal (same text as after @opgrok)
        goal: String,
        #[arg(long, default_value_t = 8)]
        hire: usize,
    },
    /// Run a harness slug (binary stub or cargo run)
    Run {
        slug: String,
        #[arg(long)]
        goal: Option<String>,
        #[arg(long, default_value_t = false)]
        dry_run: bool,
    },
    /// List crafted harness binaries
    Harnesses,
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match &cli.cmd {
        Cmd::Craft { goal, hire } => {
            let pkg = opgrok_sg_harness::craft(&cli.repo, goal, *hire)?;
            println!("@opgrok craft complete");
            println!("slug:     {}", pkg.slug);
            println!("root:     {}", pkg.root.display());
            println!("readme:   {}", pkg.readme.display());
            println!("wc:       {}", pkg.winning_condition.display());
            println!("graph:    {}", pkg.graph.display());
            println!("crate:    {}", pkg.crate_dir.display());
            println!("binary:   {}", pkg.binary_hint.display());
            println!("hired:    {}", pkg.hired.join(", "));
            println!("WIN: PASS — package has 1 README + binary entrypoint + Leslie WC");
            return Ok(());
        }
        Cmd::Run {
            slug,
            goal,
            dry_run,
        } => {
            let bin = cli
                .repo
                .join("core/binaries")
                .join(slug)
                .join("bin")
                .join(format!("opgrok-{slug}"));
            let g = goal
                .clone()
                .unwrap_or_else(|| format!("run harness {slug}"));
            let mut cmd = Command::new(&bin);
            cmd.arg("--goal").arg(&g);
            if *dry_run {
                cmd.arg("--dry-run");
            }
            let status = cmd.status().with_context(|| format!("exec {}", bin.display()))?;
            if !status.success() {
                anyhow::bail!("harness exited {}", status);
            }
            return Ok(());
        }
        Cmd::Harnesses => {
            let reg_path = cli.repo.join("core/binaries/registry.json");
            let raw = std::fs::read_to_string(&reg_path).unwrap_or_else(|_| {
                r#"{"harnesses":[]}"#.into()
            });
            println!("{raw}");
            return Ok(());
        }
        _ => {}
    }

    let idx = SuperGrokIndex::load_from_repo_root(&cli.repo).with_context(|| {
        format!(
            "load {}",
            cli.repo
                .join("core/skills/_framework/REGISTRY.json")
                .display()
        )
    })?;

    match cli.cmd {
        Cmd::Status => {
            let reg = idx.registry.as_ref().context("empty registry")?;
            println!("SuperGrok registry {}", reg.version);
            println!("layout: {}", reg.layout);
            println!("count: {}", reg.count);
            println!("skills_root: {}", reg.skills_root);
            println!("categories: {}", reg.categories.len());
            println!("invoke: @opgrok <goal>  |  opgrok-sg craft \"<goal>\"");
        }
        Cmd::Categories => {
            for c in idx.list_categories() {
                let n = idx.by_category(&c).len();
                println!("{c}\t{n}");
            }
        }
        Cmd::List { category } => {
            for sk in idx.by_category(&category) {
                println!("{}\t{}\t/{}\t{}", sk.sg_id, sk.nest, sk.name, sk.shorthand);
            }
        }
        Cmd::Route { intent, limit } => {
            for sk in idx.route(&intent, limit) {
                println!("{}\t{}\t{}\t{}", sk.name, sk.nest, sk.intent, sk.binary_id);
            }
        }
        Cmd::Show { name } => {
            let sk = idx.get(&name).with_context(|| format!("not found: {name}"))?;
            println!("name:      {}", sk.name);
            println!("sg_id:     {}", sk.sg_id);
            println!("call:      {}", sk.call);
            println!("nest:      {}", sk.nest);
            println!("path:      {}", sk.path);
            println!("binary:    {}", sk.binary_id);
            println!("intent:    {}", sk.intent);
            println!("purpose:   {}", sk.purpose);
        }
        Cmd::Load { name } => {
            let body = opgrok_sg_runtime::load_skill_markdown(&cli.repo, &idx, &name)?;
            print!("{body}");
        }
        Cmd::Craft { .. } | Cmd::Run { .. } | Cmd::Harnesses => unreachable!(),
    }
    Ok(())
}

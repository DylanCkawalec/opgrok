//! CLI: craft OPGROK SuperGrok harness packages.

use anyhow::Result;
use clap::{Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(name = "opgrok-sg-harness", about = "Craft SuperGrok harness binaries")]
struct Cli {
    #[arg(long, default_value = ".")]
    repo: PathBuf,
    #[command(subcommand)]
    cmd: Cmd,
}

#[derive(Subcommand, Debug)]
enum Cmd {
    /// Hire SuperGroks + Leslie WC + graph + README + crate → core/binaries/<slug>
    Craft {
        goal: String,
        #[arg(long, default_value_t = 8)]
        hire: usize,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.cmd {
        Cmd::Craft { goal, hire } => {
            let pkg = opgrok_sg_harness::craft(&cli.repo, &goal, hire)?;
            println!("slug:     {}", pkg.slug);
            println!("root:     {}", pkg.root.display());
            println!("readme:   {}", pkg.readme.display());
            println!("wc:       {}", pkg.winning_condition.display());
            println!("graph:    {}", pkg.graph.display());
            println!("crate:    {}", pkg.crate_dir.display());
            println!("binary:   {}", pkg.binary_hint.display());
            println!("hired:    {}", pkg.hired.join(", "));
            println!("WIN: PASS — harness package sealed (compile binary via cargo in crate/)");
        }
    }
    Ok(())
}

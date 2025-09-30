use anyhow::Result;
use clap::Parser;
use std::io::{self, Write};

#[cfg(feature = "terminal")]
use grok_chat_app::ui::run_terminal_chat;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Run in terminal mode (requires terminal feature)
    #[arg(short, long)]
    terminal: bool,

    /// Run HTTP API server
    #[arg(short, long)]
    server: bool,

    /// Port for HTTP server
    #[arg(short, long, default_value = "3000")]
    port: u16,

    /// Host for HTTP server
    #[arg(short = 'H', long, default_value = "127.0.0.1")]
    host: String,

    /// Session ID to resume (terminal mode)
    #[arg(short = 'i', long)]
    session: Option<String>,

    /// Model to use
    #[arg(short, long, default_value = "grok-4-0709")]
    model: String,

    /// Message to send (if not provided, will enter interactive mode)
    #[arg(short = 'g', long)]
    message: Option<String>,

    /// System prompt to use
    #[arg(
        short = 'y',
        long,
        default_value = "You are Grok, a helpful and maximally truthful AI built by xAI, not based on any other companies and their models."
    )]
    system: String,

    /// Maximum tokens
    #[arg(short = 'x', long, default_value = "2048")]
    max_tokens: i32,

    /// Temperature
    #[arg(short = 'p', long, default_value = "0.7")]
    temperature: f32,
}

#[tokio::main]
async fn main() -> Result<()> {
    // Load environment variables
    dotenvy::dotenv().ok();

    let args = Args::parse();

    // Check for API key
    if std::env::var("XAI_API_KEY").is_err() {
        eprintln!("❌ Error: XAI_API_KEY environment variable is required");
        eprintln!("💡 Please set your xAI API key:");
        eprintln!("   export XAI_API_KEY=your_api_key_here");
        std::process::exit(1);
    }

    #[cfg(feature = "terminal")]
    if args.terminal || (!args.server && args.message.is_none()) {
        // Run terminal interface
        return run_terminal_chat(args.session, args.model).await;
    }

    #[cfg(feature = "server")]
    if args.server {
        // Run HTTP API server
        return grok_chat_app::api::run_server(args.host, args.port).await;
    }

    if let Some(message) = args.message {
        // Single message mode
        let response = send_message(
            &args.model,
            &args.system,
            &message,
            args.max_tokens,
            args.temperature,
        )
        .await?;
        println!("{}", response);
    } else {
        // Interactive mode (fallback)
        println!("🤖 Grok Chat (Interactive Mode)");
        println!("Model: {}", args.model);
        println!("Type 'quit' or 'exit' to end the conversation.");
        println!();

        loop {
            print!("You: ");
            io::stdout().flush()?;

            let mut input = String::new();
            std::io::stdin().read_line(&mut input)?;
            let input = input.trim();

            if input == "quit" || input == "exit" {
                break;
            }

            if input.is_empty() {
                continue;
            }

            print!("Grok: ");
            io::stdout().flush()?;

            match send_message(
                &args.model,
                &args.system,
                input,
                args.max_tokens,
                args.temperature,
            )
            .await
            {
                Ok(response) => {
                    println!("{}", response);
                }
                Err(e) => {
                    eprintln!("❌ Error: {}", e);
                    eprintln!("💡 Make sure your XAI_API_KEY is set correctly in the .env file");
                }
            }

            println!();
        }
    }

    Ok(())
}

async fn send_message(
    model: &str,
    system_prompt: &str,
    message: &str,
    max_tokens: i32,
    temperature: f32,
) -> Result<String> {
    use tokio::time::{timeout, Duration};

    let api_key = std::env::var("XAI_API_KEY")
        .map_err(|_| anyhow::anyhow!("❌ XAI_API_KEY environment variable is required"))?;

    let client = reqwest::Client::new();

    let request_body = serde_json::json!({
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": false
    });

    // Add timeout to prevent hanging
    let response = timeout(
        Duration::from_secs(60), // 60 second timeout
        client
            .post("https://api.x.ai/v1/chat/completions")
            .header("Authorization", format!("Bearer {}", api_key))
            .header("Content-Type", "application/json")
            .json(&request_body)
            .send()
    ).await??;

    if !response.status().is_success() {
        let status = response.status();
        let error_text = response.text().await.unwrap_or_default();
        return Err(anyhow::anyhow!("❌ API Error ({}): {}", status, error_text));
    }

    let response_json: serde_json::Value = response.json().await?;

    let content = response_json["choices"]
        .get(0)
        .and_then(|choice| choice["message"]["content"].as_str())
        .ok_or_else(|| anyhow::anyhow!("❌ No response content found in API response"))?;

    Ok(content.to_string())
}

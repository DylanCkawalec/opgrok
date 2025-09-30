# 🤖 Grok Chat App

A lightweight, terminal-based chat application for interacting with xAI's Grok models directly from your command line. This Rust application provides a simple and efficient way to have conversations with Grok AI.

## Features

- **Interactive Terminal Chat**: Chat with Grok directly in your terminal
- **Single Message Mode**: Send individual messages for quick queries
- **Multiple Model Support**: Use any of the available Grok models
- **Configurable Parameters**: Adjust temperature, max tokens, and system prompts
- **Environment Variable Configuration**: Secure API key management
- **Cross-Platform**: Works on Linux, macOS, and Windows

## Prerequisites

- Rust 1.70 or later
- xAI API key (get from [xAI Console](https://console.x.ai/team/default/api-keys))
- SQLite (usually pre-installed on most systems)

## Installation

1. **Clone and navigate to the project:**
   ```bash
   cd /path/to/grok-chat-app
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your xAI API key
   ```

3. **Build the application:**
   ```bash
   cargo build --release
   ```

## Configuration

Edit the `.env` file with your settings:

```bash
# Required: Your xAI API key
XAI_API_KEY=your_api_key_here

# Optional: Database location (defaults to sqlite:grok_chat.db)
DATABASE_URL=sqlite:grok_chat.db

# Optional: Server settings (defaults to 127.0.0.1:3000)
SERVER_HOST=127.0.0.1
SERVER_PORT=3000

# Optional: Default model (defaults to grok-4-0709)
DEFAULT_MODEL=grok-4-0709
```

## Usage

### Interactive Chat Mode (Default)

Start an interactive chat session with Grok:

```bash
# Basic usage with default model (grok-4-0709)
cargo run

# Use a specific model
cargo run -- --model grok-3

# Use a custom system prompt
cargo run -- --system "You are a helpful coding assistant"

# Adjust parameters
cargo run -- --model grok-4-0709 --max-tokens 1024 --temperature 0.5
```

**Interactive Mode:**
- Type your message and press Enter to send
- Type 'quit' or 'exit' to end the conversation
- Each message is sent individually to Grok

### Single Message Mode

Send a single message and get a response:

```bash
# Ask a quick question
cargo run -- --message "What is the capital of France?"

# Use a specific model for the query
cargo run -- --message "Explain quantum computing" --model grok-4-0709
```

### Command Line Options

- `-t, --terminal`: Run in terminal mode (requires terminal feature)
- `-s, --server`: Run HTTP API server (requires server feature)
- `-p, --port PORT`: Port for HTTP server (default: 3000)
- `-H, --host HOST`: Host for HTTP server (default: 127.0.0.1)
- `-i, --session ID`: Session ID to resume (terminal mode)
- `-m, --model MODEL`: Choose the Grok model to use (default: grok-4-0709)
- `-g, --message MSG`: Send a single message and exit
- `-y, --system PROMPT`: Set a custom system prompt
- `-x, --max-tokens NUM`: Maximum tokens in response (default: 2048)
- `-p, --temperature TEMP`: Response creativity (0.0-2.0, default: 0.7)

## Available Models

The application supports all current Grok models available through the xAI API:

- `grok-4-0709` - Flagship model with advanced reasoning (default)
- `grok-4-fast-reasoning` - Optimized for speed with reasoning traces
- `grok-4-fast-non-reasoning` - Fast responses without reasoning traces
- `grok-3` - Previous generation model
- `grok-3-mini` - Lightweight version of Grok-3

## Development

### Building for Production

```bash
cargo build --release
```

The compiled binary will be available at `target/release/grok-chat-app`.

### Project Structure

- `src/main.rs` - Application entry point with CLI parsing and core chat logic
- `README.md` - This documentation file
- `.env.example` - Example environment configuration
- `Cargo.toml` - Rust project configuration and dependencies

## Troubleshooting

### Common Issues

1. **"XAI_API_KEY not found"**
   - Make sure you have a `.env` file with your API key
   - Check that the API key is valid in [xAI Console](https://console.x.ai)

2. **"API request failed"**
   - Verify your API key is correct and active
   - Check your internet connection
   - Ensure the model name is spelled correctly

3. **Build errors**
   - Make sure you have Rust 1.70 or later installed
   - Run `cargo clean` and try building again
   - Check that all dependencies are available

### Getting Help

For issues with:
- xAI API: Check [xAI Documentation](https://docs.x.ai)
- This application: The code is straightforward - check the main.rs file
- Models and features: Refer to [xAI Console](https://console.x.ai)

## License

This project is built for educational and personal use. Make sure to comply with xAI's API terms of service.

## Support

For issues related to:
- xAI API: Check [xAI Documentation](https://docs.x.ai)
- This application: Create an issue in the project repository
- Models and features: Refer to [xAI Console](https://console.x.ai)

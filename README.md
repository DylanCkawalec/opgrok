# 🤖 opgrok - Local xAI Grok Chat Application

A comprehensive local chat application for xAI's Grok API, featuring both a Rust CLI and a beautiful Python web interface.

## ✨ Features

### Core Capabilities
- **💬 Chat Completions**: Multi-turn conversations with context awareness
- **👁️ Vision (Multimodal)**: Analyze images by attaching them to your messages
- **📁 File Analysis**: Upload text files for context and analysis
- **🔍 Web Search**: Augment queries with real-time DuckDuckGo instant answers
- **🧠 Deep Research Mode**: Comprehensive analysis with expanded context windows
- **💰 Cost Estimation**: Live token usage and cost tracking for all models
- **📊 Session Management**: Persistent conversation history within sessions

### Supported Models
- `grok-4-0709` - Latest Grok 4 model
- `grok-4-fast-reasoning` - Fast reasoning variant
- `grok-4-fast-non-reasoning` - Fast non-reasoning variant
- `grok-3` - Grok 3 model
- `grok-3-mini` - Lightweight Grok 3

### Architecture
- **Rust CLI**: Fast, efficient terminal interface for text-based chat
- **Python Web App**: Beautiful UI with full feature support
  - Multimodal requests (images) → Direct xAI API
  - Text-only requests → Rust CLI (faster)
- **SQLite**: Optional database for persistent chat logs (server feature)

## 🚀 Quick Start

### Prerequisites
- Rust (1.70+)
- Python (3.8+)
- xAI API Key ([get one here](https://x.ai))

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/DylanCkawalec/opgrok.git
cd opgrok
```

2. **Set up your API key:**
```bash
# Create .env file
echo "XAI_API_KEY=your_api_key_here" > grok-chat-app/.env
```

3. **Run the application:**
```bash
bash scripts/run.sh
```

This will:
- Kill any processes on ports 8000/3000
- Build the Rust CLI (release mode)
- Set up Python virtual environment
- Install dependencies
- Start the web server at `http://127.0.0.1:8000`

## 📖 Usage

### Web Interface

Visit `http://127.0.0.1:8000` in your browser.

**Basic Chat:**
1. Type your message
2. Click "Send" or press Ctrl+Enter
3. View response and cost estimate

**Image Analysis (Vision):**
1. Click "Attach Files"
2. Select one or more images
3. Type a question about the image(s)
4. Send - Grok will analyze the images

**File Analysis:**
1. Attach text files (.txt, .md, .json, .py, etc.)
2. Ask questions about the content
3. Files are automatically included in context

**Web Search:**
1. Toggle "Web Search Assist" to "On"
2. Ask factual questions
3. DuckDuckGo results augment the response

**Deep Research Mode:**
1. Select "Deep Research" mode
2. Ask complex questions
3. Get comprehensive, multi-step reasoning

### Rust CLI

**Basic usage:**
```bash
cd grok-chat-app
cargo run --release --features terminal -- -g "What is 2+2?"
```

**With options:**
```bash
cargo run --release --features terminal -- \
  -g "Explain quantum computing" \
  -m grok-4-0709 \
  -x 500 \
  --temperature 0.7
```

**Terminal UI mode:**
```bash
cargo run --release --features terminal -- --terminal
```

**Available options:**
- `-g, --message <MESSAGE>` - Message to send
- `-m, --model <MODEL>` - Model to use (default: grok-4-0709)
- `-x, --max-tokens <N>` - Maximum tokens (default: 2048)
- `--temperature <TEMP>` - Temperature 0.0-2.0 (default: 0.7)
- `-y, --system <PROMPT>` - System prompt
- `--terminal` - Launch interactive terminal UI
- `-i, --session <ID>` - Resume a session

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_xai_capabilities.py
```

Tests include:
- Basic text chat
- Text file attachments
- Image analysis (vision)
- Web search augmentation
- Deep research mode
- Cost estimation
- Model listing
- Combined features

## 📁 Project Structure

```
opgrok/
├── grok-chat-app/           # Rust application
│   ├── src/
│   │   ├── main.rs          # CLI entry point
│   │   ├── lib.rs           # Library exports
│   │   ├── config/          # Configuration
│   │   ├── models/          # Data models
│   │   ├── client/          # xAI API client
│   │   ├── database/        # SQLite (optional)
│   │   ├── ui/              # Terminal UI
│   │   └── api/             # HTTP server (optional)
│   ├── Cargo.toml           # Rust dependencies
│   └── .env                 # API key (create this)
├── webapp/                  # Python web application
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── templates/       # HTML templates
│   │   └── static/          # CSS/JS
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Container support
├── scripts/
│   └── run.sh              # Build & run script
└── test_xai_capabilities.py # Test suite
```

## 🎨 Web UI Features

### Controls
- **Model Selection**: Choose from all available Grok models
- **Temperature**: Adjust randomness (0.0 = deterministic, 2.0 = very creative)
- **Max Tokens**: Limit response length
- **Expected Output Tokens**: For cost estimation
- **Mode**: Standard or Deep Research
- **Context Window**: Number of previous messages to include
- **System Prompt**: Override default behavior
- **File Attachments**: Upload text files or images
- **Web Search Assist**: Augment with real-time data

### Live Estimates
- Prompt tokens
- Completion tokens
- Total tokens
- Cost breakdown (input/output/total)
- Real-time pricing for each model

## 💰 Pricing

Default pricing (per 1M tokens, USD):

| Model | Input | Output |
|-------|-------|--------|
| grok-4-0709 | $5.00 | $15.00 |
| grok-4-fast-reasoning | $3.00 | $6.00 |
| grok-4-fast-non-reasoning | $1.50 | $3.00 |
| grok-3 | $1.00 | $2.00 |
| grok-3-mini | $0.20 | $0.40 |

Override via environment variables:
```bash
export PRICE_GROK_4_0709_INPUT_PER_MTOK=5.0
export PRICE_GROK_4_0709_OUTPUT_PER_MTOK=15.0
```

## 🔧 Advanced Configuration

### Rust Features

**Terminal UI only:**
```bash
cargo build --release --features terminal
```

**API Server only:**
```bash
cargo build --release --features server
```

**Both:**
```bash
cargo build --release --features "terminal,server"
```

### Environment Variables

```bash
# Required
XAI_API_KEY=your_key_here

# Optional
DEFAULT_MODEL=grok-4-0709
PRICE_GROK_4_0709_INPUT_PER_MTOK=5.0
PRICE_GROK_4_0709_OUTPUT_PER_MTOK=15.0
```

## 🐛 Troubleshooting

**Port already in use:**
```bash
# The run.sh script handles this automatically
# Or manually:
lsof -ti:8000 | xargs kill -9
```

**Rust binary not found:**
```bash
cd grok-chat-app
cargo build --release --features terminal
```

**API key not set:**
```bash
export XAI_API_KEY=your_key_here
# Or add to grok-chat-app/.env
```

**httpx not installed:**
```bash
source .venv/bin/activate
pip install httpx
```

## 📚 API Endpoints

### POST `/api/chat`
Main chat endpoint. Supports all features.

**Request:**
```json
{
  "message": "Hello, Grok!",
  "model": "grok-4-0709",
  "max_tokens": 2048,
  "temperature": 0.7,
  "context_window": 6,
  "mode": "standard",
  "expected_output_tokens": 512,
  "web_search": false,
  "files": [
    {"name": "file.txt", "content": "..."},
    {"name": "image.png", "content": "data:image/png;base64,..."}
  ]
}
```

**Response:**
```json
{
  "assistant": "Response text...",
  "session_id": "uuid",
  "model": "grok-4-0709",
  "mode": "standard",
  "estimate": {
    "prompt_tokens": 100,
    "completion_tokens": 512,
    "total_tokens": 612,
    "pricing": {"per_mtok_input": 5.0, "per_mtok_output": 15.0},
    "cost": {"input_usd": 0.0005, "output_usd": 0.00768, "total_usd": 0.00818}
  }
}
```

### POST `/api/estimate`
Estimate cost without inference.

### GET `/api/models`
List available models with pricing.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built with [xAI's Grok API](https://x.ai)
- Rust backend using [Tokio](https://tokio.rs), [Axum](https://github.com/tokio-rs/axum), [Ratatui](https://ratatui.rs)
- Python frontend using [FastAPI](https://fastapi.tiangolo.com)
- Web search powered by [DuckDuckGo](https://duckduckgo.com)

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check existing documentation
- Review the test suite for examples

---

**Note**: xAI currently supports chat completions with vision (analyzing images). Image generation is not supported. Use the vision feature to analyze existing images instead.

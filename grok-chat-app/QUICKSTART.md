# 🚀 Quick Start Guide

## ✅ Your App is Ready!

The Grok Chat application is **fully built and working**. Here's everything you need:

## 📍 Binary Location
```
./target/release/grok-chat-app
```

## ⚡ Common Commands

### Ask a Single Question (Fastest)
```bash
./target/release/grok-chat-app -g "What is the capital of France?"
```

### Launch Interactive Terminal UI
```bash
./target/release/grok-chat-app --terminal
```

### See All Options
```bash
./target/release/grok-chat-app --help
```

## 🎯 What Works Right Now

✅ Single message queries  
✅ Interactive terminal UI  
✅ Multi-turn conversations  
✅ Model selection (5 Grok models)  
✅ Timeout protection (60s)  
✅ Error handling with clear messages  
✅ Session management  
✅ Custom system prompts  
✅ Temperature & token control  

## 🔑 API Key Setup

Your API key is already configured in `.env`:
```bash
XAI_API_KEY=your_api_key_here
```

## 📂 File Organization

All modules are properly organized:
```
src/
├── main.rs           # CLI entry point
├── lib.rs            # Library exports
├── api/              # HTTP server (optional)
├── client/           # xAI API client (optional)
├── config/           # Configuration
├── database/         # SQLite (optional)
├── models/           # Data structures
└── ui/               # Terminal UI
```

## 🎨 Terminal UI Controls

**Insert Mode** (default):
- Type your message
- Press `Enter` to send
- Press `Esc` for Normal mode

**Normal Mode**:
- `i` - Insert mode
- `h` - Help
- `q` - Quit
- `m` - Change model
- `c` - New session

## 🤖 Available Models

- `grok-4-0709` (default, best)
- `grok-4-fast-reasoning` (fast + detailed)
- `grok-4-fast-non-reasoning` (fastest)
- `grok-3` (standard)
- `grok-3-mini` (lightweight)

## 🔧 Command Options

```bash
-g <MESSAGE>      # Send single message
-m <MODEL>        # Choose model
-p <TEMP>         # Set temperature (0.0-2.0)
-x <TOKENS>       # Max response tokens
-y <PROMPT>       # Custom system prompt
-i <SESSION>      # Resume session
--terminal        # Launch UI
--server          # HTTP API mode
```

## 📖 Full Documentation

- **Complete usage guide:** [USAGE.md](USAGE.md)
- **Main README:** [README.md](README.md)

## 🎯 Try These Examples

```bash
# Math
./target/release/grok-chat-app -g "What is 15 * 23?"

# Coding
./target/release/grok-chat-app -g "Explain Rust ownership"

# Creative
./target/release/grok-chat-app -g "Write a haiku about code" -p 1.0

# Interactive chat
./target/release/grok-chat-app --terminal
```

## ✨ Pro Tip

For daily use, add an alias to your shell:
```bash
echo 'alias grok="~/Desktop/developer/opgrok/grok-chat-app/target/release/grok-chat-app"' >> ~/.zshrc
source ~/.zshrc

# Now you can just type:
grok -g "Hello Grok!"
```

---

**Everything is working!** 🎉 Start chatting with Grok now!

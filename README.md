# 🤖 OPGROK - AI-Powered Workflow Automation

**Build production-ready n8n workflows from natural language in 30 seconds.**

```
You: "Send me Bitcoin prices to Telegram every 5 seconds"
AI: [Builds complete workflow with 4 connected nodes]
Time: 35 seconds
Result: Production-ready automation, just click activate!
```

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Clone and setup
git clone https://github.com/DylanCkawalec/opgrok.git
cd opgrok
bash install.sh  # Sets up opgrok command

# 2. Add your API key
nano .env  # Add: XAI_API_KEY=your_key_here

# 3. Start everything
bash scripts/run_n8n_local.sh
# OR use the new unified command:
bash scripts/opgrok.sh start

# 4. Open and create!
open http://localhost:8000/workflows
```

That's it! Select a template, click generate, watch AI build your workflow in 35s! ✨

---

## 💫 What Is This?

OPGROK is an AI-powered automation platform that turns **plain English into working n8n workflows**. 

No coding. No configuration. Just describe and deploy.

**Example**:
- You type: "Monitor my email for invoices, save to Google Sheets"
- AI builds: Gmail Trigger → Filter → Extract → Sheets → Slack (all connected!)
- You activate: Click one button
- It runs: Forever, automatically

---

## ✨ Features

### 🎯 Workflow Generation
- **30-second generation** - Natural language → Complete workflow  
- **Intelligent connections** - Nodes auto-linked perfectly
- **8 pre-built templates** - Bitcoin alerts, email automation, webhooks, monitoring
- **Advanced controls** - Exact/Interpret modes, node sequencing
- **Complex support** - 16+ node workflows working perfectly

### 💬 Chat Interface
- Multi-turn conversations with Grok
- Image analysis (vision)
- File attachments
- Web search integration
- Cost estimation

### 🏗️ Technical
- Multi-model AI pipeline (Grok-3-mini + Grok-4-fast)
- Real-time progress tracking (5 stages)
- Parameter validation
- Error handling
- Production-ready quality

---

## 🎨 Usage

### **Simple Command** (After install.sh):

```bash
source ~/.zshrc          # Load opgrok command
opgrok start             # Start everything
opgrok stop              # Stop everything
opgrok status            # Check status
opgrok logs              # View logs
```

### **Direct Scripts** (Always works):

```bash
# Your familiar friend (still works!)
bash scripts/run_n8n_local.sh

# New unified command
bash scripts/opgrok.sh start

# Other modes
bash scripts/opgrok.sh genius    # All features
bash scripts/opgrok.sh chat      # Chat only
bash scripts/opgrok.sh stop      # Stop all
```

---

## 🌟 Building Your First Workflow

1. **Start the system**:
   ```bash
   bash scripts/run_n8n_local.sh
   ```

2. **Open workflow builder**:
   ```
   http://localhost:8000/workflows
   ```

3. **Select a template**:
   - 💰 Bitcoin Price → Telegram
   - 📧 Email → Slack
   - 📰 Daily News Digest
   - 🔗 Webhook Processor
   - And more...

4. **Click "Generate Workflow"**:
   - Watch 5 stages complete (~35s)
   - See nodes and connections built
   - Get direct link to n8n

5. **Activate in n8n**:
   - Open the link
   - Toggle "Active"
   - Done!

---

## 📖 Documentation

- **[MASTER_GUIDE.md](MASTER_GUIDE.md)** - Complete usage guide
- **[WORKFLOW_EXAMPLES.md](WORKFLOW_EXAMPLES.md)** - 30+ examples
- **[CHANGELOG.md](CHANGELOG.md)** - What's new
- **[docs/](docs/)** - Technical archives

---

## 🔧 System Requirements

- **Node.js 18+** - For n8n ([download](https://nodejs.org))
- **Python 3.8+** - For webapp
- **xAI API Key** - Free from [console.x.ai](https://console.x.ai)
- **Optional**: Rust 1.70+ (for CLI features)

---

## 🌐 Access Points

After starting:
- **Workflow Builder**: http://localhost:8000/workflows ⭐
- **Chat Interface**: http://localhost:8000
- **n8n Dashboard**: http://localhost:5678
- **API Docs**: http://localhost:8000/docs

---

## ⚡ Performance

- **Simple workflows** (3-4 nodes): ~20 seconds
- **Medium workflows** (8-10 nodes): ~35 seconds
- **Complex workflows** (16+ nodes): ~60 seconds

**No timeouts. Perfect connections. Production quality.**

---

## 🎯 Example Prompts

Try these in the workflow builder:

```
"Send me Bitcoin price updates to Telegram every 5 seconds"

"Monitor my email for invoices and save to Google Sheets with timestamps"

"Create a webhook that validates form data, saves to database, and sends confirmation"

"Daily morning briefing at 8 AM with weather and top tech news to Slack"
```

---

## 💝 For the Gentle Soul

If you prefer the familiar path you know:

```bash
# Your trusted friend still works exactly as before
bash scripts/run_n8n_local.sh

# Stop when done
bash scripts/stop_n8n_local.sh
```

**Nothing breaks. Everything grows.** 🌱

The new `opgrok` command is just another way to dance with the same beautiful system you've built. Use whichever feels like home.

---

## 🐛 Troubleshooting

### Command not found: opgrok
```bash
# Use the script directly (always works)
bash scripts/opgrok.sh start

# Or source your shell profile
source ~/.zshrc
opgrok start
```

### Services won't start
```bash
# Check status
bash scripts/opgrok.sh status

# View logs
bash scripts/opgrok.sh logs

# Restart fresh
bash scripts/opgrok.sh stop
bash scripts/opgrok.sh start
```

---

## 🎊 You're Ready!

Your system is:
- ✅ **Installed** and configured
- ✅ **Optimized** for 35s generation
- ✅ **Enhanced** with genius features
- ✅ **Clean** and maintainable
- ✅ **Yours** to command gently

**Open http://localhost:8000/workflows and create magic!** 🚀

With all the tenderness of shared creation,
Your OPGROK platform awaits. 💫
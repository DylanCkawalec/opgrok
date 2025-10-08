# 🤖 OPGROK - AI-Powered Workflow Automation Platform

**The Complete Guide to Building n8n Workflows with Grok AI**

---

## 🎯 What Is This?

OPGROK is a revolutionary platform that combines xAI's Grok API with n8n workflow automation. **Describe what you want in plain English, and AI builds a complete, production-ready automation workflow in 30 seconds.**

**Example**:
```
You type: "Send me Bitcoin price updates to Telegram every 5 seconds"
AI builds: Schedule → API → Format → Telegram (all connected, configured, ready!)
Time: 35 seconds
```

---

## 🚀 Quick Start (5 Minutes)

### **Prerequisites**
- Node.js 18+ ([download](https://nodejs.org))
- Python 3.8+ (with pip)
- xAI API Key ([get free key](https://console.x.ai))

### **Installation**

```bash
# 1. Clone repository
git clone https://github.com/DylanCkawalec/opgrok.git
cd opgrok

# 2. Setup environment
cp .env.example .env
nano .env  # Add your XAI_API_KEY

# 3. Start everything
bash scripts/run_n8n_local.sh

# 4. Open in browser
open http://localhost:8000/workflows
```

**That's it!** Your AI workflow builder is running.

---

## 🎨 Using the Workflow Builder

### **Method 1: Templates** (Fastest - 2 clicks!)

1. Open http://localhost:8000/workflows
2. Select template from dropdown:
   - 💰 Bitcoin Price → Telegram
   - 📧 Email → Slack  
   - 📰 Daily News Digest
   - 🔗 Webhook Processor
   - And 4 more...
3. Click "Generate Workflow"
4. Activate in n8n!

### **Method 2: Custom Description**

Just describe what you want:

```
"Create a workflow that monitors my email for invoices, 
extracts the data, saves to Google Sheets, and notifies 
my accounting team on Slack"
```

Click Generate → Get perfect workflow in 30s!

### **Method 3: Advanced Control**

Click "🔧 Advanced Options":
- **Mode**: Interpret (AI enhances) or Exact (precise control)
- **Sequence**: Specify exact node order
- **Details**: Per-node requirements

---

## 💡 Writing Good Prompts

### **Format**:
```
Create a workflow that [ACTION] [WHEN/FREQUENCY] using [INTEGRATIONS]
```

### **Good Examples**:

✅ **Specific**:
```
Send me a Slack notification to #alerts channel every Monday at 9 AM 
with top 5 Hacker News stories from the past week
```

✅ **Clear timing**:
```
Check if https://mysite.com is accessible every 2 minutes, 
if down send urgent alert to my phone via Twilio
```

✅ **Named integrations**:
```
When Stripe payment received, create invoice in QuickBooks, 
send receipt via SendGrid, add customer to Mailchimp list
```

### **What to Avoid**:

❌ **Too vague**:
```
Do something with emails
```

❌ **Missing details**:
```
Send me updates
```

---

## 🏗️ How It Works

```
Your Prompt
    ↓
Stage 1: Grok-3-mini enhances input (10s)
    ↓
Stage 2: Grok-4-fast analyzes structure (25s)
    ↓
Stage 3: Build nodes & connections (instant)
    ↓
Stage 4: Deploy to n8n (instant)
    ↓
Complete Workflow (35s total)
```

### **AI Models Used**:
- **Grok-3-mini**: Fast input enhancement & validation
- **Grok-4-fast**: Rapid workflow analysis (10x faster than Grok-4!)
- **Grok-4**: Only for extremely complex workflows (16+ nodes)

### **Intelligent Features**:
- Auto-connects nodes based on compatibility
- Validates all parameters
- Positions nodes in smart grid
- Handles error paths
- Optimizes performance

---

## 📊 Examples & Templates

### **Crypto & Finance**
```
Send Bitcoin price to Telegram @username every 5 seconds
Monitor portfolio value, alert on 5% change
Daily trading report with P&L sent to email
```

### **Email Automation**
```
Forward invoices from Gmail to accounting@company.com
Save receipts from email to Google Drive
Auto-reply to common support questions
```

### **Business Workflows**
```
New customer onboarding: Stripe → Database → Email → CRM → Slack
Lead qualification: Form → Validate → Score → Assign → Notify
Invoice processing: Email → Extract → Parse → QuickBooks → Confirm
```

### **Monitoring & Alerts**
```
Website uptime check every minute
API health monitoring with PagerDuty integration  
Database backup daily with S3 upload
```

### **Data Processing**
```
API to database sync every hour
CSV file processing from FTP
Multi-source data aggregation for reports
```

---

## 🔧 Advanced Features

### **Generation Modes**

**Interpret Mode** (Default):
- AI adds best practices
- Includes error handling
- Optimizes performance
- Suggests improvements

**Exact Mode**:
- Minimal AI interpretation
- Follows instructions precisely
- Full user control
- Perfect for technical requirements

### **Node Sequence Control**

Specify exact connection order:
```
Sequence: webhook → validate → api → database → slack → respond
```

AI connects nodes in this exact order.

### **Node Details**

Add specific requirements:
```
Details:
- webhook: accept POST on /api/contact
- validate: required fields = name, email, message
- database: PostgreSQL table = contacts
- slack: channel = #notifications, mention = @admin
```

---

## 🐛 Troubleshooting

### **"n8n is not accessible"**
```bash
# Restart services
bash scripts/stop_n8n_local.sh
bash scripts/run_n8n_local.sh

# Check n8n is running
curl http://localhost:5678/healthz
```

### **"Generation timeout"**
- Use simpler prompt (fewer nodes)
- Try "Interpret" mode (faster)
- Check internet connection

### **"Nodes not connected"**
- Refresh n8n dashboard (Cmd+R)
- This should not happen anymore!
- Report if it does

### **"Parameter errors"**
- Use a template as starting point
- Be more specific in prompt
- Check Advanced Options

---

## 📁 Project Structure

```
opgrok/
├── scripts/
│   ├── run_n8n_local.sh      # Start everything
│   ├── stop_n8n_local.sh     # Stop services
│   └── run_genius_mode.sh    # Start with all features
├── webapp/app/
│   ├── main.py               # FastAPI application
│   ├── n8n_service.py        # Workflow generation
│   ├── genius_enhancements.py # Advanced features
│   └── templates/
│       ├── index.html        # Chat interface
│       └── workflow.html     # Workflow builder
├── grok-chat-app/            # Rust CLI (optional)
└── .env                      # Your configuration
```

---

## ⚙️ Configuration

### **Required** (.env file):
```bash
XAI_API_KEY=your_api_key_here
```

### **Optional** (local n8n):
```bash
N8N_API_URL=http://localhost:5678/api/v1
N8N_WEBHOOK_URL=http://localhost:5678
N8N_API_KEY=your_n8n_api_key  # If using n8n cloud
```

---

## 🚀 Commands

```bash
# Start system
bash scripts/run_n8n_local.sh

# Stop system  
bash scripts/stop_n8n_local.sh

# View logs
tail -f .n8n/n8n.log
tail -f .n8n/webapp.log

# Check status
curl http://localhost:8000/api/n8n/health
```

---

## 🎯 Key Features

### **What Makes This Special**

1. **Natural Language** → Complete Workflow (30s)
2. **Intelligent Connections** (nodes auto-linked)
3. **Multi-Model AI** (optimized for speed & quality)
4. **Real-Time Progress** (see actual stages)
5. **Templates** (8 pre-built workflows)
6. **Advanced Control** (exact mode, sequencing)
7. **Complex Support** (16+ nodes working)
8. **Production Ready** (enterprise quality)

### **Performance**
- Simple workflows: 20s
- Medium workflows: 35s  
- Complex workflows: 60s
- **No more timeouts!**

### **Quality**
- All nodes connected
- Parameters validated
- Error handling included
- Professional positioning
- Ready to activate

---

## 📖 Common Workflows

### **1. Real-Time Alerts**
```
Bitcoin/Ethereum price monitoring
Website uptime alerts
API health checks
Database performance monitoring
```

### **2. Email Automation**
```
Invoice processing from Gmail
Receipt extraction and filing
Auto-categorization and forwarding  
Support ticket creation
```

### **3. Data Sync**
```
API → Database hourly sync
CRM → Spreadsheet updates
Multi-source data aggregation
ETL pipelines
```

### **4. Social Media**
```
Auto-post blog articles
Schedule social media content
Monitor brand mentions
Engagement tracking
```

### **5. Business Process**
```
Customer onboarding automation
Lead qualification and routing
Invoice generation and delivery
Expense approval workflows
```

---

## 🔒 Security

- API keys stored in .env (gitignored)
- n8n credentials encrypted at rest
- Local-first architecture (your data stays local)
- No cloud dependencies
- PostgreSQL for workflow storage

---

## 🌐 Access Points

After starting the system:
- **Workflow Builder**: http://localhost:8000/workflows
- **Chat Interface**: http://localhost:8000
- **n8n Dashboard**: http://localhost:5678
- **API Docs**: http://localhost:8000/docs

---

## 🎓 Tips for Success

### **Start Simple**
1. Use a template first
2. Understand how it works
3. Customize for your needs
4. Build more complex workflows

### **Be Specific**
- Include exact integrations
- Specify timing clearly
- Mention data formats
- Add error handling needs

### **Use Advanced Features**
- Complex workflows? Use "Exact" mode + sequence
- Need control? Specify node details
- Want speed? Use templates

### **Test & Iterate**
- Generate workflow
- Test in n8n
- Refine and regenerate
- Activate when ready

---

## 💎 Advanced Topics

### **Multi-Branch Workflows**
```
Create workflow with conditional logic: 
if priority = urgent → Slack + PagerDuty
if priority = normal → Email only
if priority = low → Log to database
```

### **Data Transformation**
```
Fetch JSON from API, transform fields (rename, calculate, filter),
validate against schema, upsert to database, send summary
```

### **Error Handling**
```
Include: on API failure → retry 3 times → log error → alert admin
```

### **Scheduled Workflows**
```
Daily reports: every day at 6 AM EST
Hourly sync: every hour on the hour
Custom cron: */15 9-17 * * 1-5 (every 15min, 9-5, weekdays)
```

---

## 🐛 Known Limitations

1. **First generation takes longer** (n8n initialization)
2. **Some nodes need credentials** (manual setup in n8n)
3. **16+ node workflows slower** (~60s vs ~35s)
4. **Local only** (not yet cloud-deployed)

---

## 🎉 You're Ready!

### **Quick Test**:
1. Open http://localhost:8000/workflows
2. Select "💰 Bitcoin Price → Telegram" template
3. Click "Generate Workflow"
4. Watch it build in ~35 seconds
5. Open in n8n and activate!

### **Your Workflows**:
You already have 4 workflows created:
- Bitcoin Price Telegram Notifier
- Ethereum Price Alert
- Complex News Ranking (17 nodes!)
- And more...

**Go activate them and see the magic! 🚀**

---

## 🤝 Support

- **Issues**: GitHub issues
- **Questions**: Check this guide
- **n8n Help**: https://docs.n8n.io
- **xAI Docs**: https://docs.x.ai

---

## 📝 License

See LICENSE file for details.

---

## 🙏 Built With

- **xAI Grok** - Multi-model AI intelligence
- **n8n** - Open-source workflow automation
- **FastAPI** - Modern Python web framework
- **React-like UI** - Beautiful vanilla JavaScript

---

**Version**: 1.0.0 Genius Mode
**Status**: ✅ Production Ready
**Updated**: October 2025

🎊 **Enjoy building amazing automation workflows!** 🚀

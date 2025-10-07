# 🚀 START HERE - Complete Setup

## Your Current Status

✅ **Webapp running**: http://localhost:8000  
❌ **n8n NOT running**: http://localhost:5678 (needs to start)

## Quick Start (2 minutes)

### Step 1: Stop Everything
```bash
cd /Users/dylanckawalec/Desktop/developer/opgrok
bash scripts/stop_n8n_local.sh
```

### Step 2: Make Sure .env is Correct

Open your `.env` file:
```bash
nano .env
```

Should look like:
```bash
XAI_API_KEY=xai-your_actual_key_here
N8N_API_URL=http://localhost:5678/api/v1
N8N_WEBHOOK_URL=http://localhost:5678
N8N_AUTH_USER=admin
N8N_AUTH_PASSWORD='your_password'
```

**Important**: If your password has `#` or special chars, use single quotes!

Save: `Ctrl+X`, `Y`, `Enter`

### Step 3: Start EVERYTHING
```bash
bash scripts/run_n8n_local.sh
```

This will:
1. ✅ Install/start n8n (port 5678)
2. ✅ Start webapp (port 8000)
3. ✅ Connect them together

Wait for these messages:
```
✅ n8n is ready!
✅ Services started successfully!
```

### Step 4: Verify Everything Works

**Check Status Page:**
```bash
curl http://localhost:8000/api/n8n/health
```

Should show: `"healthy":true`

**Open in Browser:**
- Workflow Builder: http://localhost:8000/workflows
- n8n Dashboard: http://localhost:5678

---

## 🎯 Now Create Your First Workflow

### Option A: Dedicated Workflow Builder (Easiest)

1. **Go to**: http://localhost:8000/workflows

2. **Type this**:
   ```
   Send me an email every day at 9 AM with the weather forecast
   ```

3. **Click "Generate Workflow"**

4. **Wait 5-10 seconds** - you'll see:
   - "Grok is analyzing..."
   - "Workflow Created!"
   - Preview of the workflow nodes

5. **Click "View"** or go to: http://localhost:5678

6. **Your workflow is there!** Fully configured and ready to activate

### Option B: Use the Chat Interface

1. **Go to**: http://localhost:8000

2. **Click** the "🔧 n8n Workflow Builder" button (or use chat directly)

3. **Type naturally**:
   ```
   I need a workflow that monitors my website and alerts me if it goes down
   ```

4. **Grok automatically detects** this is a workflow request

5. **It builds it for you** and provides a link to view in n8n

---

## 📺 Visual Example

### What You'll See in Workflow Builder:

```
┌─────────────────────────────────────────┐
│ 🤖 n8n Workflow Builder                 │
│                                          │
│ ✨ Describe Your Workflow               │
│ ┌─────────────────────────────────────┐ │
│ │ Create a daily weather email...    │ │
│ └─────────────────────────────────────┘ │
│ [Generate Workflow]                     │
│                                          │
│ 💡 Try these:                           │
│ • Monitor email for invoices            │
│ • Daily morning briefing                │
└─────────────────────────────────────────┘

[Click "Generate Workflow"]
         ↓
┌─────────────────────────────────────────┐
│ 🔄 Generating Workflow...               │
│ Grok is analyzing and building...       │
└─────────────────────────────────────────┘

         ↓ (5-10 seconds)
         
┌─────────────────────────────────────────┐
│ ✅ Workflow Created!                    │
│                                          │
│ Daily Weather Email (ID: abc123)        │
│                                          │
│ View: http://localhost:5678/workflow/...│
│                                          │
│ Workflow Nodes:                         │
│ ┌─────────────────┐                     │
│ │ Schedule: 9 AM  │                     │
│ └────────┬────────┘                     │
│          ↓                               │
│ ┌─────────────────┐                     │
│ │ Weather API     │                     │
│ └────────┬────────┘                     │
│          ↓                               │
│ ┌─────────────────┐                     │
│ │ Send Email      │                     │
│ └─────────────────┘                     │
│                                          │
│ [Activate] [View in n8n]                │
└─────────────────────────────────────────┘
```

---

## 🎓 Understanding the Integration

### How It All Works:

```
You type in chat:
"Send me daily weather emails at 9 AM"
         ↓
Grok Chat (localhost:8000)
Receives your request
         ↓
Grok AI (xAI API)
Analyzes and designs workflow
         ↓
Workflow Builder Service
Creates n8n workflow JSON
         ↓
n8n API (localhost:5678/api/v1)
Stores the workflow
         ↓
n8n Dashboard (localhost:5678)
Shows your new workflow
         ↓
You click "Activate"
         ↓
Workflow runs automatically!
```

### What Gets Created:

1. **Complete workflow** with all nodes
2. **All connections** between nodes configured
3. **All parameters** set automatically
4. **Ready to activate** - just add credentials if needed

---

## 🔗 Direct Links to n8n

After generating a workflow, you can:

### View Workflow List
```
http://localhost:5678/home/workflows
```

### View Specific Workflow
```
http://localhost:5678/workflow/<workflow_id>
```

### Create New Workflow (Manual)
```
http://localhost:5678/workflow/new
```

But with AI, you don't need to create manually! Just describe it!

---

## 💡 Example Prompts to Try

### Simple Workflows:
```
"Check my website every 5 minutes and alert me if it's down"

"Send me a daily summary of Hacker News top stories"

"Monitor a folder for new CSV files and process them"
```

### Complex Workflows:
```
"When I receive an email with 'invoice' in the subject, 
extract the PDF, parse the data, save to Google Sheets, 
and notify me on Slack"

"Fetch data from my API every hour, transform it, 
save to database, and create a summary report"

"Monitor Twitter for mentions of my brand, analyze sentiment, 
and escalate negative tweets to my support team"
```

### Business Workflows:
```
"Automate new customer onboarding: create user account, 
send welcome email, add to CRM, schedule kickoff call"

"Daily standup reminder: fetch team's yesterday tasks from Jira, 
format as message, post to Slack at 9 AM"

"Invoice processing: extract data from email attachments, 
match with PO numbers, update accounting system"
```

---

## 🐛 Troubleshooting

### n8n Health Check Fails

```bash
# Check if n8n is actually running
curl http://localhost:5678/healthz

# If it fails, restart:
bash scripts/stop_n8n_local.sh
bash scripts/run_n8n_local.sh

# Watch the logs
tail -f .n8n/n8n.log
```

### Can't Access n8n Dashboard

```bash
# Make sure it's running
lsof -i:5678

# Try opening directly
open http://localhost:5678

# Check credentials in .env
cat .env | grep N8N_AUTH
```

### Workflow Generation Fails

```bash
# Check webapp logs
tail -f .n8n/webapp.log

# Verify XAI_API_KEY is set
echo $XAI_API_KEY

# Test the endpoint directly
curl http://localhost:8000/api/n8n/health
```

---

## ✅ Success Checklist

Before creating workflows, verify:

- [ ] n8n running: `curl http://localhost:5678/healthz` returns OK
- [ ] Webapp running: `curl http://localhost:8000` returns HTML
- [ ] Integration working: `curl http://localhost:8000/api/n8n/health` shows `"healthy":true`
- [ ] Can access workflow builder: http://localhost:8000/workflows
- [ ] Can access n8n dashboard: http://localhost:5678
- [ ] Can login to n8n with credentials from `.env`

---

## 🚀 You're Ready!

Once everything is running:

1. Open http://localhost:8000/workflows
2. Type what you want to automate
3. Click "Generate Workflow"
4. Watch the magic happen!
5. Activate in n8n dashboard

**That's it!** The AI handles all the complexity of building the workflow.

---

## 📚 Next Steps

- Try the example prompts above
- Read **HOW_TO_USE.md** for detailed tutorial
- Check **WORKFLOW_EXAMPLES.md** for 30+ examples
- Explore the n8n dashboard to see what's possible

Happy automating! 🎉

# 🚀 How to Use AI Workflow Generation

Your system is running! Here's how to magically create n8n workflows with Grok AI.

## 🎯 You Have Two Options

### Option 1: Dedicated Workflow Builder (Recommended) 🌟

**URL**: http://localhost:8000/workflows

This is a **dedicated interface** just for building workflows.

#### How to Use:

1. **Open the Workflow Builder**
   ```
   http://localhost:8000/workflows
   ```

2. **Describe what you want** in plain English:
   ```
   "Send me a Slack message every Monday at 9 AM with top Hacker News stories"
   
   "Create a webhook that receives form submissions and saves them to Google Sheets"
   
   "Monitor my email for invoices and extract data to Airtable"
   ```

3. **Click "Generate Workflow"**

4. **Watch the magic happen!**
   - Grok analyzes your request (2-5 seconds)
   - Designs the workflow structure
   - Configures all nodes automatically
   - Deploys to your n8n instance
   - Shows you a preview

5. **View in n8n**
   - Click the n8n dashboard link
   - Or go directly to: http://localhost:5678
   - Your workflow is there, fully configured!

6. **Activate and Run**
   - Click "Activate" in the workflow builder UI
   - Or open the workflow in n8n and activate there

---

### Option 2: Smart Chat Interface 🤖

**URL**: http://localhost:8000/

The main chat interface **automatically detects** when you're asking to create a workflow!

#### How to Use:

1. **Open the Chat**
   ```
   http://localhost:8000
   ```

2. **Just chat naturally** about automation:
   ```
   User: "I need to automate my daily standup reminders"
   
   User: "Can you build me a workflow that monitors Twitter for my brand mentions?"
   
   User: "Create an automation that backs up my database every night"
   ```

3. **Grok automatically detects** this is a workflow request

4. **It builds the workflow for you** and responds with:
   - Workflow name and ID
   - Link to view in n8n
   - Instructions to activate

5. **Activate through chat** or n8n dashboard

---

## 🎨 Visual Guide

### Workflow Builder Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🤖 n8n Workflow Builder                                    │
│  AI-Powered Automation with Grok                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ✨ Describe Your Workflow                            │  │
│  │ Tell me what automation you need...                   │  │
│  │                                                        │  │
│  │ ┌────────────────────────────────────────────────┐   │  │
│  │ │ Type here: "Send daily weather report..."     │   │  │
│  │ └────────────────────────────────────────────────┘   │  │
│  │                                                        │  │
│  │ [Generate Workflow]                                   │  │
│  │                                                        │  │
│  │ 💡 Try these examples:                                │  │
│  │ • Monitor email for invoices                          │  │
│  │ • Daily morning briefing with weather                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  📋 Your Workflows                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│  │ Daily    │ │ Invoice  │ │ Backup   │                   │
│  │ Report   │ │ Monitor  │ │ System   │                   │
│  │ [View]   │ │ [View]   │ │ [View]   │                   │
│  └──────────┘ └──────────┘ └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Example Workflow Generation

### Example 1: Simple Daily Email

**Your Input:**
```
Send me an email every day at 8 AM with a motivational quote
```

**What Happens:**
1. ⚡ Grok analyzes: "daily trigger + API call + email"
2. 🏗️ Creates workflow with:
   - Schedule Trigger (cron: 0 8 * * *)
   - HTTP Request (quote API)
   - Send Email Node
3. ⚙️ Configures all parameters automatically
4. 🚀 Deploys to http://localhost:5678

**Result:**
```
✅ I've created your n8n workflow!

Workflow Name: Daily Motivational Email
Workflow ID: abc123xyz

The workflow has been deployed to your n8n instance. You can:
- View it at: http://localhost:5678/workflow/abc123xyz
- Activate it using the activate button
- Test it manually

Would you like me to activate it now?
```

### Example 2: Complex Multi-Step Workflow

**Your Input:**
```
When I receive an email with "invoice" in the subject:
1. Extract the PDF attachment
2. Parse the invoice data
3. Save to Google Sheets
4. Notify me on Slack
5. Mark email as processed
```

**What Happens:**
1. ⚡ Grok analyzes the multi-step process
2. 🏗️ Creates workflow with:
   - Gmail Trigger (on new email)
   - IF Node (check subject)
   - Extract PDF Node
   - Function Node (parse data)
   - Google Sheets Node
   - Slack Node
   - Gmail Node (mark as read)
3. ⚙️ Connects all nodes with proper data flow
4. 🚀 Deploys complete workflow

**Result:** Fully functional 7-node workflow, ready to activate!

---

## 🔗 Integration Flow

Here's how everything connects:

```
┌──────────────────┐
│  You (User)      │
│  Type request    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Grok Chat (Port 8000)           │
│  • Receives your description     │
│  • Sends to Grok API             │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Grok AI (xAI API)               │
│  • Analyzes request              │
│  • Designs workflow structure    │
│  • Generates node configurations │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  Workflow Builder Service        │
│  • Assembles complete workflow   │
│  • Creates n8n JSON              │
│  • Validates structure           │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  n8n API (Port 5678)             │
│  • Receives workflow JSON        │
│  • Stores in database            │
│  • Makes available in dashboard  │
└────────┬─────────────────────────┘
         │
         ▼
┌──────────────────────────────────┐
│  n8n Dashboard                   │
│  • View: localhost:5678          │
│  • Your workflow is there!       │
│  • Click activate and run        │
└──────────────────────────────────┘
```

---

## 🎓 Tutorial: Your First Workflow

Let's create your first AI-generated workflow together!

### Step 1: Open Workflow Builder
```bash
open http://localhost:8000/workflows
```

### Step 2: Enter This Prompt
```
Create a workflow that checks if my website is up every 5 minutes 
and sends me a Slack message if it's down
```

### Step 3: Click "Generate Workflow"

Watch as:
- ✨ Grok analyzes the requirement
- 🔄 "Generating Workflow..." appears
- ⏱️ Takes 5-10 seconds
- ✅ "Workflow Created!" message shows

### Step 4: Review the Generated Workflow

You'll see:
```
✅ Workflow Created!

Daily Motivational Email (ID: abc123)

Workflow Nodes:
┌──────────────────────────────┐
│ Schedule Trigger             │
│ Type: n8n-nodes-base.schedule│
│ Every 5 minutes              │
└──────────────────────────────┘
         ↓
┌──────────────────────────────┐
│ HTTP Request                 │
│ Type: n8n-nodes-base.http    │
│ Check website status         │
└──────────────────────────────┘
         ↓
┌──────────────────────────────┐
│ IF Condition                 │
│ Type: n8n-nodes-base.if      │
│ Is status != 200?            │
└──────────────────────────────┘
         ↓
┌──────────────────────────────┐
│ Slack                        │
│ Type: n8n-nodes-base.slack   │
│ Send alert message           │
└──────────────────────────────┘
```

### Step 5: View in n8n Dashboard

Click the link or go to:
```
http://localhost:5678/workflow/abc123
```

### Step 6: Configure Credentials (if needed)

Some nodes need credentials (like Slack):
1. Click the node in n8n
2. Click "Create New Credential"
3. Add your Slack webhook URL
4. Save

### Step 7: Activate!

Click the toggle switch in n8n to activate the workflow.

**Done!** Your workflow is now running every 5 minutes! 🎉

---

## 💡 Pro Tips

### 1. Be Specific
❌ **Vague**: "Do something with emails"
✅ **Specific**: "When I receive an email from billing@company.com, extract the invoice amount and log it to a spreadsheet"

### 2. Include Timing
❌ **Missing**: "Send me a report"
✅ **With timing**: "Send me a report every Monday at 9 AM"

### 3. Mention Integrations
❌ **Generic**: "Send me a notification"
✅ **Specific**: "Send me a Slack notification in the #alerts channel"

### 4. Describe Data Flow
❌ **Unclear**: "Process customer data"
✅ **Clear**: "Fetch customer data from Stripe, calculate total spent, update in Salesforce"

### 5. Add Conditions
❌ **Simple**: "Monitor tickets"
✅ **With logic**: "Monitor support tickets and escalate to manager if priority is 'urgent' and unassigned for over 1 hour"

---

## 🐛 Troubleshooting

### "n8n service is not accessible"

**Check n8n is running:**
```bash
curl http://localhost:5678/healthz
```

If it fails:
```bash
# Restart n8n
bash scripts/stop_n8n_local.sh
bash scripts/run_n8n_local.sh
```

### "Workflow generated but not appearing"

**Refresh n8n dashboard:**
```bash
# Go to n8n
open http://localhost:5678

# Click refresh or press Cmd+R
```

**Check the API:**
```bash
curl -u admin:yourpassword http://localhost:5678/api/v1/workflows
```

### "Generation takes too long"

- Complex workflows take 10-15 seconds
- Check your internet connection (Grok API needs access)
- Check logs: `tail -f .n8n/webapp.log`

### "Workflow has errors in n8n"

Some nodes need credentials:
1. Open workflow in n8n
2. Click red nodes (they show errors)
3. Add required credentials
4. Save and activate

---

## 📚 More Examples

See **WORKFLOW_EXAMPLES.md** for 30+ real-world examples:
- Email automation
- Data processing
- Social media posting
- Monitoring & alerts
- Business workflows
- And much more!

---

## 🎯 Quick Links

- **Workflow Builder**: http://localhost:8000/workflows
- **Chat Interface**: http://localhost:8000
- **n8n Dashboard**: http://localhost:5678
- **API Docs**: http://localhost:8000/docs (FastAPI auto-docs)

---

## 🚀 You're Ready!

Go build something amazing! Start with a simple workflow and work your way up to complex automations.

Remember: Just describe what you want in plain English, and Grok will build it for you! 🎉

Questions? Check out:
- N8N_QUICKSTART.md - Getting started guide
- WORKFLOW_EXAMPLES.md - 30+ example workflows
- ARCHITECTURE.md - How everything works
- N8N_AUTH_GUIDE.md - Authentication help

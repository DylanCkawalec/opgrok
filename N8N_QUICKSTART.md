# n8n Workflow Builder - Quick Start Guide

🤖 **AI-Powered Workflow Automation with Grok**

This integration combines xAI's Grok API with n8n (an open-source workflow automation tool) to create a revolutionary chat-driven workflow builder. Simply describe your automation needs in natural language, and Grok will automatically generate, configure, and deploy complete n8n workflows.

## 🚀 Features

- **Natural Language Workflow Generation**: Describe your automation in plain English
- **Intelligent Workflow Design**: Grok analyzes requirements and creates optimal node structures
- **Automatic Configuration**: All node parameters, connections, and I/O are configured automatically
- **Multi-Step Processing**: Complex workflows broken down intelligently
- **Interactive Chat Interface**: Conversational workflow building experience
- **Full n8n Integration**: Direct API integration with local n8n instance

## 📋 Prerequisites

- Docker and Docker Compose installed
- xAI API Key (get one at https://console.x.ai/)
- Python 3.8+ (for local development)
- Rust toolchain (for Rust CLI component)

## 🛠️ Installation

### 1. Clone and Setup

```bash
cd /path/to/opgrok
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and add your xAI API key:

```bash
XAI_API_KEY=your_actual_api_key_here
N8N_AUTH_USER=admin
N8N_AUTH_PASSWORD=your_secure_password
```

### 3. Start Services with Docker Compose

```bash
# Start all services (n8n + webapp)
docker-compose up -d

# Or start just n8n if running webapp locally
docker-compose up -d n8n postgres
```

This will start:
- **n8n** on `http://localhost:5678`
- **Webapp** on `http://localhost:8000` (if using full docker-compose)
- **PostgreSQL** database for n8n

### 4. Verify n8n is Running

```bash
curl http://localhost:5678/healthz
```

## 🎯 Usage

### Option A: Web Interface

1. **Access the Workflow Builder**
   - Open http://localhost:8000
   - Click "🔧 n8n Workflow Builder" button

2. **Generate Your First Workflow**
   - Enter a natural language description
   - Example: "Create a workflow that monitors my Gmail for invoices and saves them to Google Sheets"
   - Click "Generate Workflow"

3. **Review and Deploy**
   - Grok will analyze, design, and deploy the workflow
   - View the generated workflow in n8n dashboard
   - Activate and test your workflow

### Option B: Direct API

```bash
# Generate a workflow
curl -X POST http://localhost:8000/api/n8n/workflows/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Send me a Slack notification every day at 9 AM with weather data",
    "auto_activate": false
  }'

# List all workflows
curl http://localhost:8000/api/n8n/workflows

# Activate a workflow
curl -X POST http://localhost:8000/api/n8n/workflows/{workflow_id}/activate

# Execute a workflow
curl -X POST http://localhost:8000/api/n8n/workflows/{workflow_id}/execute
```

### Option C: Chat-Driven Workflow Building

Use the main chat interface with workflow-aware intelligence:

```bash
# In the main chat interface, just describe your workflow:
User: "I need to automate my invoicing process. When I receive an email 
       with 'invoice' in the subject, extract the data and add it to 
       my Airtable database, then notify me on Slack."

# Grok will automatically detect this is a workflow request and build it!
```

## 📝 Example Workflow Prompts

Here are some example prompts you can try:

### Basic Automation
- "Send me a daily email digest at 8 AM"
- "Monitor a specific hashtag on Twitter and save to database"
- "Backup my Google Drive files to Dropbox weekly"

### Business Workflows
- "When a new lead fills out our contact form, create a Salesforce lead and notify sales team on Slack"
- "Extract invoice data from Gmail attachments and update QuickBooks"
- "Monitor customer support tickets and escalate urgent ones to manager"

### Data Processing
- "Fetch data from our API every hour, transform it, and send to Google Sheets"
- "Process CSV files from FTP server and insert into PostgreSQL database"
- "Aggregate metrics from multiple APIs and generate weekly reports"

### Integrations
- "Sync new Stripe customers to Mailchimp mailing list"
- "When GitHub issue is created, create Jira ticket and link them"
- "Post new blog articles from WordPress to all social media platforms"

## 🔧 How It Works

### 1. Request Analysis Phase
When you submit a workflow prompt:
- Grok analyzes the natural language description
- Identifies key automation requirements
- Determines necessary integrations and triggers

### 2. Workflow Design Phase
Grok intelligently designs the workflow:
- Selects appropriate n8n nodes (webhooks, HTTP requests, transforms, etc.)
- Plans data flow and connections
- Determines conditional logic requirements

### 3. Configuration Phase
Each node is automatically configured:
- API endpoints and authentication
- Data transformations and mappings
- Error handling and retry logic
- Input/output specifications

### 4. Deployment Phase
The complete workflow is deployed:
- JSON structure generated for n8n
- Workflow created via n8n API
- Connections and parameters validated
- Ready for activation

## 🏗️ Architecture

```
┌─────────────────┐
│   User Prompt   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  Grok API (Analysis)        │
│  - Parse requirements       │
│  - Identify nodes needed    │
│  - Design workflow structure│
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Grok API (Configuration)   │
│  - Generate node parameters │
│  - Configure connections    │
│  - Set up authentication    │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  n8n Workflow Builder       │
│  - Create workflow object   │
│  - Validate structure       │
│  - Deploy to n8n            │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  n8n Instance               │
│  - Store workflow           │
│  - Execute on triggers      │
│  - Manage credentials       │
└─────────────────────────────┘
```

## 🔐 Security Considerations

- **API Keys**: Store XAI_API_KEY securely, never commit to git
- **n8n Authentication**: Change default password in production
- **Network**: Consider using reverse proxy (nginx) in production
- **Credentials**: Use n8n's credential system for third-party integrations
- **Firewall**: Restrict access to n8n dashboard in production

## 🐛 Troubleshooting

### n8n Not Accessible
```bash
# Check if n8n container is running
docker-compose ps

# View n8n logs
docker-compose logs -f n8n

# Restart n8n
docker-compose restart n8n
```

### Workflow Generation Fails
- Ensure XAI_API_KEY is set correctly
- Check n8n API is accessible: `curl http://localhost:5678/api/v1/workflows`
- Verify authentication credentials in `.env`

### Connection Refused
- Make sure Docker containers are on same network
- Check firewall settings
- Verify ports 5678 and 8000 are not in use

## 📚 Additional Resources

- **n8n Documentation**: https://docs.n8n.io/
- **xAI API Docs**: https://docs.x.ai/
- **Community Forum**: https://community.n8n.io/

## 🎓 Advanced Usage

### Custom Node Configuration

You can provide detailed requirements in your prompt:

```
"Create a webhook endpoint that:
1. Accepts POST requests with JSON body
2. Validates that 'email' field exists
3. Sends data to https://api.example.com/users
4. On success, sends confirmation to Slack channel #notifications
5. On failure, logs to error.log file"
```

### Multi-Step Workflows

Grok can handle complex multi-step automations:

```
"Build a customer onboarding workflow:
- Trigger: New Stripe subscription
- Step 1: Create user account in database
- Step 2: Send welcome email via SendGrid
- Step 3: Add to Mailchimp list
- Step 4: Create task in Asana for account setup
- Step 5: Notify sales team on Slack"
```

### Iterative Refinement

After generating a workflow, you can refine it through chat:

```
User: "Add error handling to retry failed API calls 3 times"
User: "Change the schedule from daily to every 4 hours"
User: "Add a filter to only process items with amount > $100"
```

## 🚀 Next Steps

1. Try the example prompts above
2. Explore the n8n dashboard to see generated workflows
3. Customize workflows in n8n's visual editor
4. Add your own service credentials in n8n
5. Build more complex automations!

## 💡 Tips for Best Results

- **Be specific**: Include details about triggers, actions, and data
- **Mention integrations**: Specify which services you want to connect
- **Include conditions**: Describe any if/then logic needed
- **Define frequency**: Specify schedules for recurring tasks
- **Mention data formats**: JSON, CSV, XML, etc.

Happy automating! 🎉

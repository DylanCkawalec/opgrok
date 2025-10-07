# n8n Authentication Guide

## 🔑 Understanding Local n8n Authentication

### Important: This is NOT n8n.cloud

Your local n8n installation is **completely separate** from n8n.cloud:

- ❌ **You DON'T need** an n8n.cloud account
- ❌ **You DON'T use** your n8n.cloud credentials
- ✅ **You CREATE** your own local credentials in `.env`

Think of it like setting up your own private n8n server on your computer.

## 📝 Setting Up Authentication

### Step 1: Edit Your `.env` File

```bash
cd /Users/dylanckawalec/Desktop/developer/opgrok
nano .env  # or use your favorite editor
```

### Step 2: Configure Your Credentials

Add these lines (or modify existing ones):

```bash
# Your xAI API Key (required)
XAI_API_KEY=xai-your_actual_key_here

# Your LOCAL n8n credentials (you choose these!)
N8N_AUTH_USER=admin
N8N_AUTH_PASSWORD='mySecurePassword123'

# API URLs (keep as-is)
N8N_API_URL=http://localhost:5678/api/v1
N8N_WEBHOOK_URL=http://localhost:5678
```

### Step 3: Handle Special Characters

If your password contains special characters like `#`, `$`, `!`, wrap it in **single quotes**:

```bash
# ✅ CORRECT - Single quotes protect special characters
N8N_AUTH_PASSWORD='my#password$123!'

# ❌ WRONG - # will be treated as a comment
N8N_AUTH_PASSWORD=my#password$123!

# ❌ WRONG - $ will try to expand variables
N8N_AUTH_PASSWORD="my#password$123!"
```

### Step 4: Save and Exit

- If using nano: Press `Ctrl+X`, then `Y`, then `Enter`
- If using vim: Press `Esc`, type `:wq`, press `Enter`

## 🚀 Starting n8n

After configuring `.env`, start n8n:

```bash
bash scripts/run_n8n_local.sh
```

The script will:
1. Read your `.env` file
2. Start n8n with YOUR chosen credentials
3. Create a local n8n instance at http://localhost:5678

## 🔐 Logging In

### First Access

1. Open http://localhost:5678 in your browser
2. You'll see the n8n login screen
3. Enter:
   - **Username**: Whatever you set for `N8N_AUTH_USER` (default: `admin`)
   - **Password**: Whatever you set for `N8N_AUTH_PASSWORD`

### For Workflow Builder

The Grok chat application automatically uses these credentials from your `.env` file to communicate with n8n's API. You don't need to log in separately for the workflow builder.

## 🐛 Troubleshooting

### "Authentication Failed" when accessing n8n dashboard

**Problem**: Your browser credentials don't match `.env` file

**Solution**:
```bash
# Check what credentials are set
cat .env | grep N8N_AUTH

# If wrong, edit and fix:
nano .env

# Restart n8n:
bash scripts/stop_n8n_local.sh
bash scripts/run_n8n_local.sh
```

### "n8n service is not accessible" from workflow builder

**Problem**: Webapp can't connect to n8n API

**Solution**:
```bash
# 1. Check if n8n is running
curl http://localhost:5678/healthz

# 2. Check if credentials match
cat .env | grep N8N_AUTH

# 3. Test API authentication
curl -u admin:yourpassword http://localhost:5678/api/v1/workflows

# 4. If still failing, restart everything:
bash scripts/stop_n8n_local.sh
bash scripts/run_n8n_local.sh
```

### Password with '#' character gets cut off

**Problem**: `.env` parser treats `#` as a comment

**Solution**: Wrap password in single quotes
```bash
# Before (wrong):
N8N_AUTH_PASSWORD=mypassword#123

# After (correct):
N8N_AUTH_PASSWORD='mypassword#123'
```

### Want to change password after setup

```bash
# 1. Stop services
bash scripts/stop_n8n_local.sh

# 2. Edit .env
nano .env
# Change N8N_AUTH_PASSWORD='new_password_here'

# 3. Clear n8n data (optional, to force reset)
rm -rf .n8n/database.sqlite

# 4. Restart
bash scripts/run_n8n_local.sh
```

## 🔄 Resetting Everything

If you want to start fresh:

```bash
# Stop services
bash scripts/stop_n8n_local.sh

# Remove all n8n data
rm -rf .n8n/

# Edit .env with new credentials
nano .env

# Start fresh
bash scripts/run_n8n_local.sh
```

## 📊 Testing Your Setup

After starting n8n, test everything:

### 1. Test n8n Dashboard Access

```bash
# Open in browser
open http://localhost:5678

# You should see login page
# Enter your N8N_AUTH_USER and N8N_AUTH_PASSWORD
```

### 2. Test API Access

```bash
# Replace with your credentials from .env
curl -u admin:yourpassword http://localhost:5678/api/v1/workflows

# Should return: {"data":[]}  (empty workflow list initially)
```

### 3. Test Workflow Builder

```bash
# Open workflow builder
open http://localhost:8000/workflows

# Should show green "Connected" status for n8n
```

## 💡 Quick Reference

### Default Credentials (if you kept .env.example defaults)
- **Username**: `admin`
- **Password**: `changeme`
- **URL**: http://localhost:5678

### Where Credentials Are Used
1. **n8n Dashboard Login** (manual, in browser)
2. **Workflow Builder API** (automatic, from .env)
3. **Direct API Access** (if you use curl/scripts)

### Security Notes
- These credentials only protect your **local** n8n instance
- Only accessible from your computer (localhost)
- If you want external access, add reverse proxy with SSL
- Consider using a strong password even for local development

## ❓ Common Questions

**Q: Do I need an n8n.cloud account?**  
A: No! This is a local installation. Your n8n.cloud account (if you have one) is completely separate.

**Q: Can I use my n8n.cloud credentials?**  
A: You can, but it's not required. This is YOUR local instance with YOUR chosen credentials.

**Q: Where is my data stored?**  
A: Everything is stored in the `.n8n/` directory in your project folder.

**Q: Can other people access my workflows?**  
A: No, only accessible on your computer at http://localhost:5678

**Q: How do I make it accessible from other devices?**  
A: See DEPLOYMENT.md for production deployment with proper security.

## 🚀 Ready to Build Workflows!

Once authenticated, you can:
1. Create workflows manually in n8n dashboard
2. Generate workflows with AI at http://localhost:8000/workflows
3. Use the chat interface to build workflows conversationally

Happy automating! 🎉

# Quick Fix: Password with Special Characters

## Your Issue

Your `.env` file password ends with `#`, which gets treated as a comment and blanked out.

## The Fix (30 seconds)

### Step 1: Open your .env file

```bash
cd /Users/dylanckawalec/Desktop/developer/opgrok
nano .env
```

### Step 2: Wrap your password in single quotes

Change this:
```bash
N8N_AUTH_PASSWORD=mypassword#123
```

To this:
```bash
N8N_AUTH_PASSWORD='mypassword#123'
```

### Step 3: Save (Ctrl+X, then Y, then Enter)

### Step 4: Your complete .env should look like:

```bash
# xAI API Key
XAI_API_KEY=xai-your_actual_key_here

# n8n Local Credentials (YOU choose these, not from n8n.cloud!)
N8N_API_URL=http://localhost:5678/api/v1
N8N_WEBHOOK_URL=http://localhost:5678
N8N_AUTH_USER=admin
N8N_AUTH_PASSWORD='your#password#here'
```

### Step 5: Start the app

```bash
bash scripts/run_n8n_local.sh
```

### Step 6: Login to n8n

Open http://localhost:5678

- Username: `admin` (or whatever you set)
- Password: Your full password WITH the # characters

## Important Notes

✅ **This is a LOCAL n8n instance** - not connected to n8n.cloud  
✅ **You choose the username/password** - they're just for your local setup  
✅ **No n8n account needed** - this runs entirely on your computer  
✅ **Single quotes protect special characters** - use them for passwords with: # $ ! & * etc.

## Test It Works

```bash
# This should print your password correctly (with the #)
source .env && echo $N8N_AUTH_PASSWORD

# This should return authentication info (use your actual password)
curl -u admin:'your#password' http://localhost:5678/api/v1/workflows
```

Done! 🎉

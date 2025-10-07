# Installation Options

You have three ways to run the Grok + n8n Workflow Automation Platform, depending on your environment and preferences.

## 🎯 Quick Comparison

| Option | Best For | Requirements | Setup Time |
|--------|----------|--------------|------------|
| **Local (Recommended)** | Development, no Docker issues | Node.js 18+, Python 3.8+ | 2 min |
| **OrbStack** | Mac users with OrbStack | OrbStack installed | 3 min |
| **Docker** | Traditional Docker setup | Docker Desktop | 3 min |

---

## Option 1: Local Installation (No Docker) ⭐ RECOMMENDED

**Best for**: Development, avoiding Docker keychain issues, fastest startup

### Prerequisites
- Node.js 18+ ([download](https://nodejs.org))
- Python 3.8+
- Rust 1.70+ ([install](https://rustup.rs))
- xAI API Key ([get one](https://console.x.ai))

### Installation

```bash
# 1. Clone and setup
git clone <repo>
cd opgrok
cp .env.example .env
# Edit .env and add your XAI_API_KEY

# 2. Start everything
bash scripts/run_n8n_local.sh
```

That's it! The script will:
- ✅ Install n8n locally via npx (first run only)
- ✅ Build Rust CLI
- ✅ Setup Python environment
- ✅ Start n8n on port 5678
- ✅ Start webapp on port 8000
- ✅ Run everything in background

### Usage

```bash
# Start services
bash scripts/run_n8n_local.sh

# Stop services
bash scripts/stop_n8n_local.sh

# View logs
tail -f .n8n/n8n.log
tail -f .n8n/webapp.log
```

### Data Location
- n8n data: `.n8n/` directory
- Logs: `.n8n/n8n.log` and `.n8n/webapp.log`
- PIDs: `.n8n/n8n.pid` and `.n8n/webapp.pid`

### Pros
✅ No Docker required
✅ No keychain password issues
✅ Fast startup (once installed)
✅ Easy debugging
✅ Direct file access

### Cons
❌ Requires Node.js installation
❌ Services run in background (not containerized)

---

## Option 2: OrbStack (Mac Users)

**Best for**: Mac users using OrbStack instead of Docker Desktop

### Prerequisites
- OrbStack ([download](https://orbstack.dev))
- xAI API Key

### Installation

```bash
# 1. Start OrbStack (if not running)
open -a OrbStack

# 2. Clone and setup
git clone <repo>
cd opgrok
cp .env.example .env
# Edit .env and add your XAI_API_KEY

# 3. Start all services
bash scripts/run_n8n.sh
```

The script automatically detects OrbStack and uses the optimized `docker-compose.orbstack.yml` configuration.

### OrbStack-Specific Features
- Automatic resource management
- Faster container startup
- Better Mac integration
- No authentication issues with n8n image

### Usage

```bash
# Start services
bash scripts/run_n8n.sh

# Stop services
docker compose -f docker-compose.orbstack.yml down

# View logs
docker compose -f docker-compose.orbstack.yml logs -f

# Check status
docker compose -f docker-compose.orbstack.yml ps
```

### Pros
✅ Containerized (clean environment)
✅ OrbStack optimizations
✅ Easy backup/restore
✅ PostgreSQL included

### Cons
❌ Requires OrbStack installation
❌ Uses more resources than local

---

## Option 3: Docker Desktop

**Best for**: Traditional Docker users, production deployment

### Prerequisites
- Docker Desktop ([download](https://docker.com))
- Docker Compose
- xAI API Key

### Installation

```bash
# 1. Start Docker Desktop

# 2. Clone and setup
git clone <repo>
cd opgrok
cp .env.example .env
# Edit .env and add your XAI_API_KEY

# 3. Fix n8n image authentication (if needed)
docker login

# 4. Start all services
bash scripts/run_n8n.sh
```

### Fixing Docker Authentication Issues

If you encounter keychain password issues with the n8n image:

**Option A: Use alternative image source**
```bash
# Edit docker-compose.yml
# Change: image: n8nio/n8n:latest
# To:     image: docker.n8n.io/n8nio/n8n
```

**Option B: Use local installation instead**
```bash
# Just use the local installation method (Option 1)
bash scripts/run_n8n_local.sh
```

### Usage

```bash
# Start services
bash scripts/run_n8n.sh

# Stop services
docker-compose down

# View logs
docker-compose logs -f webapp
docker-compose logs -f n8n

# Restart a service
docker-compose restart n8n
```

### Pros
✅ Containerized (isolated)
✅ Easy backup/restore
✅ PostgreSQL included
✅ Production-ready

### Cons
❌ Requires Docker Desktop
❌ May have keychain issues
❌ Higher resource usage

---

## Troubleshooting

### Docker/OrbStack Keychain Issues

**Problem**: "Error saving credentials: error storing credentials"

**Solutions**:
1. **Use local installation** (easiest):
   ```bash
   bash scripts/run_n8n_local.sh
   ```

2. **Use alternative n8n image**:
   ```bash
   # Edit docker-compose.yml, change image to:
   image: docker.n8n.io/n8nio/n8n
   ```

3. **Skip Docker login**:
   ```bash
   # Pull image without authentication
   docker pull --disable-content-trust docker.n8n.io/n8nio/n8n
   ```

### Port Already in Use

```bash
# Find and kill process on port
lsof -ti:5678 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Or use the cleanup in the script
bash scripts/run_n8n_local.sh  # Handles this automatically
```

### n8n Not Starting (Local)

```bash
# Check logs
tail -f .n8n/n8n.log

# Check if port is free
lsof -i:5678

# Manually start n8n to see errors
npx n8n start
```

### n8n Not Starting (Docker)

```bash
# Check container status
docker ps -a

# View logs
docker logs opgrok-n8n

# Restart container
docker restart opgrok-n8n
```

---

## Which Option Should I Choose?

### Choose Local Installation If:
- ✅ You want the simplest setup
- ✅ You're having Docker keychain issues
- ✅ You want fast iteration during development
- ✅ You don't need container isolation

### Choose OrbStack If:
- ✅ You're on Mac
- ✅ You use OrbStack already
- ✅ You want containerization benefits
- ✅ You want PostgreSQL included

### Choose Docker If:
- ✅ You need production-like environment
- ✅ You want full containerization
- ✅ You're deploying to cloud later
- ✅ You have Docker already running

---

## Switching Between Options

You can switch between options at any time:

```bash
# Stop current setup
bash scripts/stop_n8n_local.sh  # For local
docker-compose down              # For Docker/OrbStack

# Start different setup
bash scripts/run_n8n_local.sh   # Local
bash scripts/run_n8n.sh         # Docker/OrbStack (auto-detects)
```

**Note**: Data is stored separately for each option:
- Local: `.n8n/` directory
- Docker/OrbStack: Docker volumes (`n8n_data`, `postgres_data`)

To migrate data between options, see the backup/restore section in DEPLOYMENT.md.

---

## Next Steps

After starting your preferred option:

1. **Access the platform**:
   - Chat: http://localhost:8000
   - Workflow Builder: http://localhost:8000/workflows
   - n8n Dashboard: http://localhost:5678

2. **Try your first workflow**:
   - Go to http://localhost:8000/workflows
   - Type: "Send me a daily email at 9 AM"
   - Click "Generate Workflow"

3. **Read the docs**:
   - [N8N_QUICKSTART.md](N8N_QUICKSTART.md) - Getting started guide
   - [WORKFLOW_EXAMPLES.md](WORKFLOW_EXAMPLES.md) - 30+ examples
   - [ARCHITECTURE.md](ARCHITECTURE.md) - How it works

Happy automating! 🚀

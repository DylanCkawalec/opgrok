# 📁 Repository Structure

Clean, organized structure of the OPGROK project.

## 📂 Root Directory

```
opgrok/
├── README.md                    # Start here - Main overview
├── MASTER_GUIDE.md              # Complete usage guide
├── WORKFLOW_EXAMPLES.md         # 30+ workflow examples
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── docker-compose.orbstack.yml  # OrbStack deployment
│
├── scripts/                     # Startup scripts
│   ├── run_n8n_local.sh        # ⭐ Main startup (no Docker)
│   ├── run_genius_mode.sh      # Advanced features
│   ├── stop_n8n_local.sh       # Stop services
│   ├── run_n8n.sh              # Docker/OrbStack mode
│   └── run.sh                  # Chat-only mode
│
├── webapp/                      # Python web application
│   ├── app/
│   │   ├── main.py             # FastAPI app (981 lines)
│   │   ├── n8n_service.py      # Workflow builder (843 lines)
│   │   ├── genius_enhancements.py  # Advanced features (238 lines)
│   │   ├── templates/
│   │   │   ├── index.html      # Chat interface
│   │   │   └── workflow.html   # Workflow builder UI
│   │   └── static/
│   │       └── styles.css      # Shared styles
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile             # Container build
│
├── grok-chat-app/              # Rust CLI (optional)
│   ├── src/                    # Rust source code
│   ├── Cargo.toml             # Rust dependencies
│   └── target/release/        # Compiled binary
│
└── docs/                       # Documentation archive
    ├── README.md              # Docs index
    └── CONSOLIDATED_DOCS.md   # Technical archive
```

## 🎯 Key Files

### **User-Facing**
- `README.md` - Start here for overview
- `MASTER_GUIDE.md` - Complete how-to guide
- `WORKFLOW_EXAMPLES.md` - Real-world examples

### **Development**
- `webapp/app/main.py` - API endpoints
- `webapp/app/n8n_service.py` - AI workflow generation
- `webapp/app/templates/workflow.html` - Workflow builder UI

### **Configuration**
- `.env` - Your API keys (create from .env.example)
- `.gitignore` - Git exclusions (updated)

### **Scripts**
- `scripts/run_n8n_local.sh` - ⭐ Use this to start

## 📦 What's Excluded (.gitignore)

- `.env` - Your secrets
- `.n8n/` - n8n data directory
- `.venv/` - Python virtual environment
- `target/` - Rust build artifacts
- `__pycache__/` - Python cache
- `*.log` - Log files
- `node_modules/` - Node.js packages

## 🎓 Documentation Organization

### Removed (13 files consolidated):
- ARCHITECTURE.md → Now in MASTER_GUIDE.md
- DEPLOYMENT.md → Now in MASTER_GUIDE.md
- GENIUS_FEATURES.md → Now in README.md  
- GENIUS_MODE_GUIDE.md → Now in MASTER_GUIDE.md
- HOW_TO_USE.md → Now in MASTER_GUIDE.md
- INSTALLATION_OPTIONS.md → Now in MASTER_GUIDE.md
- N8N_AUTH_GUIDE.md → Now in docs/CONSOLIDATED_DOCS.md
- N8N_QUICKSTART.md → Now in MASTER_GUIDE.md
- PROJECT_SUMMARY.md → Now in README.md
- QUICK_FIX.md → Now in docs/CONSOLIDATED_DOCS.md
- START_HERE.md → Now in README.md
- FINAL_SUMMARY.md → Now in MASTER_GUIDE.md
- learn.md → Removed (outdated)

### Kept (3 essential files):
- ✅ README.md - Quick overview and setup
- ✅ MASTER_GUIDE.md - Complete guide
- ✅ WORKFLOW_EXAMPLES.md - Practical examples

### Archived:
- 📦 docs/CONSOLIDATED_DOCS.md - Technical reference

---

**Total reduction**: 145 KB → 33 KB (77% smaller!)

**Status**: Clean, professional, maintainable ✅

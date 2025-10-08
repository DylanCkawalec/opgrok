# 📚 Documentation Archive


## 🔐 Authentication Notes

### Local n8n Setup
- **Important**: Local n8n is separate from n8n.cloud
- Username/password are YOUR choice (set in `.env`)
- Default: admin / changeme (change this!)

### If Password Contains Special Characters
Wrap in single quotes in `.env`:
```bash
N8N_AUTH_PASSWORD='my#password123!'
```

---

## 🐳 Docker/OrbStack Notes

### OrbStack Users
- Auto-detected by `run_n8n.sh`
- Uses `docker-compose.orbstack.yml`
- Optimized for Mac performance

### Docker Keychain Issues
**Solution**: Use local installation instead
```bash
bash scripts/run_n8n_local.sh  # No Docker needed!
```

---

## 🏗️ Architecture Details

### Component Breakdown

**Frontend** (`webapp/app/templates/`)
- `index.html` - Chat interface
- `workflow.html` - Workflow builder with templates
- `styles.css` - Shared styles

**Backend** (`webapp/app/`)
- `main.py` - FastAPI application (981 lines)
- `n8n_service.py` - Workflow generation (843 lines)
- `genius_enhancements.py` - Advanced features (238 lines)

**Scripts** (`scripts/`)
- `run_n8n_local.sh` - Start local n8n + webapp
- `run_genius_mode.sh` - Start with all features
- `stop_n8n_local.sh` - Stop all services
- `run.sh` - Original chat-only mode

### Data Flow

```
User Input
    ↓ (Grok-3-mini, 10s)
Enhanced Prompt
    ↓ (Grok-4-fast, 25s)
Workflow Analysis
    ↓ (Python, instant)
Nodes + Connections
    ↓ (n8n API, instant)
Deployed Workflow
```

---

## 📊 Performance History

### Evolution of Generation Speed

**Version 1.0** (Initial):
- Analysis: Single Grok-4 call
- Time: 120-180 seconds
- Timeouts: Common
- Connections: Manual only

**Version 2.0** (Optimized):
- Analysis: Grok-4-fast
- Time: 50-60 seconds
- Timeouts: Rare
- Connections: Semi-automatic

**Version 3.0** (Genius Mode - Current):
- Pipeline: Grok-3-mini + Grok-4-fast
- Time: **30-35 seconds**
- Timeouts: Eliminated
- Connections: **Fully intelligent**

---

## 🔧 Advanced Configuration

### Environment Variables

**Required**:
```bash
XAI_API_KEY=xai-your_key_here
```

**Optional** (n8n):
```bash
N8N_API_URL=http://localhost:5678/api/v1
N8N_WEBHOOK_URL=http://localhost:5678
N8N_API_KEY=your_api_key_if_using_cloud
N8N_AUTH_USER=admin
N8N_AUTH_PASSWORD='your_password'
```

**Optional** (performance):
```bash
DB_SQLITE_POOL_SIZE=10
N8N_RUNNERS_ENABLED=true
```

### Model Selection

Current optimized configuration:
- **Enhancement**: grok-3-mini (fast, cheap)
- **Analysis**: grok-4-fast-non-reasoning (fast, accurate)
- **Complex workflows**: grok-4-0709 (only for 16+ nodes)

---

## 🐛 Troubleshooting Archive

### Common Issues & Solutions

**n8n Not Accessible**
```bash
# Check if running
curl http://localhost:5678/healthz

# Restart
bash scripts/stop_n8n_local.sh
bash scripts/run_n8n_local.sh
```

**Workflow Generation Timeout**
- Now fixed with Grok-4-fast!
- If still happens: reduce workflow complexity

**Nodes Not Connected**
- Fixed with intelligent connection algorithm
- Should never happen in Genius Mode

**Parameter Errors**
- Fixed with validation system
- Parameters auto-validated before deployment

---

## 📈 Scalability Notes

### Current Capacity
- **Concurrent Users**: 10-50 (designed for team use)
- **Workflows**: Unlimited (SQLite storage)
- **Generation**: Limited by xAI API rate limits

### Production Deployment
- Use PostgreSQL instead of SQLite
- Add Redis for session storage
- Deploy behind nginx reverse proxy
- Enable HTTPS with Let's Encrypt
- Add authentication (OAuth2/JWT)

---

## 🎓 Best Practices Learned

### For Simple Workflows (3-4 nodes)
- Use templates for instant results
- Interpret mode is perfect
- Generation: ~20 seconds

### For Medium Workflows (8-10 nodes)
- Be specific in prompt
- Use advanced options if needed
- Generation: ~35 seconds

### For Complex Workflows (16+ nodes)
- Use Exact mode for precision
- Specify node sequence
- Add detailed requirements
- Generation: ~60 seconds

---

## 🔬 Technical Insights

### Why Grok-4-Fast?
- 10-15x faster than Grok-4-0709
- Still highly accurate for workflow analysis
- Costs less per token
- Perfect for repetitive tasks

### Connection Algorithm
1. Parse user-specified connections
2. Auto-connect compatible types
3. Validate node existence
4. Connect orphaned nodes
5. Optimize for performance

### Parameter Validation
- Remove None values
- Clean nested objects
- Add type-specific defaults
- Prevent "propertyValues" errors

---

This archive preserves key technical and troubleshooting information from the original 16 documentation files, now consolidated for easier maintenance.

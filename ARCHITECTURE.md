# Grok + n8n Architecture

## System Overview

This system combines xAI's Grok API with n8n workflow automation to create an AI-powered workflow builder that generates complete automation workflows from natural language descriptions.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
├────────────────────────────┬─────────────────────────────────────┤
│   Chat Interface           │   Workflow Builder Interface        │
│   (index.html)             │   (workflow.html)                   │
│   • Model selection        │   • Workflow prompts                │
│   • Chat with Grok         │   • Workflow preview                │
│   • File attachments       │   • Workflow management             │
│   • Web search             │   • n8n dashboard integration       │
└─────────────┬──────────────┴──────────────┬──────────────────────┘
              │                             │
              ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (main.py)                     │
├──────────────────────────────┬──────────────────────────────────┤
│   Chat Endpoints             │   n8n Workflow Endpoints          │
│   • /api/chat                │   • /api/n8n/health               │
│   • /api/chat/workflow       │   • /api/n8n/workflows            │
│   • /api/models              │   • /api/n8n/workflows/generate   │
│   • /api/estimate            │   • /api/n8n/workflows/{id}/...   │
└──────────┬───────────────────┴────────────┬─────────────────────┘
           │                                │
           ▼                                ▼
┌──────────────────────┐     ┌──────────────────────────────────┐
│   Grok API Client    │     │   n8n Service (n8n_service.py)   │
│   • Chat completions │     │   • N8NService (API client)      │
│   • Tool calling     │     │   • GrokWorkflowBuilder          │
│   • Vision/multimodal│     │   • Workflow generation          │
│   • Token estimation │     │   • Node configuration           │
└──────────┬───────────┘     └────────────┬─────────────────────┘
           │                               │
           ▼                               ▼
┌──────────────────────┐     ┌──────────────────────────────────┐
│   xAI Grok API       │     │   n8n REST API                   │
│   api.x.ai           │     │   localhost:5678/api/v1          │
│   • grok-4-0709      │     │   • Workflows CRUD               │
│   • grok-4-fast      │     │   • Execution                    │
│   • grok-code-fast-1 │     │   • Activation                   │
└──────────────────────┘     └────────────┬─────────────────────┘
                                          │
                                          ▼
                             ┌──────────────────────────────────┐
                             │   n8n Instance (Docker)          │
                             │   • Workflow engine              │
                             │   • Node execution               │
                             │   • Webhook handling             │
                             │   • Credential management        │
                             └────────────┬─────────────────────┘
                                          │
                                          ▼
                             ┌──────────────────────────────────┐
                             │   PostgreSQL Database            │
                             │   • Workflow storage             │
                             │   • Execution history            │
                             │   • Credentials (encrypted)      │
                             └──────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer

#### Chat Interface (`index.html`)
- **Purpose**: Primary chat interface with Grok
- **Features**:
  - Model selection (all Grok models)
  - Temperature, tokens, context window controls
  - File upload (text and images)
  - Web search integration
  - Tool calling support
  - Cost estimation
- **Tech**: Vanilla JavaScript, CSS Grid/Flexbox

#### Workflow Builder Interface (`workflow.html`)
- **Purpose**: Dedicated n8n workflow generation UI
- **Features**:
  - Natural language workflow prompts
  - Example prompts for common workflows
  - Real-time workflow generation
  - Workflow preview and visualization
  - Workflow management (list, activate, execute, delete)
  - n8n dashboard integration
- **Tech**: Vanilla JavaScript, CSS Grid

### 2. Backend Layer

#### FastAPI Application (`main.py`)
- **Framework**: FastAPI 0.115.0
- **Key Routes**:
  - `GET /` - Chat interface
  - `GET /workflows` - Workflow builder interface
  - `POST /api/chat` - Standard chat endpoint
  - `POST /api/chat/workflow` - Intelligent workflow-aware chat
  - `POST /api/n8n/workflows/generate` - Generate workflow from prompt
  - `GET /api/n8n/workflows` - List all workflows
  - `POST /api/n8n/workflows/{id}/activate` - Activate workflow
  - `POST /api/n8n/workflows/{id}/execute` - Execute workflow
  - `DELETE /api/n8n/workflows/{id}` - Delete workflow

#### Session Management
- **Storage**: In-memory dictionary (ephemeral)
- **Structure**: `{session_id: [messages]}`
- **Context**: Configurable window size (0-50 messages)

### 3. Workflow Generation Pipeline

#### Step 1: Analysis Phase (`GrokWorkflowBuilder.analyze_workflow_request()`)
```python
User Prompt → Grok API (grok-4-0709) → Structured JSON
{
  "workflow_name": "...",
  "description": "...",
  "nodes": [...],
  "connections": [...],
  "tags": [...]
}
```

**Grok Model**: `grok-4-0709` (reasoning model for complex analysis)
**Temperature**: `0.3` (deterministic)
**System Prompt**: Expert n8n architect persona

#### Step 2: Node Configuration Phase (`GrokWorkflowBuilder.generate_node_configuration()`)
```python
For each node:
  Node Type + Context → Grok API (grok-4-fast) → Parameters JSON
  {
    "method": "POST",
    "url": "...",
    "headers": {...},
    "body": {...}
  }
```

**Grok Model**: `grok-4-fast-non-reasoning` (fast generation)
**Temperature**: `0.2` (mostly deterministic)

#### Step 3: Workflow Assembly (`build_complete_workflow()`)
- Combine analyzed structure with configured parameters
- Generate proper n8n node IDs
- Calculate node positions for visual layout
- Build connection graph
- Create complete `N8NWorkflow` object

#### Step 4: Deployment (`N8NService.create_workflow()`)
- POST workflow JSON to n8n API
- Validate response
- Return workflow ID and metadata

### 4. n8n Service Layer

#### N8NService Class
**Purpose**: REST API client for n8n instance

**Methods**:
- `health_check()` - Verify n8n connectivity
- `list_workflows()` - Get all workflows
- `get_workflow(id)` - Get single workflow
- `create_workflow(workflow)` - Deploy new workflow
- `update_workflow(id, workflow)` - Modify workflow
- `activate_workflow(id)` - Enable workflow
- `execute_workflow(id, data)` - Manual execution
- `delete_workflow(id)` - Remove workflow

**Authentication**: HTTP Basic Auth (configurable)

#### GrokWorkflowBuilder Class
**Purpose**: AI-powered workflow generation using Grok

**Methods**:
- `analyze_workflow_request(prompt)` - Parse user intent
- `generate_node_configuration(type, context)` - Configure individual nodes
- `build_complete_workflow(prompt)` - End-to-end generation

**AI Strategy**:
- Multi-step prompt decomposition
- Structured JSON output parsing
- Fallback handling for malformed responses
- Context-aware parameter generation

### 5. Data Models

#### N8NNode
```python
{
  "id": str,           # Unique node identifier
  "name": str,         # Display name
  "type": str,         # n8n node type (e.g., "n8n-nodes-base.webhook")
  "typeVersion": int,  # Node type version
  "position": [x, y],  # Canvas position
  "parameters": {},    # Node-specific config
  "credentials": {}    # Optional credentials
}
```

#### N8NWorkflow
```python
{
  "name": str,                  # Workflow name
  "nodes": [N8NNode],          # Array of nodes
  "connections": {             # Connection graph
    "node_id": {
      "main": [[{
        "node": "target_id",
        "type": "main",
        "index": 0
      }]]
    }
  },
  "active": bool,              # Activation status
  "settings": {},              # Workflow settings
  "tags": [str]                # Categorization
}
```

### 6. Docker Infrastructure

#### Services

**n8n Container**
- Image: `n8nio/n8n:latest`
- Port: `5678`
- Environment:
  - Basic auth enabled
  - API enabled
  - Webhook URL configured
- Volumes:
  - `n8n_data:/home/node/.n8n` (persistence)
  - `./n8n/custom-nodes` (custom nodes)

**PostgreSQL Container**
- Image: `postgres:15-alpine`
- Port: `5432` (internal)
- Purpose: n8n data persistence
- Healthcheck: `pg_isready`

**Webapp Container**
- Build: `webapp/Dockerfile`
- Port: `8000`
- Environment:
  - `XAI_API_KEY` (from .env)
  - `N8N_API_URL` (internal service URL)
- Volumes:
  - `./webapp:/app/webapp` (hot reload)
  - Rust binary mounted

**Network**
- Type: Bridge network
- Name: `opgrok-network`
- Purpose: Container communication

### 7. Security Model

#### Authentication
- **n8n**: HTTP Basic Auth (configurable credentials)
- **xAI API**: Bearer token (API key)
- **Webapp**: No auth (intended for local/trusted use)

#### Secrets Management
- API keys stored in `.env` file (gitignored)
- n8n credentials encrypted at rest in PostgreSQL
- No passwords in command-line arguments

#### Network Security
- Services isolated in Docker network
- Only webapp and n8n ports exposed to host
- PostgreSQL not exposed externally

### 8. Data Flow Examples

#### Example 1: Simple Webhook Workflow

```
User: "Create a webhook that logs incoming data"
  ↓
Grok Analysis:
  Workflow: "Data Logger Webhook"
  Nodes: [Webhook, Set, HTTP Request (logging)]
  ↓
Grok Configuration:
  Webhook: POST endpoint, JSON body
  Set: Extract relevant fields
  HTTP Request: Log to external service
  ↓
n8n Deployment:
  Create workflow with 3 nodes
  Configure connections: Webhook → Set → HTTP
  Return workflow ID
  ↓
User activates in UI
  ↓
n8n enables webhook endpoint
```

#### Example 2: Scheduled Email Digest

```
User: "Email me daily at 9 AM with news headlines"
  ↓
Grok Analysis:
  Workflow: "Daily News Digest"
  Nodes: [Schedule, HTTP Request (news API), Function (format), Email]
  ↓
Grok Configuration:
  Schedule: Cron "0 9 * * *"
  HTTP Request: GET news API endpoint
  Function: Format headlines as HTML
  Email: SMTP send
  ↓
n8n Deployment:
  Create 4-node workflow
  Configure sequential connections
  ↓
User activates
  ↓
n8n executes daily at 9 AM
```

## Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- No framework dependencies (vanilla)
- Responsive design

### Backend
- Python 3.8+
- FastAPI (async web framework)
- Pydantic (data validation)
- httpx (async HTTP client)
- Jinja2 (templating)

### Workflow Engine
- n8n (open-source workflow automation)
- PostgreSQL (data persistence)
- Docker (containerization)

### AI/ML
- xAI Grok API
  - grok-4-0709 (reasoning)
  - grok-4-fast-non-reasoning (generation)
  - grok-code-fast-1 (coding tasks)

### DevOps
- Docker Compose (orchestration)
- Bash scripts (automation)
- Git (version control)

## Scaling Considerations

### Current Limitations (MVP)
- In-memory session storage (not persistent)
- Single-instance n8n (no clustering)
- No authentication on webapp
- Basic error handling

### Production Recommendations
1. **Session Persistence**
   - Use Redis for session storage
   - Enable session TTL and cleanup

2. **n8n Scaling**
   - Use n8n queue mode with Bull/Redis
   - Deploy multiple worker nodes
   - Load balance webhook endpoints

3. **Security Hardening**
   - Add authentication (OAuth2, JWT)
   - Use reverse proxy (nginx, Traefik)
   - Enable HTTPS with Let's Encrypt
   - Implement rate limiting

4. **Monitoring**
   - Add Prometheus metrics
   - Set up Grafana dashboards
   - Configure alerting (Slack, PagerDuty)
   - Log aggregation (ELK, Loki)

5. **Database**
   - Use managed PostgreSQL (RDS, Cloud SQL)
   - Enable automated backups
   - Set up replication for HA

## Performance Characteristics

### Latency Breakdown

**Workflow Generation (typical)**
- User prompt → Backend: ~10ms
- Backend → Grok Analysis: ~2-5s
- Backend → Grok Config (per node): ~1-2s
- Backend → n8n Deploy: ~100-300ms
- **Total**: ~5-15s (depends on complexity)

**Chat Response (typical)**
- User message → Backend: ~10ms
- Backend → Grok API: ~1-3s (non-streaming)
- Backend → User: ~10ms
- **Total**: ~1-3s

### Throughput
- **Concurrent Users**: Designed for ~10-50 (local/team use)
- **API Rate Limits**: Governed by xAI limits
- **n8n Capacity**: Depends on workflow complexity

## Error Handling

### Grok API Failures
- Timeout after 60-180s
- Retry with exponential backoff (TODO)
- Fallback to simpler models (TODO)
- User-friendly error messages

### n8n API Failures
- Health check before operations
- Validate workflow structure
- Rollback on deployment failure (TODO)
- Clear error reporting to user

### Workflow Execution Failures
- n8n handles retry logic
- Error workflows can be configured
- Execution logs available in n8n dashboard

## Future Enhancements

1. **Workflow Templates Library**
   - Pre-built workflow templates
   - One-click deployment
   - Community sharing

2. **Workflow Versioning**
   - Git-like version control
   - Diff visualization
   - Rollback capabilities

3. **Advanced Prompt Engineering**
   - Few-shot learning examples
   - Workflow pattern recognition
   - Optimization suggestions

4. **Real-time Collaboration**
   - WebSocket integration
   - Multi-user workflow editing
   - Live execution monitoring

5. **Workflow Testing Framework**
   - Automated testing generation
   - Mock data creation
   - Regression testing

6. **Analytics Dashboard**
   - Workflow usage metrics
   - Cost tracking
   - Performance analytics

## Contributing

See main README.md for contribution guidelines.

## License

See LICENSE file for details.

#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════
# OPGROK - Unified Control Script
# One script to rule them all: start, stop, genius, chat
# ═══════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

# ═══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════

load_environment() {
    if [[ -f "${REPO_ROOT}/.env" ]]; then
        while IFS='=' read -r key value; do
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            value="${value%\'}"
            value="${value#\'}"
            value="${value%\"}"
            value="${value#\"}"
            export "$key=$value"
        done < <(grep -E '^[A-Z_]+=' "${REPO_ROOT}/.env")
    elif [[ -f "${REPO_ROOT}/grok-chat-app/.env" ]]; then
        while IFS='=' read -r key value; do
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            value="${value%\'}"
            value="${value#\'}"
            value="${value%\"}"
            value="${value#\"}"
            export "$key=$value"
        done < <(grep -E '^[A-Z_]+=' "${REPO_ROOT}/grok-chat-app/.env")
    fi
}

check_prerequisites() {
    local mode=$1
    
    # Check .env exists
    if [[ ! -f "${REPO_ROOT}/.env" ]] && [[ ! -f "${REPO_ROOT}/grok-chat-app/.env" ]]; then
        echo "❌ No .env file found!"
        if [[ -f "${REPO_ROOT}/.env.example" ]]; then
            echo "Creating from template..."
            cp "${REPO_ROOT}/.env.example" "${REPO_ROOT}/.env"
            echo "📝 Please edit .env and add your XAI_API_KEY, then run again."
        fi
        exit 1
    fi
    
    load_environment
    
    if [[ -z "${XAI_API_KEY:-}" ]]; then
        echo "❌ XAI_API_KEY not set in .env"
        exit 1
    fi
    
    # Check Node.js for n8n modes
    if [[ "$mode" == "genius" ]] || [[ "$mode" == "workflow" ]]; then
        if ! command -v node >/dev/null 2>&1; then
            echo "❌ Node.js not found. Install from https://nodejs.org"
            exit 1
        fi
        
        local node_ver=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
        if [[ "${node_ver}" -lt 18 ]]; then
            echo "⚠️  Node.js ${node_ver} detected. Upgrade to 18+ recommended."
        fi
    fi
}

free_ports() {
    local ports=("$@")
    if command -v lsof >/dev/null 2>&1; then
        for port in "${ports[@]}"; do
            local pids=$(lsof -ti:"${port}" 2>/dev/null || true)
            if [[ -n "$pids" ]]; then
                echo "🧹 Freeing port ${port}..."
                kill -9 ${pids} 2>/dev/null || true
                sleep 0.5
            fi
        done
    fi
}

setup_python() {
    echo "🐍 Setting up Python environment..."
    if [[ ! -d .venv ]]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install --upgrade pip >/dev/null 2>&1 || true
    pip install -r webapp/requirements.txt >/dev/null 2>&1
}

build_rust() {
    echo "🦀 Building Rust CLI..."
    cargo build --release --features terminal --manifest-path grok-chat-app/Cargo.toml 2>&1 | grep -E "(Finished|error)" || true
}

# ═══════════════════════════════════════════════════════════
# START MODES
# ═══════════════════════════════════════════════════════════

start_chat_only() {
    echo "💬 Starting Chat-Only Mode"
    echo "════════════════════════════"
    
    free_ports 8000
    build_rust
    setup_python
    
    echo "🚀 Starting Grok Chat on http://localhost:8000"
    source .venv/bin/activate
    exec python -m uvicorn webapp.app.main:app --host 0.0.0.0 --port 8000 --reload
}

start_workflow() {
    echo "🔧 Starting Workflow Builder Mode"
    echo "═════════════════════════════════"
    
    free_ports 8000 5678
    build_rust
    setup_python
    
    # Configure n8n
    export N8N_BASIC_AUTH_ACTIVE=true
    export N8N_BASIC_AUTH_USER="${N8N_AUTH_USER:-admin}"
    export N8N_BASIC_AUTH_PASSWORD="${N8N_AUTH_PASSWORD:-changeme}"
    export N8N_HOST=0.0.0.0
    export N8N_PORT=5678
    export N8N_PROTOCOL=http
    export WEBHOOK_URL=http://localhost:5678/
    export N8N_LOG_LEVEL=info
    export N8N_API_URL=http://localhost:5678/api/v1
    export N8N_WEBHOOK_URL=http://localhost:5678
    export N8N_USER_FOLDER="${REPO_ROOT}/.n8n"
    
    mkdir -p .n8n
    
    # Start n8n
    echo "📊 Starting n8n..."
    npx n8n start > .n8n/n8n.log 2>&1 &
    local n8n_pid=$!
    echo "${n8n_pid}" > .n8n/n8n.pid
    
    echo "   Waiting for n8n..."
    for i in {1..30}; do
        if curl -s http://localhost:5678/healthz >/dev/null 2>&1; then
            echo "   ✅ n8n ready!"
            break
        fi
        [[ $i -eq 30 ]] && { echo "   ❌ Timeout"; exit 1; }
        sleep 2
    done
    
    # Start webapp
    echo "📱 Starting webapp..."
    source .venv/bin/activate
    python -m uvicorn webapp.app.main:app --host 0.0.0.0 --port 8000 --reload > .n8n/webapp.log 2>&1 &
    local webapp_pid=$!
    echo "${webapp_pid}" > .n8n/webapp.pid
    
    sleep 3
    
    echo ""
    echo "✅ OPGROK Workflow Builder Ready!"
    echo ""
    echo "📍 Access Points:"
    echo "   • Workflow Builder: http://localhost:8000/workflows"
    echo "   • Chat: http://localhost:8000"
    echo "   • n8n Dashboard: http://localhost:5678"
    echo ""
    echo "🛑 Stop: opgrok stop"
    echo ""
    
    # Show logs
    trap 'echo ""; echo "Services running in background. Use: opgrok stop"; exit 0' INT
    tail -f .n8n/webapp.log &
    tail -f .n8n/n8n.log &
    wait
}

start_genius() {
    echo "🧠 Starting GENIUS MODE"
    echo "══════════════════════"
    echo "✨ Multi-stage AI processing"
    echo "🔗 Intelligent connections"
    echo "⚡ Optimized performance"
    echo ""
    
    # Same as workflow but with enhanced messaging
    free_ports 8000 5678
    build_rust
    setup_python
    
    # Enhanced n8n config
    export N8N_BASIC_AUTH_ACTIVE=true
    export N8N_BASIC_AUTH_USER="${N8N_AUTH_USER:-admin}"
    export N8N_BASIC_AUTH_PASSWORD="${N8N_AUTH_PASSWORD:-changeme}"
    export N8N_HOST=0.0.0.0
    export N8N_PORT=5678
    export N8N_PROTOCOL=http
    export WEBHOOK_URL=http://localhost:5678/
    export N8N_LOG_LEVEL=info
    export N8N_API_URL=http://localhost:5678/api/v1
    export N8N_WEBHOOK_URL=http://localhost:5678
    export N8N_USER_FOLDER="${REPO_ROOT}/.n8n"
    export DB_SQLITE_POOL_SIZE=10
    export N8N_RUNNERS_ENABLED=true
    export N8N_BLOCK_ENV_ACCESS_IN_NODE=false
    export N8N_GIT_NODE_DISABLE_BARE_REPOS=true
    
    mkdir -p .n8n
    
    echo "📊 Starting n8n with genius optimizations..."
    npx n8n start > .n8n/n8n.log 2>&1 &
    echo "$!" > .n8n/n8n.pid
    
    echo "   Waiting for n8n..."
    for i in {1..30}; do
        if curl -s http://localhost:5678/healthz >/dev/null 2>&1; then
            echo "   ✅ n8n ready!"
            break
        fi
        [[ $i -eq 30 ]] && { echo "   ❌ Timeout"; exit 1; }
        sleep 2
    done
    
    echo "💎 Starting genius-enhanced webapp..."
    source .venv/bin/activate
    python -m uvicorn webapp.app.main:app --host 0.0.0.0 --port 8000 --reload > .n8n/webapp.log 2>&1 &
    echo "$!" > .n8n/webapp.pid
    
    sleep 3
    
    echo ""
    echo "🎉 GENIUS MODE ACTIVATED!"
    echo ""
    echo "🌟 Features:"
    echo "   • 30-second workflow generation"
    echo "   • Intelligent auto-connections"
    echo "   • 8 templates + advanced controls"
    echo "   • Real-time progress tracking"
    echo ""
    echo "📍 Access:"
    echo "   • http://localhost:8000/workflows"
    echo ""
    echo "🛑 Stop: opgrok stop"
    echo ""
    
    trap 'echo ""; echo "Genius mode running. Use: opgrok stop"; exit 0' INT
    tail -f .n8n/webapp.log &
    tail -f .n8n/n8n.log &
    wait
}

stop_services() {
    echo "🛑 Stopping OPGROK services..."
    
    # Stop by PIDs
    for pidfile in .n8n/n8n.pid .n8n/webapp.pid; do
        if [[ -f "${pidfile}" ]]; then
            local pid=$(cat "${pidfile}")
            if ps -p ${pid} >/dev/null 2>&1; then
                kill ${pid} 2>/dev/null || true
                sleep 1
                ps -p ${pid} >/dev/null 2>&1 && kill -9 ${pid} 2>/dev/null || true
            fi
            rm -f "${pidfile}"
        fi
    done
    
    # Fallback: kill by port
    if command -v lsof >/dev/null 2>&1; then
        for port in 5678 8000; do
            local pids=$(lsof -ti:${port} 2>/dev/null || true)
            [[ -n "$pids" ]] && kill -9 ${pids} 2>/dev/null || true
        done
    fi
    
    echo "✅ All services stopped"
    echo "   Restart: opgrok start"
}

show_status() {
    echo "📊 OPGROK Status"
    echo "═══════════════"
    
    # Check n8n
    if curl -s http://localhost:5678/healthz >/dev/null 2>&1; then
        echo "✅ n8n: Running (http://localhost:5678)"
    else
        echo "❌ n8n: Not running"
    fi
    
    # Check webapp
    if curl -s http://localhost:8000 >/dev/null 2>&1; then
        echo "✅ Webapp: Running (http://localhost:8000)"
    else
        echo "❌ Webapp: Not running"
    fi
    
    # Check PIDs
    if [[ -f .n8n/n8n.pid ]]; then
        local pid=$(cat .n8n/n8n.pid)
        if ps -p ${pid} >/dev/null 2>&1; then
            echo "   n8n PID: ${pid}"
        fi
    fi
    
    if [[ -f .n8n/webapp.pid ]]; then
        local pid=$(cat .n8n/webapp.pid)
        if ps -p ${pid} >/dev/null 2>&1; then
            echo "   Webapp PID: ${pid}"
        fi
    fi
}

show_usage() {
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🤖 OPGROK - AI-Powered Workflow Automation             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Usage: opgrok <command>

Commands:
  start, workflow       Start workflow builder + n8n + chat
  genius                Start with all genius features  
  chat                  Start chat-only mode (no n8n)
  stop                  Stop all services gracefully
  status                Show service status
  restart               Restart all services
  logs                  Show live logs
  help                  Show this help

Examples:
  opgrok start          # Start full workflow builder
  opgrok genius         # Start with all features
  opgrok chat           # Chat only (no workflow builder)
  opgrok stop           # Stop everything
  opgrok status         # Check what's running
  opgrok restart        # Refresh services

Quick Start:
  1. opgrok start
  2. Open http://localhost:8000/workflows
  3. Build amazing automation workflows!

Documentation: README.md, MASTER_GUIDE.md

EOF
}

# ═══════════════════════════════════════════════════════════
# MAIN COMMAND ROUTER
# ═══════════════════════════════════════════════════════════

COMMAND="${1:-help}"

case "$COMMAND" in
    start|workflow|w)
        check_prerequisites "workflow"
        start_workflow
        ;;
    
    genius|g)
        check_prerequisites "genius"
        start_genius
        ;;
    
    chat|c)
        check_prerequisites "chat"
        start_chat_only
        ;;
    
    stop|s)
        stop_services
        ;;
    
    restart|r)
        stop_services
        sleep 2
        check_prerequisites "workflow"
        start_workflow
        ;;
    
    status|st)
        show_status
        ;;
    
    logs|l)
        echo "📡 Live logs (Ctrl+C to exit)"
        tail -f .n8n/webapp.log .n8n/n8n.log 2>/dev/null || echo "No logs found. Start services first."
        ;;
    
    help|h|--help|-h)
        show_usage
        ;;
    
    *)
        echo "❌ Unknown command: $COMMAND"
        echo ""
        show_usage
        exit 1
        ;;
esac

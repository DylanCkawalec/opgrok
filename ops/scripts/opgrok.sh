#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════
# OPGROK - Unified Control Script
# One script to rule them all: start, stop, genius, chat
# ═══════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
# ops/scripts -> repo root
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

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
    elif [[ -f "${REPO_ROOT}/apps/chat/.env" ]]; then
        while IFS='=' read -r key value; do
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            value="${value%\'}"
            value="${value#\'}"
            value="${value%\"}"
            value="${value#\"}"
            export "$key=$value"
        done < <(grep -E '^[A-Z_]+=' "${REPO_ROOT}/apps/chat/.env")
    fi
}

check_prerequisites() {
    local mode=$1
    
    # Check .env exists
    if [[ ! -f "${REPO_ROOT}/.env" ]] && [[ ! -f "${REPO_ROOT}/apps/chat/.env" ]]; then
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
    pip install -r apps/web/requirements.txt >/dev/null 2>&1
}

build_rust() {
    echo "🦀 Building Rust CLI..."
    cargo build --release --features terminal --manifest-path apps/chat/Cargo.toml 2>&1 | grep -E "(Finished|error)" || true
}

# ═══════════════════════════════════════════════════════════
# START MODES
# ═══════════════════════════════════════════════════════════

start_chat_only() {
    echo "💬 Starting Chat-Only Mode"
    echo "════════════════════════════"
    
    free_ports 420
    build_rust
    setup_python
    
    echo "🚀 Starting Grok Chat on http://localhost:420"
    source .venv/bin/activate
    exec python -m uvicorn app.main:app --app-dir apps/web --host 0.0.0.0 --port 420 --reload
}

start_workflow() {
    echo "🔧 Starting Workflow Builder Mode"
    echo "═════════════════════════════════"
    
    free_ports 420 5678
    build_rust
    setup_python
    
    # Configure n8n - auth disabled for seamless access
    export N8N_BASIC_AUTH_ACTIVE=false
    export N8N_HOST=127.0.0.1
    export N8N_PORT=5678
    export N8N_PROTOCOL=http
    export WEBHOOK_URL=http://localhost:420/
    export N8N_LOG_LEVEL=info
    export N8N_API_URL=http://localhost:5678/api/v1
    export N8N_WEBHOOK_URL=http://localhost:420
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
    
    # Start webapp on port 420
    echo "📱 Starting webapp..."
    source .venv/bin/activate
    python -m uvicorn app.main:app --app-dir apps/web --host 0.0.0.0 --port 420 --reload > .n8n/webapp.log 2>&1 &
    local webapp_pid=$!
    echo "${webapp_pid}" > .n8n/webapp.pid
    
    sleep 3
    
    echo ""
    echo "✅ OPGROK Workflow Builder Ready!"
    echo ""
    echo "📍 Access Points:"
    echo "   • Chat: http://localhost:420"
    echo "   • Workflow Builder: http://localhost:420/workflows"
    echo "   • n8n Dashboard: http://localhost:420/n8n (proxied)"
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
    free_ports 420 5678
    build_rust
    setup_python
    
    # Enhanced n8n config - auth disabled for seamless access
    export N8N_BASIC_AUTH_ACTIVE=false
    export N8N_HOST=127.0.0.1
    export N8N_PORT=5678
    export N8N_PROTOCOL=http
    export WEBHOOK_URL=http://localhost:420/
    export N8N_LOG_LEVEL=info
    export N8N_API_URL=http://localhost:5678/api/v1
    export N8N_WEBHOOK_URL=http://localhost:420
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
    python -m uvicorn app.main:app --app-dir apps/web --host 0.0.0.0 --port 420 --reload > .n8n/webapp.log 2>&1 &
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
    echo "   • http://localhost:420/workflows"
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
        for port in 5678 420; do
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
    if curl -s http://localhost:420 >/dev/null 2>&1; then
        echo "✅ Webapp: Running (http://localhost:420)"
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

craft_harness() {
    local goal="${*:-}"
    if [[ -z "${goal}" ]]; then
        echo "Usage: opgrok craft \"<goal>\""
        echo "   or: @opgrok <goal>  in Grok Build (loads core/skills/opgrok)"
        exit 1
    fi
    echo "🔧 @opgrok craft + build"
    echo "Goal: ${goal}"
    if command -v cargo >/dev/null 2>&1; then
        cargo run -q -p opgrok-sg-cli -- --repo "${REPO_ROOT}" craft "${goal}" 2>/dev/null || true
    fi
    python3 "${REPO_ROOT}/core/tools/craft_harness.py" "${goal}"
}

build_harness_cmd() {
    local slug="${1:-}"
    local install_flag=()
    shift || true
    for a in "$@"; do
        [[ "$a" == "--install" ]] && install_flag=(--install)
    done
    if [[ -z "${slug}" ]]; then
        echo "Usage: opgrok build <slug> [--install]"; exit 1
    fi
    python3 "${REPO_ROOT}/core/tools/build_harness.py" "${slug}" "${install_flag[@]}"
}

run_harness_cmd() {
    local slug="${1:-}"
    shift || true
    if [[ -z "${slug}" ]]; then
        echo "Usage: opgrok run <slug> [--goal ...] [--dry-run]"; exit 1
    fi
    local bin="${REPO_ROOT}/core/binaries/${slug}/bin/opgrok-${slug}"
    if [[ -x "${bin}" ]]; then
        exec "${bin}" "$@"
    fi
    python3 "${REPO_ROOT}/core/tools/run_harness.py" "${slug}" --repo "${REPO_ROOT}" "$@"
}

show_usage() {
    cat << 'EOF'
OPGROK — SuperGrok harness control + app shell

Core (agent harnesses):
  craft "<goal>"        @opgrok — hire, Leslie WC, graph, skills_cache, build binary
  build <slug> [--install]  cargo release or Python entrypoint → bin/ (+ ~/.opgrok/bin)
  run <slug> [--goal] [--dry-run]  Live Grok API per node (skill injection)
  harnesses             List core/binaries/registry.json
  route "<intent>"      Route intent to SuperGroks
  validate              Leslie Gate on SuperGrok skills

App shell:
  start | workflow      Web + n8n
  genius                Genius mode
  chat                  Web only
  stop | status | logs | restart

Examples:
  opgrok craft "build a landing page with hero and pricing"
  @opgrok build me a multi-page marketing site   # in Grok Build
  opgrok start

Docs: README.md · core/harness/SPEC.md · core/skills/opgrok/SKILL.md
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

    craft|@opgrok|opgrok)
        shift || true
        craft_harness "$@"
        ;;

    build)
        shift || true
        build_harness_cmd "$@"
        ;;

    run)
        shift || true
        run_harness_cmd "$@"
        ;;

    install)
        shift || true
        build_harness_cmd "${1:-}" --install
        ;;

    harnesses|bins)
        cat "${REPO_ROOT}/core/binaries/registry.json"
        ;;

    route)
        shift || true
        ROUTE_GOAL="${*:-}"
        python3 -c "
import json, re
from pathlib import Path
root = Path(r'${REPO_ROOT}')
goal = '''${ROUTE_GOAL}'''
reg = json.loads((root/'core/skills/_framework/REGISTRY.json').read_text())
tokens = [t for t in re.split(r'[^a-z0-9\-]+', goal.lower()) if len(t)>2]
scored=[]
for sk in reg['skills']:
    blob=' '.join([sk.get('name',''), sk.get('category',''), sk.get('intent',''), sk.get('purpose','')]).lower()
    score=sum(3 for t in tokens if t in blob)
    if score: scored.append((score, sk))
scored.sort(key=lambda x:(-x[0], x[1]['name']))
for s,sk in scored[:8]:
    print(f\"{sk['name']}\t{sk.get('nest','')}\t{sk.get('intent','')[:80]}\")
"
        ;;

    validate)
        python3 "${REPO_ROOT}/core/tools/validate_supergroks.py"
        ;;
    
    help|h|--help|-h)
        show_usage
        ;;
    
    *)
        # If first arg looks like a free-form goal, treat as craft ( @opgrok UX )
        if [[ "$COMMAND" != help ]]; then
            craft_harness "$@"
        else
            show_usage
            exit 1
        fi
        ;;
esac

#!/usr/bin/env bash
set -euo pipefail

# Genius Mode - Enhanced n8n Workflow Builder with Advanced Features
# This script starts the complete system with all genius enhancements

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

echo "🧠 Starting GENIUS MODE - Advanced Workflow Builder"
echo "=================================================="
echo "✨ Multi-stage AI processing"
echo "🔗 Intelligent node connections"  
echo "⚡ Fast enhancement with Grok-3-mini"
echo "🎯 Exact/Interpret mode controls"
echo "📊 Real-time progress tracking"
echo ""

# Check prerequisites
if [[ ! -f "${REPO_ROOT}/.env" ]]; then
  echo "❌ .env file not found. Please create it:"
  echo "   cp .env.example .env"
  echo "   # Edit .env and add your XAI_API_KEY"
  exit 1
fi

# Load environment
source "${REPO_ROOT}/.env"

if [[ -z "${XAI_API_KEY:-}" ]]; then
  echo "❌ XAI_API_KEY not set in .env file"
  exit 1
fi

echo "✅ Environment configured with API key"

# Check Node.js for n8n
if ! command -v node >/dev/null 2>&1; then
  echo "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org"
  exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [[ "${NODE_VERSION}" -lt 18 ]]; then
  echo "⚠️  Node.js version $NODE_VERSION detected. Upgrade to 18+ for optimal performance"
fi

echo "✅ Node.js $(node -v) ready"

# Clean ports
echo "🧹 Preparing ports..."
for PORT in 8000 5678; do
  if lsof -ti:"${PORT}" >/dev/null 2>&1; then
    echo "   Freeing port ${PORT}..."
    lsof -ti:"${PORT}" | xargs kill -9 2>/dev/null || true
    sleep 1
  fi
done

# Build optimized Rust CLI
echo "🦀 Building optimized Rust CLI..."
cd grok-chat-app
cargo build --release --features terminal
cd ..

# Setup Python with all dependencies
echo "🐍 Setting up enhanced Python environment..."
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip >/dev/null 2>&1
pip install -r webapp/requirements.txt

# Verify all Grok models are accessible
echo "🤖 Verifying Grok model access..."
python3 -c "
import httpx, asyncio, os

async def test_models():
    api_key = os.getenv('XAI_API_KEY')
    models = ['grok-3-mini', 'grok-4-fast-non-reasoning', 'grok-4-0709']
    
    for model in models:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    'https://api.x.ai/v1/chat/completions',
                    headers={'Authorization': f'Bearer {api_key}'},
                    json={
                        'model': model,
                        'messages': [{'role': 'user', 'content': 'test'}],
                        'max_tokens': 10
                    }
                )
                if response.status_code == 200:
                    print(f'   ✅ {model} accessible')
                else:
                    print(f'   ⚠️  {model} issue: {response.status_code}')
        except Exception as e:
            print(f'   ❌ {model} failed: connection error')

asyncio.run(test_models())
"

# Enhanced n8n configuration
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER="${N8N_AUTH_USER:-yozkyo}"
export N8N_BASIC_AUTH_PASSWORD="${N8N_AUTH_PASSWORD:-changeme}"
export N8N_HOST=0.0.0.0
export N8N_PORT=5678
export N8N_PROTOCOL=http
export WEBHOOK_URL=http://localhost:5678/
export N8N_LOG_LEVEL=info
export N8N_API_URL=http://localhost:5678/api/v1
export N8N_WEBHOOK_URL=http://localhost:5678

# Enhanced n8n settings for better performance
export DB_SQLITE_POOL_SIZE=10
export N8N_RUNNERS_ENABLED=true
export N8N_BLOCK_ENV_ACCESS_IN_NODE=false
export N8N_GIT_NODE_DISABLE_BARE_REPOS=true

echo ""
echo "🚀 Starting GENIUS MODE services..."
echo ""

# Start n8n with enhanced config
echo "📊 Starting n8n with performance optimizations..."
mkdir -p .n8n
export N8N_USER_FOLDER="${REPO_ROOT}/.n8n"

npx n8n start > .n8n/n8n.log 2>&1 &
N8N_PID=$!
echo "   n8n PID: ${N8N_PID}" 
echo "${N8N_PID}" > .n8n/n8n.pid

# Wait for n8n with timeout
echo "   Waiting for n8n startup (max 60s)..."
for i in {1..30}; do
  if curl -s http://localhost:5678/healthz >/dev/null 2>&1; then
    echo "   ✅ n8n ready with genius features!"
    break
  fi
  if [[ $i -eq 30 ]]; then
    echo "   ❌ n8n startup failed. Check: tail -f .n8n/n8n.log"
    exit 1
  fi
  sleep 2
done

# Start enhanced webapp
echo "💎 Starting webapp with genius enhancements..."
python -m uvicorn webapp.app.main:app --host 0.0.0.0 --port 8000 --reload > .n8n/webapp.log 2>&1 &
WEBAPP_PID=$!
echo "   webapp PID: ${WEBAPP_PID}"
echo "${WEBAPP_PID}" > .n8n/webapp.pid

# Wait for webapp
sleep 4

echo ""
echo "🎉 GENIUS MODE ACTIVATED!"
echo ""
echo "🌟 Enhanced Features Available:"
echo "   • Multi-stage AI processing (Grok-3-mini + Grok-4)"
echo "   • Intelligent node connections"
echo "   • Advanced generation modes (Interpret/Exact)"
echo "   • Node sequence control"
echo "   • Real-time progress tracking"
echo "   • Performance optimizations"
echo "   • Template suggestions"
echo "   • Complex workflow support (16+ nodes)"
echo ""
echo "📍 Access Points:"
echo "   • 🎨 Genius Workflow Builder: http://localhost:8000/workflows"
echo "   • 💬 Enhanced Chat: http://localhost:8000"  
echo "   • 📊 n8n Dashboard: http://localhost:5678"
echo "   • 🔑 Credentials: ${N8N_BASIC_AUTH_USER} / [from .env]"
echo ""
echo "🎯 Try Advanced Features:"
echo "   1. Open the workflow builder"
echo "   2. Click '🔧 Advanced Options'"
echo "   3. Try 'Exact' mode with node sequence"
echo "   4. Watch real-time progress indicators"
echo ""
echo "💡 Complex Workflow Examples:"
echo "   • Multi-step customer onboarding (8+ nodes)"
echo "   • Data processing pipelines (12+ nodes)"  
echo "   • Business automation workflows (16+ nodes)"
echo ""
echo "🔍 Monitor:"
echo "   tail -f .n8n/n8n.log     # n8n logs"
echo "   tail -f .n8n/webapp.log  # webapp logs"
echo ""
echo "🛑 Stop:"
echo "   bash scripts/stop_n8n_local.sh"
echo ""

# Show live logs
trap 'echo ""; echo "🎉 Genius mode running in background!"; echo "Use scripts/stop_n8n_local.sh to stop"; exit 0' INT

echo "📡 Live logs (Ctrl+C to detach, services continue running):"
echo ""

tail -f .n8n/webapp.log &
tail -f .n8n/n8n.log &

wait

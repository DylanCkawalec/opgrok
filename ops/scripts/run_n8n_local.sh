#!/usr/bin/env bash
set -euo pipefail

# n8n Workflow Builder - Local Installation (No Docker)
# This script runs n8n locally via npx instead of Docker

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "${REPO_ROOT}"

echo "🤖 Starting Grok + n8n Workflow Builder (Local Mode)"
echo "===================================================="

# Check if .env exists
if [[ ! -f "${REPO_ROOT}/.env" ]] && [[ ! -f "${REPO_ROOT}/apps/chat/.env" ]]; then
  echo "⚠️  No .env file found!"
  echo "Creating .env from .env.example..."
  
  if [[ -f "${REPO_ROOT}/.env.example" ]]; then
    cp "${REPO_ROOT}/.env.example" "${REPO_ROOT}/.env"
    echo "📝 Please edit .env and add your XAI_API_KEY"
    echo "   Then run this script again."
    exit 1
  else
    echo "❌ .env.example not found. Please create .env manually."
    exit 1
  fi
fi

# Load environment variables (handle special characters properly)
if [[ -f "${REPO_ROOT}/.env" ]]; then
  # Use a safer method that handles special characters in passwords
  while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue
    # Remove quotes if present
    value="${value%\'}"
    value="${value#\'}"
    value="${value%\"}"
    value="${value#\"}"
    # Export the variable
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

# Verify API key
if [[ -z "${XAI_API_KEY:-}" ]]; then
  echo "❌ XAI_API_KEY not set in .env file"
  exit 1
fi

echo "✅ Environment configured"

# Check for Node.js
if ! command -v node >/dev/null 2>&1; then
  echo "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org"
  exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [[ "${NODE_VERSION}" -lt 18 ]]; then
  echo "⚠️  Node.js version $NODE_VERSION detected. n8n requires Node.js 18 or higher."
  echo "   Please upgrade: https://nodejs.org"
  exit 1
fi

echo "✅ Node.js $(node -v) detected"

# Check for lsof
if ! command -v lsof >/dev/null 2>&1; then
  echo "⚠️  lsof not found (optional for port cleanup)"
else
  # Free up ports if needed
  echo "\U0001f9f9 Checking ports 420 and 5678..."
  for PORT in 420 5678; do
    PIDS="$(lsof -ti:"${PORT}" 2>/dev/null || true)"
    if [[ -n "${PIDS}" ]]; then
      echo "Killing processes on port ${PORT}: ${PIDS}"
      kill -9 ${PIDS} 2>/dev/null || true
      sleep 1
    fi
  done
fi

# Build Rust binary
echo "🦀 Building Rust CLI..."
cargo build --release --features terminal --manifest-path apps/chat/Cargo.toml

# Set up Python virtual environment
echo "🐍 Setting up Python environment..."
VENV_DIR="${REPO_ROOT}/.venv"
if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip >/dev/null 2>&1 || true
pip install -r apps/web/requirements.txt

# Set n8n configuration - auth disabled for seamless access
export N8N_BASIC_AUTH_ACTIVE=false
export N8N_HOST=127.0.0.1
export N8N_PORT=5678
export N8N_PROTOCOL=http
export WEBHOOK_URL=http://localhost:420/
export N8N_LOG_LEVEL=info

# Update .env for webapp to use local n8n
export N8N_API_URL=http://localhost:5678/api/v1
export N8N_WEBHOOK_URL=http://localhost:420

echo ""
echo "🚀 Starting services..."
echo ""

# Start n8n in background
echo "📊 Starting n8n (local installation)..."
echo "   This will download n8n on first run (may take a minute)"
echo ""

# Create n8n data directory
mkdir -p "${REPO_ROOT}/.n8n"
export N8N_USER_FOLDER="${REPO_ROOT}/.n8n"

# Start n8n in background
npx n8n start > "${REPO_ROOT}/.n8n/n8n.log" 2>&1 &
N8N_PID=$!
echo "   n8n PID: ${N8N_PID}"
echo "${N8N_PID}" > "${REPO_ROOT}/.n8n/n8n.pid"

# Wait for n8n to start
echo "   Waiting for n8n to start..."
for i in {1..30}; do
  if curl -s http://localhost:5678/healthz >/dev/null 2>&1; then
    echo "   ✅ n8n is ready!"
    break
  fi
  if [[ $i -eq 30 ]]; then
    echo "   ❌ n8n failed to start. Check logs: cat ${REPO_ROOT}/.n8n/n8n.log"
    exit 1
  fi
  sleep 2
done

# Start webapp in background
echo "📱 Starting webapp..."
python -m uvicorn app.main:app --app-dir apps/web --host 0.0.0.0 --port 420 --reload > "${REPO_ROOT}/.n8n/webapp.log" 2>&1 &
WEBAPP_PID=$!
echo "   webapp PID: ${WEBAPP_PID}"
echo "${WEBAPP_PID}" > "${REPO_ROOT}/.n8n/webapp.pid"

# Wait for webapp to start
sleep 3

echo ""
echo "✅ Services started successfully!"
echo ""
echo "\U0001f4cd Access Points:"
echo "   \u2022 Grok Chat: http://localhost:420"
echo "   \u2022 Workflow Builder: http://localhost:420/workflows"
echo "   \u2022 n8n Dashboard: http://localhost:420/n8n (proxied)"
echo ""
echo "\U0001f4d6 Quick Start:"
echo "   1. Open http://localhost:420"
echo "   2. Describe your automation workflow"
echo "   3. Click 'Generate Workflow'"
echo "   4. View and activate in n8n dashboard"
echo ""
echo "📚 Documentation: See N8N_QUICKSTART.md for detailed guide"
echo ""
echo "🔍 View logs:"
echo "   tail -f ${REPO_ROOT}/.n8n/n8n.log"
echo "   tail -f ${REPO_ROOT}/.n8n/webapp.log"
echo ""
echo "🛑 Stop services:"
echo "   bash ops/scripts/stop_n8n_local.sh"
echo "   (or kill PIDs: ${N8N_PID} ${WEBAPP_PID})"
echo ""
echo "Press Ctrl+C to view logs (services will continue running in background)"
echo ""

# Show logs in foreground
trap 'echo ""; echo "Services still running in background. Use scripts/stop_n8n_local.sh to stop."; exit 0' INT

tail -f "${REPO_ROOT}/.n8n/webapp.log" &
tail -f "${REPO_ROOT}/.n8n/n8n.log" &

wait

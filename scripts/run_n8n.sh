#!/usr/bin/env bash
set -euo pipefail

# n8n Workflow Builder - Startup Script (Docker/OrbStack)
# This script starts the complete n8n + Grok Chat integration using containers

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

echo "🤖 Starting Grok + n8n Workflow Builder"
echo "========================================"

# Check if .env exists
if [[ ! -f "${REPO_ROOT}/.env" ]] && [[ ! -f "${REPO_ROOT}/grok-chat-app/.env" ]]; then
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

# Load environment variables
if [[ -f "${REPO_ROOT}/.env" ]]; then
  export $(grep -E '^[A-Z_]+=' "${REPO_ROOT}/.env" | sed 's/[[:space:]]//g')
elif [[ -f "${REPO_ROOT}/grok-chat-app/.env" ]]; then
  export $(grep -E '^[A-Z_]+=' "${REPO_ROOT}/grok-chat-app/.env" | sed 's/[[:space:]]//g')
fi

# Verify API key
if [[ -z "${XAI_API_KEY:-}" ]]; then
  echo "❌ XAI_API_KEY not set in .env file"
  exit 1
fi

echo "✅ Environment configured"

# Check if Docker/OrbStack is running
DOCKER_TYPE="Docker"
if ! docker info >/dev/null 2>&1; then
  echo "❌ Docker/OrbStack is not running."
  echo "   Please start OrbStack or Docker Desktop."
  echo ""
  echo "💡 Alternatively, use local installation (no Docker required):"
  echo "   bash scripts/run_n8n_local.sh"
  exit 1
fi

# Detect if using OrbStack
if docker info 2>/dev/null | grep -qi "orbstack"; then
  DOCKER_TYPE="OrbStack"
  COMPOSE_FILE="docker-compose.orbstack.yml"
else
  COMPOSE_FILE="docker-compose.yml"
fi

echo "✅ ${DOCKER_TYPE} is running"

# Check for docker-compose
if command -v docker-compose >/dev/null 2>&1; then
  COMPOSE_CMD="docker-compose"
elif docker compose version >/dev/null 2>&1; then
  COMPOSE_CMD="docker compose"
else
  echo "❌ docker-compose not found"
  exit 1
fi

echo "🐳 Using: ${COMPOSE_CMD} with ${COMPOSE_FILE}"

# Build Rust binary first (for local development)
echo "🦀 Building Rust CLI..."
cargo build --release --features terminal --manifest-path grok-chat-app/Cargo.toml

# Start services
echo "🚀 Starting services with ${DOCKER_TYPE}..."
${COMPOSE_CMD} -f ${COMPOSE_FILE} up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Access Points:"
echo "   • Grok Chat: http://localhost:8000"
echo "   • Workflow Builder: http://localhost:8000/workflows"
echo "   • n8n Dashboard: http://localhost:5678"
echo "   • n8n Credentials: admin / changeme (change in .env)"
echo ""
echo "📖 Quick Start:"
echo "   1. Open http://localhost:8000/workflows"
echo "   2. Describe your automation workflow"
echo "   3. Click 'Generate Workflow'"
echo "   4. View and activate in n8n dashboard"
echo ""
echo "📚 Documentation: See N8N_QUICKSTART.md for detailed guide"
echo ""
echo "🔍 View logs:"
echo "   ${COMPOSE_CMD} -f ${COMPOSE_FILE} logs -f webapp"
echo "   ${COMPOSE_CMD} -f ${COMPOSE_FILE} logs -f n8n"
echo ""
echo "🛑 Stop services:"
echo "   ${COMPOSE_CMD} -f ${COMPOSE_FILE} down"
echo ""

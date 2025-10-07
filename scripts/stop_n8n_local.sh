#!/usr/bin/env bash
set -euo pipefail

# Stop locally running n8n and webapp services

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "🛑 Stopping n8n Workflow Builder services..."

# Stop by PIDs if available
if [[ -f "${REPO_ROOT}/.n8n/n8n.pid" ]]; then
  N8N_PID=$(cat "${REPO_ROOT}/.n8n/n8n.pid")
  if ps -p ${N8N_PID} >/dev/null 2>&1; then
    echo "Stopping n8n (PID: ${N8N_PID})..."
    kill ${N8N_PID} 2>/dev/null || true
    sleep 2
    # Force kill if still running
    if ps -p ${N8N_PID} >/dev/null 2>&1; then
      kill -9 ${N8N_PID} 2>/dev/null || true
    fi
  fi
  rm -f "${REPO_ROOT}/.n8n/n8n.pid"
fi

if [[ -f "${REPO_ROOT}/.n8n/webapp.pid" ]]; then
  WEBAPP_PID=$(cat "${REPO_ROOT}/.n8n/webapp.pid")
  if ps -p ${WEBAPP_PID} >/dev/null 2>&1; then
    echo "Stopping webapp (PID: ${WEBAPP_PID})..."
    kill ${WEBAPP_PID} 2>/dev/null || true
    sleep 1
    if ps -p ${WEBAPP_PID} >/dev/null 2>&1; then
      kill -9 ${WEBAPP_PID} 2>/dev/null || true
    fi
  fi
  rm -f "${REPO_ROOT}/.n8n/webapp.pid"
fi

# Fallback: kill by port
if command -v lsof >/dev/null 2>&1; then
  for PORT in 5678 8000; do
    PIDS=$(lsof -ti:${PORT} 2>/dev/null || true)
    if [[ -n "${PIDS}" ]]; then
      echo "Killing remaining processes on port ${PORT}..."
      kill -9 ${PIDS} 2>/dev/null || true
    fi
  done
fi

echo "✅ Services stopped"
echo ""
echo "To restart: bash scripts/run_n8n_local.sh"

#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root (directory containing this script/..)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "${REPO_ROOT}"

echo "🔧 Ensuring required tools are available..."
command -v lsof >/dev/null || { echo "lsof not found; please install lsof"; exit 1; }

echo "🧹 Freeing ports (420, 3000) if occupied..."
for PORT in 420 3000; do
  PIDS="$(lsof -ti:"${PORT}" || true)"
  if [[ -n "${PIDS}" ]]; then
    echo "Killing processes on port ${PORT}: ${PIDS}"
    kill -9 ${PIDS} || true
  else
    echo "Port ${PORT} is free"
  fi
done

echo "🦀 Building Rust CLI (terminal feature)..."
cargo build --release --features terminal --manifest-path apps/chat/Cargo.toml

echo "🐍 Setting up Python virtual environment..."
VENV_DIR="${REPO_ROOT}/.venv"
if [[ ! -d "${VENV_DIR}" ]]; then
  python3 -m venv "${VENV_DIR}"
fi
source "${VENV_DIR}/bin/activate"
pip install --upgrade pip >/dev/null 2>&1 || true
pip install -r apps/web/requirements.txt

echo "🔐 Loading XAI_API_KEY from environment or .env file..."
if [[ -z "${XAI_API_KEY:-}" ]]; then
  if [[ -f "${REPO_ROOT}/apps/chat/.env" ]]; then
    # shellcheck disable=SC2046
    export $(grep -E '^XAI_API_KEY=' "${REPO_ROOT}/apps/chat/.env" | sed 's/[[:space:]]//g') || true
  fi
fi

if [[ -z "${XAI_API_KEY:-}" ]]; then
  echo "❌ XAI_API_KEY not set. Please set it in environment or apps/chat/.env"
  exit 1
fi

echo "🚀 Starting Grok Chat Web App (FastAPI) on http://127.0.0.1:420 ..."
echo "   Using API Key: ${XAI_API_KEY:0:10}..."

# Start server (foreground)
exec python -m uvicorn app.main:app --app-dir apps/web --host 0.0.0.0 --port 420 --reload

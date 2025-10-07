#!/usr/bin/env bash
set -euo pipefail

cd /Users/dylanckawalec/Desktop/developer/opgrok

# Load environment variables
if [[ -f .env ]]; then
    export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)
fi

# Activate venv
source .venv/bin/activate

# Start webapp
exec python -m uvicorn webapp.app.main:app --host 0.0.0.0 --port 8000 --reload

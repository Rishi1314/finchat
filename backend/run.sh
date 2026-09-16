#!/usr/bin/env bash
set -euo pipefail

# run.sh — setup venv, install deps (if needed), load .env, and start Uvicorn
# Usage: from project root or from backend/ folder: ./backend/run.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Prefer venv at project root (.venv) then backend/.venv
if [ -f "$PROJECT_ROOT/.venv/bin/activate" ]; then
	VENV_ACT="$PROJECT_ROOT/.venv/bin/activate"
elif [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
	VENV_ACT="$SCRIPT_DIR/.venv/bin/activate"
else
	echo "No virtualenv found. Creating .venv in project root ($PROJECT_ROOT/.venv)..."
	python3 -m venv "$PROJECT_ROOT/.venv"
	VENV_ACT="$PROJECT_ROOT/.venv/bin/activate"
fi

# shellcheck source=/dev/null
. "$VENV_ACT"

# Install requirements if uvicorn not available in the venv
if ! command -v uvicorn >/dev/null 2>&1; then
	echo "Installing Python requirements..."
	pip install -r "$PROJECT_ROOT/requirements.txt"
fi

# Load environment variables from backend/.env if present
if [ -f "$SCRIPT_DIR/.env" ]; then
	set -a
	# shellcheck disable=SC1090
	. "$SCRIPT_DIR/.env"
	set +a
fi

echo "Starting Uvicorn (app: app.main:app) on 127.0.0.1:8000..."
exec uvicorn app.main:app --reload --host 127.0.0.1 --port 8000


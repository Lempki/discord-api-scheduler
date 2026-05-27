#!/usr/bin/env bash
set -e

trap 'echo; echo "ERROR: Setup failed (line $LINENO). Press Enter to close..."; read -r _' ERR

echo "=== discord-api-scheduler setup ==="
echo

# Create virtual environment if it doesn't already exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists, skipping creation."
fi

# Upgrade pip
echo "Upgrading pip..."
.venv/bin/python -m pip install --upgrade pip --quiet

# Install package with dev extras (editable)
echo "Installing package and dev dependencies..."
.venv/bin/python -m pip install -e ".[dev]"

# Copy .env.template to .env if .env doesn't exist yet
if [ ! -f ".env" ]; then
    cp .env.template .env
    echo "Created .env from .env.template"
    echo "  > Edit .env and set DISCORD_API_SECRET before running the API."
else
    echo ".env already exists, skipping."
fi

echo
echo "Setup complete!"
echo "  Activate venv : source .venv/bin/activate"
echo "  Run the API   : .venv/bin/python -m uvicorn scheduler_api.main:app --reload"
echo "  Run tests     : .venv/bin/python -m pytest"
echo
read -rp "Press Enter to close..."

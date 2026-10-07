#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv > /dev/null 2>&1; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source "$HOME/.local/bin/env"
fi

uv sync --group dev

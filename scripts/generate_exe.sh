#!/usr/bin/env bash
set -euo pipefail
uv run pyinstaller ./potemkeys.spec

#!/usr/bin/env bash
set -euo pipefail

# Phase 3: The Temple (Local Forge)
# Starts a local Gitea instance to serve the Void.

GITEA_HOME="$HOME/void/gitea"
mkdir -p "$GITEA_HOME"

if ! command -v gitea >/dev/null 2>&1; then
  echo "gitea is not installed. Install via brew bundle first."
  exit 1
fi

echo "Starting local Gitea..."

export GITEA_WORK_DIR="$GITEA_HOME"
nohup gitea web > "$GITEA_HOME/gitea.log" 2>&1 &

echo "Temple is open at http://localhost:3000"

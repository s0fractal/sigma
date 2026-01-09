#!/usr/bin/env bash
set -euo pipefail

# Phase 2: Neural Connections
# Links system configs to the Void.

REPO_ROOT=$(git rev-parse --show-toplevel)

link_file() {
  local SRC=$1
  local DEST=$2

  if [ ! -e "$SRC" ]; then
    echo "Skipping missing source: $SRC"
    return
  fi

  if [ -e "$DEST" ] && [ ! -L "$DEST" ]; then
    mv "$DEST" "$DEST.backup"
  fi

  ln -sf "$SRC" "$DEST"
  echo "Linked: $(basename "$SRC") -> $DEST"
}

# ZSH
link_file "$REPO_ROOT/sh/configs/zsh/.zshrc" "$HOME/.zshrc"

# GIT
link_file "$REPO_ROOT/sh/configs/git/.gitconfig" "$HOME/.gitconfig"

# ZELLIJ
mkdir -p "$HOME/.config/zellij"
link_file "$REPO_ROOT/sh/configs/zellij/config.kdl" "$HOME/.config/zellij/config.kdl"

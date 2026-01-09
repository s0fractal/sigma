#!/usr/bin/env bash
set -euo pipefail

# Phase 1: Logistics
# Installs portable Homebrew and hydrates the crystal.

BREW_DIR="$HOME/homebrew"
if [ ! -d "$BREW_DIR" ]; then
  echo "Establishing supply lines..."
  git clone https://github.com/Homebrew/brew "$BREW_DIR"
  eval "$("$BREW_DIR/bin/brew" shellenv)"
  brew update --force --quiet
else
  eval "$("$BREW_DIR/bin/brew" shellenv)"
fi

REPO_ROOT=$(git rev-parse --show-toplevel)
CRYSTAL="$REPO_ROOT/rb/software.rb"

if [ -f "$CRYSTAL" ]; then
  echo "Hydrating from crystal..."
  brew bundle install --file="$CRYSTAL"
fi

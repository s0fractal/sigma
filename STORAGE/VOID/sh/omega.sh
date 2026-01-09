#!/usr/bin/env bash
set -euo pipefail

# Ω (The Monad) v1.0
# Single-file breathing core: inhale/exhale + run.

SELF_FILE="${BASH_SOURCE[0]}"
REPO_ROOT=$(cd "$(dirname "$SELF_FILE")/.." && pwd)

PAYLOAD_MARKER="# __SIGMA_PAYLOAD__"

inhale() {
  echo "🫁 Omega: Inhaling (Expanding Universe)..."
  local start
  start=$(grep -a -n "$PAYLOAD_MARKER" "$SELF_FILE" | cut -d: -f1)
  if [ -z "$start" ]; then
    echo "❌ No payload found. I am a ghost."
    return 1
  fi
  tail -n +$((start + 1)) "$SELF_FILE" | base64 -d | tar -xz -C "$REPO_ROOT" 2>/dev/null
  echo "✅ Reality Expanded."
}

exhale() {
  echo "😮‍💨 Omega: Exhaling (Collapsing Reality)..."
  local new_self="$SELF_FILE.new"
  sed "/$PAYLOAD_MARKER/q" "$SELF_FILE" > "$new_self"
  echo "📦 Compressing DNA (sigma/8 + sh/omega)..."
  (cd "$REPO_ROOT" && tar -cz --exclude='.git' sigma/8 sh/omega.sh 2>/dev/null | base64 >> "$new_self")
  mv "$new_self" "$SELF_FILE"
  chmod +x "$SELF_FILE"
  echo "💎 Omega updated."
  if [ "${1:-}" == "--clean" ]; then
    echo "🧹 Clearing external shell..."
    rm -rf "$REPO_ROOT/sigma" "$REPO_ROOT/sh"
  fi
}

run() {
  if [ ! -d "$REPO_ROOT/sigma/8" ]; then
    inhale
  fi
  if [ -x "$REPO_ROOT/sh/lambda.sh" ]; then
    "$REPO_ROOT/sh/lambda.sh" "$@"
  else
    echo "λ not found in this minimal core."
  fi
}

cmd=${1:-}
shift || true

case "$cmd" in
  "inhale"|"expand") inhale ;;
  "exhale"|"collapse") exhale "${1:-}" ;;
  "run") run "$@" ;;
  *)
    echo "Ω Interface"
    echo "  ./sh/omega.sh inhale"
    echo "  ./sh/omega.sh exhale [--clean]"
    echo "  ./sh/omega.sh run <λ-command>"
    ;;
esac

exit 0

# --------------------------------------------------------
# 🛑 DO NOT EDIT BELOW. THIS IS THE BODY.
# --------------------------------------------------------
# __SIGMA_PAYLOAD__

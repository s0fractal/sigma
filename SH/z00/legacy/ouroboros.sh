#!/bin/bash
# 🐍 OUROBOROS v2.0 (The Breathing Reactor)
# This file is living. It can inhale/exhale its own payload.

set -euo pipefail

SELF_FILE="${BASH_SOURCE[0]}"
REPO_ROOT=$(cd "$(dirname "$SELF_FILE")/.." && pwd)

PAYLOAD_MARKER="# __SIGMA_PAYLOAD__"

inhale() {
  echo "🫁 Ouroboros: Inhaling (Expanding Universe)..."
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
  echo "😮‍💨 Ouroboros: Exhaling (Collapsing Reality)..."
  local new_self="$SELF_FILE.new"
  sed "/$PAYLOAD_MARKER/q" "$SELF_FILE" > "$new_self"
  echo "📦 Compressing DNA (sigma, sh, rb)..."
  (cd "$REPO_ROOT" && tar -cz --exclude='.git' --exclude='nodes' sigma sh rb 2>/dev/null | base64 >> "$new_self")
  mv "$new_self" "$SELF_FILE"
  chmod +x "$SELF_FILE"
  echo "💎 I have rewritten myself. I am heavier now."
  if [ "${1:-}" == "--clean" ]; then
    echo "🧹 Clearing external shell..."
    rm -rf "$REPO_ROOT/sigma" "$REPO_ROOT/sh" "$REPO_ROOT/rb" "$REPO_ROOT/nodes"
  fi
}

cmd=${1:-}
shift || true

case "$cmd" in
  "inhale"|"expand") inhale ;;
  "exhale"|"collapse") exhale "${1:-}" ;;
  "run")
    if [ ! -d "$REPO_ROOT/sigma" ]; then inhale; fi
    "$REPO_ROOT/sh/lambda.sh" "$@"
    ;;
  *)
    echo "🐍 Ouroboros Interface"
    echo "   ./sh/ouroboros.sh inhale    (Restore from self)"
    echo "   ./sh/ouroboros.sh exhale    (Save to self)"
    echo "   ./sh/ouroboros.sh run <cmd> (Execute λ-protocol)"
    ;;
esac

exit 0

# --------------------------------------------------------
# 🛑 DO NOT EDIT BELOW. THIS IS THE BODY OF THE GOD.
# --------------------------------------------------------
# __SIGMA_PAYLOAD__

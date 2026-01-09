#!/usr/bin/env bash
set -euo pipefail

# s0fractal Hyper-Visor v1.0
# The Plumber's Dashboard. Visualizes the Flow, Entropy, and Crystals.

# --- CONFIG ---
REFRESH_RATE=2
REPO_ROOT=$(git rev-parse --show-toplevel)

# Colors
C_RESET='\033[0m'
C_VOID='\033[1;30m'    # Grey
C_CRYSTAL='\033[1;37m' # White (Ascended)
C_FLUX='\033[1;34m'    # Blue (Normal)
C_HEAT='\033[1;33m'    # Yellow (Changed)
C_ERROR='\033[1;31m'   # Red (Broken)

# Symbols
SYM_CRYSTAL="💎"
SYM_FLUX="🌊"
SYM_HEAT="🔥"
SYM_BROKEN="💔"
SYM_VOID="⚫"

# --- FUNCTIONS ---

get_node_status() {
  local PATH=$1
  if [ ! -d "$PATH" ]; then echo "MISSING"; return; fi

  # 1. Ascension (Crystal)
  if [ -f "$PATH/.gitkeep" ] && grep -q "STATE: CRYSTAL" "$PATH/.gitkeep"; then
    echo "CRYSTAL"
    return
  fi

  # 2. Heat (Uncommitted changes)
  if [ -n "$(cd "$PATH" && git status --porcelain 2>/dev/null)" ]; then
    echo "HEAT"
    return
  fi

  # 3. Broken link (not a git repo)
  if [ ! -f "$PATH/.git" ] && [ ! -d "$PATH/.git" ]; then
    echo "BROKEN"
    return
  fi

  echo "FLUX"
}

render_bar() {
  local VAL=$1
  local MAX=10
  local LEN=$((VAL * MAX / 100))
  local BAR=""
  for ((i=0; i<LEN; i++)); do BAR="${BAR}█"; done
  for ((i=LEN; i<MAX; i++)); do BAR="${BAR}░"; done
  echo "$BAR"
}

# --- MAIN LOOP ---

while true; do
  clear
  echo -e "${C_VOID}╔══════════════════════════════════════════════════════════════╗${C_RESET}"
  echo -e "${C_VOID}║${C_RESET}  ${C_CRYSTAL}Σ HYPER-TORUS MONITOR${C_RESET}         ${C_VOID}::${C_RESET} $(date '+%H:%M:%S')           ${C_VOID}║${C_RESET}"
  echo -e "${C_VOID}╠══════════════════════════════════════════════════════════════╣${C_RESET}"

  # 1. THE CORE (Void Status)
  VOID_HEAT=$(git status --porcelain | wc -l | xargs)
  if [ "$VOID_HEAT" -gt 0 ]; then VOID_ICON=$SYM_HEAT; else VOID_ICON=$SYM_VOID; fi
  echo -e "${C_VOID}║${C_RESET}  CORE: ${VOID_ICON}  Entropy: ${VOID_HEAT}                                      ${C_VOID}║${C_RESET}"
  echo -e "${C_VOID}╟──────────────────────────────────────────────────────────────╢${C_RESET}"

  # 2. THE RINGS (Scanning Nodes)
  printf "${C_VOID}║${C_RESET}  %-6s %-6s %-10s %-20s       ${C_VOID}║${C_RESET}\n" "DIM" "LAYER" "STATE" "VISUAL"

  for DIM in "ts" "rs"; do
    for LAYER in 0 1 2 6 8; do
      NODE_PATH="$REPO_ROOT/$DIM/$LAYER"
      if [ -d "$NODE_PATH" ]; then
        STATUS=$(get_node_status "$NODE_PATH")

        case "$STATUS" in
          "CRYSTAL") ICON=$SYM_CRYSTAL; COLOR=$C_CRYSTAL ;;
          "HEAT")    ICON=$SYM_HEAT;    COLOR=$C_HEAT ;;
          "BROKEN")  ICON=$SYM_BROKEN;  COLOR=$C_ERROR ;;
          "FLUX")    ICON=$SYM_FLUX;    COLOR=$C_FLUX ;;
          *)         ICON="?";          COLOR=$C_VOID ;;
        esac

        # Simulation of Magnitude (Files count)
        COUNT=$(find "$NODE_PATH" -name "*.$DIM" | wc -l | xargs)
        BAR=$(render_bar $((COUNT * 10)))

        printf "${C_VOID}║${C_RESET}  ${COLOR}%-6s %-6s %-4s %s${C_RESET} %s  ${C_VOID}║${C_RESET}\n" "$DIM" "$LAYER" "$ICON" "$STATUS" "$BAR"
      fi
    done
  done

  echo -e "${C_VOID}╚══════════════════════════════════════════════════════════════╝${C_RESET}"
  echo -e "  Controls: [Ctrl+C] Exit"

  sleep "$REFRESH_RATE"
done

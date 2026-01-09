#!/usr/bin/env bash
set -euo pipefail

# s0fractal Vision v1.0
# Generates a vector snapshot of the system state (retina.svg)

REPO_ROOT=$(git rev-parse --show-toplevel)
OUTPUT_FILE="$REPO_ROOT/retina.svg"
source "$REPO_ROOT/sh/tensor.sh"

echo "🧿 Generating Retina Snapshot..."

cat << EOF > "$OUTPUT_FILE"
<svg width="800" height="800" viewBox="-400 -400 800 800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
      <feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      text { font-family: monospace; font-size: 12px; fill: white; text-anchor: middle; }
      .orbit { fill: none; stroke-width: 1; opacity: 0.5; }
      .node { stroke: none; }
      .void { fill: #111; stroke: #333; }
    </style>
  </defs>

  <rect x="-400" y="-400" width="800" height="800" fill="#050505" />
  <circle cx="0" cy="0" r="30" class="void" />
  <text x="0" y="5" font-size="20">Σ</text>
EOF

for LAYER in {0..6}; do
  RADIUS=$((50 + LAYER * 50))
  echo "  <circle cx='0' cy='0' r='$RADIUS' stroke='#333' class='orbit' />" >> "$OUTPUT_FILE"

  for DIM in "${ALL_DIMS[@]}"; do
    if [[ "$DIM" == "sh" || "$DIM" == "rb" ]]; then continue; fi

    case "$DIM" in
      "ts") ANGLE=0 ;;
      "rs") ANGLE=120 ;;
      "sigma") ANGLE=240 ;;
      *) ANGLE=$((ANGLE + 45)) ;;
    esac

    RAD_ANGLE=$(echo "$ANGLE * 3.14159 / 180" | bc -l)
    CX=$(echo "$RADIUS * c($RAD_ANGLE)" | bc -l)
    CY=$(echo "$RADIUS * s($RAD_ANGLE)" | bc -l)

    NODE_PATH="$REPO_ROOT/$DIM/$LAYER"
    COLOR=$(get_color "$DIM")
    case "$COLOR" in
      *34m) HEX="#3388FF" ;;
      *31m) HEX="#FF4433" ;;
      *35m) HEX="#CC00FF" ;;
      *) HEX="#666666" ;;
    esac

    OPACITY="0.3"
    FILTER=""
    if [ -d "$NODE_PATH" ]; then
      OPACITY="1.0"
      if [ -n "$(cd "$NODE_PATH" 2>/dev/null && git status --porcelain)" ]; then
        FILTER="filter='url(#glow)'"
        HEX="#FFFF00"
      fi
    fi

    echo "  <circle cx='$CX' cy='$CY' r='10' fill='$HEX' opacity='$OPACITY' $FILTER class='node' />" >> "$OUTPUT_FILE"
    if [ "$OPACITY" == "1.0" ]; then
      echo "  <line x1='0' y1='0' x2='$CX' y2='$CY' stroke='$HEX' stroke-width='1' opacity='0.2' />" >> "$OUTPUT_FILE"
      echo "  <text x='$CX' y='$((CY + 20))'>$DIM-$LAYER</text>" >> "$OUTPUT_FILE"
    fi
  done
done

echo "</svg>" >> "$OUTPUT_FILE"

echo "✅ Retina snapshot created: retina.svg"
open "$OUTPUT_FILE" 2>/dev/null || xdg-open "$OUTPUT_FILE" 2>/dev/null || true

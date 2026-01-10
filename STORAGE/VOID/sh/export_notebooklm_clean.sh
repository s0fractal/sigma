#!/usr/bin/env bash
set -euo pipefail

# SIGMA Export: All domains (LAW, CORE, CLI, RUNTIME, SENSE, STORAGE)

REPO_ROOT=$(git rev-parse --show-toplevel)
OUT_DIR="$REPO_ROOT/exports"
OUT_FILE="$OUT_DIR/sigma_prime_digest.txt"

mkdir -p "$OUT_DIR"

echo "Σ-GLYPH PRIME DIGEST" > "$OUT_FILE"
echo "Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$OUT_FILE"
echo "Scope: Entire Architecture" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

# Collect files from all core directories
files=()
while IFS= read -r f; do files+=("$f"); done < <(rg --files \
  -g "*.{md,sigma,ts,py,sh,json,rs,rb,dna,lean,yml,txt,kdl}" \
  -g "!**/node_modules/**" \
  -g "!**/.git/**" \
  -g "!**/exports/**" \
  -g "!**/__pycache__/**" \
  "$REPO_ROOT")

printf "%s\n" "${files[@]}" | sort -u | while read -r file; do
  [ -f "$file" ] || continue
  echo "----- FILE: ${file#$REPO_ROOT/} -----" >> "$OUT_FILE"
  cat "$file" >> "$OUT_FILE"
  echo -e "\n" >> "$OUT_FILE"
done

echo "OK: $OUT_FILE"

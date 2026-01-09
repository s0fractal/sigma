#!/usr/bin/env bash
set -euo pipefail

# Clean export: all sigma only

REPO_ROOT=$(git rev-parse --show-toplevel)
OUT_DIR="$REPO_ROOT/exports"
OUT_FILE="$OUT_DIR/notebooklm_clean.txt"

mkdir -p "$OUT_DIR"

echo "Σ NOTEBOOKLM CLEAN EXPORT" > "$OUT_FILE"
echo "Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

files=()
while IFS= read -r f; do files+=("$f"); done < <(rg --files -g "sigma/**" "$REPO_ROOT")

printf "%s\n" "${files[@]}" | sort -u | while read -r file; do
  [ -f "$file" ] || continue
  echo "----- FILE: ${file#$REPO_ROOT/} -----" >> "$OUT_FILE"
  cat "$file" >> "$OUT_FILE"
  echo "" >> "$OUT_FILE"
done

echo "OK: $OUT_FILE"

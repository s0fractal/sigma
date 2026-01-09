#!/usr/bin/env bash
set -euo pipefail

# Exports project knowledge into a single text file for NotebookLM.

REPO_ROOT=$(git rev-parse --show-toplevel)
OUT_DIR="$REPO_ROOT/exports"
OUT_FILE="$OUT_DIR/notebooklm.txt"

mkdir -p "$OUT_DIR"

echo "Σ NOTEBOOKLM EXPORT" > "$OUT_FILE"
echo "Generated: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

collect_files() {
  local pattern=$1
  rg --files -g "$pattern" "$REPO_ROOT"
}

{
  collect_files "sigma/**" 
  collect_files "sh/**/*.sh"
  collect_files "sh/*.sh"
} | sort -u | while read -r file; do
  [ -f "$file" ] || continue
  echo "----- FILE: ${file#$REPO_ROOT/} -----" >> "$OUT_FILE"
  cat "$file" >> "$OUT_FILE"
  echo "" >> "$OUT_FILE"
done

echo "OK: $OUT_FILE"

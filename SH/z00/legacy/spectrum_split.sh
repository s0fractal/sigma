#!/usr/bin/env bash
set -euo pipefail

# Split sigma/matrix.sigma into sigma/spectrum/*.sigma files.

REPO_ROOT=$(git rev-parse --show-toplevel)
MATRIX_FILE="$REPO_ROOT/sigma/matrix.sigma"
OUT_DIR="$REPO_ROOT/sigma/spectrum"

if [ ! -f "$MATRIX_FILE" ]; then
  echo "matrix.sigma not found"
  exit 1
fi

mkdir -p "$OUT_DIR"

python3 - <<'PY'
import re
from pathlib import Path

root = Path.cwd()
matrix = root / "sigma" / "matrix.sigma"
out_dir = root / "sigma" / "spectrum"
out_dir.mkdir(exist_ok=True)

lines = matrix.read_text().splitlines()

rows = []
for line in lines:
    if line.startswith("###"):
        break
    if "|" not in line:
        continue
    if line.strip().startswith("---") or line.strip().startswith("ID"):
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 10:
        continue
    rows.append(parts)

def q(v):
    return "'" + v.replace("'", "''") + "'"

for parts in rows:
    id_, typ, path, hex_, syntax, mute, lift, mass, entropy, imp = parts[:10]
    if not id_:
        continue
    fm = [
        "---",
        f"GLYPH: {id_}",
        f"TYPE: {typ}",
        f"PATH: {q(path)}",
        f"HEX: {q(hex_)}",
        f"SYNTAX: {syntax}",
        f"MUTE: {q(mute)}",
        f"LIFT: {q(lift)}",
        f"🪨MASS: {mass}",
        f"🌀ENTROPY: {entropy}",
        f"IMPORT: {q(imp)}",
        "---",
        "",
        f"# Spectrum: {id_}",
        "",
        "Derived from matrix.sigma.",
        "",
    ]
    (out_dir / f"{id_}.sigma").write_text("\n".join(fm))
PY

echo "OK: $OUT_DIR"

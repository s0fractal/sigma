#!/usr/bin/env python3
import os
from pathlib import Path

# Σ-GLYPH EXPORTER: Universal Archival Engine
# V1.0.0 - Export sigma/ and PY/ for cross-model consultation

SIGMA_ROOT = Path("/Users/s0fractal/SIGMA")
EXPORT_FILE = SIGMA_ROOT / "sigma_full_codebase.txt"

def export():
    print(f"--- Exporting Σ-GLYPH Codebase to {EXPORT_FILE.name} ---")
    
    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        # 1. Export sigma/
        f.write("# === DIMENSION: SIGMA (Intents & Seeds) ===\n\n")
        sigma_dir = SIGMA_ROOT / "sigma"
        for path in sorted(sigma_dir.rglob("*.sigma")):
            rel_path = path.relative_to(SIGMA_ROOT)
            f.write(f"## FILE: {rel_path}\n")
            f.write("```sigma\n")
            f.write(path.read_text(encoding="utf-8"))
            f.write("\n```\n\n")
            
        # 2. Export PY/z00 (Engines)
        f.write("# === DIMENSION: PY (Python Engines & Tools) ===\n\n")
        py_dir = SIGMA_ROOT / "PY/z00"
        for path in sorted(py_dir.glob("*.py")):
            rel_path = path.relative_to(SIGMA_ROOT)
            f.write(f"## FILE: {rel_path}\n")
            f.write("```python\n")
            f.write(path.read_text(encoding="utf-8"))
            f.write("\n```\n\n")

    print(f"✅ Export Complete. Volume materialized at: {EXPORT_FILE}")

if __name__ == "__main__":
    export()

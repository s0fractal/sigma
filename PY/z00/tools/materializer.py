#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Σ-GLYPH MATERIALIZER: Unfolding DNA into Spectrums
# Version: V1.0.0

def repo_root() -> Path:
    cur = Path.cwd()
    for parent in [cur] + list(cur.parents):
        if (parent / ".git").exists():
            return parent
    return cur

# --- CONFIGURATION ---
SIGMA_ROOT = Path("/Users/s0fractal/SIGMA")
SOURCE_DIR = SIGMA_ROOT / "sigma"

TAG_MAP = {
    "md": (SIGMA_ROOT / "MD", ".md"),
    "ts": (SIGMA_ROOT / "TS", ".ts"),
    "rs": (SIGMA_ROOT / "RS", ".rs"),
    "dna": (SIGMA_ROOT / "DNA", ".dna"),
    "sh": (SIGMA_ROOT / "SH", ".sh"),
    "rb": (SIGMA_ROOT / "RB", ".rb"),
    "py": (SIGMA_ROOT / "PY", ".py"),
    "json": (SIGMA_ROOT / "JSON", ".json"),
    "glyph": (SIGMA_ROOT / "GLYPH", ".glyph"),
}

# --- EXTRACTION ---
def extract_block(text: str, tag: str) -> str | None:
    # Pattern to match @[tag] followed by optional backticks and content
    # Handles both @[tag] and @[tag]\n```lang\ncontent\n```
    pattern = re.compile(rf"@\[{re.escape(tag)}\]\n(?:```\w*\n)?(.*?)(?:\n```)?(?=\n@\[|\Z)", re.DOTALL)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

import sys

def main():
    print("=== Σ-GLYPH MATERIALIZER: Initiating Unfolding Cycle ===\n")

    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} not found.")
        return

    # Check for tag filtering
    target_tags = sys.argv[1:] if len(sys.argv) > 1 else TAG_MAP.keys()
    print(f"Targeting Spectrum(s): {', '.join(target_tags)}\n")

    # Scan for .sigma files in sigma/ (our SSOT)
    for path in SOURCE_DIR.glob("**/*.sigma"):
        rel_path = path.relative_to(SOURCE_DIR)
        
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"   ❌ Error reading {rel_path}: {e}")
            continue
        
        materialized_any = False
        for tag in target_tags:
            if tag not in TAG_MAP:
                continue
            
            target_base, ext = TAG_MAP[tag]
            block = extract_block(content, tag)
            if block:
                if not materialized_any:
                    print(f"🧬 Materializing: {rel_path}")
                    materialized_any = True
                
                # Target path keeps the relative structure but changes extension
                target_path = target_base / rel_path.with_suffix(ext)
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Write the projection
                try:
                    target_path.write_text(block + "\n", encoding="utf-8")
                    print(f"   -> Projected [{tag}]: {target_path.relative_to(SIGMA_ROOT)}")
                except Exception as e:
                    print(f"   ❌ Error projecting [{tag}] to {target_path}: {e}")

    print("\n--- Materialization Complete. The Hologram is Synchronized. ---")

if __name__ == "__main__":
    main()

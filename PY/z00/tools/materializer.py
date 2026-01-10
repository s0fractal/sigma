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
MD_DIR = SIGMA_ROOT / "MD"
TS_DIR = SIGMA_ROOT / "TS"
RS_DIR = SIGMA_ROOT / "RS"
DNA_DIR = SIGMA_ROOT / "DNA"

TAG_MAP = {
    "md": (MD_DIR, ".md"),
    "ts": (TS_DIR, ".ts"),
    "rs": (RS_DIR, ".rs"),
    "dna": (DNA_DIR, ".dna"),
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

def main():
    print("=== Σ-GLYPH MATERIALIZER: Initiating Unfolding Cycle ===\n")

    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} not found.")
        return

    # Scan for .sigma files in sigma/ (our SSOT)
    for path in SOURCE_DIR.glob("**/*.sigma"):
        rel_path = path.relative_to(SOURCE_DIR)
        print(f"🧬 Materializing: {rel_path}")
        
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"   ❌ Error reading {rel_path}: {e}")
            continue
        
        for tag, (target_base, ext) in TAG_MAP.items():
            block = extract_block(content, tag)
            if block:
                # Target path keeps the relative structure but changes extension
                # e.g. sigma/laws/TopologicalCanon.sigma -> DNA/laws/TopologicalCanon.dna
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

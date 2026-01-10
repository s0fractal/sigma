#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Σ-GLYPH MATERIALIZER: Unfolding DNA into Spectrums
# Version: V1.1.0 (Self-Anchored)

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
    # Match starting @[tag]
    start_marker = f"@[{tag}]\n"
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return None
    
    # Text starting after the tag marker
    remaining = text[start_idx + len(start_marker):]
    
    # End marker: either the next @[tag] or the end of the file
    end_idx = remaining.find("\n@[")
    block = remaining[:end_idx] if end_idx != -1 else remaining
    
    # Cleanup markdown backticks if present
    content = block.strip()
    if content.startswith("```"):
        content = re.sub(r"^```\w*\n", "", content)
    if content.endswith("```"):
        content = content[:-3].strip()
        
    return content

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
        
        # Parse FOLDER tag if present
        folder_match = re.search(r"📁FOLDER:\s*(\w+)", content)
        folder = folder_match.group(1) if folder_match else None
        
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
                
                # If folder exists, we insert it into the projection path
                if folder:
                    target_path = target_base / rel_path.parent / folder / rel_path.with_suffix(ext).name
                else:
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

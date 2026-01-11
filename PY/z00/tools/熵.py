import os
import re
from pathlib import Path

SOURCE_DIR = Path("/Users/s0fractal/SIGMA/sigma")

STRATUM_TO_ENTROPY = {
    "z00": -1,
    "m00": 0,
    "m32": -32768,
    "m24": -24576,
    "m16": -16384,
    "m01": -16384,
    "m02": -8192,
    "p32": 32767,
    "p20": 20480,
    "p08": 8192,
}

def process_file(path: Path):
    try:
        content = path.read_text(encoding="utf-8")
    except: return

    # 1. Identify legacy stratum
    stratum_match = re.search(r"🪐STRATUM:\s*(\w+)", content)
    stratum = stratum_match.group(1) if stratum_match else None
    
    # 2. Check for existing numeric entropy
    has_entropy = False
    phys_match = re.search(r"⚖️PHYSICS:\s*\n((?:\s+[\w\W]+?:\s*[\-\dxA-F]+\n?)*)", content, re.MULTILINE)
    if phys_match:
        if "ENTROPY:" in phys_match.group(1):
             # check if it's numeric
             val_match = re.search(r"ENTROPY:\s*(-?\d+)", phys_match.group(1))
             if val_match:
                 has_entropy = True

    # 3. Determine target entropy if missing
    if not has_entropy:
        target_entropy = STRATUM_TO_ENTROPY.get(stratum, -32768)
        
        # If it's in a specific folder, use that as a hint
        if not stratum:
            if "z00" in str(path): target_entropy = -1
            elif "m16" in str(path): target_entropy = -16384
            elif "p32" in str(path): target_entropy = 32767
        
        # Add physics block if missing
        if not phys_match:
            # Find metadata section (between --- and ---)
            meta_match = re.search(r"---(.*?)---", content, re.DOTALL)
            if meta_match:
                physics_block = f"⚖️PHYSICS:\n  OP: 0\n  FLAGS: 1\n  PHASE: 0\n  AMPLITUDE: 65535\n  ENTROPY: {target_entropy}\n"
                content = content.replace("---", f"---\n{physics_block}", 1)
        else:
            # Update existing physics block with entropy
            # If entropy was a string like "Low", replace it
            block = phys_match.group(1)
            if "ENTROPY:" in block:
                new_block = re.sub(r"ENTROPY:\s*.*", f"ENTROPY: {target_entropy}", block)
                content = content.replace(block, new_block)
            else:
                 content = content.replace("⚖️PHYSICS:", f"⚖️PHYSICS:\n  ENTROPY: {target_entropy}")

    # 4. Remove 🪐STRATUM
    content = re.sub(r"🪐STRATUM:\s*\w+\n?", "", content)

    # Save
    path.write_text(content, encoding="utf-8")
    print(f"Processed: {path.relative_to(SOURCE_DIR)} (Entropy set/verified, Stratum purged)")

def main():
    print("=== Σ-GLYPH: ENTROPY PURGE INITIATED ===\n")
    for path in SOURCE_DIR.glob("**/*.sigma"):
        process_file(path)

if __name__ == "__main__":
    main()

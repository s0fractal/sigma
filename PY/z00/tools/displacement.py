import os
import re
from pathlib import Path

SOURCE_DIR = Path("/Users/s0fractal/SIGMA/sigma")

def parse_entropy(text):
    phys_match = re.search(r"⚖️PHYSICS:\s*\n((?:\s+[\w\W]+?:\s*[\-\dxA-F]+\n?)*)", text, re.MULTILINE)
    if phys_match:
        for line in phys_match.group(1).split("\n"):
            if "ENTROPY:" in line:
                val = line.split(":", 1)[1].strip()
                try:
                    return int(val)
                except: continue
    return -32768 # Default for m32

def entropy_to_stratum(entropy):
    if entropy == -1: return "z00"
    if entropy == 0: return "m00"
    prefix = "m" if entropy < 0 else "p"
    bucket = abs(entropy) // 1024
    return f"{prefix}{bucket:02}"

def main():
    print("=== Σ-GLYPH: EXECUTING DISPLACEMENT ===\n")
    for path in list(SOURCE_DIR.glob("**/*.sigma")):
        # Skip root artifacts
        if path.parent == SOURCE_DIR: continue
        
        try:
            content = path.read_text(encoding="utf-8")
        except: continue
        
        entropy = parse_entropy(content)
        stratum = entropy_to_stratum(entropy)
        
        target_dir = SOURCE_DIR / stratum
        target_path = target_dir / path.name
        
        if path != target_path:
            target_dir.mkdir(parents=True, exist_ok=True)
            print(f"Displacing {path.relative_to(SOURCE_DIR)} -> {stratum}/")
            os.rename(path, target_path)

    # Cleanup empty directories
    for root, dirs, _ in os.walk(SOURCE_DIR, topdown=False):
        for name in dirs:
            dir_path = Path(root) / name
            # Keep core strata
            if name in ["m00", "m16", "m24", "m32", "z00", "p32", "p31"]: continue
            if not any(dir_path.iterdir()):
                print(f"Removing empty directory: {dir_path.relative_to(SOURCE_DIR)}")
                os.rmdir(dir_path)

if __name__ == "__main__":
    main()

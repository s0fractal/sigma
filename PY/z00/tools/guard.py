#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# Σ-GLYPH ENTROPY GUARD
# V1.3.1 - Emoji Aware

SIGMA_ROOT = Path("/Users/s0fractal/SIGMA")
SOURCE_DIR = SIGMA_ROOT / "sigma"

def parse_physics(text: str) -> dict:
    physics = {"ENTROPY": -32768}
    phys_match = re.search(r"(?:⚖️)?PHYSICS:\s*\n((?:\s+[\w\W]+?:\s*[\-\dxA-F]+\n?)*)", text, re.MULTILINE)
    if phys_match:
        for line in phys_match.group(1).split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key = re.sub(r'[^\w]', '', key).strip()
                if "ENTROPY" in key.upper():
                    try:
                        physics["ENTROPY"] = int(val.strip())
                    except: continue
    return physics

def get_glyph_registry():
    registry = {}
    for path in SOURCE_DIR.glob("**/*.sigma"):
        try:
            content = path.read_text(encoding="utf-8")
            glyph_match = re.search(r"^GLYPH:\s*([\w=]+)", content, re.MULTILINE)
            if glyph_match:
                glyph = glyph_match.group(1)
                phys = parse_physics(content)
                dna_match = re.search(r"🧬DNA:\s*\n?((?:\s*-\s*[\w=]+\n?)+|(?:\s*[\w=]+\s*)+)", content)
                dependencies = []
                if dna_match:
                    raw_dna = dna_match.group(1)
                    dependencies = [d.strip("- ").strip() for d in raw_dna.split() if d.strip("- ").strip()]
                
                registry[glyph] = {
                    "path": path,
                    "entropy": phys["ENTROPY"],
                    "deps": dependencies
                }
        except: continue
    return registry

def audit_entropy(registry):
    violations = []
    print("🛡️  Auditing Entropy Hierarchy...")
    for glyph, data in registry.items():
        if data["entropy"] == -1: continue 
        for dep in data["deps"]:
            if dep not in registry: continue
            dep_data = registry[dep]
            if dep_data["entropy"] > data["entropy"]:
                rel_path = data["path"].relative_to(SOURCE_DIR)
                violations.append({
                    "src": glyph, "src_e": data["entropy"],
                    "dep": dep, "dep_e": dep_data["entropy"],
                    "path": rel_path
                })
    return violations

def main():
    registry = get_glyph_registry()
    violations = audit_entropy(registry)
    if not violations:
        print("\n✅ ENTROPY HIERARCHY: Pure. Stability is preserved.")
        sys.exit(0)
    print(f"\n❌ VIOLATION: Entropy Inversion Detected ({len(violations)})")
    for v in violations:
        print(f"   - {v['path']} ({v['src_e']}) -> imports {v['dep']} ({v['dep_e']})")
    sys.exit(1)

if __name__ == "__main__":
    main()

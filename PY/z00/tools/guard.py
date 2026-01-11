#!/usr/bin/env python3
import os
import re
import sys
import shutil
from pathlib import Path

# Σ-GLYPH GUARD
# V1.4.0: Entropy Hierarchy & Vector Topology

SIGMA_ROOT = Path("/Users/s0fractal/SIGMA")
SOURCE_DIR = SIGMA_ROOT / "sigma"
PROJECTION_DIRS = ["TS", "RS", "SH", "PY", "DNA", "GLYPH"]
WHITELIST = ["deno.json", ".DS_Store", "README.md"]

def parse_physics(text: str) -> dict:
    physics = {"ENTROPY": -32768}
    phys_match = re.search(r"(?:⚖️)?PHYSICS:\s*\n((?:\s+[\w\W]+?:\s*[\-\dxA-F]+\n?)*)", text, re.MULTILINE)
    if phys_match:
        for line in phys_match.group(1).split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key = re.sub(r'[^\w]', '', key).strip().upper()
                if "ENTROPY" in key:
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
                violations.append(f"Entropy Inversion: {rel_path} ({data['entropy']}) -> {dep} ({dep_data['entropy']})")
    return violations

def audit_vector_topology(fix=False):
    violations = []
    print("📐 Auditing Vector Topology...")
    
    for dim in PROJECTION_DIRS:
        dim_dir = SIGMA_ROOT / dim
        if not dim_dir.exists(): continue
        
        for item in dim_dir.iterdir():
            if item.name in WHITELIST: continue
            
            # Pattern: stratum (m00, p31, z00)
            if not re.match(r"^[mpz]\d{2}$", item.name):
                violations.append(f"Non-vector folder in {dim}/: {item.name}")
                if fix:
                    print(f"   🛠 Purging legacy dissonance: {item}")
                    if item.is_dir(): shutil.rmtree(item)
                    else: item.unlink()
    
    return violations

def main():
    fix_mode = "--fix" in sys.argv
    registry = get_glyph_registry()
    
    entropy_violations = audit_entropy(registry)
    vector_violations = audit_vector_topology(fix=fix_mode)
    
    violations = entropy_violations + vector_violations
    
    if not violations:
        print("\n✅ THE FIELD IS PURE. Hierarchy and Topology are synchronized.")
        sys.exit(0)
    
    print(f"\n❌ VIOLATIONS DETECTED ({len(violations)})")
    for v in violations:
        print(f"   - {v}")
    
    if not fix_mode:
        print("\n   [Tip]: Run with --fix to automatically purge legacy dissonance.")
    
    sys.exit(1)

if __name__ == "__main__":
    main()

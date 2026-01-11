#!/usr/bin/env python3
import os
import re
import sys
import shutil
import hashlib
from pathlib import Path

# Σ-GLYPH GUARD
# V1.5.0: Liquid Polish - Purging Dissonance

SIGMA_ROOT = Path("/Users/s0fractal/SIGMA")
SOURCE_DIR = SIGMA_ROOT / "sigma"
PROJECTION_DIRS = ["TS", "RS", "SH", "PY", "DNA", "GLYPH"]
WHITELIST = ["deno.json", ".DS_Store", "README.md", "pantheon"]

def parse_physics(text: str) -> dict:
    physics = {"OP": 0, "FLAGS": 0, "PHASE": 0, "AMPLITUDE": 0, "ENTROPY": 0}
    
    # V2.0 Symbolic Keys (Precise Search)
    symbol_map = {"⚙️": "OP", "🚩": "FLAGS", "🌊": "PHASE", "🔊": "AMPLITUDE", "🌀": "ENTROPY"}
    for sym, key in symbol_map.items():
        match = re.search(f"{sym}:?\\s*(-?\\d+|0x[a-fA-F0-9]+)", text)
        if match:
            val = match.group(1)
            try:
                physics[key] = int(val, 16) if val.startswith("0x") else int(val)
            except: continue

    # Fallback: Legacy PHYSICS block parsing
    if all(physics[k] == 0 for k in ["PHASE", "AMPLITUDE", "ENTROPY"]):
        header_match = re.search(r"(?:⚖️)?\s*PHYSICS(?:\s*\(Wave Function\))?:?\s*\n+", text, re.MULTILINE)
        if header_match:
            start_idx = header_match.end()
            remaining = text[start_idx:].lstrip("\n")
            found_any = False
            for line in remaining.split("\n"):
                clean_line = line.split("#")[0].strip()
                if not clean_line: continue
                if ":" in clean_line:
                    key, val = clean_line.split(":", 1)
                    key = re.sub(r'[^\w]', '', key).strip().upper()
                    if key in physics:
                        found_any = True
                        val = val.strip()
                        try:
                            if val.startswith("0x"): physics[key] = int(val, 16)
                            else: physics[key] = int(re.search(r'-?\d+', val).group())
                        except: continue
                    elif found_any: break
                else: break
    return physics

def calculate_checksum(content: str) -> str:
    if "\n🔒:" in content:
        clean_content = content.rsplit("\n🔒:", 1)[0].rstrip()
    elif "\nCHECKSUM:" in content:
        clean_content = content.rsplit("\nCHECKSUM:", 1)[0].rstrip()
    else:
        clean_content = content.strip()
    return hashlib.sha256(clean_content.encode("utf-8")).hexdigest()

def get_glyph_registry():
    registry = {}
    for path in SOURCE_DIR.glob("**/*.sigma"):
        try:
            content = path.read_text(encoding="utf-8")
            glyph_match = re.search(r"(?:GLYPH|Σ-GLYPH SEED|🧬):\s*([\w=]+)", content, re.MULTILINE)
            if glyph_match:
                glyph = glyph_match.group(1)
                phys = parse_physics(content)
                dna_match = re.search(r"(?:🧬DNA|DNA:|🔗|🔗:):\s*\n+((?:\s*(?:-\s*|Ref:\s*)?[\w=]+\n?)*)", content)
                dependencies = []
                if dna_match:
                    raw_dna = dna_match.group(1)
                    dependencies = [d.replace("Ref:", "").strip("- ").strip() for d in raw_dna.splitlines() if d.strip()]
                    if not dependencies:
                        dependencies = [d.strip("- ").strip() for d in raw_dna.split() if d.strip("- ").strip()]
                registry[glyph] = {
                    "path": path,
                    "entropy": phys["ENTROPY"],
                    "deps": dependencies,
                    "content": content
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
        for stratum_dir in dim_dir.iterdir():
            if stratum_dir.name in WHITELIST: continue
            if not re.match(r"^[mpz]\d{2}$", stratum_dir.name):
                violations.append(f"Non-vector folder in {dim}/: {stratum_dir.name}")
                if fix:
                    print(f"   🛠 Purging legacy dimension dissonance: {stratum_dir}")
                    if stratum_dir.is_dir(): shutil.rmtree(stratum_dir)
                    else: stratum_dir.unlink()
                continue
            
            # Sub-folder Audit: Deep Purge of legacy nested folders (like 'tools/')
            if stratum_dir.is_dir():
                for sub in stratum_dir.iterdir():
                    if sub.name in WHITELIST: continue
                    if sub.is_dir():
                        violations.append(f"Legacy nested folder in {dim}/{stratum_dir.name}/: {sub.name}")
                        if fix:
                            print(f"   🛠 Liquidating nested dissonance: {sub}")
                            shutil.rmtree(sub)

    # Dimensional Dissonance: Purging extra m00 in PY if z00 exists (for seeds)
    py_m00 = SIGMA_ROOT / "PY" / "m00"
    py_z00 = SIGMA_ROOT / "PY" / "z00"
    if py_m00.exists() and py_z00.exists():
        for item in py_m00.iterdir():
            if (py_z00 / item.name).exists():
                violations.append(f"Duplicate projection in PY/m00/: {item.name}")
                if fix:
                    print(f"   🛠 Purging duplicate: {item}")
                    if item.is_dir(): shutil.rmtree(item)
                    else: item.unlink()
    
    return violations

def audit_checksums(registry, fix=False):
    violations = []
    print("⚓ Auditing Physical Checksums...")
    for glyph, data in registry.items():
        path = data["path"]
        content = data["content"]
        checksum_match = re.search(r"\n(?:CHECKSUM|🔒):\s*(.*)$", content, re.MULTILINE)
        if not checksum_match: continue
        
        current_checksum = checksum_match.group(1).strip()
        expected_checksum = calculate_checksum(content)
        
        if current_checksum != expected_checksum:
            rel_path = path.relative_to(SOURCE_DIR)
            violations.append(f"Checksum Mismatch: {rel_path} (Expected {expected_checksum[:8]}...)")
            if fix:
                print(f"   🛠 Resealing Seed: {rel_path}")
                marker = "🔒:" if "\n🔒:" in content else "CHECKSUM:"
                parts = content.rsplit(f"\n{marker}", 1)
                new_content = parts[0] + f"\n{marker} {expected_checksum}"
                path.write_text(new_content, encoding="utf-8")
    return violations

def main():
    fix_mode = "--fix" in sys.argv
    registry = get_glyph_registry()
    entropy_violations = audit_entropy(registry)
    vector_violations = audit_vector_topology(fix=fix_mode)
    checksum_violations = audit_checksums(registry, fix=fix_mode)
    violations = entropy_violations + vector_violations + checksum_violations
    if not violations:
        print("\n✅ THE FIELD IS PURE. Hierarchy, Topology, and Checks are verified.")
        sys.exit(0)
    print(f"\n❌ VIOLATIONS DETECTED ({len(violations)})")
    for v in violations:
        print(f"   - {v}")
    if not fix_mode:
        print("\n   [Tip]: Run with --fix to automatically resolve violations.")
    sys.exit(1)

if __name__ == "__main__":
    main()

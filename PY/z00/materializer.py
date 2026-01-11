#!/usr/bin/env python3
import os
import re
import struct
import hashlib
import sys
import math
from pathlib import Path

# Σ-GLYPH MATERIALIZER: Atomic Fusion Engine
# V2.1.1 - Lossless Symbolic: Wave Cards, @[yaml] Config, Dipole Topology

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

# --- ATOMIC FUNCTIONS ---

def parse_physics(text: str) -> dict:
    physics = {"OP": 0, "FLAGS": 0, "PHASE": 0, "AMPLITUDE": 0, "ENTROPY": 0}
    
    # V2.1 Symbolic Keys (Precise Search - robust to comments)
    symbol_map = {"⚙️": "OP", "🚩": "FLAGS", "🌊": "PHASE", "🔊": "AMPLITUDE", "🌀": "ENTROPY"}
    for sym, key in symbol_map.items():
        match = re.search(f"{sym}:?\\s*(-?\\d+|0x[a-fA-F0-9]+)(?:\\s*#.*|$)", text, re.MULTILINE)
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

def get_identity(text: str, glyph_name: str) -> bytes:
    # V2.1 ⚛️ and 🧬
    atom_match = re.search(r"⚛️:\s*([a-fA-F0-9]{64})", text)
    if atom_match: return bytes.fromhex(atom_match.group(1))
    
    # Check for name-based lookup
    name_match = re.search(r"^🧬:\s*([\w=]+)", text, re.MULTILINE)
    if not name_match: name_match = re.search(r"🧬IDENTITY:\s*([a-fA-F0-9]{64})", text)
    
    if name_match and len(name_match.group(1)) == 64: return bytes.fromhex(name_match.group(1))

    # Legacy fallbacks
    atom_match = re.search(r"Atom:\s*([a-fA-F0-9]{64})", text)
    if atom_match: return bytes.fromhex(atom_match.group(1))

    # Search for first content block after Header if needed
    first_block_match = re.search(r"(?:@\[\w+\]\n|---.*?\n\n)(.*?)\n(?=@\[|🔒:|CHECKSUM:|$)", text, re.DOTALL)
    content = first_block_match.group(1).strip() if first_block_match else glyph_name
    return hashlib.sha256(content.encode("utf-8")).digest()

def entropy_to_stratum(entropy: int) -> str:
    if entropy == -1 or entropy == 0: return "z00"
    prefix = "m" if entropy < 0 else "p"
    # Dipole Topology: -32..+32 layers
    bucket = math.ceil(abs(entropy) / 1024)
    if bucket > 32: bucket = 32
    return f"{prefix}{int(bucket):02}"

def extract_block(text: str, tag: str) -> str | None:
    suppressed_marker = f"@[{tag}:doc]\n"
    if suppressed_marker in text: return None

    start_marker = f"@[{tag}]\n"
    start_idx = text.find(start_marker)
    if start_idx == -1: return None
    remaining = text[start_idx + len(start_marker):]
    # V2.1 Checksum symbol 🔒:
    end_match = re.search(r"\n@\[|\n+CHECKSUM:|\n+🔒:", remaining)
    block = remaining[:end_match.start()] if end_match else remaining
    content = block.strip()
    if content.startswith("```"):
        content = re.sub(r"^```[ \w]*\n", "", content)
    if content.endswith("```"):
        content = content[:-3].strip()
    return content

def main():
    print("=== Σ-GLYPH MATERIALIZER: Atomic Fusion V2.1.1 (Symbolic Standard) ===\n")
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} not found.")
        return

    glyph_registry = {}
    sigma_files = list(SOURCE_DIR.glob("**/*.sigma"))
    for path in sigma_files:
        try:
            content = path.read_text(encoding="utf-8")
            glyph_match = re.search(r"^(?:GLYPH|Σ-GLYPH SEED|🧬):\s*([\w=]+)", content, re.MULTILINE)
            if glyph_match:
                glyph_registry[glyph_match.group(1)] = path.relative_to(SOURCE_DIR)
        except: continue

    spectrum_templates = {}
    for glyph, rel_path in glyph_registry.items():
        if glyph in TAG_MAP:
            try:
                content = (SOURCE_DIR / rel_path).read_text(encoding="utf-8")
                # V2.1: Look inside @[yaml] block for IMPORT config
                yaml_block = extract_block(content, "yaml")
                if yaml_block:
                    match = re.search(r"IMPORT:\s*['\"]?(.*?)['\"]?$", yaml_block, re.MULTILINE)
                    if match:
                        spectrum_templates[glyph] = match.group(1).strip()
                else:
                    # Legacy fallback
                    match = re.search(r"IMPORT:\s*'(.*?)'", content)
                    if match: spectrum_templates[glyph] = match.group(1)
            except: continue

    for path in sigma_files:
        try: content = path.read_text(encoding="utf-8")
        except: continue
            
        phys = parse_physics(content)
        stratum = entropy_to_stratum(phys["ENTROPY"])
        glyph_match = re.search(r"^(?:GLYPH|Σ-GLYPH SEED|🧬):\s*([\w=]+)", content, re.MULTILINE)
        this_glyph = glyph_match.group(1) if glyph_match else path.stem
        
        dependencies = []
        dna_match = re.search(r"^(?:🧬DNA|DNA:|🔗|🔗:):\s*\n+((?:\s*(?:-\s*|Ref:\s*)?[\w=]+\n?)*)", content, re.MULTILINE)
        if dna_match:
            raw_dna = dna_match.group(1)
            dependencies = [d.replace("Ref:", "").strip("- ").strip() for d in raw_dna.splitlines() if d.strip("- ").strip()]
            if not dependencies:
                 dependencies = [d.strip("- ").strip() for d in raw_dna.split() if d.strip("- ").strip()]
        
        if not dependencies: # Inline DNA support
             dna_match = re.search(r"DNA:\s*([\w\s=]+)(?:\s*#|$)", content)
             if dna_match:
                 dependencies = dna_match.group(1).split()
        
        for tag, (out_dir, ext) in TAG_MAP.items():
            block = extract_block(content, tag)
            if block is not None:
                # V2.1: Path building
                glyph_fn = this_glyph if tag == "glyph" else path.stem
                target_path = out_dir / stratum / f"{glyph_fn}{ext}"
                
                # Spectral Fusion
                atoms = []
                for dep in dependencies:
                    if dep in glyph_registry:
                        try:
                            dep_content = (SOURCE_DIR / glyph_registry[dep]).read_text(encoding="utf-8")
                            atom_block = extract_block(dep_content, tag)
                            if atom_block: atoms.append(atom_block)
                        except: continue
                if atoms:
                    if block.startswith("#!"):
                        lines = block.split("\n")
                        block = lines[0] + "\n\n" + "\n".join(atoms) + "\n\n" + "\n".join(lines[1:])
                    else:
                        block = "\n".join(atoms) + "\n\n" + block

                if stratum != "z00" and tag in spectrum_templates:
                    template = spectrum_templates[tag]
                    imports = [template.replace("%n", d).replace("%p", str(glyph_registry[d].with_suffix("")).replace(".sigma", "").replace("rs" if tag=="rs" else "", "::" if tag=="rs" else "/")) 
                               for d in dependencies if d in glyph_registry and d != this_glyph]
                    if imports: block = "\n".join(imports) + "\n\n" + block

                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(block + "\n", encoding="utf-8")

    print("\n--- Materialization Complete. The Atomic Order is Established. ---")

if __name__ == "__main__":
    main()

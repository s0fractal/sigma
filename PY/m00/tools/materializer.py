#!/usr/bin/env python3
import os
import re
import struct
import hashlib
import sys
from pathlib import Path

# Σ-GLYPH MATERIALIZER: Unfolding DNA into Spectrums
# Version: V1.2.0 (Dynamic Equilibrium)

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

# --- HELPERS ---

def extract_block(text: str, tag: str) -> str | None:
    start_marker = f"@[{tag}]\n"
    start_idx = text.find(start_marker)
    if start_idx == -1: return None
    remaining = text[start_idx + len(start_marker):]
    end_idx = remaining.find("\n@[")
    block = remaining[:end_idx] if end_idx != -1 else remaining
    content = block.strip()
    if content.startswith("```"):
        content = re.sub(r"^```[ \w]*\n", "", content)
    if content.endswith("```"):
        content = content[:-3].strip()
    return content

def parse_physics(text: str) -> dict:
    physics = {"OP": 0, "FLAGS": 0, "PHASE": 0, "AMPLITUDE": 0, "ENTROPY": 0}
    # Match block even with varying whitespace
    phys_match = re.search(r"⚖️PHYSICS:\s*\n((?:\s+[\w\W]+?:\s*[\-\dxA-F]+\n?)*)", text, re.MULTILINE)
    if phys_match:
        block = phys_match.group(1)
        for line in block.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key, val = key.strip(), val.strip()
                try:
                    if val.startswith("0x"): physics[key] = int(val, 16)
                    else: physics[key] = int(val)
                except: continue
    return physics

def get_identity(text: str, glyph_name: str) -> bytes:
    id_match = re.search(r"🧬IDENTITY:\s*([a-fA-F0-9]{64})", text)
    if id_match: return bytes.fromhex(id_match.group(1))
    
    first_block_match = re.search(r"@\[\w+\]\n(.*?)\n(?=@\[|$)", text, re.DOTALL)
    content = first_block_match.group(1).strip() if first_block_match else glyph_name
    return hashlib.sha256(content.encode("utf-8")).digest()

def entropy_to_stratum(entropy: int) -> str:
    if entropy == -1: return "z00"
    if entropy == 0: return "m00"
    prefix = "m" if entropy < 0 else "p"
    bucket = abs(entropy) // 1024
    return f"{prefix}{bucket:02}"

# --- MAIN ---

def main():
    print("=== Σ-GLYPH MATERIALIZER: Initiating Unfolding Cycle (V1.2.0) ===\n")

    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} not found.")
        return

    # Pass 1: Build Registry
    glyph_registry = {}
    spectrum_templates = {}
    sigma_files = list(SOURCE_DIR.glob("**/*.sigma"))
    
    for path in sigma_files:
        rel_path = path.relative_to(SOURCE_DIR)
        try:
            content = path.read_text(encoding="utf-8")
            glyph_match = re.search(r"^GLYPH:\s*([\w=]+)", content, re.MULTILINE)
            if glyph_match:
                glyph_registry[glyph_match.group(1)] = rel_path
            if "🌈SPECTRUM" in content:
                import_match = re.search(r"^IMPORT:\s*'(.*)'", content, re.MULTILINE)
                dna_match = re.search(r"^🧬DNA:\s*(\w+)", content, re.MULTILINE)
                if import_match and dna_match:
                    spectrum_templates[dna_match.group(1)] = import_match.group(1)
        except: continue

    # Pass 2: Materialize
    target_tags = sys.argv[1:] if len(sys.argv) > 1 else TAG_MAP.keys()
    
    for path in sigma_files:
        rel_path = path.relative_to(SOURCE_DIR)
        try:
            content = path.read_text(encoding="utf-8")
        except: continue
            
        phys = parse_physics(content)
        stratum_match = re.search(r"🪐STRATUM:\s*(\w+)", content)
        stratum = stratum_match.group(1) if stratum_match else "m32"
        
        # Dynamic Override
        dynamic_stratum = entropy_to_stratum(phys["ENTROPY"])
        if stratum.startswith("m") or stratum.startswith("p"):
            stratum = dynamic_stratum
            
        glyph_match = re.search(r"GLYPH:\s*([\w=]+)", content)
        this_glyph = glyph_match.group(1) if glyph_match else rel_path.stem
        
        dna_match = re.search(r"🧬DNA:\s*(.*)", content)
        dependencies = dna_match.group(1).split() if dna_match else []
        
        folder_match = re.search(r"📁FOLDER:\s*(\w+)", content)
        folder = folder_match.group(1) if folder_match else None
        
        # Pantheon Logic
        is_pantheon = phys["AMPLITUDE"] >= 65535 and phys["ENTROPY"] <= -32768
        if is_pantheon and folder != "spectrum":
            folder = "pantheon"
        
        materialized_any = False
        for tag in target_tags:
            if tag not in TAG_MAP: continue
            
            target_base, ext_out = TAG_MAP[tag]
            block = extract_block(content, tag)
            
            # Target path logic
            glyph_fn = this_glyph if tag == "glyph" else rel_path.stem
            if tag == "glyph":
                if folder:
                    target_path = target_base / stratum / folder / f"{glyph_fn}{ext_out}"
                else:
                    target_path = target_base / stratum / f"{glyph_fn}{ext_out}"
            else:
                if folder:
                    target_path = target_base / stratum / folder / f"{rel_path.name.replace('.sigma', ext_out)}"
                else:
                    target_path = target_base / stratum / f"{rel_path.name.replace('.sigma', ext_out)}"

            # GLYPH Crystallization
            if tag == "glyph" and not block:
                if not materialized_any:
                    print(f"🧬 Materializing: {rel_path} -> {stratum}")
                    materialized_any = True
                
                ident = get_identity(content, this_glyph)
                head = struct.pack(">BBHHh", phys["OP"], phys["FLAGS"], phys["PHASE"], phys["AMPLITUDE"], phys["ENTROPY"])
                
                target_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    target_path.write_bytes(head + ident)
                    print(f"   💎 Crystallized [glyph]: {target_path.relative_to(SIGMA_ROOT)}")
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                continue

            if block:
                if not materialized_any:
                    print(f"🧬 Materializing: {rel_path} -> {stratum}")
                    materialized_any = True
                
                if stratum != "z00" and tag in spectrum_templates:
                    template = spectrum_templates[tag]
                    imports = [template.replace("%n", d).replace("%p", str(glyph_registry[d].with_suffix("")).replace(".sigma", "").replace("rs" if tag=="rs" else "", "::" if tag=="rs" else "/")) 
                               for d in dependencies if d in glyph_registry and d != this_glyph]
                    if imports: block = "\n".join(imports) + "\n\n" + block

                target_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    target_path.write_text(block + "\n", encoding="utf-8")
                    print(f"   -> Projected [{tag}]: {target_path.relative_to(SIGMA_ROOT)}")
                except Exception as e:
                    print(f"   ❌ Error: {e}")

    print("\n--- Materialization Complete. The Hologram is Synchronized. ---")

if __name__ == "__main__":
    main()

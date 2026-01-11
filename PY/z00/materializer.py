#!/usr/bin/env python3
import os
import re
import struct
import hashlib
import sys
from pathlib import Path

# Σ-GLYPH MATERIALIZER: Atomic Fusion Engine
# V1.5.2 - Spectral Autonomy: Implicit Projection, doc-block suppression

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
    atom_match = re.search(r"Atom:\s*([a-fA-F0-9]{64})", text)
    if atom_match: return bytes.fromhex(atom_match.group(1))
    id_match = re.search(r"🧬IDENTITY:\s*([a-fA-F0-9]{64})", text)
    if id_match: return bytes.fromhex(id_match.group(1))
    first_block_match = re.search(r"@\[\w+\]\n(.*?)\n(?=@\[|CHECKSUM:|$)", text, re.DOTALL)
    content = first_block_match.group(1).strip() if first_block_match else glyph_name
    return hashlib.sha256(content.encode("utf-8")).digest()

def entropy_to_stratum(entropy: int) -> str:
    if entropy == -1 or entropy == 0: return "z00"
    prefix = "m" if entropy < 0 else "p"
    bucket = math.ceil(abs(entropy) / 1024)
    return f"{prefix}{int(bucket):02}"

def extract_block(text: str, tag: str) -> str | None:
    # Explicitly check for doc suppression
    suppressed_marker = f"@[{tag}:doc]\n"
    if suppressed_marker in text: return None

    start_marker = f"@[{tag}]\n"
    start_idx = text.find(start_marker)
    if start_idx == -1: return None
    remaining = text[start_idx + len(start_marker):]
    end_match = re.search(r"\n@\[|\n+CHECKSUM:", remaining)
    block = remaining[:end_match.start()] if end_match else remaining
    content = block.strip()
    if content.startswith("```"):
        content = re.sub(r"^```[ \w]*\n", "", content)
    if content.endswith("```"):
        content = content[:-3].strip()
    return content

def main():
    print("=== Σ-GLYPH MATERIALIZER: Atomic Fusion V1.5.2 (Spectral Autonomy) ===\n")
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} not found.")
        return

    glyph_registry = {}
    spectrum_templates = {}
    sigma_files = list(SOURCE_DIR.glob("**/*.sigma"))
    
    # Pre-scan for registry and templates (Global implicit search)
    for path in sigma_files:
        try:
            content = path.read_text(encoding="utf-8")
            glyph_match = re.search(r"(?:GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content, re.MULTILINE)
            if glyph_match:
                glyph_registry[glyph_match.group(1)] = path.relative_to(SOURCE_DIR)
            
            # Implicit template detection
            import_match = re.search(r"^IMPORT:\s*'(.*)'", content, re.MULTILINE)
            if import_match:
                dna_match = re.search(r"(?:🧬DNA|🔗 CONNECTIONS \(Gravity\)):\s*\n+((?:\s*(?:-\s*|Ref:\s*)[\w=]+\n?)*|(?:\s*[\w=]+\s*)*)", content)
                if dna_match:
                    raw_dna = dna_match.group(1)
                    deps = [d.replace("Ref:", "").strip("- ").strip() for d in raw_dna.split() if d.strip("- ").strip()]
                    if deps:
                        spectrum_templates[deps[0]] = import_match.group(1)
        except: continue

    target_tags = sys.argv[1:] if len(sys.argv) > 1 else TAG_MAP.keys()
    
    for path in sigma_files:
        try:
            content = path.read_text(encoding="utf-8")
        except: continue
            
        phys = parse_physics(content)
        stratum = entropy_to_stratum(phys["ENTROPY"])
        glyph_match = re.search(r"(?:GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content)
        this_glyph = glyph_match.group(1) if glyph_match else path.stem
        
        dependencies = []
        dna_match = re.search(r"(?:🧬DNA|🔗 CONNECTIONS \(Gravity\)):\s*\n+((?:\s*(?:-\s*|Ref:\s*)[\w=]+\n?)*|(?:\s*[\w=]+\s*)*)", content)
        if dna_match:
            raw_dna = dna_match.group(1)
            dependencies = [d.replace("Ref:", "").strip("- ").strip() for d in raw_dna.splitlines() if d.strip()]
            if not dependencies:
                 dependencies = [d.strip("- ").strip() for d in raw_dna.split() if d.strip("- ").strip()]
        
        rel_sigma_path = path.relative_to(SOURCE_DIR)
        sub_folders = rel_sigma_path.parent.parts[1:]
        folder_path = Path(*sub_folders) if sub_folders else None
        
        is_pantheon = phys["AMPLITUDE"] >= 65535 and phys["ENTROPY"] <= -32768
        if is_pantheon:
            folder_path = Path("pantheon")

        materialized_any = False
        for tag in target_tags:
            if tag not in TAG_MAP: continue
            target_base, ext_out = TAG_MAP[tag]
            block = extract_block(content, tag)
            
            glyph_fn = this_glyph if tag == "glyph" else path.stem
            target_path = target_base / stratum / (folder_path if folder_path else "") / (f"{glyph_fn}{ext_out}" if tag == "glyph" else f"{path.name.replace('.sigma', ext_out)}")

            if tag == "glyph" and not block:
                if not materialized_any:
                    print(f"🧬 Atomizing: {path.name} -> {stratum}")
                    materialized_any = True
                ident = get_identity(content, this_glyph)
                head = struct.pack(">BBHHh", phys["OP"], phys["FLAGS"], phys["PHASE"], phys["AMPLITUDE"], phys["ENTROPY"])
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_bytes(head + ident)
                continue

            if block:
                if not materialized_any:
                    print(f"🧬 Fusing: {path.name} -> {stratum}")
                    materialized_any = True
                
                atoms = []
                for d in dependencies:
                    if d in glyph_registry:
                        atom_path = SOURCE_DIR / glyph_registry[d]
                        try:
                            atom_content = atom_path.read_text(encoding="utf-8")
                            if "🧪ATOM" in atom_content:
                                atom_block = extract_block(atom_content, tag)
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

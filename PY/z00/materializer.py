#!/usr/bin/env python3
from __future__ import annotations
import os
import re
import struct
import hashlib
import sys
import math
import json
from pathlib import Path

# Σ-GLYPH MATERIALIZER: Atomic Fusion Engine
# V2.2.0 - The Nervous System: Robust Metadata, Ghost Projections, OS Ready

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
    symbol_map = {"⚙️": "OP", "🚩": "FLAGS", "🌊": "PHASE", "🔊": "AMPLITUDE", "🌀": "ENTROPY"}
    for sym, key in symbol_map.items():
        match = re.search(f"{sym}:?\\s*(-?\\d+|0x[a-fA-F0-9]+)(?:\\s*#.*|$)", text, re.MULTILINE)
        if match:
            val = match.group(1)
            try:
                physics[key] = int(val, 16) if val.startswith("0x") else int(val)
            except: continue
    return physics

def extract_block(text: str, tag: str) -> str | None:
    suppressed_marker = f"@[{tag}:doc]"
    if suppressed_marker in text: return None

    start_marker = f"@[{tag}]"
    lines = text.splitlines()
    block_lines = []
    active = False
    
    for line in lines:
        if line.strip() == start_marker:
            active = True
            continue
        if active:
            if line.startswith("@[") or line.startswith("🔒:") or line.startswith("CHECKSUM:"):
                break
            block_lines.append(line)
    
    if not block_lines and not active: return None
    
    content = "\n".join(block_lines).strip()
    if content.startswith("```"):
        content = re.sub(r"^```[ \w]*\n", "", content)
    if content.endswith("```"):
        content = content[:-3].strip()
    return content

def parse_yaml_block(text: str) -> dict:
    """Robust line-based YAML extraction for core metadata."""
    data = {}
    if not text: return data
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line or ":" not in line: continue
        key, val = line.split(":", 1)
        key = key.strip().upper()
        val = val.strip().strip("'\"")
        data[key] = val
    return data

def entropy_to_stratum(entropy: int) -> str:
    if entropy == -1 or entropy == 0: return "z00"
    prefix = "m" if entropy < 0 else "p"
    bucket = math.ceil(abs(entropy) / 1024)
    if bucket > 32: bucket = 32
    return f"{prefix}{int(bucket):02}"

def materialize():
    print("=== Σ-GLYPH MATERIALIZER: Atomic Fusion V2.2.0 ===\n")
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} not found.")
        return

    glyph_registry = {}
    sigma_files = list(SOURCE_DIR.glob("**/*.sigma"))
    for path in sigma_files:
        try:
            content = path.read_text(encoding="utf-8")
            glyph_match = re.search(r"^(?:🧬|GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content, re.MULTILINE)
            if glyph_match:
                glyph_registry[glyph_match.group(1)] = path.relative_to(SOURCE_DIR)
        except: continue

    # Spectrum Templates (e.g. IMPORT commands)
    spectrum_configs = {}
    for glyph, rel_path in glyph_registry.items():
        if glyph in TAG_MAP:
            try:
                content = (SOURCE_DIR / rel_path).read_text(encoding="utf-8")
                yaml_block = extract_block(content, "yaml")
                if yaml_block:
                    spectrum_configs[glyph] = parse_yaml_block(yaml_block)
            except: continue

    for path in sigma_files:
        try: content = path.read_text(encoding="utf-8")
        except: continue
            
        phys = parse_physics(content)
        stratum = entropy_to_stratum(phys["ENTROPY"])
        glyph_match = re.search(r"^(?:🧬|GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content, re.MULTILINE)
        this_glyph = glyph_match.group(1) if glyph_match else path.stem
        
        # DNA Extraction
        dna_match = re.search(r"^(?:🧬DNA|DNA:|🔗|🔗:):\s*\n+((?:\s*(?:-\s*|Ref:\s*)?[\w=]+\n?)*)", content, re.MULTILINE)
        dependencies = []
        if dna_match:
            raw_dna = dna_match.group(1)
            dependencies = [d.replace("Ref:", "").strip("- ").strip() for d in raw_dna.splitlines() if d.strip("- ").strip()]
            if not dependencies:
                 dependencies = [d.strip("- ").strip() for d in raw_dna.split() if d.strip("- ").strip()]
        
        for tag, (out_dir, ext) in TAG_MAP.items():
            block = extract_block(content, tag)
            
            # GHOST PROJECTION: Warning for missing block in active spectrum
            if block is None and tag in spectrum_configs and stratum != "p32":
                # Only warn for established strata
                print(f"⚠️  Ghost Projection: {this_glyph} missing @[{tag}] block.")
                continue

            if block is not None:
                glyph_fn = this_glyph if tag == "glyph" else path.stem
                target_path = out_dir / stratum / f"{glyph_fn}{ext}"
                
                # Spectral Fusion (Axiom Injection)
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

                # Spectrum Injection (e.g. Imports)
                if stratum != "z00" and tag in spectrum_configs:
                    config = spectrum_configs[tag]
                    if "IMPORT" in config:
                        template = config["IMPORT"]
                        imports = []
                        for d in dependencies:
                            if d in glyph_registry and d != this_glyph:
                                rel_dep = str(glyph_registry[d].with_suffix("")).replace(".sigma", "").replace(tag, "::" if tag=="rs" else "/")
                                imports.append(template.replace("%n", d).replace("%p", rel_dep))
                        if imports: block = "\n".join(imports) + "\n\n" + block

                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(block + "\n", encoding="utf-8")

    print("\n--- Materialization Complete. The Nervous System is Synced. ---")

if __name__ == "__main__":
    materialize()

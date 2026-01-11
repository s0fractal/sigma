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
# V2.5.1 - Projection S: Map-Aware Symlinks

import protocol
import scr1
import physics

# --- CONFIGURATION ---
SIGMA_ROOT = protocol.ROOT
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
    "lock": (SIGMA_ROOT / "LOCK", ".lock"),
    "glyph": (SIGMA_ROOT / "GLYPH", ".glyph"),
}

# --- ATOMIC FUNCTIONS ---

def parse_physics(text: str) -> dict:
    physics = {"OP": protocol.OP_LITERAL, "FLAGS": 0, "PHASE": 0, "AMPLITUDE": 0, "ENTROPY": 0}
    symbol_map = {"⚙️": "OP", "🚩": "FLAGS", "🌊": "PHASE", "🔊": "AMPLITUDE", "🌀": "ENTROPY"}
    for sym, key in symbol_map.items():
        match = re.search(f"^{sym}:?\\s*(-?\\d+|0x[a-fA-F0-9]+)", text, re.MULTILINE)
        if match:
            val = match.group(1)
            try:
                physics[key] = int(val, 16) if val.startswith("0x") else int(val)
            except: continue
    return physics

def extract_block(text: str, tag: str) -> str | None:
    """SCR-1: Strict Canonical Block Extraction."""
    content = text.replace("\r\n", "\n").replace("\r", "\n")
    start_marker = f"@[{tag}]"
    
    parts = re.split(f"^{re.escape(start_marker)}\\n", content, flags=re.MULTILINE)
    if len(parts) < 2: return None
    
    payload_raw = parts[1]
    # End search: next block or seal
    end_match = re.search(r"^\n(@\[|🔒:|CHECKSUM:)", payload_raw, re.MULTILINE)
    payload = payload_raw[:end_match.start()] if end_match else payload_raw
    
    return payload.strip("\n")

def extract_link(text: str) -> str | None:
    """Extracts symlink target from @[link] block."""
    return extract_block(text, "link")

def parse_yaml_metadata(text: str) -> dict:
    """Standardized metadata extraction for @[yaml] blocks."""
    data = {}
    if not text: return data
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line or ":" not in line: continue
        key, val = line.split(":", 1)
        data[key.strip().upper()] = val.strip().strip("'\"")
    return data

def materialize():
    print("=== Σ-GLYPH MATERIALIZER: Atomic Fusion V2.5.1 (Symlink Map) ===\n")
    if not SOURCE_DIR.exists():
        print(f"Error: Source directory {SOURCE_DIR} not found.")
        return

    glyph_registry = {}
    sigma_files = sorted(list(SOURCE_DIR.glob("**/*.sigma")), key=lambda p: str(p))
    
    for path in sigma_files:
        try:
            content = path.read_text(encoding="utf-8")
            glyph_match = re.search(r"^(?:🧬|GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content, re.MULTILINE)
            if glyph_match:
                glyph_registry[glyph_match.group(1)] = path.relative_to(SOURCE_DIR)
        except: continue

    spectrum_configs = {}
    for path in sigma_files:
        try:
             content = path.read_text(encoding="utf-8")
             yaml_block = extract_block(content, "yaml")
             if yaml_block:
                 glyph_match = re.search(r"^(?:🧬|GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content, re.MULTILINE)
                 if glyph_match:
                     spectrum_configs[glyph_match.group(1)] = parse_yaml_metadata(yaml_block)
        except: continue

    for path in sigma_files:
        try: content = path.read_text(encoding="utf-8")
        except: continue
            
        phys = parse_physics(content)
        stratum = physics.entropy_to_stratum(phys["ENTROPY"])
        glyph_match = re.search(r"^(?:🧬|GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content, re.MULTILINE)
        this_glyph = glyph_match.group(1) if glyph_match else path.stem
        
        dna_match = re.search(r"^(?:🧬DNA|DNA:|🔗|🔗:):\s*\n+((?:\s*(?:-\s*|Ref:\s*)?[\w=]+\n?)*)", content, re.MULTILINE)
        dependencies = []
        if dna_match:
            raw_dna = dna_match.group(1)
            dependencies = [d.replace("Ref:", "").strip("- ").strip() for d in raw_dna.splitlines() if d.strip("- ").strip()]
        
        # 1. Parse Links
        links_map = {}
        link_block = extract_link(content)
        if link_block:
            for line in link_block.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    links_map[k.strip()] = v.strip()
                elif line.strip():
                    links_map["*"] = line.strip()

        for tag, (out_dir, ext) in TAG_MAP.items():
            block = extract_block(content, tag)
            if block is not None:
                glyph_fn = this_glyph if tag == "glyph" else path.stem
                target_path = out_dir / stratum / f"{glyph_fn}{ext}"
                
                # Axiom Injection
                atoms = []
                for dep in dependencies:
                    if dep in glyph_registry:
                        try:
                            dep_content = (SOURCE_DIR / glyph_registry[dep]).read_text(encoding="utf-8")
                            atom_block = extract_block(dep_content, tag)
                            if atom_block: atoms.append(atom_block)
                        except: continue
                
                final_block = (("\n\n".join(atoms) + "\n\n") if atoms else "") + block

                if stratum != "z00" and this_glyph in spectrum_configs:
                    config = spectrum_configs[this_glyph]
                    if "IMPORT" in config:
                        template = config["IMPORT"]
                        imports = []
                        for d in dependencies:
                            if d in glyph_registry and d != this_glyph:
                                rel_dep = str(glyph_registry[d].with_suffix("")).replace(".sigma", "").replace(tag, "::" if tag=="rs" else "/")
                                imports.append(template.replace("%n", d).replace("%p", rel_dep))
                        if imports: final_block = "\n".join(imports) + "\n\n" + final_block

                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(final_block + "\n", encoding="utf-8")
                
                # 2. Link Processing
                link_target_str = links_map.get(tag) or links_map.get("*")
                if link_target_str:
                    link_name = (SIGMA_ROOT / link_target_str).resolve()
                    
                    # Security check: Ensure link is within SIGMA_ROOT
                    try:
                         link_name.relative_to(SIGMA_ROOT)
                    except ValueError:
                         print(f"⚠️  Security Block: Link target {link_name} outside Root.")
                         continue

                    link_name.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        rel_target = os.path.relpath(target_path, link_name.parent)
                        if link_name.exists() or link_name.is_symlink():
                            link_name.unlink()
                        os.symlink(rel_target, link_name)
                    except Exception as e:
                        print(f"⚠️  Link Error {this_glyph} ({tag}): {e}")

    print("\n--- Materialization Complete. The Lattice is Reified. ---")

if __name__ == "__main__":
    materialize()

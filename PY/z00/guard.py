#!/usr/bin/env python3
from __future__ import annotations
import os
import re
import sys
import shutil
import hashlib
import math
from pathlib import Path

# Σ-GLYPH GUARD
# V2.3.3 - Deterministic Resonance: Sorted Audit, Strict SCR-1

import protocol

SIGMA_ROOT = protocol.ROOT
SOURCE_DIR = SIGMA_ROOT / "sigma"

def normalize_text(text: str) -> str:
    """SCR-1: UTF-8, LF endings, no trailing whitespace."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines)

def calculate_node_hash(content: str) -> str:
    """SCR-1: Hash body by excluding Identity header and Seal."""
    # 1. Strip seal
    body = content
    markers = ["\n🔒:", "\nCHECKSUM:"]
    idx = -1
    for m in markers:
        m_idx = content.rfind(m)
        if m_idx > idx: idx = m_idx
    
    if idx != -1: body = content[:idx]
    else: body = content.strip()
        
    # 2. Exclude Identity and metadata lines that are human-only
    # We define payload as everything NOT starting with 🧬IDENTITY, 🔒:, or CHECKSUM:
    # also normalized to remove aesthetic variance in the header
    lines = body.splitlines()
    filtered_lines = []
    
    # Heuristic: We only hash content that affects the materialization
    # However, for bit-purity of the SEEDS themselves, we hash the entire normalized seed body
    # excluding identity-loop headers.
    for l in lines:
        s_line = l.strip()
        if re.match(r"^(🧬IDENTITY:|IDENTITY:|CHECKSUM:|🔒:)", s_line):
            continue
        filtered_lines.append(l)
    
    canon_body = "\n".join(filtered_lines).strip()
    return hashlib.sha256(canon_body.encode("utf-8")).hexdigest()

def audit_lattice(fix=False):
    violations = []
    print("🛡️  Guarding Lattice (Deterministic Resonance)...")
    
    # DETERMINISTIC: Sorted file list
    sigma_files = sorted(list(SOURCE_DIR.glob("**/*.sigma")), key=lambda p: str(p))
    
    # Aggregate Lattice Hash
    lattice_hasher = hashlib.sha256()

    for path in sigma_files:
        try:
            raw_content = path.read_text(encoding="utf-8")
            content = normalize_text(raw_content)
            
            id_match = re.search(r"^🧬IDENTITY:\s*([a-fA-F0-9]{64})", content, re.MULTILINE)
            seal_match = re.search(r"\n(?:🔒:|CHECKSUM:)\s*(.*)$", content, re.MULTILINE)
            
            node_hash = calculate_node_hash(content)
            current_id = id_match.group(1) if id_match else None
            current_seal = seal_match.group(1).strip() if seal_match else None

            # Add to aggregate hash for deterministic traversal proof
            lattice_hasher.update(node_hash.encode())

            needs_fix = False
            if node_hash != current_id:
                violations.append(f"Identity Drift: {path.relative_to(SOURCE_DIR)}")
                needs_fix = True
            if node_hash != current_seal:
                violations.append(f"Seal Dissonance: {path.relative_to(SOURCE_DIR)}")
                needs_fix = True

            if needs_fix and fix:
                print(f"   🛠 Healing: {path.name} -> {node_hash[:16]}...")
                # 1. Update/Add Identity Header
                if id_match:
                    new_content = content.replace(id_match.group(0), f"🧬IDENTITY: {node_hash}")
                else:
                    header_pat = r"^(Σ-GLYPH SEED|🧬):\s*([\w=]+)(\n?)"
                    match = re.search(header_pat, content, re.MULTILINE)
                    if match:
                        new_content = content[:match.end()] + f"🧬IDENTITY: {node_hash}\n" + content[match.end():]
                    else:
                        new_content = f"🧬IDENTITY: {node_hash}\n" + content
                
                # 2. Update/Add Seal
                sm = re.search(r"\n(?:🔒:|CHECKSUM:)\s*(.*)$", new_content, re.MULTILINE)
                if sm:
                    start, end = sm.span()
                    marker = "CHECKSUM:" if "CHECKSUM:" in sm.group(0) else "🔒:"
                    new_content = new_content[:start] + f"\n{marker} {node_hash}"
                else:
                    new_content = new_content.strip() + f"\n\n🔒: {node_hash}"
                
                path.write_text(new_content, encoding="utf-8")
                    
        except Exception as e:
            violations.append(f"Core Fault: {path.name} ({e})")
            
    print(f"\n🌀 Lattice Resonance Hash: {lattice_hasher.hexdigest()}")
    return violations

def main():
    fix_mode = "--fix" in sys.argv
    violations = audit_lattice(fix=fix_mode)
    
    if not violations:
        print("✅ THE LATTICE IS BIT-PURE.")
        sys.exit(0)
    
    print(f"\n❌ VIOLATIONS: {len(violations)}")
    sys.exit(1)

if __name__ == "__main__":
    main()

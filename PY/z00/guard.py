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
# V2.3.4 - Deterministic Resonance: Library-Driven SCR-1

import protocol
import scr1

SIGMA_ROOT = protocol.ROOT
SOURCE_DIR = SIGMA_ROOT / "sigma"

def audit_lattice(fix=False, source_dir: Path = SOURCE_DIR):
    violations = []
    print(f"🛡️  Guarding Lattice (SCR-1 Library Compliance) | Fix={fix}...")
    
    # DETERMINISTIC: Sorted file list
    sigma_files = sorted(list(source_dir.glob("**/*.sigma")), key=lambda p: str(p))
    
    # Aggregate Lattice Hash
    lattice_hasher = hashlib.sha256()

    for path in sigma_files:
        try:
            raw_content = path.read_text(encoding="utf-8")
            
            # Identity and Seal extraction for verification
            id_match = re.search(r"^🧬IDENTITY:\s*([a-fA-F0-9]{64})", raw_content, re.MULTILINE)
            seal_match = re.search(r"\n(?:🔒:|CHECKSUM:)\s*(.*)$", raw_content, re.MULTILINE)
            
            # USE CANONICAL LIBRARY
            node_hash = scr1.get_node_hash(raw_content)
            
            current_id = id_match.group(1) if id_match else None
            current_seal = seal_match.group(1).strip() if seal_match else None

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
                
                # 1. Strip existing seal and identity line if any (pre-emptive cleaning)
                # But scr1.canonicalize_sigma returns bytes of the BODY.
                # We need to rebuild the file.
                
                # Normalize line endings first for consistent replacement
                content = raw_content.replace("\r\n", "\n").replace("\r", "\n")
                
                # Remove identity lines
                content = re.sub(r"^(🧬IDENTITY:|IDENTITY:).*?\n", "", content, flags=re.MULTILINE)
                
                # Remove seal
                seal_pattern = r"\n(?:🔒:|CHECKSUM:)\s*[0-9a-f]{64}\s*$"
                match = list(re.finditer(seal_pattern, content, re.MULTILINE))
                if match:
                    content = content[:match[-1].start()]
                
                # Now prepend new identity and append new seal
                # We preserve the header "Σ-GLYPH SEED: ..." or "🧬: ..."
                header_pat = r"^(Σ-GLYPH SEED|🧬):\s*([\w=]+)(\n?)"
                header_match = re.search(header_pat, content, re.MULTILINE)
                
                if header_match:
                    # Insert after the first header line
                    final_content = content[:header_match.end()] + f"🧬IDENTITY: {node_hash}\n" + content[header_match.end():]
                else:
                    final_content = f"🧬IDENTITY: {node_hash}\n" + content
                
                # Ensure spacing before seal
                final_content = final_content.rstrip() + f"\n\n🔒: {node_hash}\n"
                
                path.write_text(final_content, encoding="utf-8")
                    
        except Exception as e:
            # Still report core faults to avoid silent success if a file cannot be read
            violations.append(f"Core Fault: {path.name} ({e})")
            raise e
            
    print(f"\n🌀 Lattice Resonance Hash: {lattice_hasher.hexdigest()}")
    print(f"📡 Protocol Version: {protocol.VERSION}")
    return violations

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Σ-GLYPH Guard")
    parser.add_argument("--fix", action="store_true", help="Heal the lattice.")
    args = parser.parse_args()
    
    violations = audit_lattice(fix=args.fix)
    
    if not violations:
        print("✅ THE LATTICE IS BIT-PURE (SCR-1).")
        sys.exit(0)
    
    print(f"\n❌ VIOLATIONS: {len(violations)}")
    sys.exit(1)

if __name__ == "__main__":
    main()

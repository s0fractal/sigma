#!/usr/bin/env python3
from __future__ import annotations
import sys
import argparse
import hashlib
from pathlib import Path

# Σ-GLYPH CLI: The System Orchestrator
# V2.3.0 - Deterministic Resonance: NodeHash & canonical Forge

import materializer
import guard

TEMPLATE_V2_3 = """Σ-GLYPH SEED: {NAME}
🧬IDENTITY: {ID}

---
# === 🧬 IDENTITY ===
🧬: {NAME}
DNA: {DNA}
⚛️: {ATOM}
🎨: #FFFFFF

# === ⚖️ PHYSICS (Wave Function) ===
⚙️: 0
🚩: 1
🌊: {PHASE}
🔊: 65535
🌀: -32768

# === 🔗 GRAVITY (Dependencies) ===
🔗:
  - SATOSHI
---

# {NAME}

Intent for {NAME} established.

🌊

@[dna]
{DNA}

🔒: {ID}
"""

def calc_spectral_analysis(text: str):
    h = hashlib.sha256(text.encode()).hexdigest()
    color = f"#{h[:6].upper()}"
    return h, color

def cmd_forge(name: str, phase: int = 0, dna: str = None):
    """Forges a new seed at p32 with V2.3 Identity."""
    if not dna: dna = name
    atom, _ = calc_spectral_analysis(name)
    
    # Pre-calculate temporary identity for the template
    # (Since forge uses a fixed template, we can approximate or leave as placeholder)
    temp_id = "00"*32 
    content = TEMPLATE_V2_3.format(
        NAME=name,
        ID=temp_id,
        DNA=dna,
        ATOM=atom,
        PHASE=phase
    )
    
    target_path = Path("/Users/s0fractal/SIGMA/sigma/p32") / f"{name}.sigma"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    
    # Self-Seal immediately to get the true SCR-1 NodeHash
    sys.argv = ["guard.py", "--fix"]
    guard.main()
    print(f"✨ Forged and Sealed: {name}.sigma")

def main():
    parser = argparse.ArgumentParser(description="Σ-GLYPH CLI: System Orchestrator V2.3")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Materialize all intents (SCR-1).")
    
    check_parser = subparsers.add_parser("check", help="Audit lattice (SCR-1/Identity).")
    check_parser.add_argument("--fix", action="store_true", help="Fix violations.")

    calc_parser = subparsers.add_parser("calc", help="Spectral analysis.")
    calc_parser.add_argument("text")

    forge_parser = subparsers.add_parser("forge", help="Forge seed template (V2.3).")
    forge_parser.add_argument("name")
    forge_parser.add_argument("--phase", type=int, default=0)
    forge_parser.add_argument("--dna")

    subparsers.add_parser("version", help="System version.")

    args = parser.parse_args()

    if args.command == "sync":
        materializer.materialize()
    elif args.command == "check":
        sys.argv = ["guard.py"] + (["--fix"] if args.fix else [])
        guard.main()
    elif args.command == "calc":
        h, color = calc_spectral_analysis(args.text)
        print(f"🧬 Spectral Analysis:\n   Atom:  {h}\n   Color: {color}")
    elif args.command == "forge":
        cmd_forge(args.name, args.phase, args.dna)
    elif args.command == "version":
        print("Σ-GLYPH OS V2.3.0 (Deterministic Resonance)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

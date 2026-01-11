#!/usr/bin/env python3
from __future__ import annotations
import sys
import argparse
import hashlib
from pathlib import Path

# Σ-GLYPH CLI: The System Orchestrator
# V2.2.1 - The Nervous System: Forge V2.1 Template

import materializer
import guard

TEMPLATE_V2_1 = """Σ-GLYPH SEED: {NAME}

---
# === 🧬 IDENTITY ===
🧬: {NAME}
DNA: {DNA}
⚛️: {ATOM}
🎨: {COLOR}

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

{INTENT}

🌊

@[dna]
{DNA}

🔒: VALIDATING...
"""

def calc_spectral_analysis(text: str):
    """Calculates Spectral resonance (Color/Hash)."""
    h = hashlib.sha256(text.encode()).hexdigest()
    color = f"#{h[:6].upper()}"
    return h, color

def cmd_forge(name: str, phase: int = 0, dna: str = None):
    """Forges a new Sigma seed with the V2.1 Symbolic Standard."""
    if not dna: dna = name
    atom, color = calc_spectral_analysis(name)
    content = TEMPLATE_V2_1.format(
        NAME=name,
        DNA=dna,
        ATOM=atom,
        COLOR=color,
        PHASE=phase,
        INTENT=f"Intent for {name} established."
    )
    # Default to p32 for new seeds (Chaos)
    target_path = Path("/Users/s0fractal/SIGMA/sigma/p32") / f"{name}.sigma"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    print(f"✨ Forged: {name}.sigma at {target_path}")

def main():
    parser = argparse.ArgumentParser(description="Σ-GLYPH CLI: System Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    # sync
    subparsers.add_parser("sync", help="Materialize all intents into dimension spectrums.")
    
    # check
    check_parser = subparsers.add_parser("check", help="Audit lattice topology and checksums.")
    check_parser.add_argument("--fix", action="store_true", help="Automatically resolve violations.")

    # calc
    calc_parser = subparsers.add_parser("calc", help="Calculate spectral color and hash for text.")
    calc_parser.add_argument("text", help="Text to analyze.")

    # forge
    forge_parser = subparsers.add_parser("forge", help="Forge a new seed template.")
    forge_parser.add_argument("name", help="Name of the glyph.")
    forge_parser.add_argument("--phase", type=int, default=0, help="Phase of the wave function.")
    forge_parser.add_argument("--dna", help="DNA formula for the glyph.")

    # version
    subparsers.add_parser("version", help="Show system version.")

    args = parser.parse_args()

    if args.command == "sync":
        materializer.materialize()
    elif args.command == "check":
        sys.argv = ["guard.py"] + (["--fix"] if args.fix else [])
        guard.main()
    elif args.command == "calc":
        h, color = calc_spectral_analysis(args.text)
        print(f"🧬 Spectral Analysis:")
        print(f"   Atom:  {h}")
        print(f"   Color: {color}")
    elif args.command == "forge":
        cmd_forge(args.name, args.phase, args.dna)
    elif args.command == "version":
        print("Σ-GLYPH OS V2.2.1 (The Nervous System)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations
import sys
import argparse
import hashlib
from pathlib import Path

# Σ-GLYPH CLI: The System Orchestrator
# V2.2.0 - The Nervous System

import materializer
import guard

def calc_spectral_analysis(text: str):
    """Calculates Spectral resonance (Color/Hash)."""
    h = hashlib.sha256(text.encode()).hexdigest()
    color = f"#{h[:6].upper()}"
    print(f"🧬 Spectral Analysis:")
    print(f"   Atom:  {h}")
    print(f"   Color: {color}")

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

    # version
    subparsers.add_parser("version", help="Show system version.")

    args = parser.parse_args()

    if args.command == "sync":
        materializer.materialize()
    elif args.command == "check":
        # Simulate running guard logic
        sys.argv = ["guard.py"] + (["--fix"] if args.fix else [])
        guard.main()
    elif args.command == "calc":
        calc_spectral_analysis(args.text)
    elif args.command == "version":
        print("Σ-GLYPH OS V2.2.0 (The Nervous System)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

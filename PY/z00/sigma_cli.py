#!/usr/bin/env python3
from __future__ import annotations
import sys
import argparse
import hashlib
from pathlib import Path

# Σ-GLYPH CLI: The System Orchestrator
# V2.3.1 - Deterministic Resonance: Absolute Path Immunity

import materializer
import guard
import protocol

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

def get_repo_root() -> Path:
    return protocol.ROOT

def calc_spectral_analysis(text: str):
    h = hashlib.sha256(text.encode()).hexdigest()
    color = f"#{h[:6].upper()}"
    return h, color

def cmd_forge(name: str, phase: int = 0, dna: str = None):
    """Forges a new seed at p32 with V2.3 Identity."""
    if not dna: dna = name
    atom, _ = calc_spectral_analysis(name)
    
    temp_id = "00"*32 
    content = TEMPLATE_V2_3.format(
        NAME=name,
        ID=temp_id,
        DNA=dna,
        ATOM=atom,
        PHASE=phase
    )
    
    # DETERNMINISTIC PATHS
    target_path = get_repo_root() / "sigma" / "p32" / f"{name}.sigma"
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")
    
    # Self-Seal immediately
    sys.argv = ["guard.py", "--fix"]
    guard.main()
    print(f"✨ Forged and Sealed: {name}.sigma")

def cmd_path_check():
    """CI Test: Ensure no absolute paths exist in the lattice or tools."""
    root = get_repo_root()
    print(f"🧐 Auditing for Path Leaks in {root}...")
    # Split pattern to avoid self-detection
    abs_pattern = "/" + "Users" + "/"
    found = False
    
    # Scan PY, TS, and sigma
    for dir_name in ["PY", "TS", "sigma"]:
        search_dir = root / dir_name
        if not search_dir.exists(): continue
        
        for path in search_dir.glob("**/*"):
            if path.is_dir() or path.suffix in [".png", ".jpg", ".bin"]: continue
            try:
                content = path.read_text()
                if abs_pattern in content:
                    print(f"   [FAIL] Absolute path leak in: {path.relative_to(root)}")
                    found = True
            except: continue
            
    if found:
        print("\n❌ PATH AUDIT FAILED.")
        sys.exit(1)
    else:
        print("\n✅ ZERO PATH LEAKS DETECTED.")

def main():
    parser = argparse.ArgumentParser(description="Σ-GLYPH CLI: System Orchestrator V2.3.1")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("sync", help="Materialize all intents (SCR-1).")
    subparsers.add_parser("check", help="Audit lattice (SCR-1/Identity).").add_argument("--fix", action="store_true")
    
    test_parser = subparsers.add_parser("test", help="Run system tests.")
    test_parser.add_argument("suite", choices=["path-check"])

    calc_parser = subparsers.add_parser("calc", help="Spectral analysis.")
    calc_parser.add_argument("text")

    forge_parser = subparsers.add_parser("forge", help="Forge seed (V2.3).")
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
    elif args.command == "test":
        if args.suite == "path-check": cmd_path_check()
    elif args.command == "calc":
        h, color = calc_spectral_analysis(args.text)
        print(f"🧬 Spectral Analysis:\n   Atom:  {h}\n   Color: {color}")
    elif args.command == "forge":
        cmd_forge(args.name, args.phase, args.dna)
    elif args.command == "version":
        print(f"Σ-GLYPH OS V{protocol._data.get('VERSION', '2.3.1')} (Resonance Stable)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

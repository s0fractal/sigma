import sys
import os
import argparse
import hashlib
from pathlib import Path

# Σ-GLYPH CLI: The System Orchestrator
# V2.3.1 - Deterministic Resonance: Absolute Path Immunity

import materializer
import guard
import protocol
import physics
import collider

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
    """Discovery with override support."""
    override = os.environ.get("SIGMA_ROOT") or os.environ.get("SIGMA_GARDEN")
    if override:
        return Path(override).resolve()
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
    guard.audit_lattice(fix=True)
    print(f"✨ Forged and Sealed: {name}.sigma")

def cmd_path_check():
    """CI Test: Ensure no absolute paths exist in the lattice or tools."""
    root = get_repo_root()
    print(f"🧐 Auditing for Path Leaks in {root} (Strict Mode)...")
    
    # Expanded patterns to detect
    patterns = [
        "/" + "Users" + "/",
        "/" + "home" + "/",
        "C" + ":" + "\\",
        "file" + ":" + "//",
        "~" + "/"
    ]
    
    found = False
    
    # Scan PY, TS, sigma, SH, MD, LOCK, JSON
    for dir_name in ["PY", "TS", "sigma", "SH", "MD", "LOCK", "JSON"]:
        search_dir = root / dir_name
        if not search_dir.exists(): continue
        
        for path in sorted(search_dir.glob("**/*"), key=lambda p: str(p)):
            if path.is_dir() or path.suffix in [".png", ".jpg", ".bin", ".pyc", ".lock"]: continue
            try:
                content = path.read_text(encoding="utf-8")
                
                for p in patterns:
                    if p in content:
                        # Extra check: is it inside a .sigma block?
                        # We just report it regardless of context for strict determinism.
                        print(f"   [FAIL] Leak '{p}' in: {path.relative_to(root)}")
                        found = True
                        break # Only report once per file
            except Exception as e:
                # print(f"   [SKIP] {path.name}: {e}")
                continue
            
    if found:
        print("\n❌ PATH AUDIT FAILED. Purge absolute references.")
        sys.exit(1)
    else:
        print("\n✅ ZERO PATH LEAKS DETECTED.")

def main():
    parser = argparse.ArgumentParser(description="Σ-GLYPH CLI: System Orchestrator V2.3.1")
    subparsers = parser.add_subparsers(dest="command")

    sync_parser = subparsers.add_parser("sync", help="Materialize all intents (SCR-1).")
    sync_parser.add_argument("--core-only", action="store_true", help="Only extract deterministic blocks.")

    check_parser = subparsers.add_parser("check", help="Audit lattice (SCR-1/Identity).")
    check_parser.add_argument("--fix", action="store_true")
    check_parser.add_argument("--strict", action="store_true", help="Fail hard on any dissonance.")
    
    test_parser = subparsers.add_parser("test", help="Run system tests.")
    test_parser.add_argument("suite", choices=["path-check"])

    calc_parser = subparsers.add_parser("calc", help="Spectral analysis.")
    calc_parser.add_argument("text")

    poi_parser = subparsers.add_parser("poi", help="Harmonization Layer (PoI).")
    poi_parser.add_argument("--strict", action="store_true", help="Fail on 🔴.")
    poi_parser.add_argument("--json", action="store_true", help="Output JSON report.")

    forge_parser = subparsers.add_parser("forge", help="Forge seed (V2.3).")
    forge_parser.add_argument("name")
    forge_parser.add_argument("--phase", type=int, default=0)
    forge_parser.add_argument("--dna")

    subparsers.add_parser("version", help="System version.")

    args = parser.parse_args()

    if args.command == "sync":
        materializer.materialize()
    elif args.command == "check":
        violations = guard.audit_lattice(fix=args.fix)
        if violations:
            if args.strict:
                print("\n❌ STRICT MODE: Dissonance detected. Blocking evolution.")
                sys.exit(1)
            else:
                print(f"\n⚠️  Total Violations: {len(violations)}")
    elif args.command == "test":
        if args.suite == "path-check": cmd_path_check()
    elif args.command == "calc":
        h, color = calc_spectral_analysis(args.text)
        print(f"🧬 Spectral Analysis:\n   Atom:  {h}\n   Color: {color}")
    elif args.command == "poi":
        results = collider.collide()
        if args.json:
            print(collider.generate_report(results, "json"))
        else:
            print(collider.generate_report(results, "human"))
        
        if args.strict:
            has_red = any(r.status == "🔴" for r in results)
            if has_red:
                print("\n❌ STRICT MODE: Dissonance (🔴) detected.")
                sys.exit(1)
    elif args.command == "forge":
        cmd_forge(args.name, args.phase, args.dna)
    elif args.command == "version":
        print(f"Σ-GLYPH OS V{protocol._data.get('VERSION', '2.3.1')} (Resonance Stable)")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

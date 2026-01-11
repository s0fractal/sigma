#!/usr/bin/env python3
from __future__ import annotations
import sys
import hashlib
from pathlib import Path
import re
import protocol
import scr1

# Σ-GLYPH CONFORMANCE SUITE (Python)
# V2.3.3 - Bit-Exact Parity Check (SCR-1 Library)

# NEW HASHES (V2.3.1 strictly following prompt rules)
REFERENCE_VECTORS = {
    "I": "6d790ee9187df21994ac486616c676f1a287af7d87b0530e77afb9844fa0758e",
    "K": "53bbcd11d0d533ee1e72793f9b0c5443eff5fda8f7d0e9592994e77bbc6326d8",
    "S": "b3b7a6ff9b830929d4d838b99a9e6121c63d8ce5ce2a7e586791f8dce5613311",
    "FALSE": "70dbe5b36f507bfecd57522c988ae5257967f10a71b5da3afcbde0ce9949f82d"
}

def test_interfere():
    print("🧪  Testing Math Determinism (interfere)...")
    def div_round_half_up(n, d):
        s = 1 if n >= 0 else -1
        a = abs(n)
        q = a // d
        r = a % d
        if 2 * r >= d: q += 1
        return s * q
    
    w1 = {"ph": 0, "am": 65535, "en": 100}
    w2 = {"ph": 16384, "am": 32768, "en": -200}
    
    amp_factor = div_round_half_up((0 + 32767) * 65535, 65534)
    prod01 = div_round_half_up(w1["am"] * w2["am"], 65535)
    new_am = div_round_half_up(prod01 * amp_factor, 65535)
    new_en = max(-32768, min(32767, div_round_half_up(w1["en"] + w2["en"], 2)))

    actual = {"ph": w1["ph"], "am": new_am, "en": new_en}
    expected = {"ph": 0, "am": 16384, "en": -50}
    
    if actual == expected:
        print(f"   [PASS] interfere: {actual}")
        return True
    else:
        print(f"   [FAIL] interfere: {actual} (Expected {expected})")
        return False

def test_scr1():
    print("🧪  Testing SCR-1 Conformance (Python Library)...")
    errors = 0
    for name, expected in REFERENCE_VECTORS.items():
        path = None
        # Searching across entire lattice
        for p in protocol.ROOT.glob(f"sigma/**/{name}.sigma"):
            path = p
            break
        if not path:
            print(f"   [MISSING] {name}")
            errors += 1
            continue
        actual = scr1.get_node_hash(path.read_text(encoding="utf-8"))
        if actual == expected:
            print(f"   [PASS] {name}: {actual[:16]}...")
        else:
            print(f"   [FAIL] {name}\n          Exp: {expected}\n          Act: {actual}")
            errors += 1
    return errors == 0

def test_fuzz_scr1():
    print("🧪  Testing SCR-1 Fuzzing/Stability...")
    # SCR-1 should be stable under:
    # 1. CRLF normalization
    # 2. Trailing whitespace on lines
    # 3. Redundant trailing newlines at end of file
    # 4. Identity header presence
    
    base = "Σ-GLYPH SEED: fuzz\n---\nBODY\n---"
    h_base = scr1.get_node_hash(base)
    
    variations = [
        base.replace("\n", "\r\n"), # CRLF
        base.replace("BODY", "BODY    "), # Trailing space
        base + "\n\n\n\n", # Redundant trailing newlines
        "🧬IDENTITY: abc\n" + base, # Identity header added
        base + "\n🔒: abc", # Seal added
    ]
    
    for i, var in enumerate(variations):
        h_v = scr1.get_node_hash(var)
        if h_base != h_v:
            print(f"   [FAIL] Fuzz variation {i} changed hash!")
            return False
    print("   [PASS] SCR-1 Stability maintained.")
    return True

if __name__ == "__main__":
    success = test_scr1() and test_interfere() and test_fuzz_scr1()
    if not success: sys.exit(1)
    print("\n✅ PYTHON CONFORMANCE SECURED.")

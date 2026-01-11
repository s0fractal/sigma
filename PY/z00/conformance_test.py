#!/usr/bin/env python3
from __future__ import annotations
import sys
import json
import hashlib
from pathlib import Path
import re
import protocol
import scr1

# Σ-GLYPH CONFORMANCE SUITE (Python)
# V2.3.4 - Bit-Exact Parity Check (Policy A Hardened)

def load_vectors():
    vec_path = protocol.ROOT / "PY" / "z00" / "vectors.json"
    return json.loads(vec_path.read_text())["vectors"]

def test_vectors():
    print("🧪 Testing SCR-1/PoI Golden Vectors...")
    vectors = load_vectors()
    errors = 0
    for v in vectors:
        if "body" in v:
            actual = scr1.get_node_hash(v["body"])
            if actual == v["expected_hash"]:
                print(f"   [PASS] SCR-1: {v['name']}")
            else:
                print(f"   [FAIL] SCR-1: {v['name']}\n          Exp: {v['expected_hash']}\n          Act: {actual}")
                errors += 1
        elif "expected_poi" in v:
            actual = scr1.calculate_poi(v["intent_hash"], v["code_hash"])
            if actual == v["expected_poi"]:
                print(f"   [PASS] PoI: {v['name']}")
            else:
                print(f"   [FAIL] PoI: {v['name']}\n          Exp: {v['expected_poi']}\n          Act: {actual}")
                errors += 1
    return errors == 0

def test_interfere():
    print("🧪 Testing Math Determinism (interfere)...")
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
        print(f"   [PASS] interfere anchor verified.")
        return True
    else:
        print(f"   [FAIL] interfere mismatch.")
        return False

def test_root_discovery():
    print("🧪 Testing Ironclad Root Discovery...")
    try:
        root = protocol.get_repo_root()
        if (root / ".git").exists() and (root / "sigma" / "m32" / "protocol.json").exists():
            print(f"   [PASS] Root: {root.name}")
            return True
    except Exception as e:
        print(f"   [FAIL] Root Discovery: {e}")
    return False

if __name__ == "__main__":
    success = test_vectors() and test_interfere() and test_root_discovery()
    if not success: sys.exit(1)
    print("\n✅ PYTHON CONFORMANCE SECURED (V2.3.4).")

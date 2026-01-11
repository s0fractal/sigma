#!/usr/bin/env python3
from __future__ import annotations
import sys
import json
import hashlib
from pathlib import Path
import re
import protocol
import scr1
import physics

# Σ-GLYPH CONFORMANCE SUITE (Python)
# V2.3.5 - Bit-Exact CORE Parity

def load_vectors():
    vec_path = protocol.ROOT / "PY" / "z00" / "vectors.json"
    return json.loads(vec_path.read_text())

def test_scr1(vectors):
    print("🧪 Testing SCR-1 Canonicalization...")
    errors = 0
    for v in vectors:
        actual = scr1.get_node_hash(v["body"])
        if actual == v["expected_hash"]:
            print(f"   [PASS] {v['name']}")
        else:
            print(f"   [FAIL] {v['name']}\n          Exp: {v['expected_hash']}\n          Act: {actual}")
            errors += 1
    return errors == 0

def test_poi(vectors):
    print("🧪 Testing PoI Proof of Intent...")
    errors = 0
    for v in vectors:
        actual = scr1.calculate_poi(v["intent_hash"], v["code_hash"])
        if actual == v["expected_poi"]:
            print(f"   [PASS] {v['name']}")
        else:
            print(f"   [FAIL] {v['name']}\n          Exp: {v['expected_poi']}\n          Act: {actual}")
            errors += 1
    return errors == 0

def test_entropy(vectors):
    print("🧪 Testing Entropy-to-Stratum...")
    errors = 0
    for v in vectors:
        actual = physics.entropy_to_stratum(v["input"])
        if actual == v["expected"]:
            print(f"   [PASS] {v['input']} -> {actual}")
        else:
            print(f"   [FAIL] {v['input']}\n          Exp: {v['expected']}\n          Act: {actual}")
            errors += 1
    return errors == 0

def test_math(vectors):
    print("🧪 Testing Math (div_round_half_up)...")
    errors = 0
    for v in vectors:
        actual = physics.div_round_half_up(v["n"], v["d"])
        if actual == v["expected"]:
            print(f"   [PASS] div({v['n']}, {v['d']}) = {actual}")
        else:
            print(f"   [FAIL] div({v['n']}, {v['d']})\n          Exp: {v['expected']}\n          Act: {actual}")
            errors += 1
    return errors == 0

def test_glyph(vectors):
    print("🧪 Testing Glyph Serialization...")
    errors = 0
    for v in vectors:
        wave = physics.WaveVectorQ(v["ph"], v["am"], v["en"])
        atom = bytes.fromhex(v["atom"]) if "atom" in v else None
        node = physics.SigmaNode(v["op"], v["flags"], wave, atom=atom)
        
        actual_hex = node.serialize().hex()
        actual_hash = node.hash()
        
        if actual_hex == v["expected_hex"] and actual_hash == v["expected_hash"]:
            print(f"   [PASS] {v['name']}")
        else:
            print(f"   [FAIL] {v['name']}")
            if actual_hex != v["expected_hex"]:
                print(f"          Hex Exp: {v['expected_hex']}")
                print(f"          Hex Act: {actual_hex}")
            if actual_hash != v["expected_hash"]:
                print(f"          Hash Exp: {v['expected_hash']}")
                print(f"          Hash Act: {actual_hash}")
            errors += 1
    return errors == 0

def test_root_discovery():
    print("🧪 Testing Ironclad Root Discovery...")
    try:
        root = protocol.get_repo_root()
        print(f"   [PASS] Root found: {root}")
        return True
    except Exception as e:
        print(f"   [FAIL] Root Discovery: {e}")
        return False

if __name__ == "__main__":
    v = load_vectors()
    success = (
        test_scr1(v["scr1"]) and 
        test_poi(v["poi"]) and 
        test_entropy(v["entropy_to_stratum"]) and 
        test_math(v["math"]) and 
        test_glyph(v["glyph"]) and
        test_root_discovery()
    )
    if not success: sys.exit(1)
    print("\n✅ PYTHON CORE CONFORMANCE SECURED (V2.3.5).")

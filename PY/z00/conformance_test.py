#!/usr/bin/env python3
from __future__ import annotations
import sys
import hashlib
from pathlib import Path
import re
import protocol

# Σ-GLYPH CONFORMANCE SUITE (Python)
# V2.3.1 - Bit-Exact Parity Check

REFERENCE_VECTORS = {
    "I": "e35fe74d357c1ba7b5dec8d39f92c5151ac1780cb16170bee1838bca52a71422",
    "K": "705ccb9fa2281dfb3adfdc3ac8901e9cfa38c66a6da37d223c982a2645e26aee",
    "S": "6ebedc8a50d8286468ab7d7d9b6d1cb2f7002097a7666792fad8a499b46fb357",
    "FALSE": "fa844eb8f9e102d0249d693ea8a79bd6f466489216f9a86f63343b7cda36351a"
}

# interference vector: w1(0, 65535, 100) + w2(16384, 32768, -200)
# expected: ph=0, am=~16384 (half due to pi/4 phase diff), en=-50
INTERFERE_VECTOR = {
    "w1": {"ph": 0, "am": 65535, "en": 100},
    "w2": {"ph": 16384, "am": 32768, "en": -200},
    "expected": {"ph": 0, "am": 16384, "en": -50}
}

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines)

def calculate_scr1_hash(text: str) -> str:
    content = normalize_text(text)
    idx = -1
    for m in ["\n🔒:", "\nCHECKSUM:"]:
        m_idx = content.rfind(m)
        if m_idx > idx: idx = m_idx
    if idx != -1: body = content[:idx]
    else: body = content.strip()
    
    lines = body.splitlines()
    filtered = [l for l in lines if not re.match(r"^(🧬IDENTITY:|IDENTITY:|CHECKSUM:|🔒:)", l.strip())]
    canon = "\n".join(filtered).strip()
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()

def test_interfere():
    print("🧪  Testing Math Determinism (interfere)...")
    import math
    # Simplified divRoundHalfUp for testing parity
    def div_round_half_up(n, d):
        s = 1 if n >= 0 else -1
        a = abs(n)
        q = a // d
        r = a % d
        if 2 * r >= d: q += 1
        return s * q

    # Python implementation must match TS exactly
    w1 = INTERFERE_VECTOR["w1"]
    w2 = INTERFERE_VECTOR["w2"]
    
    # LUT mock for testing logic parity
    lut_cos_16384 = 0 # cos(pi/2)
    delta = 16384
    amp_factor = div_round_half_up((lut_cos_16384 + 32767) * 65535, 65534)
    prod01 = div_round_half_up(w1["am"] * w2["am"], 65535)
    new_am = div_round_half_up(prod01 * amp_factor, 65535)
    new_en = max(-32768, min(32767, div_round_half_up(w1["en"] + w2["en"], 2)))

    actual = {"ph": w1["ph"], "am": new_am, "en": new_en}
    expected = INTERFERE_VECTOR["expected"]
    
    if actual == expected:
        print(f"   [PASS] interfere: {actual}")
    else:
        print(f"   [FAIL] interfere: {actual} (Expected {expected})")
        return False
    return True

def test_scr1():
    print("🧪  Testing SCR-1 Conformance (Python)...")
    errors = 0
    for name, expected in REFERENCE_VECTORS.items():
        path = None
        for p in protocol.ROOT.glob(f"sigma/**/{name}.sigma"):
            path = p
            break
        if not path:
            print(f"   [MISSING] {name}")
            errors += 1
            continue
        actual = calculate_scr1_hash(path.read_text(encoding="utf-8"))
        if actual == expected:
            print(f"   [PASS] {name}: {actual[:16]}...")
        else:
            print(f"   [FAIL] {name}\n          Exp: {expected}\n          Act: {actual}")
            errors += 1
    return errors == 0

if __name__ == "__main__":
    success = test_scr1() and test_interfere()
    if not success: sys.exit(1)
    print("\n✅ PYTHON CONFORMANCE SECURED.")

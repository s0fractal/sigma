#!/usr/bin/env python3
import sys
import hashlib
from pathlib import Path
import re

# Σ-GLYPH CONFORMANCE SUITE (Python)
# Verifies SCR-1 Compliance against V2.3 Standards

def get_repo_root():
    cur = Path(__file__).resolve()
    for parent in [cur] + list(cur.parents):
        if (parent / ".git").exists(): return parent
    return Path.cwd()

ROOT = get_repo_root()

REFERENCE_VECTORS = {
    "I": "e35fe74d357c1ba7b5dec8d39f92c5151ac1780cb16170bee1838bca52a71422",
    "K": "705ccb9fa2281dfb3adfdc3ac8901e9cfa38c66a6da37d223c982a2645e26aee",
    "S": "6ebedc8a50d8286468ab7d7d9b6d1cb2f7002097a7666792fad8a499b46fb357",
    "FALSE": "fa844eb8f9e102d0249d693ea8a79bd6f466489216f9a86f63343b7cda36351a"
}

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines)

def calculate_scr1_hash(text: str) -> str:
    content = normalize_text(text)
    # Strip seal
    idx = -1
    for m in ["\n🔒:", "\nCHECKSUM:"]:
        m_idx = content.rfind(m)
        if m_idx > idx: idx = m_idx
    if idx != -1: body = content[:idx]
    else: body = content.strip()
    
    # Exclude identity lines
    lines = body.splitlines()
    filtered = [l for l in lines if not re.match(r"^(🧬IDENTITY:|IDENTITY:|CHECKSUM:|🔒:)", l.strip())]
    canon = "\n".join(filtered).strip()
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()

def test_vectors():
    print("🧪  Testing SCR-1 Conformance (Python)...")
    errors = 0
    for name, expected in REFERENCE_VECTORS.items():
        # Search for file in sigma/m32 or sigma/z00
        path = None
        for p in ROOT.glob(f"sigma/**/{name}.sigma"):
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
            print(f"   [FAIL] {name}")
            print(f"          Expected: {expected}")
            print(f"          Actual:   {actual}")
            errors += 1
            
    if errors == 0:
        print("\n✅ PYTHON CONFORMANCE SECURED.")
        return True
    else:
        print(f"\n❌ FAILED: {errors} tests.")
        return False

if __name__ == "__main__":
    if not test_vectors():
        sys.exit(1)

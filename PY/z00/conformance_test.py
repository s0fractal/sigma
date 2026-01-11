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
import cas
import wire
import collider
import shutil

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

def test_cas(vectors):
    print("🧪 Testing CAS Store...")
    errors = 0
    cas_root = protocol.ROOT / "test_cas"
    if cas_root.exists(): shutil.rmtree(cas_root)
    store = cas.CASStore(cas_root)
    for v in vectors.get("cas", []):
        data = bytes.fromhex(v["data_hex"])
        h = store.put(data)
        if h != v["expected_hash"]:
            print(f"   [FAIL] Put mismatch\n          Exp: {v['expected_hash']}\n          Act: {h}")
            errors += 1
        else:
            print(f"   [PASS] Put {h[:16]} verified.")
        
        checked = store.get(h)
        if checked != data:
            print(f"   [FAIL] Get mismatch for {h}")
            errors += 1
        else:
            print(f"   [PASS] Get {h[:16]} verified.")
    if cas_root.exists(): shutil.rmtree(cas_root)
    return errors == 0

def test_wire(vectors):
    print("🧪 Testing Wire Protocol...")
    errors = 0
    for v in vectors.get("wire", []):
        payload = bytes.fromhex(v["payload_hex"])
        packet = wire.encode_packet(v["type"], payload)
        if packet.hex() != v["expected_packet_hex"]:
            print(f"   [FAIL] Packet encode mismatch\n          Exp: {v['expected_packet_hex']}\n          Act: {packet.hex()}")
            errors += 1
        else:
            print(f"   [PASS] Encode Packet verified.")
        
        ptype, p_payload = wire.decode_packet(packet)
        if ptype != v["type"] or p_payload != payload:
            print(f"   [FAIL] Packet decode mismatch")
            errors += 1
        else:
            print(f"   [PASS] Decode Packet verified.")
    return errors == 0

def test_collider(vectors):
    print("🧪 Testing Harmonization Layer (Collider)...")
    test_root = protocol.ROOT / "PY" / "test_collider"
    if test_root.exists(): shutil.rmtree(test_root)
    test_root.mkdir(parents=True)
    
    # 1. Setup Environment
    for v in vectors.get("collider", []):
        s_path = test_root / v["sigma_path"]
        s_path.parent.mkdir(parents=True, exist_ok=True)
        s_path.write_text(v["sigma_content"], encoding="utf-8")
        
        if v["code_content"] is not None:
            c_path = test_root / v["code_path"]
            c_path.parent.mkdir(parents=True, exist_ok=True)
            c_path.write_text(v["code_content"], encoding="utf-8")
            
    # 2. Run Collider
    results = collider.collide(root=test_root)
    
    status_map = {}
    for r in results:
        name = Path(r.intent_path).name
        status_map[name] = r.status

    errors = 0
    # 3. Verify
    for v in vectors.get("collider", []):
        name = Path(v["sigma_path"]).name
        actual = status_map.get(name)
        if actual == v["expected_status"]:
            print(f"   [PASS] {v['name']} ({name} -> {actual})")
        else:
            print(f"   [FAIL] {v['name']}: Exp {v['expected_status']}, Got {actual}")
            errors += 1

    if test_root.exists(): shutil.rmtree(test_root)
    return errors == 0

if __name__ == "__main__":
    v = load_vectors()
    success = (
        test_scr1(v["scr1"]) and 
        test_poi(v["poi"]) and 
        test_entropy(v["entropy_to_stratum"]) and 
        test_math(v["math"]) and 
        test_glyph(v["glyph"]) and
        test_root_discovery() and
        test_cas(v) and
        test_wire(v) and
        test_collider(v)
    )
    if not success: sys.exit(1)
    print("\n✅ PYTHON CORE CONFORMANCE SECURED (V2.3.5).")

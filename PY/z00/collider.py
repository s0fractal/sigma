#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

import scr1
import protocol
import core_materialize

# Σ-GLYPH COLLIDER (Harmonization Layer)
# V1.0.0 - PROJECTION A1 - Deterministic Proof-of-Intent

@dataclass
class CircleStatus:
    intent_path: str
    code_path: str
    intent_hash: str
    code_hash: str
    poi: str
    status: str  # 🟢, 🟡, 🔴
    details: str

def compute_hash_of_file_content(content: str) -> str:
    """Computes SHA-256 of raw string content (UTF-8)."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def analyze_pair(sigma_path: Path, code_path: Path, code_tag: str) -> CircleStatus:
    # 1. Intent Analysis
    try:
        sigma_content = sigma_path.read_text(encoding="utf-8")
        # Extract the BLOCK for this specific tag to compare logic?
        # PROJECTION A1 Goal: "Hash(Intent) from SCR-1 canonical bytes of .sigma"
        # Wait, SCR-1 is the WHOLE .sigma file canonicalized (minus seal/id).
        # And "Hash(Code) from raw bytes of the generated code file".
        
        # Intent Hash = Hash(SCR-1(sigma_file))
        intent_can = scr1.canonicalize_sigma(sigma_content) # returns bytes
        intent_hash = hashlib.sha256(intent_can).hexdigest()
        
    except Exception as e:
        return CircleStatus(str(sigma_path), str(code_path), "ERROR", "ERROR", "ERROR", "🔴", f"Read Error: {e}")

    # 2. Code Analysis
    if not code_path.exists():
        return CircleStatus(
            intent_path=str(sigma_path),
            code_path=str(code_path),
            intent_hash=intent_hash,
            code_hash="MISSING",
            poi="VOID",
            status="🟡",
            details="Genesis Pending"
        )
    
    try:
        code_content = code_path.read_text(encoding="utf-8")
        code_hash = compute_hash_of_file_content(code_content)
    except Exception as e:
         return CircleStatus(str(sigma_path), str(code_path), intent_hash, "ERROR", "ERROR", "🔴", f"Code Read Error: {e}")

    # 3. PoI and Status
    # But wait! If the code file exists, DOES IT M ATCH what the materializer WOULD produce?
    # The collider checks (Intent <-> Code).
    # If I edit the .sigma file (Intent changes), Hash(Intent) changes.
    # If I don't run materializer, Code file stays old. Hash(Code) stays old.
    # 
    # How do we verify Harmony?
    # We need to know if the Code that IS there is causally linked to the Intent that IS there.
    # Usually this means: Re-materialize in memory and compare?
    # OR: Does the code file contain a PoI seal? 
    # The prompt says: "Computes Proof-of-Intent (PoI) exactly as specified..."
    # "Emits ... circle summary".
    # 
    # If the request implies checking if they are "Synced", then we must know what the code SHOULD be.
    # However, "Harmonization Layer" often implies checking signature chains.
    # 
    # PROJECTION A1 text: "build a verifier that ... Computes Hash(Intent) ... Computes Hash(Code) ... Emits report"
    # It doesn't explicitly say "Check if code content == extract_block(intent)".
    # BUT, 🔴 is "intent changed but code not regenerated".
    # This implies we MUST check content equality or use the PoI embedded in the code (if any).
    # 
    # Since our generated code DO NOT standardly carry a PoI signature yet (only .sigma carries ID/Seal),
    # The only way to detect "intent changed but code not regenerated" is to compare:
    #   A) The code on disk
    #   B) The code that WOULD be generated from the current intent block.
    #
    # Let's verify this assumption.
    # If I verify (Input .sigma) against (Output .py), I must extract the @[py] block from .sigma.
    # If (Output .py) != (Content of @[py]), then 🔴.
    # If they match, then 🟢.
    
    # Let's extract the expected payload.
    expected_payload = core_materialize.extract_block(sigma_content, code_tag)
    
    if expected_payload is None:
        # If no block for this tag, but code exists?
        # Or maybe we shouldn't even look for code if no block?
        # For this collider, we assume we only check pairs where the Intent *defines* the code.
        return CircleStatus(str(sigma_path), str(code_path), intent_hash, code_hash, "VOID", "🟡", "No Block in Intent")

    # Normalize expected payload similarly to how it's written?
    # core_materialize writes: block + "\n"
    expected_code_content = expected_payload + "\n"
    
    # We can also check equality of HASHES.
    expected_code_hash = compute_hash_of_file_content(expected_code_content)

    poi = scr1.calculate_poi(intent_hash, code_hash)

    status = "🟢" if code_hash == expected_code_hash else "🔴"
    details = "Harmonic" if status == "🟢" else "Dissonance: Content Mismatch"

    return CircleStatus(
        intent_path=str(sigma_path),
        code_path=str(code_path),
        intent_hash=intent_hash,
        code_hash=code_hash,
        poi=poi,
        status=status,
        details=details
    )

def collide(root: Path = protocol.ROOT, quiet: bool = False) -> List[CircleStatus]:
    results = []
    
    source_dir = root / "sigma"
    # We only care about .sigma files
    sigma_files = sorted(list(source_dir.glob("**/*.sigma")), key=lambda p: str(p))
    
    for sigma_path in sigma_files:
        # We need to know where it maps.
        # We'll use core_materialize logic for path mapping.
        # But we need to check ALL tags defined in TAG_MAP?
        # The prompt says "Pair discovery is deterministic".
        
        # Let's iterate over TAG_MAP
        for tag, ext in core_materialize.TAG_MAP.items():
            # Does this file HAVE this tag?
            # Optimization: check content first? Or just calculate path?
            # To be strictly correct, we verify pairs that *Should* exist.
            
            # Re-read content to check existence of block? 
            # (analyze_pair re-reads it, which is slow but safe. Let's optimize slightly by reading once if needed, 
            # but for now simplicity > perf).
            
            # Determine equivalent path
            # From core_materialize:
            # entropy = ... -> stratum
            # glyph_id = ...
            # target = ROOT / TAG / stratum / id + ext
            
            try:
                content = sigma_path.read_text(encoding="utf-8")
                block = core_materialize.extract_block(content, tag)
                if block is None:
                    continue # No intent for this fiber
                
                # Calculate Stratum
                import re
                import physics
                phys_match = re.search(r"^🌀:?\s*(-?\d+)", content, re.MULTILINE)
                entropy = int(phys_match.group(1)) if phys_match else 0
                stratum = physics.entropy_to_stratum(entropy)
                
                # Calculate ID
                glyph_id = core_materialize.get_glyph_id(sigma_path)
                
                dim_dir = root / tag.upper()
                code_path = dim_dir / stratum / f"{glyph_id}{ext}"
                
                result = analyze_pair(sigma_path, code_path, tag)
                results.append(result)
                
            except Exception as e:
                # Malformed file?
                results.append(CircleStatus(str(sigma_path), "UNKNOWN", "ERROR", "ERROR", "ERROR", "🔴", f"Discovery Error: {e}"))

    return results

def generate_report(results: List[CircleStatus], output_format: str = "json") -> str:
    if output_format == "json":
        data = [asdict(r) for r in results]
        return json.dumps(data, indent=2)
    else:
        # Human Summary
        lines = []
        lines.append(f"Harmonization Checks: {len(results)}")
        for r in results:
            lines.append(f"{r.status} {Path(r.intent_path).name} -> {Path(r.code_path).name} | PoI: {r.poi[:8]}")
        return "\n".join(lines)

if __name__ == "__main__":
    # Barebones run
    res = collide()
    print(generate_report(res, "human"))

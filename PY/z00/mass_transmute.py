#!/usr/bin/env python3
import os
import re
import sys
import math
from pathlib import Path

# Σ-GLYPH: MASS TRANSMUTATION ENGINE (V2.1)
# Path: /Users/s0fractal/SIGMA/PY/z00/transmute.py

SIGMA_ROOT = Path("/Users/s0fractal/SIGMA")
SOURCE_DIR = SIGMA_ROOT / "sigma"

TEMPLATE = """Σ-GLYPH SEED: {NAME}

---
# === 🧬 IDENTITY ===
🧬: {NAME}
DNA: {DNA}
⚛️: {ATOM}
🎨: {COLOR}

# === ⚖️ PHYSICS (Wave Function) ===
⚙️: {OP}
🚩: {FLAGS}
🌊: {PHASE}
🔊: {AMPLITUDE}
🌀: {ENTROPY}

# === 🔗 GRAVITY (Dependencies) ===
🔗:
  - SATOSHI
---

{BODY}

🌊

@[dna]
{DNA_RAW}

🔒: VALIDATING...
"""

def entropy_to_stratum(entropy: int) -> str:
    if entropy == -1 or entropy == 0: return "z00"
    prefix = "m" if entropy < 0 else "p"
    bucket = math.ceil(abs(entropy) / 1024)
    if bucket > 32: bucket = 32
    return f"{prefix}{int(bucket):02}"

def parse_sigma(path: Path):
    content = path.read_text(encoding="utf-8")
    
    # 🧬 IDENTITY
    name_match = re.search(r"^(?:GLYPH|Σ-GLYPH SEED|🧬):\s*([\w=]+)", content, re.MULTILINE)
    name = name_match.group(1) if name_match else path.stem
    
    dna_match = re.search(r"^(?:🧬DNA|DNA:|🔗|🔗:):\s*\n+((?:\s*(?:-\s*|Ref:\s*)?[\w=]+\n?)*)", content, re.MULTILINE)
    dna_raw = " ".join(dna_match.group(1).split()) if dna_match else name
    
    atom_match = re.search(r"⚛️:\s*([a-fA-F0-9]{64})", content)
    atom = atom_match.group(1) if atom_match else "00"*32
    
    color_match = re.search(r"(?:🎨:|Color:|HEX:)\s*(#[a-fA-F0-9]{6})", content)
    color = color_match.group(1) if color_match else "#FFFFFF"

    # ⚖️ PHYSICS
    physics = {"OP": 0, "FLAGS": 1, "PHASE": 0, "AMPLITUDE": 65535, "ENTROPY": 0}
    symbol_map = {"⚙️": "OP", "🚩": "FLAGS", "🌊": "PHASE", "🔊": "AMPLITUDE", "🌀": "ENTROPY"}
    for sym, key in symbol_map.items():
        m = re.search(f"{sym}:?\\s*(-?\\d+|0x[a-fA-F0-9]+)", content)
        if m: physics[key] = int(m.group(1), 16) if m.group(1).startswith("0x") else int(m.group(1))
    
    # Legacy Physics Fallback
    if re.search(r"⚖️PHYSICS:", content):
        for k in physics:
            m = re.search(f"{k}:\\s*(-?\\d+|0x[a-fA-F0-9]+)", content)
            if m: physics[k] = int(m.group(1), 16) if m.group(1).startswith("0x") else int(m.group(1))

    # 📜 BODY
    # Extract everything after the first --- block and before the last @[dna] or CHECKSUM
    parts = content.split("---")
    if len(parts) >= 3:
        body = parts[2].split("🌊")[0].strip()
        # Clean body of legacy markers
        body = re.sub(r"🧬 IDENTITY.*?\n", "", body, flags=re.DOTALL)
        body = re.sub(r"⚖️ PHYSICS.*?\n", "", body, flags=re.DOTALL)
        body = re.sub(r"📖 INTENT.*?\n", "", body, flags=re.DOTALL)
        body = re.sub(r"🔗 CONNECTIONS.*?\n", "", body, flags=re.DOTALL)
    else:
        body = content.split("🌊")[0].strip()

    return {
        "NAME": name,
        "DNA": dna_raw,
        "DNA_RAW": dna_raw,
        "ATOM": atom,
        "COLOR": color,
        "OP": physics["OP"],
        "FLAGS": physics["FLAGS"],
        "PHASE": physics["PHASE"],
        "AMPLITUDE": physics["AMPLITUDE"],
        "ENTROPY": physics["ENTROPY"],
        "BODY": body
    }

def main():
    for path in SOURCE_DIR.glob("**/*.sigma"):
        if path.name == "template.sigma": continue
        print(f"Transmuting: {path.relative_to(SOURCE_DIR)}")
        try:
            data = parse_sigma(path)
            stratum = entropy_to_stratum(data["ENTROPY"])
            
            # Renaming logic (Liquidating I=I.sigma etc)
            clean_name = data["NAME"].replace("=", "")
            target_path = SOURCE_DIR / stratum / f"{clean_name}.sigma"
            
            new_content = TEMPLATE.format(**data)
            
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(new_content, encoding="utf-8")
            
            if target_path != path:
                path.unlink()
                print(f"  -> Moved to: {target_path.relative_to(SOURCE_DIR)}")
        except Exception as e:
            print(f"  !! Error: {e}")

if __name__ == "__main__":
    main()

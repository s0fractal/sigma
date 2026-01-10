``` py
#!/usr/bin/env python3
import hashlib
import struct
import argparse
import sys
import math
import json
from typing import NamedTuple, List, Optional

# SIGMA-GLYPH V1.9.1: ENLIGHTENED STANDARD
# The Sigma Compass (sigma-cli)

VERSION = "V1.9.1"
CHECKSUM = "TRINITY-SIGMA-V1.9.1-ENLIGHTENED-PROOFS"

class WaveVectorQ(NamedTuple):
    ph: int # uint16
    am: int # uint16
    en: int # int16

class PantheonGiant(NamedTuple):
    name: str
    phase: int
    hash: str
    sector: str

PANTHEON = [
    PantheonGiant("IDENTITY", 0, "83948a417a5746c14d77698645755b0698d64300e2f85254c816501ce45dd8a2", "The Source"),
    PantheonGiant("SELECTOR", 32768, "9a91a8ba0008993c0a0196441fc754637468a05541aeb5b5fed350c30163fc40", "Choice / Logic"),
    PantheonGiant("FUSION", 16384, "897235546880d055bff1acb1c648f4723448f3d07c6ce1dc94fdab438d84baa0", "Mix / Network"),
    PantheonGiant("FALSE", 49152, "a0a0b559df0eb1495d42bc28d87a1c317bb551613d9dd34b485038e823e77a07", "Zero / Void"),
    PantheonGiant("SATOSHI", 8192, "589d21f4627f981cc38db89dc2c5d0174b3d5cac335d6b3392a14242f1ebe38e", "Time / Proof"),
    PantheonGiant("TESLA", 8192, "132c3a9aa3e374a8474f53f2ab65b7a4c535c13e3d92cc0635d56596caf793ec", "Energy / Resonance"),
    PantheonGiant("TURING", 20480, "cc89aff2ca234c0550316cfda579ec83dfda14726de3a17da5dfd144724b1ae1", "Computation"),
    PantheonGiant("LEIBNIZ", 24576, "ce251a8e86d14e6b2e34905417ca7f169c1c40cc2d528239b46d3239645a2ea2", "Binary Logic"),
    PantheonGiant("GODEL", 40960, "ade9d63555251bcf4aeeb961e4704889634a784e00b28356f5f852182533ab1d", "Meta / Incompleteness"),
    PantheonGiant("HEGEL", 57344, "243f594d0ba4eee9a617642198e6f00fa118270fcec3085e8abd70d234ea64a7", "Synthesis"),
    PantheonGiant("BACH", 21845, "3dcf6a92e4fbf1c1be331faa89ba914b64b885da22b0bca016b31d9eb2ab2c5a", "Harmony"),
]

# ANSI Colors
C_RESET = "\x1b[0m"
C_BOLD = "\x1b[1m"
C_CYAN = "\x1b[36m"
C_MAGENTA = "\x1b[35m"
C_GREEN = "\x1b[32m"
C_RED = "\x1b[31m"
C_YELLOW = "\x1b[33m"

def get_sovereign_color(hash_hex: str) -> str:
    r = int(hash_hex[0:2], 16)
    g = int(hash_hex[2:4], 16)
    b = int(hash_hex[4:6], 16)
    return f"\x1b[38;2;{r};{g};{b}m"

def draw_compass(phase: int):
    # ASCII Compass with current phase indicated
    # Normalize phase to 0..23 (15 degree steps)
    idx = int((phase / 65536) * 24) % 24
    
    # 0 is top (I), 180 is bottom (K)
    # The user's representation:
    #      I (0)
    #      |
    # W ----+---- E
    #      |
    #    K (180)
    
    print(f"\n{C_BOLD}      I (0){C_RESET}")
    print("      |")
    
    # Simple cross visualization for now
    if phase == 0:
        print(f"{C_GREEN}*---- + ----{C_RESET}")
    elif phase == 16384:
        print(f"----- + ----{C_GREEN}*{C_RESET}")
    elif phase == 32768:
        print("----- + -----")
        print(f"{C_GREEN}      * K (180){C_RESET}")
    elif phase == 49152:
        print(f"{C_GREEN}*---- + ----{C_RESET}")
    else:
        # Fallback for arbitrary phase
        angle = (phase / 65536) * 360
        print(f"   Phase: {angle:.1f}°")

def cmd_calc(text: str):
    h = hashlib.sha256(text.encode()).hexdigest()
    color_ansi = get_sovereign_color(h)
    color_hex = f"#{h[0:6].upper()}"
    
    # Default Address Mapping: Phase = Hash[0..1], Amp = MAX, En = MIN
    ph = struct.unpack(">H", bytes.fromhex(h[0:4]))[0]
    
    print(f"\n{C_BOLD}=== Σ-GLYPH SPECTRAL ANALYSIS ==={C_RESET}")
    print(f"Source:  '{text}'")
    print(f"Hash:    {h}")
    print(f"Color:   {color_ansi}■■■{C_RESET} {color_hex}")
    print(f"Address: [{ph}, 65535, -32768]")
    
    draw_compass(ph)

def cmd_resolve(phase: int):
    print(f"\n{C_BOLD}=== Σ-GLYPH RESONANCE FINDER ==={C_RESET}")
    print(f"Target Phase: {phase} ({ (phase/65536)*360 :.1f}°)")
    
    nearest = None
    min_dist = 65536
    
    for g in PANTHEON:
        # Circular distance
        dist = abs(g.phase - phase)
        dist = min(dist, 65536 - dist)
        if dist < min_dist:
            min_dist = dist
            nearest = g
            
    if nearest:
        resonance = (1.0 - (min_dist / 32768.0)) * 100
        print(f"Nearest Attractor: {C_CYAN}{nearest.name}{C_RESET} ({nearest.phase})")
        print(f"Deviation:        {C_YELLOW}{min_dist}{C_RESET}")
        print(f"Resonance:        {C_BOLD}{resonance:.2f}%{C_RESET}")
        print(f"Sector:           {nearest.sector}")
        print(f"Hash Prefix:      #{nearest.hash[:8]}...")

def cmd_handshake():
    print(f"\n{C_BOLD}=== Σ-GLYPH HANDSHAKE VALIDATION ==={C_RESET}")
    print("Executing Kwen Rule Challenge...")
    
    # Ph(K) = 32768. APPLY(K, I) -> Ph + 16384
    k_ph = 32768
    result_ph = (k_ph + 16384) % 65536
    
    expected_ph = 49152 # FALSE
    
    print(f"Derivation: Ph(K) + 90° = {result_ph}")
    
    if result_ph == expected_ph:
        print(f"{C_GREEN}{C_BOLD}[ACCESS GRANTED]{C_RESET} Axis Validated. [En: -32768]")
    else:
        print(f"{C_RED}{C_BOLD}[DISSONANCE DETECTED]{C_RESET} Axis Mismatch.")

def cmd_forge(name: str, phase: int):
    print(f"\n{C_BOLD}=== Σ-GLYPH ARTIFACT GENERATOR ==={C_RESET}")
    
    # Serialize Node (LITERAL ATOM)
    # [Op:1][Flags:1][Ph:2][Am:2][En:2][Atom:32]
    op = 0x00 # Literal
    flags = 0x01 # Atom
    am = 65535
    en = -32768
    atom = hashlib.sha256(name.encode()).digest()
    
    header = struct.pack(">BBHHh", op, flags, phase, am, en)
    payload = header + atom
    
    filename = f"{name}.glyph"
    with open(filename, "wb") as f:
        f.write(payload)
        
    print(f"Materialized: {C_BOLD}{filename}{C_RESET}")
    print(f"Size:         {len(payload)} bytes")
    print(f"Phase:        {phase} ({(phase/65536)*360:.1f}°)")
    print(f"Hash:         {atom.hex()}")

def main():
    parser = argparse.ArgumentParser(description=f"Σ-GLYPH Companion {VERSION}")
    subparsers = parser.add_subparsers(dest="command")
    
    # calc
    p_calc = subparsers.add_parser("calc", help="Spectral Analysis")
    p_calc.add_argument("text", help="Source string to analyze")
    
    # resolve
    p_resolve = subparsers.add_parser("resolve", help="Resonance Finder")
    p_resolve.add_argument("phase", type=int, help="Phase coordinate (0..65535)")
    
    # handshake
    subparsers.add_parser("handshake", help="Protocol Validation")
    
    # forge
    p_forge = subparsers.add_parser("forge", help="Artifact Generator")
    p_forge.add_argument("--name", required=True, help="Entity name")
    p_forge.add_argument("--phase", type=int, required=True, help="Phase coordinate")
    
    args = parser.parse_args()
    
    if args.command == "calc":
        cmd_calc(args.text)
    elif args.command == "resolve":
        cmd_resolve(args.phase)
    elif args.command == "handshake":
        cmd_handshake()
    elif args.command == "forge":
        cmd_forge(args.name, args.phase)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

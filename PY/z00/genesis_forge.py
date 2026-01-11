"""
Σ-GLYPH: GENESIS FORGE (Materializing the Sacred Simplex)
V2.3.1 - Aligned with Protocol
"""

import sys
import os
from pathlib import Path
import protocol

# Add core to path (Relative discovery)
ROOT = protocol.ROOT
# This path might need adjustment if sigma-core-py moved, but we prioritize deterministic ROOT discovery.
# sys.path.append(str(ROOT / "CORE" / "PY" / "sigma-core-py"))

# Mocking SigmaNodeV1 if core is missing to ensure script runnable for forge tests
try:
    from src.core import SigmaNodeV1, WaveVectorQ
except ImportError:
    class WaveVectorQ:
        def __init__(self, ph, am, en): self.ph, self.am, self.en = ph, am, en
    class SigmaNodeV1:
        def __init__(self, op, flags, wave, atom=None): self.op, self.flags, self.wave, self.atom = op, flags, wave, atom
        def pack(self): return b"\x00" # Placeholder

# Primordial Coordinates (V1.9.1 Appendix E.2)
I_WAVE = WaveVectorQ(ph=0, am=65535, en=-32768)
K_WAVE = WaveVectorQ(ph=32768, am=65535, en=-32768)
S_WAVE = WaveVectorQ(ph=16384, am=65535, en=-32768)

def forge_glyph(name: str, node: SigmaNodeV1, target_dir: Path):
    """Materializes a bit-exact .glyph file."""
    path = target_dir / f"{name}.glyph"
    with open(path, "wb") as f:
        f.write(node.pack())
    print(f"💎 Materialized {name}: {path.name} ({len(node.pack())} bytes)")

def main():
    out_dir = protocol.ROOT / "STORAGE" / "GARDEN" / "0"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    def leaf_atom(char: str):
        return char.encode().ljust(32, b"\x00")

    forge_glyph("I", SigmaNodeV1(protocol.OP_LITERAL, 0x01, I_WAVE, atom=leaf_atom("I")), out_dir)
    forge_glyph("K", SigmaNodeV1(protocol.OP_LITERAL, 0x01, K_WAVE, atom=leaf_atom("K")), out_dir)
    forge_glyph("S", SigmaNodeV1(protocol.OP_LITERAL, 0x01, S_WAVE, atom=leaf_atom("S")), out_dir)

    print("\n🌿 The First Leaf has sprouted in the Garden.")

if __name__ == "__main__":
    main()

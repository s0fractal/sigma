from __future__ import annotations
import struct
import hashlib
from typing import Optional
import protocol

# Σ-GLYPH PHYSICS LAYER
# V2.3.4 - Bit-Exact CORE Determinism

def div_round_half_up(n: int, d: int) -> int:
    """Integer division with round-half-up (round-away-from-zero)."""
    if d <= 0: raise ValueError("d must be positive")
    s = -1 if n < 0 else 1
    a = abs(n)
    q = a // d
    r = a % d
    if 2 * r >= d:
        q += 1
    return s * q

def entropy_to_stratum(entropy: int) -> str:
    """Canonical entropy-to-stratum mapping."""
    if entropy == -1: return "z00"
    if entropy == 0: return "m00"
    prefix = "m" if entropy < 0 else "p"
    bucket = abs(entropy) // 1024
    return f"{prefix}{bucket:02}"

class WaveVectorQ:
    def __init__(self, ph: int, am: int, en: int):
        self.ph = ph # uint16
        self.am = am # uint16
        self.en = en # int16

    def __eq__(self, other):
        if not isinstance(other, WaveVectorQ): return False
        return self.ph == other.ph and self.am == other.am and self.en == other.en

class SigmaNode:
    def __init__(self, op: int, flags: int, wave: WaveVectorQ, 
                 atom: Optional[bytes] = None, 
                 left: Optional[bytes] = None, 
                 right: Optional[bytes] = None):
        self.op = op
        self.flags = flags & 0x07 # Only lower 3 bits
        self.wave = wave
        self.atom = atom
        self.left = left
        self.right = right

    def serialize(self) -> bytes:
        """Bit-exact binary serialization (matching Deno)."""
        # Header: op(B), flags(B), ph(H), am(H), en(h) -> 8 bytes, Big-Endian (>)
        data = struct.pack(">BBHHh", self.op, self.flags, self.wave.ph, self.wave.am, self.wave.en)
        
        if self.flags & protocol.F_ATOM:
            if not self.atom or len(self.atom) != 32: raise ValueError("F_ATOM set but atom invalid")
            data += self.atom
        if self.flags & protocol.F_LEFT:
            if not self.left or len(self.left) != 32: raise ValueError("F_LEFT set but left invalid")
            data += self.left
        if self.flags & protocol.F_RIGHT:
            if not self.right or len(self.right) != 32: raise ValueError("F_RIGHT set but right invalid")
            data += self.right
        return data

    @classmethod
    def parse(cls, data: bytes) -> SigmaNode:
        """Parse bit-exact binary representation."""
        if len(data) < 8: raise ValueError("Data too short")
        op, flags, ph, am, en = struct.unpack(">BBHHh", data[:8])
        wave = WaveVectorQ(ph, am, en)
        
        offset = 8
        atom, left, right = None, None, None
        
        if flags & protocol.F_ATOM:
            atom = data[offset:offset+32]
            offset += 32
        if flags & protocol.F_LEFT:
            left = data[offset:offset+32]
            offset += 32
        if flags & protocol.F_RIGHT:
            right = data[offset:offset+32]
            offset += 32
            
        return cls(op, flags, wave, atom, left, right)

    def hash(self) -> str:
        """SHA-256 hex hash of serialized bytes."""
        return hashlib.sha256(self.serialize()).hexdigest()

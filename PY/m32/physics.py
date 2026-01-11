```python
import struct
import hashlib
from typing import Optional
import protocol

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
        data = struct.pack(">BBHHh", self.op, self.flags, self.wave.ph, self.wave.am, self.wave.en)
        if self.flags & protocol.F_ATOM:
            data += self.atom
        if self.flags & protocol.F_LEFT:
            data += self.left
        if self.flags & protocol.F_RIGHT:
            data += self.right
        return data

    def hash(self) -> str:
        return hashlib.sha256(self.serialize()).hexdigest()
```

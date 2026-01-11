import struct
import hashlib
import math
from typing import Optional
import protocol

def div_round_half_up(n: int, d: int) -> int:
    """Integer division with symmetric round-half-up (away from zero)."""
    if d <= 0: raise ValueError("d must be positive")
    s = 1 if n >= 0 else -1
    n_abs = abs(n)
    q_abs = (n_abs + (d // 2)) // d
    return s * q_abs

def clamp_i16(x: int) -> int:
    return max(-32768, min(32767, x))

# Canonical LUT generation (満足 Appendices A.2)
LUT_COS = [round(32767 * math.cos((i * math.pi) / 32768)) for i in range(32769)]
LUT_COS[0] = 32767
LUT_COS[16384] = 0
LUT_COS[32768] = -32767

def interfere(w1: 'WaveVectorQ', w2: 'WaveVectorQ') -> 'WaveVectorQ':
    new_ph = w1.ph
    new_en = clamp_i16(div_round_half_up(w1.en + w2.en, 2))

    x = w1.ph - w2.ph
    d32 = abs(x)
    delta = min(d32, 65536 - d32)

    r = LUT_COS[delta]
    num = (r + 32767) * 65535
    amp_factor = div_round_half_up(num, 65534)

    prod01 = div_round_half_up(w1.am * w2.am, 65535)
    new_am = div_round_half_up(prod01 * amp_factor, 65535)

    return WaveVectorQ(new_ph, int(new_am), new_en)

def entropy_to_stratum(entropy: int) -> str:
    """Canonical entropy-to-stratum mapping."""
    if entropy == -1 or entropy == 0: return "z00"
    prefix = "m" if entropy < 0 else "p"
    bucket = abs(entropy) // 1024
    if bucket > 32: bucket = 32
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

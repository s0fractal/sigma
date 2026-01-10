import struct
from typing import NamedTuple, Optional

class WaveVectorQ(NamedTuple):
    ph: int # uint16
    am: int # uint16
    en: int # int16

def div_round_half_up(n: int, d: int) -> int:
    """
    Integer division with round-half-up (MUST).
    Semantics: round-half-away-from-zero.
    
    MUST: d MUST be > 0. Behavior for d <= 0 is undefined (implementation fault).
    MUST: Implementations MUST promote n to a wider signed type before negation 
          to avoid overflow (e.g., -(-32768)). Python handles this natively with arbitrary precision ints.
    MUST: Promotion width MUST be at least 64-bit (equivalent).
    Note: div_round_half_up(0, d) == 0; result sign follows n (away-from-zero for ties).
    """
    if d <= 0:
        raise ValueError(f"System Fault: div_round_half_up divisor MUST be positive (d={d})")
    
    # Python integers are arbitrary precision, so overflow on -(-32768) is impossible.
    s = -1 if n < 0 else 1
    a = abs(n)
    
    q = a // d
    r = a % d
    
    if 2 * r >= d:
        q += 1
        
    return s * q

def clamp_i16(x: int) -> int:
    """Clamps result to i16 range (Section 3.1)."""
    if x < -32768:
        return -32768
    if x > 32767:
        return 32767
    return x

class SigmaNodeV1:
    """
    SigmaNodeV1 Canonical Structure (MUST)
    Layout: [Op:1][Flags:1][Ph:2][Am:2][En:2][Atom?:32][Left?:32][Right?:32]
    """
    def __init__(self, op: int, flags: int, wave: WaveVectorQ, atom: Optional[bytes] = None, left: Optional[bytes] = None, right: Optional[bytes] = None):
        self.op = op
        self.flags = flags
        self.wave = wave
        self.atom = atom
        self.left = left
        self.right = right

    def pack(self) -> bytes:
        # Header: Op(B), Flags(B), Ph(H), Am(H), En(h)
        # > Big-endian
        header = struct.pack(">BBHHh", self.op, self.flags & 0x07, self.wave.ph, self.wave.am, self.wave.en)
        
        body = b""
        if self.atom: body += self.atom
        if self.left: body += self.left
        if self.right: body += self.right
        
        return header + body

    @classmethod
    def unpack(cls, data: bytes):
        if len(data) < 8:
            raise ValueError("Buffer too short for SigmaNodeV1 header")
            
        op, flags, ph, am, en = struct.unpack(">BBHHh", data[:8])
        wave = WaveVectorQ(ph, am, en)
        
        ptr = 8
        atom = None
        left = None
        right = None
        
        if flags & 0x01: # F_ATOM
            atom = data[ptr:ptr+32]
            ptr += 32
        if flags & 0x02: # F_LEFT
            left = data[ptr:ptr+32]
            ptr += 32
        if flags & 0x04: # F_RIGHT
            right = data[ptr:ptr+32]
            ptr += 32
            
        return cls(op, flags, wave, atom, left, right)

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
    """Canonical entropy-to-stratum mapping with clamping."""
    entropy = clamp_i16(entropy) # Forced clamp per spec
    if entropy == -1 or entropy == 0: return "z00"
    prefix = "m" if entropy < 0 else "p"
    bucket = abs(entropy) // 1024
    if bucket > 32: bucket = 32
    return f"{prefix}{bucket:02}"

def extract_block(text: str, tag: str) -> str | None:
    """SCR-1: Strict Canonical Block Extraction."""
    import re
    content = text.replace("\r\n", "\n").replace("\r", "\n")
    start_marker = f"@[{tag}]"
    
    parts = re.split(f"^{re.escape(start_marker)}\\n", content, flags=re.MULTILINE)
    if len(parts) < 2: return None
    
    payload_raw = parts[1]
    # End search: next block or seal
    end_match = re.search(r"^\n(@\[|🔒:|CHECKSUM:)", payload_raw, re.MULTILINE)
    payload = payload_raw[:end_match.start()] if end_match else payload_raw
    
    return payload.strip("\n")

def parse_physics(text: str) -> dict:
    """Parses standard physics metadata from sigma content."""
    import re
    physics = {"OP": 0, "FLAGS": 0, "PHASE": 0, "AMPLITUDE": 0, "ENTROPY": 0}
    symbol_map = {"⚙️": "OP", "🚩": "FLAGS", "🌊": "PHASE", "🔊": "AMPLITUDE", "🌀": "ENTROPY"}
    for sym, key in symbol_map.items():
        match = re.search(f"^{sym}:?\\s*(-?\\d+|0x[a-fA-F0-9]+)", text, re.MULTILINE)
        if match:
            val = match.group(1)
            try:
                physics[key] = int(val, 16) if val.startswith("0x") else int(val)
            except: continue
    return physics

def parse_yaml_metadata(text: str) -> dict:
    """Standardized metadata extraction for @[yaml] blocks."""
    data = {}
    if not text: return data
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line or ":" not in line: continue
        key, val = line.split(":", 1)
        data[key.strip().upper()] = val.strip().strip("'\"")
    return data

def get_glyph_id(path) -> str:
    """Extracts Glyph Identity from file content or filename fallback."""
    import re
    from pathlib import Path
    if not isinstance(path, Path):
        path = Path(path)
    try:
        content = path.read_text(encoding="utf-8")
        match = re.search(r"^(?:🧬|GLYPH|Σ-GLYPH SEED):\s*([\w=]+)", content, re.MULTILINE)
        if match: return match.group(1)
    except: pass
    return path.stem

def from_physics_metadata(phys: dict, atom: bytes = None) -> 'SigmaNode':
    """Creates SigmaNode from PHYSICS block metadata for deterministic glyph materialization."""
    wave = WaveVectorQ(
        ph=phys.get("PHASE", 0),
        am=phys.get("AMPLITUDE", 65535),
        en=phys.get("ENTROPY", 0)
    )
    return SigmaNode(
        op=phys.get("OP", 0),
        flags=phys.get("FLAGS", 0),
        wave=wave,
        atom=atom,
        left=None,
        right=None
    )

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

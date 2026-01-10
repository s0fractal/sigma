"""
Σ-GLYPH V1.9.1: Interference & Resonance Logic
Reference Implementation (Python)
"""

import math
from typing import NamedTuple
from .core import div_round_half_up, clamp_i16

class WaveVectorQ(NamedTuple):
    ph: int # uint16
    am: int # uint16
    en: int # int16

# Canonical LUT generation (Appendices A.2)
# 32769 entries (0..32768)
LUT_COS = [0] * 32769
for i in range(32769):
    # Fixed-point cosine mapping: 32767 * cos(i * pi / 32768)
    # We use round() for the initial generation, then enforce anchors.
    val = round(32767 * math.cos((i * math.pi) / 32768))
    LUT_COS[i] = val

# Enforce Bit-Exact Anchors (MUST)
LUT_COS[0] = 32767
LUT_COS[16384] = 0
LUT_COS[32768] = -32767

def interfere(w1: WaveVectorQ, w2: WaveVectorQ) -> WaveVectorQ:
    """
    Calculates the interference of two waves (MUST).
    Bit-exact parity with V1.9.1 engine.
    """
    # 1. New Phase: Dominant phase (currently w1)
    new_ph = w1.ph
    
    # 2. New Entropy: Arithmetic mean of entropies
    new_en = clamp_i16(div_round_half_up(w1.en + w2.en, 2))
    
    # 3. Resonance Calculation
    # Delta: Toroidal phase difference [0..32768]
    x = w1.ph - w2.ph
    d32 = abs(x)
    delta = min(d32, 65536 - d32)
    
    # Resonance Factor: derived from LUT_COS
    r = LUT_COS[delta]
    # amp_factor = ((r + 32767) * 65535) / 65534
    num = (r + 32767) * 65535
    amp_factor = div_round_half_up(num, 65534)
    
    # 4. New Amplitude
    # am_new = ((am1 * am2 / 65535) * amp_factor) / 65535
    prod01 = div_round_half_up(w1.am * w2.am, 65535)
    new_am = div_round_half_up(prod01 * amp_factor, 65535)
    
    return WaveVectorQ(
        ph=int(new_ph),
        am=int(new_am),
        en=int(new_en)
    )

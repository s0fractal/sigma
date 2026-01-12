# Binary .qwave Format Specification

**Version**: 1.0\
**Purpose**: Deterministic quantum record serialization\
**Philosophy**: `.qwave` as primary, `.sigma` as projection

---

## Design Principles

1. **Fixed-point arithmetic** - No floats, only integers
2. **Bit-exact determinism** - Same input → same bytes
3. **Compatible with WaveVectorQ** - Can convert losslessly
4. **Compact** - Minimal overhead
5. **Extensible** - Version field for future upgrades

---

## Binary Layout

### Header (32 bytes)

```
Offset | Size | Type   | Field          | Description
-------|------|--------|----------------|---------------------------
0      | 4    | u8[4]  | magic          | "QWAV" (0x51574156)
4      | 2    | u16    | version        | Format version (0x0100 = 1.0)
6      | 2    | u16    | flags          | Feature flags
8      | 8    | u64    | glyph_id_hash  | SHA-256 hash of glyph_id (first 8 bytes)
16     | 8    | u64    | block_height   | Bitcoin block height (anchor)
24     | 8    | u64    | timestamp      | Unix timestamp (creation)
```

### WaveVectorK (16 bytes)

```
Offset | Size | Type   | Field          | Description
-------|------|--------|----------------|---------------------------
0      | 2    | u16    | theta          | Poloidal angle (0..65535 → 0..2π)
2      | 2    | u16    | phi            | Toroidal angle (0..65535 → 0..2π)
4      | 2    | u16    | amplitude      | Wave amplitude (0..65535)
6      | 2    | i16    | entropy        | Entropy level (-32768..32767)
8      | 2    | i16    | omega_theta    | Angular velocity θ (quantized)
10     | 2    | i16    | omega_phi      | Angular velocity φ (quantized)
12     | 4    | u32    | reserved       | Reserved for future use
```

### Trajectory Ensemble (variable)

```
Offset | Size | Type   | Field          | Description
-------|------|--------|----------------|---------------------------
0      | 2    | u16    | count          | Number of trajectories (0..65535)
2      | N*10 | -      | trajectories   | Array of TrajectoryPoint
```

### TrajectoryPoint (10 bytes each)

```
Offset | Size | Type   | Field          | Description
-------|------|--------|----------------|---------------------------
0      | 2    | u16    | theta          | Poloidal angle
2      | 2    | u16    | phi            | Toroidal angle
4      | 2    | u16    | weight         | Probability weight (0..65535 → 0..1)
6      | 4    | u32    | reserved       | Reserved
```

### Footer (32 bytes)

```
Offset | Size | Type   | Field          | Description
-------|------|--------|----------------|---------------------------
0      | 32   | u8[32] | checksum       | SHA-256 of entire record (excluding this field)
```

---

## Total Size

```
Minimum (no trajectories):
  Header:     32 bytes
  WaveVectorK: 16 bytes
  Ensemble:    2 bytes (count=0)
  Footer:     32 bytes
  Total:      82 bytes

With N trajectories:
  Total: 82 + (N * 10) bytes
```

---

## Conversion Formulas

### Angles (u16 ↔ radians)

```python
# Encode: radians → u16
def encode_angle(radians: float) -> int:
    """Convert 0..2π to 0..65535"""
    normalized = radians % (2 * math.pi)
    return int((normalized / (2 * math.pi)) * 65536) & 0xFFFF

# Decode: u16 → radians
def decode_angle(value: int) -> float:
    """Convert 0..65535 to 0..2π"""
    return (value / 65536) * 2 * math.pi
```

### Angular Velocity (i16 ↔ rad/block)

```python
# Quantization: 1 unit = 2π/65536 rad/block ≈ 0.0001 rad/block
OMEGA_SCALE = 2 * math.pi / 65536

# Encode: rad/block → i16
def encode_omega(omega: float) -> int:
    """Convert angular velocity to i16"""
    quantized = int(omega / OMEGA_SCALE)
    return max(-32768, min(32767, quantized))

# Decode: i16 → rad/block
def decode_omega(value: int) -> float:
    """Convert i16 to angular velocity"""
    return value * OMEGA_SCALE
```

### Weight (u16 ↔ probability)

```python
# Encode: 0..1 → u16
def encode_weight(weight: float) -> int:
    """Convert probability to u16"""
    return int(weight * 65535) & 0xFFFF

# Decode: u16 → 0..1
def decode_weight(value: int) -> float:
    """Convert u16 to probability"""
    return value / 65535
```

---

## Compatibility with WaveVectorQ

### Q → K (lossless)

```python
def q_to_k_binary(wave_q: WaveVectorQ) -> bytes:
    """Convert WaveVectorQ to binary WaveVectorK."""
    # phase (0..65535) → phi (u16) - direct copy
    phi = wave_q.phase
    
    # entropy (-32768..32767) → theta (u16)
    # Map: -32..+32 → 0..65535
    normalized_entropy = wave_q.entropy / 1024  # -32..+32
    theta = int(((normalized_entropy + 32) / 64) * 65536) & 0xFFFF
    
    # amplitude - direct copy
    amplitude = wave_q.amplitude
    
    # entropy - direct copy
    entropy = wave_q.entropy
    
    # omega - default to 0
    omega_theta = 0
    omega_phi = 0
    
    return struct.pack(
        '<HHHhhhI',  # Little-endian
        theta, phi, amplitude, entropy,
        omega_theta, omega_phi, 0  # reserved
    )
```

### K → Q (lossless)

```python
def k_to_q_binary(data: bytes) -> WaveVectorQ:
    """Convert binary WaveVectorK to WaveVectorQ."""
    theta, phi, amplitude, entropy, omega_theta, omega_phi, _ = struct.unpack(
        '<HHHhhhI', data
    )
    
    # phi (u16) → phase (0..65535) - direct copy
    phase = phi
    
    return WaveVectorQ(
        phase=phase,
        amplitude=amplitude,
        entropy=entropy
    )
```

---

## Example: Minimal .qwave File

```python
import struct
import hashlib

def create_minimal_qwave(glyph_id: str, wave_k: WaveVectorK) -> bytes:
    """Create minimal .qwave file (no trajectories)."""
    
    # Header
    magic = b'QWAV'
    version = 0x0100
    flags = 0x0000
    glyph_hash = hashlib.sha256(glyph_id.encode()).digest()[:8]
    block_height = 0
    timestamp = int(time.time())
    
    header = struct.pack(
        '<4sHHQQQ',
        magic, version, flags,
        int.from_bytes(glyph_hash, 'little'),
        block_height, timestamp
    )
    
    # WaveVectorK
    wave_data = struct.pack(
        '<HHHhhhI',
        encode_angle(wave_k.theta),
        encode_angle(wave_k.phi),
        wave_k.amplitude,
        wave_k.entropy,
        encode_omega(wave_k.omega_theta),
        encode_omega(wave_k.omega_phi),
        0  # reserved
    )
    
    # Ensemble (empty)
    ensemble = struct.pack('<H', 0)  # count = 0
    
    # Calculate checksum
    body = header + wave_data + ensemble
    checksum = hashlib.sha256(body).digest()
    
    return body + checksum

# Usage
wave = WaveVectorK(
    theta=math.pi/2,
    phi=math.pi/4,
    amplitude=32768,
    entropy=0,
    omega_theta=0.1,
    omega_phi=0.05
)

qwave_bytes = create_minimal_qwave("TEST_GLYPH", wave)
# Result: 82 bytes, bit-exact, deterministic
```

---

## Advantages

1. **Deterministic**: Same input → same bytes (no float rounding)
2. **Compact**: 82 bytes minimum vs ~500 bytes JSON
3. **Fast**: Binary parsing vs JSON parsing
4. **Compatible**: Lossless Q ↔ K conversion
5. **Extensible**: Version + flags + reserved fields

---

## Next Steps

1. Implement `qwave_codec.py` (encode/decode)
2. Update `quantum_record.py` to use binary format
3. Add to Akasha CAS (content-addressed storage)
4. Integrate with materializer

---

**This is the foundation for `.qwave` as primary, `.sigma` as projection!** 🌀

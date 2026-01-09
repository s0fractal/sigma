/**
 * Σ-GLYPH Core Architecture Implementation (RFC v0.2.12 - Refined)
 * Bit-Exact Determinism Reference
 */

export enum OpCode {
  LITERAL = 0x00,
  REF = 0x01,
  APPLY = 0x02,
  LAMBDA = 0x03,
  DISSONANCE = 0xff,
}

export enum Flags {
  F_ATOM = 0x01,
  F_LEFT = 0x02,
  F_RIGHT = 0x04,
}

export interface WaveVectorQ {
  ph: number; // uint16
  am: number; // uint16
  en: number; // int16
}

export interface SigmaNode {
  op: OpCode;
  flags: number;
  wave: WaveVectorQ;
  atom?: Uint8Array;  // 32 bytes
  left?: Uint8Array;  // 32 bytes
  right?: Uint8Array; // 32 bytes
}

// --- Math & LUT ---

/**
 * Integer division with round-half-up (round-away-from-zero).
 * MUST handle signed n correctly as per RFC 3.1.
 */
export function divRoundHalfUp(n: bigint, d: bigint): bigint {
  if (d <= 0n) throw new Error("d must be positive");
  const s = n < 0n ? -1n : 1n;
  const a = n < 0n ? -n : n;
  let q = a / d;
  const r = a % d;
  if (2n * r >= d) {
    q = q + 1n;
  }
  return s * q;
}

export function clampI16(x: number): number {
  return Math.max(-32768, Math.min(32767, x));
}

// Canonical LUT generation (満足 Appendices A.2)
const LUT_COS = new Int16Array(32769);
for (let i = 0; i <= 32768; i++) {
  LUT_COS[i] = Math.round(32767 * Math.cos((i * Math.PI) / 32768));
}
// Enforce anchors (MUST)
LUT_COS[0] = 32767;
LUT_COS[16384] = 0;
LUT_COS[32768] = -32767;

export function interfere(w1: WaveVectorQ, w2: WaveVectorQ): WaveVectorQ {
  const new_ph = w1.ph;

  // Promotion to int32 (Number handles this for 16-bit inputs)
  const en1 = BigInt(w1.en);
  const en2 = BigInt(w2.en);
  const new_en = clampI16(Number(divRoundHalfUp(en1 + en2, 2n)));

  // Delta calculation (manual abs/toroidal min)
  const x = Number(w1.ph) - Number(w2.ph); // Promotion to int32
  const d32 = Math.abs(x);
  const delta = Math.min(d32, 65536 - d32);

  // Resonance
  const r = BigInt(LUT_COS[delta]); // Promotion to int32
  const num = (r + 32767n) * 65535n; // Promotion to int64
  const amp_factor = divRoundHalfUp(num, 65534n); // 0..65535 (uint16 domain)

  // Amplitude
  const prod01 = divRoundHalfUp(BigInt(w1.am) * BigInt(w2.am), 65535n); // Promotion to uint64
  const new_am = divRoundHalfUp(prod01 * amp_factor, 65535n);

  return {
    ph: new_ph,
    am: Number(new_am),
    en: Number(new_en),
  };
}

// --- Serialization ---

export function serializeNode(node: SigmaNode): Uint8Array {
  const popcount = (n: number) => {
    let count = 0;
    while (n > 0) {
      if (n & 1) count++;
      n >>= 1;
    }
    return count;
  };

  const expected_len = 8 + 32 * popcount(node.flags & 0x07);
  const buf = new Uint8Array(expected_len);
  const dv = new DataView(buf.buffer);

  dv.setUint8(0, node.op);
  dv.setUint8(1, node.flags & 0x07);
  dv.setUint16(2, node.wave.ph, false); // Big-Endian
  dv.setUint16(4, node.wave.am, false);
  dv.setInt16(6, node.wave.en, false);

  let offset = 8;
  if (node.flags & Flags.F_ATOM) {
    if (!node.atom) throw new Error("F_ATOM set but atom missing");
    buf.set(node.atom, offset);
    offset += 32;
  }
  if (node.flags & Flags.F_LEFT) {
    if (!node.left) throw new Error("F_LEFT set but left missing");
    buf.set(node.left, offset);
    offset += 32;
  }
  if (node.flags & Flags.F_RIGHT) {
    if (!node.right) throw new Error("F_RIGHT set but right missing");
    buf.set(node.right, offset);
    offset += 32;
  }

  return buf;
}

export async function hashNode(node: SigmaNode): Promise<Uint8Array> {
  const bytes = serializeNode(node);
  const hashBuffer = await crypto.subtle.digest("SHA-256", bytes.buffer as ArrayBuffer);
  return new Uint8Array(hashBuffer);
}

export function toHex(bytes: Uint8Array): string {
  return Array.from(bytes)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

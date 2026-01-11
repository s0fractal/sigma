/**
 * Σ-GLYPH Core Architecture Implementation (RFC v0.2.12 - Refined)
 * Bit-Exact Determinism Reference
 * V2.3.1 - Aligned with protocol.json
 */

import protocolData from "../../sigma/m32/protocol.json" with { type: "json" };

export enum OpCode {
  LITERAL = protocolData.OPCODES.LITERAL,
  REF = protocolData.OPCODES.REF,
  APPLY = protocolData.OPCODES.APPLY,
  LAMBDA = protocolData.OPCODES.LAMBDA,
  DISSONANCE = protocolData.OPCODES.DISSONANCE,
}

export enum Flags {
  F_ATOM = protocolData.FLAGS.F_ATOM,
  F_LEFT = protocolData.FLAGS.F_LEFT,
  F_RIGHT = protocolData.FLAGS.F_RIGHT,
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
  return Math.max(protocolData.WAVE_LIMITS.EN_MIN, Math.min(protocolData.WAVE_LIMITS.EN_MAX, x));
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

  const en1 = BigInt(w1.en);
  const en2 = BigInt(w2.en);
  const new_en = clampI16(Number(divRoundHalfUp(en1 + en2, 2n)));

  const x = Number(w1.ph) - Number(w2.ph);
  const d32 = Math.abs(x);
  const delta = Math.min(d32, 65536 - d32);

  const r = BigInt(LUT_COS[delta]);
  const num = (r + 32767n) * 65535n;
  const amp_factor = divRoundHalfUp(num, 65534n);

  const prod01 = divRoundHalfUp(BigInt(w1.am) * BigInt(w2.am), 65535n);
  const new_am = divRoundHalfUp(prod01 * amp_factor, 65535n);

  return {
    ph: new_ph,
    am: Number(new_am),
    en: Number(new_en),
  };
}

export function entropyToStratum(entropy: number): string {
  if (entropy === -1) return "z00";
  if (entropy === 0) return "m00";
  const prefix = entropy < 0 ? "m" : "p";
  const bucket = Math.floor(Math.abs(entropy) / 1024);
  return `${prefix}${bucket.toString().padStart(2, "0")}`;
}

/**
 * Ironclad repository root discovery in TypeScript.
 */
export function getRepoRoot(): string {
  const envRoot = Deno.env.get("SIGMA_ROOT") || Deno.env.get("SIGMA_GARDEN");
  if (envRoot) return envRoot;

  // Search upwards for .git and protocol.json
  let curr = Deno.cwd();
  while (true) {
    try {
      const gitDir = `${curr}/.git`;
      const protocolFile = `${curr}/sigma/m32/protocol.json`;
      Deno.statSync(gitDir);
      Deno.statSync(protocolFile);
      return curr;
    } catch {
      const parent = curr.substring(0, curr.lastIndexOf("/"));
      if (!parent || parent === curr) break;
      curr = parent;
    }
  }
  throw new Error("Σ-GLYPH FATAL: Repository root discovery failed. Set SIGMA_ROOT.");
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

export function parseNode(data: Uint8Array): SigmaNode {
  const dv = new DataView(data.buffer, data.byteOffset, data.byteLength);
  const op = dv.getUint8(0) as OpCode;
  const flags = dv.getUint8(1);
  const wave: WaveVectorQ = {
    ph: dv.getUint16(2, false),
    am: dv.getUint16(4, false),
    en: dv.getInt16(6, false),
  };

  const node: SigmaNode = { op, flags, wave };
  let offset = 8;
  if (flags & Flags.F_ATOM) {
    node.atom = data.slice(offset, offset + 32);
    offset += 32;
  }
  if (flags & Flags.F_LEFT) {
    node.left = data.slice(offset, offset + 32);
    offset += 32;
  }
  if (flags & Flags.F_RIGHT) {
    node.right = data.slice(offset, offset + 32);
    offset += 32;
  }
  return node;
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

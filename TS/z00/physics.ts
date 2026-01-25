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
  F_V2 = 0x08,       // 10-byte header (Toroidal)
  F_PORTAL = 0x10,   // Portal Witness (p->m transition)
  F_INCOMPLETE = 0x20, // Incomplete Projection (missing op/context)
}

export enum Season {
  DEEP_CLEAN = 0,
  SPECTRAL_SCAN = 1,
  SAP_FLOW = 2,
  FORK_CONTROL = 3,
  EMERGENCE = 4,
  QUIET = 5
}

export interface WaveVectorQ {
  theta1: number; // uint16: Resonance Angle (External/Time)
  theta2: number; // uint16: Morphism Angle (Internal/Transformation)
  prob: number;   // uint16: Probability [0...65535 -> 0...1.0]
  en: number;     // int16: Structural entropy (determines nested depth)
}

export function divRoundHalfUp(n: bigint, d: bigint): bigint {
  if (d <= 0n) throw new Error("d must be positive");
  let s = 1n;
  if (n < 0n) {
      s = -1n;
      n = -n;
  }
  const half = d / 2n;
  return s * ((n + half) / d);
}

export function clampI16(x: number): number {
  return Math.max(-32768, Math.min(32767, x));
}

export interface SigmaNode {
  op: number;
  flags: number;
  wave: WaveVectorQ;
  atom?: Uint8Array;
  left?: Uint8Array;
  right?: Uint8Array;
}

export function wrapDeltaU16(a: number, b: number): number {
  const d = Math.abs(a - b);
  return Math.min(d, 65536 - d);
}

export function circularMean(a: number, b: number): number {
  // Use sin/cos for proper wrap-around averaging on T1
  const s = Math.sin((a * Math.PI) / 32768) + Math.sin((b * Math.PI) / 32768);
  const c = Math.cos((a * Math.PI) / 32768) + Math.cos((b * Math.PI) / 32768);
  let angle = (Math.atan2(s, c) * 32768) / Math.PI;
  if (angle < 0) angle += 65536;
  return Math.round(angle) % 65536;
}

/**
 * Toroidal Distance on T^2 (normalized to [0...32768])
 */
export function toroidalDistance(w1: WaveVectorQ, w2: WaveVectorQ): number {
  const d1 = wrapDeltaU16(w1.theta1, w2.theta1);
  const d2 = wrapDeltaU16(w1.theta2, w2.theta2);
  return Math.sqrt(d1 * d1 + d2 * d2);
}

/**
 * Bayesian Probability Integration (Log-Odds)
 * P = (p1*p2) / (p1*p2 + (1-p1)*(1-p2))
 */
export function integrateProb(p1: number, p2: number): number {
  if (p1 === 0 || p2 === 0) return 0;
  if (p1 === 65535 || p2 === 65535) return 65535;

  const v1 = p1 / 65535;
  const v2 = p2 / 65535;
  const den = v1 * v2 + (1 - v1) * (1 - v2);
  if (den === 0) return 32768; // Undefined case
  const P = (v1 * v2) / den;
  return Math.round(P * 65535);
}

export function interfere(w1: WaveVectorQ, w2: WaveVectorQ): WaveVectorQ {
  const dist1 = wrapDeltaU16(w1.theta1, w2.theta1);
  const dist2 = wrapDeltaU16(w1.theta2, w2.theta2);
  
  // Angular Coherence: 1.0 at dist=0, 0.0 at dist=32768
  // We use a cosine-like falloff or linear falloff. 
  // For a rigorous torus, we use the average coherence.
  const coherence = ( (32768 - dist1) / 32768 ) * ( (32768 - dist2) / 32768 );
  
  const new_en = clampI16(Number(divRoundHalfUp(BigInt(w1.en) + BigInt(w2.en), 2n)));
  const bayes_prob = integrateProb(w1.prob, w2.prob);
  
  // Final probability is Bayesian integrated prob weighted by angular coherence
  const new_prob = Math.round(bayes_prob * coherence);

  const new_theta1 = circularMean(w1.theta1, w2.theta1);
  const new_theta2 = circularMean(w1.theta2, w2.theta2);

  return { theta1: new_theta1, theta2: new_theta2, prob: new_prob, en: new_en };
}

/**
 * Converts entropy into a nested 'Raukuška' path (Mollusk Shell).
 * Higher invariance (lower entropy) leads to deeper nesting.
 */
export function entropyToStratum(entropy: number): string {
  if (entropy === 0) return "z00";
  
  const prefix = entropy < 0 ? "m" : "p";
  const absEn = Math.abs(entropy);
  let depth = Math.floor(absEn / 1024);
  if (depth > 32) depth = 32;

  const pathParts: string[] = [prefix];
  
  // Build hierarchical path: e.g. p/32/31/30...
  // In our toroidal model, p-layers go p/32 -> p/01 (Chaos sifting)
  // m-layers go m/01 -> m/32 (Crystal deepening)
  if (prefix === "p") {
    for (let i = 32; i >= 32 - depth; i--) {
      pathParts.push(i.toString().padStart(2, "0"));
    }
  } else {
    for (let i = 1; i <= depth; i++) {
      pathParts.push(i.toString().padStart(2, "0"));
    }
  }
  
  return pathParts.join("/");
}

export function serializeNode(node: SigmaNode): Uint8Array {
  const popcount = (n: number) => {
    let count = 0;
    while (n > 0) {
      if (n & 1) count++;
      n >>= 1;
    }
    return count;
  };
  
  // Ensure F_V2 is set for 10-byte headers to prevent corruption
  node.flags |= Flags.F_V2;
  
  // Apply Portal Witness if transitioned to m-stratum
  if (node.wave.en < 0) {
    node.flags |= Flags.F_PORTAL;
  }

  const expected_len = 10 + 32 * popcount(node.flags & 0x07);
  const buf = new Uint8Array(expected_len);
  const dv = new DataView(buf.buffer);
  dv.setUint8(0, node.op);
  dv.setUint8(1, node.flags); // Include V2 and Portal flags
  dv.setUint16(2, node.wave.theta1, false);
  dv.setUint16(4, node.wave.theta2, false);
  dv.setUint16(6, node.wave.prob, false);
  dv.setInt16(8, node.wave.en, false);
  let offset = 10;
  if (node.flags & 0x01) { buf.set(node.atom!, offset); offset += 32; }
  if (node.flags & 0x02) { buf.set(node.left!, offset); offset += 32; }
  if (node.flags & 0x04) { buf.set(node.right!, offset); offset += 32; }
  return buf;
}

export function toHex(bytes: Uint8Array): string {
  return Array.from(bytes).map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Σ-PoI: d5ebf99a5638bd2bee1171b0641f31434e00846f7fcbdb3aeefc17871608a2c5

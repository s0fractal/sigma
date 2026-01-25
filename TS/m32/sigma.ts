/**
 * Σ-GLYPH Core Architecture Implementation (RFC v0.2.12 - Refined)
 * Bit-Exact Determinism Reference
 * V2.4.0 - Core Determinism Stabilization
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
  theta1: number; // uint16: Resonance Angle (External/Time)
  theta2: number; // uint16: Morphism Angle (Internal/Transformation)
  prob: number;   // uint16: Probability (Density of reality)
  en: number;     // int16: Structural entropy (determines nested depth)
}

export interface SigmaNode {
  op: OpCode;
  flags: number;
  wave: WaveVectorQ;
  atom?: Uint8Array;  // 32 bytes
  left?: Uint8Array;  // 32 bytes
  right?: Uint8Array; // 32 bytes
}

import {
  divRoundHalfUp,
  clampI16,
  interfere,
  entropyToStratum,
  serializeNode,
} from "../z00/physics.ts";

export {
  divRoundHalfUp,
  clampI16,
  interfere,
  entropyToStratum,
  serializeNode,
};

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

// Serialization is now in z00/physics.ts

export function parseNode(data: Uint8Array): SigmaNode {
  const dv = new DataView(data.buffer, data.byteOffset, data.byteLength);
  const op = dv.getUint8(0) as OpCode;
  const flags = dv.getUint8(1);
  const wave: WaveVectorQ = {
    theta1: dv.getUint16(2, false),
    theta2: dv.getUint16(4, false),
    prob: dv.getUint16(6, false),
    en: dv.getInt16(8, false),
  };

  const node: SigmaNode = { op, flags, wave };
  let offset = 10;
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

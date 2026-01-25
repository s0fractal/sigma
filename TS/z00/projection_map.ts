/**
 * PROJECTION MAP: SIGMA <-> QWAVE
 * Deterministic bridge between SigmaNode (10B header) and QWaveRecord (32+16B).
 * V1.0.0 - Toroidal Symmetry Aligned
 */

import { SigmaNode, WaveVectorQ, Flags } from "./physics.ts";

export const PROJECTION_VERSION = 1;

export interface WaveVectorK {
  theta: number;      // u16
  phi: number;        // u16
  amplitude: number;  // u16
  entropy: number;    // i16
  omegaTheta: number; // i16
  omegaPhi: number;   // i16
}

export interface QWaveRecord {
  magic: string;      // "QWAV"
  version: number;    // u16 (0x0100)
  flags: number;      // u16
  glyphHash: Uint8Array; // 8 bytes
  blockHeight: bigint;   // u64
  timestamp: bigint;     // u64
  wave: WaveVectorK;
}

/**
 * SigmaNode -> QWaveRecord
 * Loss Model:
 * - theta1 -> theta (Lossless)
 * - theta2 -> phi (Lossless)
 * - prob -> amplitude (Lossless)
 * - en -> entropy (Lossless)
 * - omega_theta -> 0 (Information discarded)
 * - omega_phi -> 0 (Information discarded)
 */
export function sigmaToQWave(
  node: SigmaNode, 
  glyphHash: Uint8Array, 
  blockHeight: bigint = 0n
): QWaveRecord {
  return {
    magic: "QWAV",
    version: 0x0100,
    flags: node.flags,
    glyphHash: glyphHash.slice(0, 8),
    blockHeight: blockHeight,
    timestamp: BigInt(Math.floor(Date.now() / 1000)),
    wave: {
      theta: node.wave.theta1,
      phi: node.wave.theta2,
      amplitude: node.wave.prob,
      entropy: node.wave.en,
      omegaTheta: 0,
      omegaPhi: 0,
    }
  };
}

/**
 * QWaveRecord -> SigmaNode
 * Loss Model:
 * - theta -> theta1 (Lossless)
 * - phi -> theta2 (Lossless)
 * - amplitude -> prob (Lossless)
 * - entropy -> en (Lossless)
 * - omega_theta/phi (Information lost in bridge)
 */
export function qWaveToSigma(record: QWaveRecord, op?: number): SigmaNode {
  const wave: WaveVectorQ = {
    theta1: record.wave.theta,
    theta2: record.wave.phi,
    prob: record.wave.amplitude,
    en: record.wave.entropy,
  };

  let finalFlags = record.flags | Flags.F_V2;
  let finalOp = op;

  if (finalOp === undefined) {
    // F_INCOMPLETE indicates that 'op' was not provided via bridge
    finalFlags |= Flags.F_INCOMPLETE;
    finalOp = 0; // Default to LITERAL/0 if missing, but flagged
  }

  return {
    op: finalOp,
    flags: finalFlags,
    wave: wave,
  };
}

/**
 * Serializes QWaveRecord to 48 bytes (Header 32 + Wave 16)
 */
export function serializeQWave(record: QWaveRecord): Uint8Array {
  const buf = new Uint8Array(48);
  const dv = new DataView(buf.buffer);

  // Header (32 bytes)
  dv.setUint8(0, 0x51); // 'Q'
  dv.setUint8(1, 0x57); // 'W'
  dv.setUint8(2, 0x41); // 'A'
  dv.setUint8(3, 0x56); // 'V'
  dv.setUint16(4, record.version, false);
  dv.setUint16(6, record.flags, false);
  buf.set(record.glyphHash, 8);
  dv.setBigUint64(16, record.blockHeight, false);
  dv.setBigUint64(24, record.timestamp, false);

  // WaveVectorK (16 bytes)
  dv.setUint16(32, record.wave.theta, false);
  dv.setUint16(34, record.wave.phi, false);
  dv.setUint16(36, record.wave.amplitude, false);
  dv.setInt16(38, record.wave.entropy, false);
  dv.setInt16(40, record.wave.omegaTheta, false);
  dv.setInt16(42, record.wave.omegaPhi, false);
  dv.setUint32(44, 0, false); // Reserved

  return buf;
}

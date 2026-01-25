/**
 * QUANTUM MUD ADAPTER
 * Maps non-semantic system metrics to SIGMA perturbations.
 * V1.0 - Perturbation Sync
 */

export interface SystemMetrics {
  cpuUsage: number;    // [0..1.0]
  ioWait: number;     // [0..1.0]
  netLatency: number; // [0..1.0]
  entropySource: number; // Random jitter [0..65535]
}

export interface Perturbations {
  deltaSap: number;
  deltaPressure: number;
  thetaNoise: number;
}

const MAX_PRESSURE_DELTA = 1000; // Aligned with the formula (m.cpuUsage * 700 + m.ioWait * 300)
const MAX_SAP_DELTA = 500;

/**
 * Normalizes input metrics to SIGMA perturbations.
 * STRICT INVARIANT: Non-numeric data is physically impossible to pass here.
 * Only primitive numbers are accepted and clamped.
 */
export function metricsToPerturbations(m: SystemMetrics): Perturbations {
  // Hard Clamping to prevent external "God-mode" spikes
  const pressure = Math.min(MAX_PRESSURE_DELTA, (m.cpuUsage * 0.7 + m.ioWait * 0.3) * 1000);
  const sap = Math.min(MAX_SAP_DELTA, m.netLatency * 500);
  
  // Full toroidal noise: 0..65535 jitter
  const noise = Math.floor(m.entropySource) % 65536;

  return {
    deltaPressure: Math.round(pressure),
    deltaSap: Math.round(sap),
    thetaNoise: noise
  };
}

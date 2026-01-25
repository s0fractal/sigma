/**
 * QUARANTINE FIBER
 * Isolated environment for external perturbations with Season Gating.
 * V1.0 - Survival Sifting
 */

import { SystemMetrics, metricsToPerturbations } from "./quantum_mud_adapter.ts";

export enum Season {
  EMERGENCE = "EMERGENCE",
  DEEP_CLEAN = "DEEP_CLEAN",
  QUIET = "QUIET"
}

export class QuarantineFiber {
  private survivalCycles: Map<string, number> = new Map();
  private K_THRESHOLD = 3;

  /**
   * Processes external metrics through the Season Gate.
   */
  processMetrics(metrics: SystemMetrics, currentSeason: Season): void {
    if (currentSeason !== Season.EMERGENCE) {
      // Direct decoupling: In non-emergence seasons, noise is discarded.
      return;
    }

    const p = metricsToPerturbations(metrics);
    this.trackSurvival("system_load", p.deltaPressure > 500);
    
    // Log sifting
    if (this.isSifted("system_load")) {
        // Here we would apply the delta to the Lattice p-stratum
        // console.log("🌱 Metric sifted into p-stratum: Structural branch permitted.");
    }
  }

  private trackSurvival(metricId: string, isSignificant: boolean): void {
    if (isSignificant) {
      const current = this.survivalCycles.get(metricId) || 0;
      this.survivalCycles.set(metricId, current + 1);
    } else {
      this.survivalCycles.set(metricId, 0); // Reset on drop
    }
  }

  private isSifted(metricId: string): boolean {
    return (this.survivalCycles.get(metricId) || 0) >= this.K_THRESHOLD;
  }
}

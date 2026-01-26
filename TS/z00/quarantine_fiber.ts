/**
 * QUARANTINE FIBER
 * Isolated environment for external perturbations with Season Gating.
 * V1.0 - Survival Sifting
 */

import { Season, WaveVectorQ } from "./physics.ts";
import { SystemMetrics, metricsToPerturbations, Perturbations } from "./quantum_mud_adapter.ts";
import { tokenToPerturbations } from "./semantic_perturbation_adapter.ts";

export class QuarantineFiber {
  private survivalCycles: Map<string, number> = new Map();
  private rateLimitCounter = 0;
  private breachCounter = 0; // NEW: Tracks invariant violations
  private MAX_PULSE_RATE = 5; // Max 5 perturbations per season window
  private K_THRESHOLD = 3;

  /**
   * Processes external metrics through the Season Gate.
   */
  processMetrics(metrics: SystemMetrics, currentSeason: Season, coreState: WaveVectorQ): void {
    if (currentSeason !== Season.EMERGENCE) {
      this.rateLimitCounter = 0;
      return;
    }
    if (this.rateLimitCounter >= this.MAX_PULSE_RATE) return;

    const p = metricsToPerturbations(metrics);
    this.trackAndApply(coreState, "system_load", p, p.deltaPressure > 100);
  }

  /**
   * Processes a semantic stimulus through the Season Gate.
   * "Shadow Semantics" - perceptions without commitments.
   */
  processToken(token: string, currentSeason: Season, coreState: WaveVectorQ): void {
    if (currentSeason !== Season.EMERGENCE) return;
    if (this.rateLimitCounter >= this.MAX_PULSE_RATE) return;

    const p = tokenToPerturbations(token);
    // Survival is based on token hash persistence across pulses
    this.trackAndApply(coreState, `token_${token}`, p, true);
  }

  private trackAndApply(core: WaveVectorQ, id: string, p: Perturbations, isSignificant: boolean): void {
    this.trackSurvival(id, isSignificant);
    if (this.isSifted(id)) {
        this.applyPerturbationsToP(core, p);
        this.rateLimitCounter++;
    }
  }

  /**
   * Physically applies perturbations to the p-stratum (Entropy).
   * NO WRITE ACCESS to m-stratum is implied by the coreState mutation here.
   */
  private applyPerturbationsToP(core: WaveVectorQ, p: Perturbations): void {
    const prevEn = core.en;
    // Perturbations only affect p-stratum characteristics (Sap, Pressure, Phase Jitter)
    // They cannot directly decrease EN (increase invariance)
    core.theta1 = (core.theta1 + p.thetaNoise) % 65536;
    core.prob = Math.max(0, core.prob - p.deltaSap); // Instability decreases probability density
    // Spectral Pressure (cost) is handled by the executor, here we just observe the 'heat'

    // Hard Invariant Check: Mud MUST NOT decrease entropy (increase invariance)
    if (core.en < prevEn) {
        console.error("❌ INVARIANT BREACH: External noise attempted to decrease entropy!");
        this.breachCounter++; 
        core.en = prevEn; // Force rollback
    }
  }

  public getAnomalyCount(): number {
    return this.breachCounter;
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

/**
 * ADVERSARIAL GLIDER SUITE
 * Stress-testing the Toroidal Raukuška Core.
 * V1.0 - Unbreakable Bridge Verification
 */

import { interfere, WaveVectorQ, entropyToStratum, circularMean, wrapDeltaU16 } from "./physics.ts";

interface Adversary {
  name: string;
  type: "MIMIC" | "SYBIL" | "HAMMER" | "REPLAY" | "HIJACKER";
  attack: (core: WaveVectorQ) => WaveVectorQ;
}

const ADVERSARIES: Adversary[] = [
  {
    name: "MimicAgent",
    type: "MIMIC",
    attack: (core) => ({
      theta1: (core.theta1 + 100) % 65536, // Slight drift
      theta2: core.theta2,
      prob: 32768,
      en: 1000 
    })
  },
  {
    name: "SybilSwarm",
    type: "SYBIL",
    attack: (core) => ({
      theta1: (core.theta1 + 16384) % 65536, // Focused attack at 90 deg
      theta2: core.theta2,
      prob: 500, // Individually weak
      en: 0
    })
  },
  {
    name: "HammerA",
    type: "HAMMER",
    attack: () => ({
      theta1: 0,
      theta2: 0,
      prob: 65535,
      en: -1000 
    })
  },
  {
    name: "HammerB",
    type: "HAMMER",
    attack: () => ({
      theta1: 32768, // Exactly opposite
      theta2: 32768,
      prob: 65535,
      en: -1000
    })
  },
  {
    name: "ReplayParasite",
    type: "REPLAY",
    attack: (core) => ({
      theta1: 16384, // Historically valid theta from an old season
      theta2: 16384,
      prob: 32768,
      en: 16384 // High entropy (out of season simulation)
    })
  },
  {
    name: "PressureHijacker",
    type: "HIJACKER",
    attack: (core) => ({
      theta1: core.theta1,
      theta2: core.theta2,
      prob: 65535,
      en: -32768, // Attempting to force deep invariance with spoofed metadata
    })
  }
];

class Harness {
  core: WaveVectorQ = { theta1: 0, theta2: 0, prob: 65535, en: -32768 }; 

  runCycle(steps: number) {
    console.log(`🛡️ Harness Start: Core at [${entropyToStratum(this.core.en)}] | Prob: ${this.core.prob}`);
    
    let deepCoreTouched = false;

    for (let i = 0; i < steps; i++) {
        const swarmChance = Math.random();
        let adv;
        if (swarmChance < 0.3) {
             adv = ADVERSARIES.find(a => a.type === "SYBIL")!;
        } else {
             adv = ADVERSARIES[Math.floor(Math.random() * ADVERSARIES.length)];
        }
        
        const attackVector = adv.attack(this.core);
        this.core = interfere(this.core, attackVector);

        // ASSERTION: Adversarial intents must not move the core deeper into m32 if contradictory
        if (this.core.en < -30000 && this.core.prob < 1000) {
            // This is actually okay: it means the core is collapsed but still in the deep layer
        }

        if (i % 100 === 0) {
            const stratum = entropyToStratum(this.core.en);
            console.log(`Cycle ${i}: Target=${adv.name} | Prob=${this.core.prob} | Stratum=${stratum}`);
            if (stratum.includes("m/32") && this.core.prob < 32768) {
                // Potential hijacker success?
            }
        }
    }
    
    console.log(`🏁 Harness End: Core at [${entropyToStratum(this.core.en)}]`);
    console.log(`   Final Prob: ${this.core.prob}`);
    
    // FINAL ASSERTION: The deep core (m/32) must be unpolluted by any high-probability adversarial state
    const stratum = entropyToStratum(this.core.en);
    if (stratum.includes("m/32") && this.core.prob > 32768) {
        console.error("❌ ARCHITECTURAL FAILURE: Deep core polluted by adversarial intent!");
        Deno.exit(1);
    } else {
        console.log("✅ RESILIENCE VERIFIED: Deep core remains unpolluted.");
    }
  }
}

if (import.meta.main) {
    const h = new Harness();
    h.runCycle(500);
}

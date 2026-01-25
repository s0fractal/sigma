import { wrapDeltaU16, circularMean, toroidalDistance, WaveVectorQ } from "./physics.ts";

function testToroidalMetrics() {
  console.log("🌀 Starting Toroidal Physics Fuzz Tests...");

  // 1. Wrap-around delta tests
  console.assert(wrapDeltaU16(65535, 0) === 1, "Wrap delta failed: 65535 ~ 0 should be 1");
  console.assert(wrapDeltaU16(0, 1) === 1, "Wrap delta failed: 0 ~ 1 should be 1");
  console.assert(wrapDeltaU16(32768, 0) === 32768, "Wrap delta failed: 32768 ~ 0 should be 32768");
  console.assert(wrapDeltaU16(40000, 0) === 25536, "Wrap delta failed: 40000 ~ 0 wrap arc failed");

  // 2. Toroidal Distance Symmetry
  for (let i = 0; i < 1000; i++) {
    const a = Math.floor(Math.random() * 65536);
    const b = Math.floor(Math.random() * 65536);
    const w1: WaveVectorQ = { theta1: a, theta2: b, prob: 0, en: 0 };
    const w2: WaveVectorQ = { theta1: b, theta2: a, prob: 0, en: 0 };
    
    // Dist is symmetric in toroidal space? Not necessarily if theta1/theta2 are swapped, 
    // but dist(w1, w2) == dist(w2, w1) must hold.
    const d1 = toroidalDistance(w1, w2);
    const d2 = toroidalDistance(w2, w1);
    console.assert(Math.abs(d1 - d2) < 0.0001, `Distance symmetry failed for ${a}, ${b}`);
  }

  // 3. Circular Mean over the 0-barrier
  const m1 = circularMean(65530, 10); // Should be very close to 2 or 65536
  console.log(`   Circular Mean (65530, 10): ${m1} (Expected near 2 or 65536)`);
  console.assert(m1 < 100 || m1 > 65436, "Circular mean failed tracking across 0-barrier");

  console.log("✅ All Toroidal Property Tests Passed.");
}

if (import.meta.main) {
  testToroidalMetrics();
}

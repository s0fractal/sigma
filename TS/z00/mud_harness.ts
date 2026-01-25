/**
 * MUD HARNESS
 * Stress-testing the system with real (simulated) metric floods.
 * V1.0 - Seasonality & Persistence Test
 */

import { Season, WaveVectorQ } from "./physics.ts";
import { QuarantineFiber } from "./quarantine_fiber.ts";
import { SystemMetrics } from "./quantum_mud_adapter.ts";

function runMudTest() {
  const fiber = new QuarantineFiber();
  let coreState: WaveVectorQ = { theta1: 0, theta2: 0, prob: 65535, en: 0 };
  
  console.log("🌦️ Starting Mud Harness: 10 Pulse Cycle...");

  for (let i = 0; i < 10; i++) {
    const season = (i % 6) as Season;
    const metrics: SystemMetrics = {
      cpuUsage: 0.8, // Heavy load simulation
      ioWait: 0.1,
      netLatency: 0.05,
      entropySource: Math.random() * 65535
    };

    fiber.processMetrics(metrics, season, coreState);
    console.log(`Pulse ${i} [${Season[season]}]: Prob=${coreState.prob}`);
  }

  console.log("✅ Mud Harness completed.");
}

if (import.meta.main) {
  runMudTest();
}

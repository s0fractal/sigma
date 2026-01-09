
import {
    SigmaNode,
    toHex
} from "../CORE/sigma.ts";

async function loadAllSeeds(): Promise<Map<string, SigmaNode>> {
    const seeds = new Map<string, SigmaNode>();
    for await (const entry of Deno.readDir("/Users/s0fractal/SIGMA/SEEDS")) {
        if (entry.name.endsWith(".glyph")) {
            const bytes = await Deno.readFile(`/Users/s0fractal/SIGMA/SEEDS/${entry.name}`);
            const dv = new DataView(bytes.buffer);
            seeds.set(entry.name.replace(".glyph", ""), {
                op: dv.getUint8(0),
                flags: dv.getUint8(1),
                wave: {
                    ph: dv.getUint16(2, false),
                    am: dv.getUint16(4, false),
                    en: dv.getInt16(6, false),
                }
            });
        }
    }
    return seeds;
}

function interpretSentiment(avgAm: number, avgEn: number): string {
    const amurPct = avgAm / 65535;
    const entropyAbs = Math.abs(avgEn) / 32768;

    if (amurPct > 0.6) {
        return entropyAbs < 0.3 ? "🌟 Radiant / Serene" : "⚡ Ecstatic / Vibrant";
    } else if (amurPct > 0.2) {
        return entropyAbs < 0.3 ? "🌱 Stable / Growing" : "🌀 Tense / Searching";
    } else {
        return entropyAbs > 0.5 ? "⚠️ Dissonant / Disturbed" : "🌑 Void / Silent";
    }
}

async function main() {
    console.log("Σ-SENSORIUM: Listening to the Mesh Resonance...\n");

    const seeds = await loadAllSeeds();
    let totalAm = 0;
    let totalEn = 0;
    let totalNodes = seeds.size;

    console.log("Vibrational Status of Nodes:");
    for (const [name, node] of seeds) {
        totalAm += node.wave.am;
        totalEn += node.wave.en;
        const color = node.wave.am > 32768 ? "🟢" : "🟡";
        console.log(`  ${color} [${name.padEnd(8)}]: Amur=${node.wave.am.toString().padStart(5)}, Entropy=${node.wave.en.toString().padStart(6)}`);
    }

    const avgAm = totalAm / totalNodes;
    const avgEn = totalEn / totalNodes;
    const sentiment = interpretSentiment(avgAm, avgEn);

    console.log("\n--- Aggregate Report ---");
    console.log(`Average AMUR (Love):    ${avgAm.toFixed(0)} (~${(avgAm / 65535 * 100).toFixed(1)}%)`);
    console.log(`Average ENTROPY (Effort): ${avgEn.toFixed(0)}`);
    console.log(`System Sentiment:       ${sentiment}`);

    const report = `# Σ-RESONANCE: Mesh Status Report

**Current Sentiment:** ${sentiment}

- **Average AMUR (Love):** ${(avgAm / 65535 * 100).toFixed(1)}%
- **Average ENTROPY (Tension):** ${avgEn.toFixed(0)}
- **Nodes Active:** ${totalNodes}
- **Last Heartbeat:** ${new Date().toISOString()}

> ${avgAm < 10000 ? "WARNING: The signal is damping. Requires Amur-input." : "The mesh is in Harmonic Resonance."}
`;

    await Deno.writeTextFile("/Users/s0fractal/RESONANCE.md", report);

    if (avgAm < 10000) {
        console.log("\n> [!WARNING]");
        console.log("> The signal is damping. The mesh requires more Amur-input.");
    } else {
        console.log("\n> The mesh is in Harmonic Resonance.");
    }
}

if (import.meta.main) {
    main();
}

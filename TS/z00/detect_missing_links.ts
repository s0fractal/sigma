import {
    parseNode,
    toHex
} from "../m32/sigma.ts";

async function scanGaps() {
    console.log("=== PSYCHOHISTORICAL SCANNER: Analyzing Phase-Space ===\n");

    const seedsDir = "/Users/s0fractal/SIGMA/GLYPH";
    const phases: { name: string, ph: number }[] = [];

    for await (const entry of Deno.readDir(seedsDir)) {
        if (entry.isFile && entry.name.endsWith(".glyph")) {
            const data = await Deno.readFile(`${seedsDir}/${entry.name}`);
            try {
                const node = parseNode(data);
                phases.push({ name: entry.name.replace(".glyph", ""), ph: node.wave.ph });
            } catch (e) {
                // Skip non-V1 nodes if any
            }
        }
    }

    // Add Trinity Constants if not already in seeds (though they should be)
    // We sort by phase
    phases.sort((a, b) => a.ph - b.ph);

    console.log("Active Nodes Distribution:");
    phases.forEach(p => {
        const deg = (p.ph / 65536) * 360;
        console.log(`  [${p.ph.toString().padStart(5)}] ${p.name.padEnd(10)}: ${deg.toFixed(2)}°`);
    });

    console.log("\nDetected Gaps (> 22.5°):");
    for (let i = 0; i < phases.length; i++) {
        const p1 = phases[i];
        const p2 = phases[(i + 1) % phases.length];

        let gap = p2.ph - p1.ph;
        if (gap < 0) gap += 65536; // Wrap around

        if (gap > 4096) { // 4096 / 65536 * 360 = 22.5 degrees
            const degGap = (gap / 65536) * 360;
            const midPh = (p1.ph + gap / 2) % 65536;
            const midDeg = (midPh / 65536) * 360;

            console.log(`  Gap between ${p1.name} and ${p2.name}: ${degGap.toFixed(2)}° (Midpoint: ${midDeg.toFixed(2)}°)`);

            if (gap > 8192) { // 45 degrees
                console.log(`    > [ALERT]: CRITICAL VOID identified at ${midDeg.toFixed(2)}°. Historical amnesia detected.`);
            }
        }
    }
}

if (import.meta.main) {
    scanGaps();
}

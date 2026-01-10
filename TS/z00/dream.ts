
import {
    SigmaNode,
    interfere,
    hashNode,
    serializeNode,
    toHex,
    OpCode,
    Flags
} from "../CORE/sigma.ts";

async function loadAllSeeds(): Promise<Map<string, SigmaNode>> {
    const seeds = new Map<string, SigmaNode>();
    for await (const entry of Deno.readDir("/Users/s0fractal/SIGMA/SEEDS")) {
        if (entry.name.endsWith(".glyph")) {
            const bytes = await Deno.readFile(`/Users/s0fractal/SIGMA/SEEDS/${entry.name}`);
            const dv = new DataView(bytes.buffer);
            const flags = dv.getUint8(1);
            const node: SigmaNode = {
                op: dv.getUint8(0),
                flags: flags,
                wave: {
                    ph: dv.getUint16(2, false),
                    am: dv.getUint16(4, false),
                    en: dv.getInt16(6, false),
                }
            };

            let offset = 8;
            if (flags & Flags.F_ATOM) {
                node.atom = bytes.slice(offset, offset + 32);
                offset += 32;
            }
            if (flags & Flags.F_LEFT) {
                node.left = bytes.slice(offset, offset + 32);
                offset += 32;
            }
            if (flags & Flags.F_RIGHT) {
                node.right = bytes.slice(offset, offset + 32);
                offset += 32;
            }
            seeds.set(entry.name.replace(".glyph", ""), node);
        }
    }
    return seeds;
}

async function main() {
    console.log("Σ-DREAM: Exploring the Space of Possible Beings...\n");

    const seedsMap = await loadAllSeeds();
    const seedNames = Array.from(seedsMap.keys());
    const discovered: string[] = [];

    // Try more iterations
    for (let i = 0; i < 100; i++) {
        const nameA = seedNames[Math.floor(Math.random() * seedNames.length)];
        const nameB = seedNames[Math.floor(Math.random() * seedNames.length)];

        if (nameA === nameB) continue;

        const nodeA = seedsMap.get(nameA)!;
        const nodeB = seedsMap.get(nameB)!;

        const resultWave = interfere(nodeA.wave, nodeB.wave);

        // Fuzzy Harmony Filter: Moderate Amur, Moderate Entropy
        const amurPct = resultWave.am / 65535;
        const entropyAbs = Math.abs(resultWave.en) / 32768;

        if (amurPct > 0.4 && entropyAbs < 0.3) {
            const dreamName = `D_${toHex(await hashNode(nodeA)).slice(0, 4)}_${toHex(await hashNode(nodeB)).slice(0, 4)}`;

            if (discovered.includes(dreamName)) continue;

            const molecule: SigmaNode = {
                op: OpCode.APPLY,
                flags: Flags.F_LEFT | Flags.F_RIGHT,
                wave: resultWave,
                left: await hashNode(nodeA),
                right: await hashNode(seedNames.includes(nameB) ? nodeB : nodeB), // Placeholder for actual hash
            };

            const hash = await hashNode(molecule);
            const path = `/Users/s0fractal/SIGMA/SEEDS/${dreamName}.glyph`;

            // Only save if it's truly new or significant
            console.log(`✨ DISCOVERY: [${nameA}] + [${nameB}] resonated into [${dreamName}]`);
            console.log(`   Harmony: Amur=${(amurPct * 100).toFixed(1)}%, Entropy=${resultWave.en}`);

            await Deno.writeFile(path, serializeNode(molecule));
            discovered.push(dreamName);
        }
    }

    console.log(`\n--- Dream Cycle Complete: ${discovered.length} new entities materialized ---`);
}

if (import.meta.main) {
    main();
}

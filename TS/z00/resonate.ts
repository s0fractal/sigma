import {
    hashNode,
    toHex,
    OpCode,
    Flags,
    SigmaNode,
    WaveVectorQ,
} from "../m32/sigma.ts";

async function hashFile(path: string): Promise<Uint8Array> {
    const data = await Deno.readFile(path);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    return new Uint8Array(hashBuffer);
}

async function calculateDirectoryResonance(path: string): Promise<Uint8Array> {
    const fileHashes: Map<string, Uint8Array> = new Map();
    try {
        for await (const entry of Deno.readDir(path)) {
            if (entry.isFile && !entry.name.startsWith(".")) {
                const h = await hashFile(`${path}/${entry.name}`);
                fileHashes.set(entry.name, h);
            } else if (entry.isDirectory && !entry.name.startsWith(".")) {
                // Recursive resonance? For now, let's keep it 1-level deep for simplicity
                // as per the current node structure.
                const h = await calculateDirectoryResonance(`${path}/${entry.name}`);
                fileHashes.set(entry.name, h);
            }
        }
    } catch (_e) {
        return new Uint8Array(32).fill(0); // Dissonant null-hash
    }

    if (fileHashes.size === 0) return new Uint8Array(32).fill(0);

    const sortedNames = Array.from(fileHashes.keys()).sort();
    const combined = new Uint8Array(32 * sortedNames.length);
    for (let i = 0; i < sortedNames.length; i++) {
        combined.set(fileHashes.get(sortedNames[i])!, i * 32);
    }
    const resonanceHash = await crypto.subtle.digest("SHA-256", combined);
    return new Uint8Array(resonanceHash);
}

async function getProjectResonance() {
    const nodes = ["0", "1", "2"];
    const resonanceData: Record<string, any> = {};

    for (const node of nodes) {
        const nodePath = `/Users/s0fractal/${node}`;
        resonanceData[node] = {
            ts: toHex(await calculateDirectoryResonance(`${nodePath}/ts`)),
            rs: toHex(await calculateDirectoryResonance(`${nodePath}/rs`)),
            md: toHex(await calculateDirectoryResonance(`${nodePath}/md`)),
        };
    }
    return resonanceData;
}

async function cmdAudit() {
    console.log("Σ-RESONATE: Auditing project topology...");
    const data = await getProjectResonance();
    for (const [node, dims] of Object.entries(data)) {
        console.log(`\nNode [${node}]:`);
        for (const [dim, hash] of Object.entries(dims as any)) {
            const status = hash === "0".repeat(64) ? "🌑 VOID" : "✅ RESONANT";
            console.log(`  ${dim.padEnd(4)}: ${hash} [${status}]`);
        }
    }
}

async function cmdSeal() {
    console.log("Σ-RESONATE: Sealing project state...");
    const data = await getProjectResonance();
    const sealPath = "/Users/s0fractal/SIGMA/SENSE/resonance-seal.json";
    await Deno.writeTextFile(sealPath, JSON.stringify(data, null, 2));
    console.log(`Success: Resonance sealed at ${sealPath}`);
}

async function cmdCheck() {
    console.log("Σ-RESONATE: Verifying seal...");
    const sealPath = "/Users/s0fractal/SIGMA/SENSE/resonance-seal.json";
    try {
        const sealedData = JSON.parse(await Deno.readTextFile(sealPath));
        const currentData = await getProjectResonance();

        let dissonanceCount = 0;
        for (const node of Object.keys(sealedData)) {
            for (const dim of Object.keys(sealedData[node])) {
                if (sealedData[node][dim] !== currentData[node][dim]) {
                    console.error(`⚠️ DISSONANCE detected in node [${node}] dimension [${dim}]!`);
                    console.error(`  Expected: ${sealedData[node][dim]}`);
                    console.error(`  Found:    ${currentData[node][dim]}`);
                    dissonanceCount++;
                }
            }
        }

        if (dissonanceCount === 0) {
            console.log("✅ Project is in Harmonic Resonance with the seal.");
        } else {
            console.error(`\nFAILED: ${dissonanceCount} points of dissonance found.`);
            Deno.exit(1);
        }
    } catch (e) {
        console.error("Error: Seal not found or corrupted. Use 'seal' to create one.");
        Deno.exit(1);
    }
}

const command = Deno.args[0];

switch (command) {
    case "audit":
        await cmdAudit();
        break;
    case "seal":
        await cmdSeal();
        break;
    case "check":
        await cmdCheck();
        break;
    default:
        console.log("Usage: resonate <audit|seal|check>");
}

```

🌊

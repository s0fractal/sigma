import {
    hashNode,
    toHex,
} from "../m32/sigma.ts";
import { PANTHEON_REGISTRY, ForgeManager, GiantDef } from "../RUNTIME/FORGE_MANAGER.ts";

/**
 * Chromatic Audit: The Spectral Shift
 * Projects the 24-bit color (first 3 bytes of hash) for each Giant.
 */

async function chromaticAudit() {
    console.log("=== CHROMATIC AUDIT: The Spectral Shift ===\n");
    console.log("Mapping Pantheon Giants to their Sovereign Colors (First 3 bytes of Hash)\n");

    const results: { name: string, hex: string, ph: number }[] = [];

    // Use a temporary node creation to get the hashes
    for (const def of PANTHEON_REGISTRY) {
        // We can just re-hash based on the FORGE_MANAGER logic
        const atom = def.hexSource ?
            new Uint8Array(def.hexSource.match(/.{1,2}/g)!.map(byte => parseInt(byte, 16))) :
            new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(def.source!)));

        const node = {
            op: 0x01, // Lit
            flags: 0x01, // Atom
            wave: { ph: def.phase, am: 65535, en: -32768 },
            atom: atom
        };

        const hash = await hashNode(node as any);
        const hex = toHex(hash);
        const color = `#${hex.slice(0, 6).toUpperCase()}`;

        results.push({ name: def.name, hex: color, ph: def.phase });
    }

    console.log("GIANT    | PHASE  | SOVEREIGN COLOR | VISUAL (Approx)");
    console.log("---------|--------|-----------------|----------------");
    results.forEach(r => {
        const visual = getAnsiColor(r.hex);
        console.log(`${r.name.padEnd(8)} | ${r.ph.toString().padStart(6)} | ${r.hex.padEnd(15)} | ${visual} ■■■\x1b[0m`);
    });

    console.log("\n[INTUITION]:");
    console.log("- Does the color 'feel' like the entity?");
    console.log("- Is there a topological drift between the Phase (Angle) and the projected Hue?");
}

function getAnsiColor(hex: string) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `\x1b[38;2;${r};${g};${b}m`;
}

if (import.meta.main) {
    chromaticAudit();
}

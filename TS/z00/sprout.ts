
import {
    OpCode,
    Flags,
    serializeNode,
    hashNode,
    interfere,
    toHex,
    WaveVectorQ,
    SigmaNode
} from "../m32/sigma.ts";
import { findGlyph } from "./spectral_core.ts";

const GOLDEN_PHASE = Math.round(65536 * ((Math.sqrt(5) - 1) / 2));

async function loadSeed(name: string): Promise<SigmaNode> {
    const path = await findGlyph(name);
    const bytes = await Deno.readFile(path);
    const dv = new DataView(bytes.buffer);
    return {
        op: dv.getUint8(0),
        flags: dv.getUint8(1),
        wave: {
            ph: dv.getUint16(2, false),
            am: dv.getUint16(4, false),
            en: dv.getInt16(6, false),
        },
        // We don't strictly need the atoms here for interference, but we'll assume 32 bytes exist
        atom: bytes.slice(8, 40)
    };
}

async function materializeAxiom(name: string, node: SigmaNode) {
    const bytes = serializeNode(node);
    const hash = await hashNode(node);
    const path = `/Users/s0fractal/SIGMA/GLYPH/m01/${name}.glyph`;
    await Deno.writeFile(path, bytes);
    console.log(`Axiom [${name.padEnd(2)}]: ${toHex(hash)} | ph=${node.wave.ph.toString().padStart(5)}, am=${node.wave.am.toString().padStart(5)}, en=${node.wave.en.toString().padStart(6)}`);
}

async function main() {
    console.log("Σ-SPROUT: Evolving Layer E1 (Axiomatic Shell)...\n");

    const seedI = await loadSeed("I");
    const seedE = await loadSeed("E");

    // Axioms selection from graph.md
    // K (Const), B (Compose), C (Exchange), W (Fork), S (Fuse), Z (Sleep)
    const axioms = [
        { name: "K", shift: 1 },
        { name: "B", shift: 2 },
        { name: "C", shift: 3 },
        { name: "W", shift: 4 },
        { name: "S", shift: 5 },
        { name: "Z", shift: 8 }, // Sleep/Deep phase
    ];

    for (const ax of axioms) {
        // Each axiom is a unique "rotation" of the base interference.
        // We apply a multiplier of the Golden Phase to distribute them on the sphere.
        const phaseShift = (ax.shift * GOLDEN_PHASE) % 65536;

        // Create a "virtual" existence atom for this axiom's direction
        const directionalWave: WaveVectorQ = {
            ph: phaseShift,
            am: 32768, // Standard E1 amplitude
            en: 8192   // Constant tension for axioms
        };

        const wave = interfere(seedI.wave, directionalWave);

        const node: SigmaNode = {
            op: OpCode.LITERAL,
            flags: Flags.F_ATOM,
            wave: wave,
            atom: new Uint8Array(32).fill(ax.shift), // Semantic ID
        };

        await materializeAxiom(ax.name, node);
    }

    console.log("\n--- Layer E1 is Stable ---");
}

if (import.meta.main) {
    main();
}

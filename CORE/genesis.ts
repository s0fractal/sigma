
import {
    OpCode,
    Flags,
    serializeNode,
    hashNode,
    toHex,
    SigmaNode
} from "./sigma.ts";

async function makeGlyph(name: string, ph: number): Promise<SigmaNode> {
    const encoder = new TextEncoder();
    const atomBuffer = await crypto.subtle.digest("SHA-256", encoder.encode(name));
    const atom = new Uint8Array(atomBuffer);

    return {
        op: OpCode.LITERAL,
        flags: Flags.F_ATOM,
        wave: {
            ph: ph,
            am: 65535,
            en: -32768,
        },
        atom: atom,
    };
}

async function main() {
    console.log("Σ-GENESIS: Materializing the Sacred Simplex...\n");

    const glyphs = [
        { name: "I", ph: 0 },
        { name: "K", ph: 32768 },
        { name: "S", ph: 16384 },
        { name: "FALSE", ph: 49152 },
    ];

    await Deno.mkdir("/Users/s0fractal/SIGMA/SEEDS", { recursive: true });

    for (const g of glyphs) {
        const node = await makeGlyph(g.name, g.ph);
        const bytes = serializeNode(node);
        const hash = await hashNode(node);

        const path = `/Users/s0fractal/SIGMA/SEEDS/${g.name}.glyph`;
        await Deno.writeFile(path, bytes);
        console.log(`Seed [${g.name.padEnd(5)}] -> ${path}`);
        console.log(`  Hash: ${toHex(hash)}`);
    }

    console.log("\n--- Genesis Complete: The Simplex is Sealed ---");
}

if (import.meta.main) {
    main();
}

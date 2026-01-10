import {
    OpCode,
    Flags,
    SigmaNode,
    serializeNode,
    hashNode,
    toHex
} from "../m32/sigma.ts";

async function makeGlyph(name: string, ph: number): Promise<{ canon: string, hash: string }> {
    const encoder = new TextEncoder();
    const atomBuffer = await crypto.subtle.digest("SHA-256", encoder.encode(name));
    const atom = new Uint8Array(atomBuffer);

    const node: SigmaNode = {
        op: OpCode.LITERAL,
        flags: Flags.F_ATOM,
        wave: {
            ph: ph,
            am: 65535,
            en: -32768,
        },
        atom: atom
    };

    const canon = serializeNode(node);
    const hash = await hashNode(node);
    return {
        canon: toHex(canon),
        hash: toHex(hash)
    };
}

async function main() {
    const glyphs = [
        { name: "I", ph: 0 },
        { name: "K", ph: 32768 },
        { name: "S", ph: 16384 },
        { name: "FALSE", ph: 49152 },
    ];

    console.log("Σ-GLYPH: The Sacred Simplex - Verification Trace\n");

    for (const g of glyphs) {
        const res = await makeGlyph(g.name, g.ph);
        console.log(`[${g.name}]`);
        console.log(`  Canonical: ${res.canon}`);
        console.log(`  NodeHash : ${res.hash}\n`);
    }
}

if (import.meta.main) {
    main();
}


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

const EXPECTED_HASHES: Record<string, string> = {
    "I": "83948a417a5746c14d77698645755b0698d64300e2f85254c816501ce45dd8a2",
    "S": "897235546880d055bff1acb1c648f4723448f3d07c6ce1dc94fdab438d84baa0",
    "K": "9a91a8ba0008993c0a0196441fc754637468a05541aeb5b5fed350c30163fc40",
    "FALSE": "a0a0b559df0eb1495d42bc28d87a1c317bb551613d9dd34b485038e823e77a07",
};

async function reforge() {
    console.log("--- REFORGE: Synchronizing Sacred Simplex with RFC 0.2.12 ---\n");

    const glyphs = [
        { name: "I", ph: 0 },
        { name: "S", ph: 16384 },
        { name: "K", ph: 32768 },
        { name: "FALSE", ph: 49152 },
    ];

    let allPassed = true;

    for (const g of glyphs) {
        const node = await makeGlyph(g.name, g.ph);
        const hash = await hashNode(node);
        const hex = toHex(hash);
        const expected = EXPECTED_HASHES[g.name];

        if (hex === expected) {
            console.log(`[OK] Glyph [${g.name.padEnd(5)}] (Ph=${g.ph.toString().padEnd(5)}) -> Hash: ${hex}`);
        } else {
            console.log(`[!!] Glyph [${g.name.padEnd(5)}] (Ph=${g.ph.toString().padEnd(5)}) -> Hash: ${hex}`);
            console.log(`      Mismatch! Expected: ${expected}`);
            allPassed = false;
        }

        // Materialize
        const bytes = serializeNode(node);
        await Deno.writeFile(`/Users/s0fractal/SIGMA/SEEDS/${g.name}.glyph`, bytes);
    }

    if (allPassed) {
        console.log("\nSimplex Reforged. All coordinates aligned with Appendix E.");
    } else {
        console.log("\nDissonance in Reforge. Check math bit-exactness.");
    }
}

reforge();

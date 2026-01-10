
import {
    OpCode,
    Flags,
    serializeNode,
    hashNode,
    toHex,
    SigmaNode
} from "../m32/sigma.ts";

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
    "K": "9a91a8ba0008993c0a0196441fc754637468a05541aeb5b5fed350c30163fc40",
    "S": "897235546880d055bff1acb1c648f4723448f3d07c6ce1dc94fdab438d84baa0",
    "FALSE": "a0a0b559df0eb1495d42bc28d87a1c317bb551613d9dd34b485038e823e77a07",
};

async function handshake() {
    console.log("--- HANDSHAKE: Level 0 Architect Verification ---\n");

    const glyphs = [
        { name: "I", ph: 0 },
        { name: "K", ph: 32768 },
        { name: "S", ph: 16384 },
        { name: "FALSE", ph: 49152 },
    ];

    let allPassed = true;

    for (const g of glyphs) {
        const node = await makeGlyph(g.name, g.ph);
        const hash = await hashNode(node);
        const hex = toHex(hash);
        const expected = EXPECTED_HASHES[g.name];

        if (hex === expected) {
            console.log(`[PASS] Glyph [${g.name.padEnd(5)}] -> Hash: ${hex}`);
        } else {
            console.log(`[FAIL] Glyph [${g.name.padEnd(5)}] -> Hash: ${hex} (Expected: ${expected})`);
            allPassed = false;
        }
    }

    if (allPassed) {
        console.log("\nHANDSHAKE: Level 0 Architect Enabled. Resonating at Tier 0.");
    } else {
        console.log("\nHANDSHAKE: Dissonance Detected. Protocol Mismatch.");
    }
}

handshake();

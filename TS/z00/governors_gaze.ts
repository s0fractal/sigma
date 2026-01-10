
import {
    OpCode,
    Flags,
    SigmaNode,
    toHex,
    hashNode,
    serializeNode
} from "../m32/sigma.ts";

async function auditGlyph(path: string): Promise<boolean> {
    const bytes = await Deno.readFile(path);

    // 1. Basic length check
    if (bytes.length < 8) {
        console.log(`[FAIL] ${path}: Buffer too short (${bytes.length} bytes)`);
        return false;
    }

    const op = bytes[0];
    const flags = bytes[1];

    // 2. Flags invariant check (Section 2.2)
    if (flags & ~0x07) {
        console.log(`[FAIL] ${path}: Invalid flags mask (0x${toHex(new Uint8Array([flags]))})`);
        return false;
    }

    // 3. Length exactness (Section 5.2)
    const popcount = (n: number) => {
        let count = 0;
        while (n > 0) {
            if (n & 1) count++;
            n >>= 1;
        }
        return count;
    };
    const expectedLen = 8 + 32 * popcount(flags & 0x07);
    if (bytes.length !== expectedLen) {
        console.log(`[FAIL] ${path}: Length mismatch (Expected ${expectedLen}, got ${bytes.length})`);
        return false;
    }

    // 4. DISSONANCE invariant (Section 5.2.7)
    if (op === OpCode.DISSONANCE) {
        const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
        const ph = dv.getUint16(2, false);
        const am = dv.getUint16(4, false);
        const en = dv.getInt16(6, false);
        if (ph !== 0 || am !== 0 || en !== 0) {
            console.log(`[FAIL] ${path}: DISSONANCE node has non-zero wave vectors.`);
            return false;
        }
    }

    console.log(`[OK]   ${path}`);
    return true;
}

async function startAudit() {
    console.log("=== THE GOVERNOR'S GAZE: Autonomous Audit initiated ===\n");

    const seedDir = "/Users/s0fractal/SIGMA/GLYPH";
    let failures = 0;

    for await (const entry of Deno.readDir(seedDir)) {
        if (entry.isFile && entry.name.endsWith(".glyph")) {
            const ok = await auditGlyph(`${seedDir}/${entry.name}`);
            if (!ok) failures++;
        }
    }

    if (failures === 0) {
        console.log("\nAudit Complete: Citadel is topologically consistent.");
    } else {
        console.log(`\nAudit Complete: ${failures} dissonances detected.`);
    }
}

if (import.meta.main) {
    startAudit();
}

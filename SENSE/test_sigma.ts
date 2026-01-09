import {
    OpCode,
    Flags,
    serializeNode,
    hashNode,
    toHex,
    interfere,
} from "../CORE/sigma.ts";

async function runTests() {
    console.log("--- Σ-GLYPH TV-N1: LITERAL ---");
    const atomAA = new Uint8Array(32).fill(0xaa);
    const nodeN1 = {
        op: OpCode.LITERAL,
        flags: Flags.F_ATOM,
        wave: { ph: 0, am: 65535, en: 0 },
        atom: atomAA,
    };
    const hexN1 = toHex(serializeNode(nodeN1));
    const hashN1 = toHex(await hashNode(nodeN1));
    console.log("Canonical Hex:", hexN1);
    console.log("Expected Hash: 06872cfe75b1bc5b49400c2dcf15b94cd2eddfd57c69b3cfbdfa4cd40a5271cd");
    console.log("Actual Hash:  ", hashN1);

    console.log("\n--- Σ-GLYPH TV-N3: DISSONANCE (Signal Damped) ---");
    // SHA-256("Signal Damped") = 7dc48fe882dc426083223e5fb26889ace68aa8f54abd4e37690b72327b87748c
    const signalDampedHash = "7dc48fe882dc426083223e5fb26889ace68aa8f54abd4e37690b72327b87748c";
    const atomDamped = new Uint8Array(
        signalDampedHash.match(/.{1,2}/g)!.map((byte) => parseInt(byte, 16))
    );
    const nodeN3 = {
        op: OpCode.DISSONANCE,
        flags: Flags.F_ATOM,
        wave: { ph: 0, am: 0, en: 0 },
        atom: atomDamped,
    };
    const hashN3 = toHex(await hashNode(nodeN3));
    console.log("Expected Hash: 041e53b1b4de36f92821bc72cd6c0fcf497a9d2e828ebd8bbf6618f06bf61fb9");
    console.log("Actual Hash:  ", hashN3);

    console.log("\n--- Interference Test ---");
    const w1 = { ph: 0, am: 65535, en: 100 };
    const w2 = { ph: 16384, am: 65535, en: 200 }; // 90 degree phase shift
    const result = interfere(w1, w2);
    console.log("W1 + W2 (90deg phase) Result:", result);
    // At 16384 (PI/2), LUT_COS is 0. 
    // amp_factor = round((0 + 32767) * 65535 / 65534) = round(32767.5) = 32768.
    // prod01 = round(65535 * 65535 / 65535) = 65535.
    // new_am = round(65535 * 32768 / 65535) = 32768.
    // new_en = round((100 + 200) / 2) = 150.
}

runTests();

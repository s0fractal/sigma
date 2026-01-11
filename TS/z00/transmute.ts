```ts

import {
    OpCode,
    Flags,
    toHex,
    SigmaNode
} from "../m32/sigma.ts";
import { findGlyph } from "./spectral_core.ts";

async function loadSeed(name: string): Promise<SigmaNode> {
    const path = await findGlyph(name);
    const bytes = await Deno.readFile(path);
    const dv = new DataView(bytes.buffer);

    const flags = dv.getUint8(1);
    return {
        op: dv.getUint8(0),
        flags: flags,
        wave: {
            ph: dv.getUint16(2, false),
            am: dv.getUint16(4, false),
            en: dv.getInt16(6, false),
        }
    };
}

function generateTS(name: string, node: SigmaNode): string {
    const { ph, am, en } = node.wave;
    const phos = (ph / 65535 * 360).toFixed(2);
    const amur = (am / 65535 * 100).toFixed(2);

    let body = "";
    if (node.op === OpCode.LITERAL) {
        if (name === "I") {
            body = `export const ${name} = <T>(x: T): T => x;`;
        } else {
            body = `export const ${name} = { type: "LITERAL", phos: ${ph}, amur: ${am} };`;
        }
    } else if (node.op === OpCode.APPLY) {
        body = `// Molecule born from interference\nexport const ${name} = "RESONANT_BOND";`;
    }

    return `/**
 * Σ-GLYPH Silicon Echo: ${name}
 *
 * PHOS (Identity): ${ph} (~${phos}°)
 * AMUR (Attraction): ${am} (~${amur}%)
 * ENTROPY (Tension): ${en}
 *
 * Intent: ${name}.glyph
 */

${body}
`;
}

async function main() {
    const seeds = ["I", "K", "S", "FALSE"];
    console.log("Σ-TRANSMUTE: Projecting Intent into Silicon...\n");

    await Deno.mkdir("./ts_echo", { recursive: true });

    for (const name of seeds) {
        try {
            const node = await loadSeed(name);
            const code = generateTS(name, node);
            const targetPath = `./ts_echo/${name}.ts`;
            await Deno.writeTextFile(targetPath, code);
            console.log(`Transmuted [${name.padEnd(2)}] -> ${targetPath}`);
        } catch (e) {
            console.error(`Failed to transmute [${name}]: ${e.message}`);
        }
    }

    console.log("\n

🌊

// Σ-PoI: 6a30949ca078999b324005e63d8bbc3638ba833385397e80dd45954404d5afcb

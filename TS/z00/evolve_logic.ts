```ts

import {
    OpCode,
    Flags,
    serializeNode,
    hashNode,
    toHex,
    SigmaNode,
    interfere
} from "../m32/sigma.ts";

async function saveGlyph(name: string, node: SigmaNode) {
    const bytes = serializeNode(node);
    const hash = await hashNode(node);
    const path = `./GLYPH/m32/${name}.glyph`;
    await Deno.writeFile(path, bytes);
    console.log(`Materialized [${name.padEnd(5)}] -> ${toHex(hash)}`);
}

async function materializeLogic() {
    console.log("

```ts
import {
    OpCode,
    Flags,
    serializeNode,
    hashNode,
    toHex,
    interfere,
} from "../m32/sigma.ts";

async function runTests() {
    console.log("

```ts
import { hashNode, toHex, OpCode, Flags, interfere, SigmaNode } from "../m32/sigma.ts";

async function hashFile(path: string): Promise<Uint8Array> {
    const data = await Deno.readFile(path);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    return new Uint8Array(hashBuffer);
}

async function getDirectoryHashes(path: string): Promise<Map<string, Uint8Array>> {
    const hashes = new Map<string, Uint8Array>();
    for await (const entry of Deno.readDir(path)) {
        if (entry.isFile && !entry.name.startsWith(".")) {
            const h = await hashFile(`${path}/${entry.name}`);
            hashes.set(entry.name, h);
        }
    }
    return hashes;
}

/**
 * Calculates the Resonance Hash of a directory.
 * Standard: SHA-256(sorted list of hashes)
 */
async function calculateResonance(path: string): Promise<Uint8Array> {
    const fileHashes = await getDirectoryHashes(path);
    const sortedNames = Array.from(fileHashes.keys()).sort();
    const combined = new Uint8Array(32 * sortedNames.length);
    for (let i = 0; i < sortedNames.length; i++) {
        combined.set(fileHashes.get(sortedNames[i])!, i * 32);
    }
    const resonanceHash = await crypto.subtle.digest("SHA-256", combined);
    return new Uint8Array(resonanceHash);
}

async function auditNode(nodePath: string) {
    console.log(`\n

🌊

// Σ-PoI: 880c546ba11973aa9b2a44bc23652ba1fad3f3aaba1622a514a59eec9092ca0b

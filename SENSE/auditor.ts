import { hashNode, toHex, OpCode, Flags, interfere, SigmaNode } from "../CORE/sigma.ts";

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
    console.log(`\n--- Auditing Node: ${nodePath} ---`);
    const dimensions = ["ts", "rs", "md"];
    const dimHashes = new Map<string, Uint8Array>();

    for (const dim of dimensions) {
        const dimPath = `${nodePath}/${dim}`;
        try {
            const h = await calculateResonance(dimPath);
            dimHashes.set(dim, h);
            console.log(`Dim [${dim}]: ${toHex(h)}`);
        } catch (e) {
            console.log(`Dim [${dim}]: NOT FOUND or EMPTY`);
        }
    }

    // Generate SigmaNode for the node's resonance
    // Conceptual: Node = ts APPLY rs
    if (dimHashes.has("ts") && dimHashes.has("rs")) {
        const sigmaNode: SigmaNode = {
            op: OpCode.APPLY,
            flags: Flags.F_LEFT | Flags.F_RIGHT,
            wave: { ph: 0, am: 65535, en: 0 },
            left: dimHashes.get("ts"),
            right: dimHashes.get("rs"),
        };
        const nodeHash = await hashNode(sigmaNode);
        console.log(`Full Node Resonance (ts + rs): ${toHex(nodeHash)}`);
    }
}

async function main() {
    const nodes = ["0", "1", "2"];
    for (const node of nodes) {
        await auditNode(`/Users/s0fractal/${node}`);
    }
}

if (import.meta.main) {
    main();
}

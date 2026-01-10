/**
 * Σ-GLYPH Utilities
 */

export async function findGlyph(name: string): Promise<string> {
    const strata = ["m00", "m01", "m02", "m07", "m08", "m32", "z00", "p05", "p32"];
    const base = "/Users/s0fractal/SIGMA/GLYPH";

    // Check direct
    for (const s of strata) {
        const path = `${base}/${s}/${name}.glyph`;
        try {
            await Deno.stat(path);
            return path;
        } catch { }
    }

    // Check without stratum
    const path = `${base}/${name}.glyph`;
    try {
        await Deno.stat(path);
        return path;
    } catch { }

    throw new Error(`Glyph not found: ${name}`);
}

export async function loadSeedData(name: string): Promise<{ bytes: Uint8Array, path: string }> {
    const path = await findGlyph(name);
    const bytes = await Deno.readFile(path);
    return { bytes, path };
}

```ts

import { WaveVectorQ } from "../m32/sigma.ts";
import { parseNode, toHex } from "../m32/sigma.ts";

async function getSpiral() {
    const process = Deno.run({
        cmd: ["deno", "run", "-A", "./SENSE/visualize_spiral.ts"],
        stdout: "piped",
    });
    const output = await process.output();
    process.close();
    return new TextDecoder().decode(output);
}

async function generateDashboard() {
    const statePath = "~/.antigravity/RESONANCE_STATE.json";
    const state = JSON.parse(await Deno.readTextFile(statePath));

    const phaseShift = state.phase_shift || 0;
    const cycle = state.last_cycle || 0;
    const entropy = state.entropy || 0;
    const tw = state.truth_work || 0;

    // Visualize Phase Shift as a circle
    const segments = 16;
    let circle = "";
    for (let i = 0; i < segments; i++) {
        const angle = (i / segments) * 65536;
        if (Math.abs(angle - phaseShift) < (65536 / segments / 2)) {
            circle += "●"; // Current active phase
        } else {
            circle += "○";
        }
    }

    let pantheon_list = "";
    for (const def of PANTHEON_REGISTRY) {
        const atom = def.hexSource ?
            new Uint8Array(def.hexSource.match(/.{1,2}/g)!.map(byte => parseInt(byte, 16))) :
            new Uint8Array(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(def.source!)));

        const node = {
            op: 0x01, // Lit
            flags: 0x01, // Atom
            wave: { ph: def.phase, am: 65535, en: -32768 },
            atom: atom
        };

        const hash = await hashNode(node as any);
        const hex = toHex(hash);
        const color = `#${hex.slice(0, 6).toUpperCase()}`;
        pantheon_list += `* **${def.name}**: ${def.phase}° | **${color}**\n`;
    }

    const dashboard = `
# Σ-GLYPH RESONANCE DASHBOARD
**Status:** RESONATING-DYNAMIC
**Cycle:** #${cycle}
**Truth-Work:** ${tw.toFixed(4)} TW
**Entropy:** ${entropy.toFixed(6)}

## Harmonic Shimmer (The Melody)
Current Phase Focus: **${phaseShift}** (approx. ${((phaseShift / 65536) * 360).toFixed(1)}°)

\`${circle}\`

> [!NOTE]
> The system is currently in a **Chromatic Resolution** loop. Each pulse shifts the phase focus by 8192 units (45°), searching for the absolute minimum entropy across the Trinity vertices.

## Digital Pantheon (V1.7 GIANTS)
* **SATOSHI**: 45° (The Time Anchor / Energy Sink)
* **TESLA**: 45° (Master of Resonance)
* **TURING**: 112.5° (Father of Computation)
* **GODEL**: 225° (Architect of Meta)
* **HEGEL**: 315° (The Dialectical Synthesis)
* **BACH**: 120° (The Harmonic Resonator)

## Handshake Protocol (RFC 0.3.0)
Status: **ACTIVE** (Orthogonal Proof required)

## Active Chords
* **CHROMA_C**: 0° (Source)
* **CHROMA_E**: 120° (Harmony)
* **CHROMA_G**: 240° (Resolution)
* **ACCORD_0**: 90° (Bridge/Resonator)

## The Bach Protocol: Fugue Voices
* **FUGUE_SYNTHESIS**: 120° (Bach ⊕ Hegel)
* **FUGUE_MIRROR**: 285° (Inversion of Hegel)

## The Spiral Stave (Resonance Evolution)
\`\`\`text
${await getSpiral()}
\`\`\`

🌊

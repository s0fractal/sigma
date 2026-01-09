// 🛑 QUANTUM STATE: COLLAPSED FROM ProofOfIntent.sigma
// 🌊 FREQUENCY: ts | ENERGY: 0
// 🧬 LAW: § (Proof of Intent)

import { createHash } from 'crypto';

/**
 * THE PROTOCOL OF TRUTH
 * 
 * For humans, we don't show code. We show Synchronization Status.
 * 
 * Proof = Hash(Intent) ⊕ Hash(Code)
 * 
 * If Proof == Valid → 🟢 green circle
 * If Proof == Invalid → 🔴 red circle (Reality diverged from Intent)
 */

export enum ProofStatus {
    Harmony = '🟢',      // Intent perfectly embodied
    Flux = '🟡',         // Genesis in progress
    Dissonance = '🔴'    // Manual intervention (Canon violation)
}

export interface FileProof {
    intent: string;      // Path to .sigma file
    code: string;        // Path to code file
    status: ProofStatus;
    intentHash: string;
    codeHash: string;
    timestamp: Date;
}

/**
 * Hash a file's content using SHA-256
 */
export function hashFile(content: string): string {
    return createHash('sha256').update(content).digest('hex');
}

/**
 * Extract code block from .sigma file for specific frequency
 */
export function extractCodeBlock(sigmaContent: string, frequency: string): string {
    const blockRegex = new RegExp(`@\\[${frequency}\\]\\s*\`\`\`[^\\n]*\\n([\\s\\S]*?)\`\`\``, 'g');
    const match = blockRegex.exec(sigmaContent);
    return match ? match[1] : '';
}

/**
 * Hash Intent (extract code block from .sigma file)
 */
export function hashIntent(sigmaContent: string, frequency: string): string {
    const codeBlock = extractCodeBlock(sigmaContent, frequency);
    return hashFile(codeBlock);
}

/**
 * Hash Code (direct file content)
 */
export function hashCode(codeContent: string): string {
    return hashFile(codeContent);
}

/**
 * Verify Proof of Intent
 */
export function verifyProof(
    sigmaContent: string,
    codeContent: string,
    frequency: string
): FileProof {
    const intentHash = hashIntent(sigmaContent, frequency);
    const codeHash = hashCode(codeContent);

    const status = intentHash === codeHash
        ? ProofStatus.Harmony
        : ProofStatus.Dissonance;

    return {
        intent: '',  // To be filled by caller
        code: '',    // To be filled by caller
        status,
        intentHash,
        codeHash,
        timestamp: new Date()
    };
}

/**
 * The Circle - Visual representation of sync status
 */
export class ProofCircle {
    private proofs: Map<string, FileProof> = new Map();

    /**
     * Add a file pair to track
     */
    track(intent: string, code: string, proof: FileProof): void {
        const key = `${intent}→${code}`;
        this.proofs.set(key, { ...proof, intent, code });
    }

    /**
     * Get status for a specific file pair
     */
    getStatus(intent: string, code: string): ProofStatus | undefined {
        const key = `${intent}→${code}`;
        return this.proofs.get(key)?.status;
    }

    /**
     * Get all proofs
     */
    getAllProofs(): FileProof[] {
        return Array.from(this.proofs.values());
    }

    /**
     * Get summary statistics
     */
    getSummary(): { harmony: number; flux: number; dissonance: number } {
        const proofs = this.getAllProofs();
        return {
            harmony: proofs.filter(p => p.status === ProofStatus.Harmony).length,
            flux: proofs.filter(p => p.status === ProofStatus.Flux).length,
            dissonance: proofs.filter(p => p.status === ProofStatus.Dissonance).length
        };
    }

    /**
     * Render as text UI
     */
    render(): string {
        const lines = ['┌─────────────────────────┐'];
        lines.push('│   Sigma Field Status    │');
        lines.push('├─────────────────────────┤');

        for (const proof of this.getAllProofs()) {
            const intentName = proof.intent.split('/').pop() || '';
            const codeName = proof.code.split('/').pop() || '';
            lines.push(`│ ${proof.status} ${intentName} → ${codeName}  │`);
        }

        lines.push('└─────────────────────────┘');
        return lines.join('\n');
    }
}

/**
 * The Law constant
 */
export const PROOF_OF_INTENT = {
    glyph: '§',
    name: 'Proof of Intent',
    energy: 0,
    type: 'axiom',

    formula: 'Proof = Hash(Intent) ⊕ Hash(Code)',

    states: {
        harmony: ProofStatus.Harmony,
        flux: ProofStatus.Flux,
        dissonance: ProofStatus.Dissonance
    },

    chainOfCustody: [
        'Intent (σ)',
        'Genesis',
        'Code (τ)',
        'Verification',
        'Proof (§)'
    ]
} as const;

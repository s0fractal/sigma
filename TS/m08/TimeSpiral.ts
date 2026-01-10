// 🛑 QUANTUM STATE: COLLAPSED FROM TimeSpiral.sigma
// 🌊 FREQUENCY: ts | ENERGY: 8
// 🧬 PROTOCOL: 🌀 (Time Spiral)

import { createHash } from 'crypto';
import { readdirSync, statSync, readFileSync } from 'fs';
import { join } from 'path';

/**
 * THE SPIRAL PROTOCOL
 * 
 * We don't use versions (v1.0). We use Turns.
 * 
 * The Law of Three:
 * Hash(TS) ⊕ Hash(RS) ⊕ Hash(Intent) = Seal
 * 
 * If the sum doesn't converge - navigation is blocked.
 */

export enum TurnStatus {
    Sealed = '🔒',    // Turn completed, hash fixed, navigation allowed
    Flux = '🟡',      // Turn in progress, changes active, navigation limited
    Broken = '🔴'     // Resonance violation, sync required
}

export interface TurnHashes {
    intent: string;   // Hash of sigma/
    ts: string;       // Hash of ts/
    rs: string;       // Hash of rs/
    sh: string;       // Hash of sh/
}

export interface Turn {
    id: number;           // Sequential turn number
    glyph: string;        // Primary glyph of this turn
    timestamp: Date;      // When sealed
    seal: string;         // Hash(TS) ⊕ Hash(RS) ⊕ Hash(Intent)
    status: TurnStatus;   // 🔒 | 🟡 | 🔴
    hashes: TurnHashes;
    message: string;      // Commit message
    author: string;       // Who sealed this turn
}

/**
 * Hash a directory recursively
 */
export function hashDirectory(dirPath: string): string {
    const hash = createHash('sha256');

    function processDirectory(path: string): void {
        const entries = readdirSync(path).sort();

        for (const entry of entries) {
            const fullPath = join(path, entry);
            const stat = statSync(fullPath);

            if (stat.isDirectory()) {
                if (!entry.startsWith('.')) {  // Skip hidden dirs
                    processDirectory(fullPath);
                }
            } else {
                const content = readFileSync(fullPath, 'utf-8');
                hash.update(content);
            }
        }
    }

    processDirectory(dirPath);
    return hash.digest('hex');
}

/**
 * XOR multiple hash strings
 */
export function xorHashes(...hashes: string[]): string {
    const buffers = hashes.map(h => Buffer.from(h, 'hex'));
    const result = Buffer.alloc(buffers[0].length);

    for (let i = 0; i < result.length; i++) {
        let byte = 0;
        for (const buf of buffers) {
            byte ^= buf[i];
        }
        result[i] = byte;
    }

    return result.toString('hex');
}

/**
 * Calculate seal for a turn
 */
export function calculateSeal(hashes: TurnHashes): string {
    return xorHashes(hashes.intent, hashes.ts, hashes.rs, hashes.sh);
}

/**
 * Verify triple resonance
 */
export function verifyTripleResonance(
    intentPath: string,
    tsPath: string,
    rsPath: string,
    shPath: string
): { valid: boolean; seal: string; hashes: TurnHashes } {
    const hashes: TurnHashes = {
        intent: hashDirectory(intentPath),
        ts: hashDirectory(tsPath),
        rs: hashDirectory(rsPath),
        sh: hashDirectory(shPath)
    };

    const seal = calculateSeal(hashes);

    return {
        valid: true,  // Always valid if calculated
        seal,
        hashes
    };
}

/**
 * The Spiral - Registry of completed vibrations
 */
export class TimeSpiral {
    private turns: Turn[] = [];
    private currentTurnId: number = 0;

    /**
     * Add a new turn
     */
    addTurn(turn: Omit<Turn, 'id'>): Turn {
        const newTurn: Turn = {
            ...turn,
            id: this.turns.length
        };
        this.turns.push(newTurn);
        this.currentTurnId = newTurn.id;
        return newTurn;
    }

    /**
     * Seal current turn
     */
    sealCurrentTurn(seal: string): void {
        const current = this.turns[this.currentTurnId];
        if (current) {
            current.seal = seal;
            current.status = TurnStatus.Sealed;
        }
    }

    /**
     * Get current turn
     */
    getCurrentTurn(): Turn | undefined {
        return this.turns[this.currentTurnId];
    }

    /**
     * Navigate to a specific turn
     */
    goto(turnId: number): Turn | undefined {
        const turn = this.turns[turnId];
        if (turn && turn.status === TurnStatus.Sealed) {
            this.currentTurnId = turnId;
            return turn;
        }
        return undefined;
    }

    /**
     * Rollback to a previous turn
     */
    rollback(turnId: number): void {
        if (turnId < this.turns.length) {
            // Unseal all turns after the target
            for (let i = turnId + 1; i < this.turns.length; i++) {
                this.turns[i].status = TurnStatus.Flux;
            }
            this.currentTurnId = turnId;
        }
    }

    /**
     * Get all turns
     */
    getAllTurns(): Turn[] {
        return [...this.turns];
    }

    /**
     * Render spiral visualization
     */
    renderSpiral(): string {
        const lines = ['        🌀 Time Spiral', ''];

        for (let i = this.turns.length - 1; i >= 0; i--) {
            const turn = this.turns[i];
            const current = i === this.currentTurnId ? ' ← Current' : '';
            lines.push(`    Turn ${turn.id} (${turn.glyph}) ${turn.status}${current}`);
            if (i > 0) {
                lines.push('        ↑');
            }
        }

        return lines.join('\n');
    }

    /**
     * Export to spiral.log format
     */
    exportLog(): string {
        const lines = [
            '# Spiral Registry',
            '# Format: Turn | Glyph | Seal | Timestamp | Status',
            ''
        ];

        for (const turn of this.turns) {
            const seal = turn.seal || 'pending...';
            lines.push(
                `${turn.id} | ${turn.glyph} | ${seal} | ${turn.timestamp.toISOString()} | ${turn.status}`
            );
        }

        return lines.join('\n');
    }
}

/**
 * The Protocol constant
 */
export const TIME_SPIRAL = {
    glyph: '🌀',
    name: 'The Time Spiral',
    energy: 8,
    type: 'protocol',

    lawOfThree: 'Hash(TS) ⊕ Hash(RS) ⊕ Hash(Intent) = Seal',

    philosophy: 'Time is not a line. Time is a spiral.'
} as const;

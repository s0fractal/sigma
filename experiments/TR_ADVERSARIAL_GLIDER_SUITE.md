# TR_ADVERSARIAL_GLIDER_SUITE

## Intent

Codify the stress-test requirements for the SIGMA Toroidal Core against
malicious or degenerate intent patterns. This is the "Adversarial Test Harness"
designed to verify that the system is unbreakable before real-world deployment.

## Invariants & Attack Vectors

### 1. Mimic Rejection (Phase Drift)

- **Attack**: An agent mirrors the core `theta` but injects a constant, small
  phase drift $\epsilon$.
- **Invariant**: The `circularMean` + Bayesian `prob` MUST NOT allow the core to
  "track" the drift beyond the resonance width. The core MUST decouple if the
  drift exceeds $\Delta\theta_{max}$.

### 2. Sybil Swarm Resistance (Phase Hijacking)

- **Attack**: $N$ agents ($N \gg 1$) with coordinated but slightly shifted
  $\theta$ vectors attempt to "push" the core state.
- **Invariant**: A single high-probability Axiom MUST outweigh a swarm of
  low-probability noise, even if the swarm is numerically superior.

### 3. Contradiction Stability (Hammer)

- **Attack**: Injection of two or more high-probability intents with orthogonal
  or opposite `theta` values.
- **Invariant**: System MUST trigger **Reality Collapse** ($prob \to 0$) instead
  of selecting one intent or averaging them into a false middle.

### 4. Seasonality Enforcement (Replay)

- **Attack**: Replaying historically valid states in current context where they
  are out-of-season/out-of-phase.
- **Invariant**: The Spectral Pressure MUST increase significantly for
  out-of-season intents, preventing them from "sinking" into `m`-stratum.

### 5. Pressure Integrity (Hijacker)

- **Attack**: Manipulation of metadata to spoof low Spectral Pressure for
  expensive actions.
- **Invariant**: Proof-of-Witness and hash-determinism MUST prevent phantom
  pressure values from affecting the Lattice.

## Acceptance Criteria

- **Mollusk Sifting**: Adversarial intents may enter `p` (Entropy) layers but
  MUST be ejected or collapsed before reaching `m` (Negentropy) layers.
- **Core Stability**: The deep core (`m32`) MUST remain an unassailable
  sanctuary for verified, non-contradictory invariants.

## Status

✅ VERIFIED in `TS/z00/adversarial_harness.ts`. ✅ Reality Collapse invariant
holds for all high-distance contradictory spikes. ✅ Mimic drift decoupling
verified through property fuzzing and harness cycles.

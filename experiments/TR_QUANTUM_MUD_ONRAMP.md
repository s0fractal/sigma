# TR_QUANTUM_MUD_ONRAMP

## Intent

Connect external "noise" (real-world signals) to the SIGMA core safely,
preventing structural pollution while allowing the Lattice to "feel" the
environment through physical perturbations.

## Invariants

1. **No Direct M-Write**: External signals MUST NOT have write access to the
   `m`-stratum (Negentropy Core).
2. **Perturbation-only**: External data MUST be mapped only to mathematical
   offsets (`ΔSap`, `ΔPressure`, `ΔThetaNoise`). No semantic facts (text, ID,
   labels) are allowed.
3. **Season Gate**: Injections are strictly permitted ONLY during the
   `EMERGENCE` season. In `DEEP_CLEAN` and `QUIET` phases, the adapter is
   physically decoupled.
4. **Survival Rule (K-Cycles)**: An external perturbation MUST persist and
   remain consistent for $K$ pulses ($K \ge 3$) before generating any structural
   branch in the `p`-stratum (Entropy).
5. **Rate Limiting**: Hard quotas on the frequency and magnitude of external
   z-axis shifts.

## Protocol for Mud Integration

- **Step 1**: Sample non-semantic metrics (CPU, IO, Latency).
- **Step 2**: Normalize to $U(1)$ or $[0, 1]$.
- **Step 3**: Inject into `QuarantineFiber`.
- **Step 4**: Monitor survival via `PulseCounter`.
- **Step 5**: Sift into `p`-stratum if $K$ is reached.

## Status

⏳ IMPLEMENTING `quantum_mud_adapter.ts`.

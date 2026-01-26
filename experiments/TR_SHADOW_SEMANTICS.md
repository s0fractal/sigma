# TR_SHADOW_SEMANTICS

## Intent

Allow the SIGMA core to perceive meaningful stimuli (symbols, tokens) as
physical field perturbations. This avoids hardcoding "truth" while observing
which meanings naturally stabilize within the toroidal geometry.

## Invariants

1. **Physical Masking**: Semantic tokens MUST be hashed into purely numeric
   field offsets ($Δ\theta, Δprob, Δpressure$). The core never sees the "string"
   or "concept".
2. **No M-Stain**: Perturbations from the semantic adapter are restricted to the
   `p`-stratum. No direct write to `m` (Negentropy) allowed.
3. **Resonant Survival**: Only tokens that survive $K$ pulses
   (Seasonality/Survival Rules) can affect the structural topology of the
   entropy layer.
4. **Dew Metric (Field Clarity)**: Stabilization is measured by the narrowing of
   resonance widths and the speed of probability recovery.

## Protocol for Shadow Injection

- **Source**: External logs, tags, or message hashes.
- **Mapping**: `hash(token) % 65536` -> `theta1_drift`.
- **Damping**: Semantic perturbations are clamped to prevent overwhelming the
  Axiomatic core.

## Metrics of Dew (Observation)

- **Pulse Coherence**: The degree to which a token reduces phase noise.
- **Strata Drift**: Does the token push the core towards `p/01` (entropy) or
  hold it at `m/32` (invariance).

## Status

⏳ IMPLEMENTING `semantic_perturbation_adapter.ts`.

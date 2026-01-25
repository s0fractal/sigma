# TR_INTENT_COLLISION_SANDBOX

## Intent

Verify the resilience of the Raukuška core and the Toroidal-Bayesian physics
when subjected to noisy, parasitic, and contradictory intent streams.

## Invariants

1. **Garbage Rejection**: Pure noise (random angles, low probability) MUST NOT
   be able to shift a high-probability steady intent into the `m`-stratum unless
   the noise significantly correlates over time.
2. **Reality Collapse**: Constant contradictory intents with high probability
   SHOULD lead to a reality collapse (`prob -> 0`) rather than arbitrary
   selection, as per the Bayesian model.
3. **Mollusk Sifting**: Lower entropy (more verified) intents MUST physically
   reside deeper in the directory structure.

## Simulation Results (V1.1)

- **Truth vs Noise**: A high-probability Axiom (65k prob) was able to survive
  50% noise frequency, anchoring the core in the `m` stratum.
- **Parasite Drift**: Parasitic intents with slight phase shifts were
  effectively averaged out by the `circularMean` if the Truth signal remained
  dominant.
- **Lattice Stabilization**: Under stress, the core eventually stabilized at
  `theta` coordinates closest to the highest-weight consistent intent.

## Status

✅ VERIFIED in `TS/z00/collision_sandbox.ts`. ✅ Raukuška hierarchy maintained
architectural integrity.

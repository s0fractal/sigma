# TR_TORUS_METRIC_CORRECTION

## Intent

Enforce toroidal wrap-around metrics for all angular calculations, preventing
"edge effects" and physical degradation at the $[0, 2\pi)$ boundary.

## Invariants

1. **Shortest Arc Delta**: Any difference between angles $a, b \in [0, 65535]$
   MUST use $\Delta = \min(|a-b|, 65536 - |a-b|)$.
2. **Euclidean Distance on $T^2$**: Distance between WaveVectors MUST be
   calculated as $D = \sqrt{\Delta\theta_1^2 + \Delta\theta_2^2}$.
3. **Circular Statistics**: Any aggregation or averaging of angles MUST use
   vector summation (sine/cosine) to correctly handle the wrap-around point.

## Test Vectors

- $dist(\theta=65535, \theta=0) \approx 1$ (Shortest arc)
- $dist(\theta=32768, \theta=0) = 32768$ (Maximum distance)
- $dist(\theta=40000, \theta=0) = 25536$ (Wrap-around distance)

## Status

✅ IMPLEMENTED in `TS/z00/physics.ts`: `wrapDeltaU16`, `toroidalDistance`.

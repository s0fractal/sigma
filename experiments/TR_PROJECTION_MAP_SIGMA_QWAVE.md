# TR_PROJECTION_MAP_SIGMA_QWAVE

## Intent

Establish a deterministic, bidirectional (where possible) bridge between the
in-memory `SigmaNode` and the persistent `.qwave` record format.

## Invariants

1. **One Source of Truth**: The mapping MUST be centralized in
   `projection_map.ts`. Ad-hoc conversions in other modules are prohibited.
2. **Loss Model Transparency**:
   - `theta1/theta2`, `prob`, and `en` MUST be preserved losslessly.
   - `omega` values from `QWave` ARE DISCARDED when converting to `SigmaNode`
     (V2).
   - `SigmaNode.op` MUST be provided externally during `QWave -> Sigma`
     conversion as it not part of the `WaveVectorK` state.
3. **Format Versioning**: The bridge version `ProjectionVersion = 1` MUST be
   checked.
4. **Flag Preservation**: `F_V2` and `F_PORTAL` MUST be mapped to the `QWave`
   flag field.

## Round-Trip Stability

Test Case: `node == qWaveToSigma(sigmaToQWave(node))`

- ✅ `theta1`: Stable
- ✅ `theta2`: Stable
- ✅ `prob`: Stable
- ✅ `en`: Stable
- ⚠️ `op`: Requires external preservation.

## Status

✅ IMPLEMENTED in `TS/z00/projection_map.ts`.

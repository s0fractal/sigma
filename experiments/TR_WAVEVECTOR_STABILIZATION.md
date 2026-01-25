# TR_WAVEVECTOR_STABILIZATION

## Intent

Stabilize the transformation from Linear Phase-Amplitude to Toroidal
Angle-Probability coordinates, ensuring physical conservation laws and
architectural integrity.

## Invariants

1. **Angle Integration (Circular Mean)**: Angles $\theta_1, \theta_2$ MUST be
   merged using circular statistics. Arithmetric mean is prohibited to avoid
   phase-flip degradation.
2. **Probability Conservation (Log-Odds)**: Reality density `prob` MUST be
   integrated via Bayesian log-odds (Bayes' rule) to prevent "reality doping"
   (self-amplifying hallucinations).
3. **Format Versioning (F_V2)**: Any node using the 10-byte toroidal header MUST
   set the `F_V2` flag (0x08).
4. **Portal Witness (F_PORTAL)**: Transition to the `m`-stratum (negentropy)
   MUST be marked with the `F_PORTAL` flag (0x10) as a proof-of-witness.

## Mathematical Proof

$$ \theta_{integrated} = \operatorname{atan2}\left(\sum \sin(\theta_i), \sum \cos(\theta_i)\right) $$

$$ P_{integrated} = \frac{p_1 p_2}{p_1 p_2 + (1-p_1)(1-p_2)} $$

## Status

✅ IMPLEMENTED in `TS/z00/physics.ts` ✅ VERIFIED in `TS/m32/sigma.ts` parser.

# TR_STRUCTURAL_REFINEMENT

## Intent

Refine core structural invariants to prevent topological asymmetry and define
strict policies for stochastic edge cases.

## Invariants

### 1. Raukuška Baselayer Quantization (Task A)

- **Constraint**: Every state with non-zero entropy MUST reside in a quantized
  layer.
- **Fix**: For $en < 0$, the depth is now $\max(1, \lfloor |en|/1024 \rfloor)$.
- **Stability**: Prevents "phantom cores" at $m/$ without a layer index.

### 2. Bayesian Reality Collapse (Task B)

- **Policy**: In `integrateProb`, if the evidence is perfectly contradictory
  ($den = 0$), the result MUST be $prob = 0$.
- **Reasoning**: Silence/Collapse is the only physical response to absolute
  contradiction in a Bayesian toroid.

### 3. Noise Entropy Invariant (Task C)

- **Constraint**: External perturbations from the `QuarantineFiber` MUST NOT be
  able to decrease entropy (increase the invariance depth).
- **Enforcement**: Explicit check and rollback in `applyPerturbationsToP`.

## Status

✅ IMPLEMENTED in `physics.ts` and `quarantine_fiber.ts`. ✅ VERIFIED through
structural analysis.

# Σ-GLYPH Specification V2.3: Deterministic Resonance

## 1. SCR-1: Sigma Canonical Representation

To ensure bit-exact reproducibility, the extraction of data from a `.sigma` file
must follow these rules:

### A. Byte Normalization

- **Encoding**: UTF-8.
- **Line Endings**: LF (`0x0A`). All CRLF must be converted to LF before
  processing.
- **Whitespace**: No trailing spaces on any line.

### B. Block Extraction Algorithm

1. Locate the marker: `@[tag]\n`.
2. Locate the next marker start: `\n@[` OR the seal: `\n🔒:`.
3. The **Payload** is exactly every byte between the end of the `\n` in the
   start marker and the byte before the `\n` of the next marker/seal.
4. **Fences**: If the payload starts with `` ``` `` and ends with `` ``` ``, the
   fences and the immediately following/preceding newlines are **INCLUDED** in
   the raw payload for hashing (to avoid heuristic stripping), unless
   specifically stripped by the materializer for dimension-specific projection.

### C. Identity Extraction

- **Canonical Body**: Everything from byte 0 to the byte immediately preceding
  the `\n🔒:` seal.
- **NodeHash**: `SHA-256(Canonical Body)`.

---

## 2. PoI-1: Proof of Intent

Verification protocol for the relationship between Intent (Sigma) and Projection
(Generated Code).

- **Formula**: `PoI = SHA-256(IntentHash || CodeHash)`
- **Verification States**:
  - 🟢 **Pure**: `PoI` matches, `NodeHash` is valid.
  - 🔴 **Dissonance**: Hashes mismatch (Symmetry Breaking).
  - 🟡 **Ghost**: `NodeHash` is valid, but projected file is missing.

---

## 3. Core Identities (Test Vectors)

| Glyph     | DNA Formula     | Expected SCR-1 NodeHash (Prefix) |
| :-------- | :-------------- | :------------------------------- |
| **I**     | `λx.x`          | `3ef2...`                        |
| **K**     | `λx.y.x`        | `...`                            |
| **S**     | `λx.y.z.xz(yz)` | `...`                            |
| **FALSE** | `λx.y.y`        | `...`                            |

---

## 4. Path Philosophy

- Tools MUST use `Path(__file__).parents[2]` or `.git` discovery.
- Use `SIGMA_GARDEN` env var for external storage; default to
  `Path.home() / .sigma_garden`.

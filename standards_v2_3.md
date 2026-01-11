# Σ-GLYPH Specification V2.3: Deterministic Resonance

### 1. SCR-1: Stable Canonical Resonance

To achieve deterministic identity, every `.sigma` file MUST follow the SCR-1
extraction rules:

- **Normalization**: UTF-8, LF endings, no trailing whitespace, exactly one
  final `\n`.
- **Policy A (Strict Identity)**: Any content change (excluding markers) MUST
  result in a different NodeHash.
- **NodeHash Extraction**:
  1. Strip the seal line using strictly matched regex:
     `\n(?:🔒:|CHECKSUM:)\s*[0-9a-f]{64}\s*$`.
  2. Remove the `🧬IDENTITY:` header line.
  3. Return resulting UTF-8 bytes for hashing.
- **Seal**: `🔒: <hash>` must match `NodeHash`.

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

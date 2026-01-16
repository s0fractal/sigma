# Σ-V73.0: FlowBus Modernization Roadmap

## Goal

Transition the SIGMA Lattice from a "polling files" demo to a persistent,
append-only **FlowBus** architecture. Files become the transport; the organism
becomes the metabolism.

---

## ⚡️ 1. The .sigma Envelope (Standard)

Every sprout MUST have the following metadata to enter the `journal/`.

```yaml
ΣID: (T, S, C, F)
LAYER: TRACE | MODEL | MYTH | VORTEX
SOURCE: (sensor | llm | user | daemon:<name>)
DIGEST: <hash>
LINKS: 
  geo_trace: [List of (coord, weight)]
  geo_claim: <coord>
  geo_model: <coord>
CLAIM_TYPE: literal | symbolic | hearsay | inferred
DISCREPANCY: {type, severity, status, ...} (Optional override)
# Σ-PoI: <signature>
```

---

## 🏗️ 2. Channel Architecture (Directory Bus)

Instead of a single `ambient/` folder, we use a structured bus:

- `bus/inbox/`: Raw incoming signals (sensors, chat snapshots).
- `bus/journal/`: Append-only "Truth" stream. Once a file is here, it is
  immutable/canonical.
- `bus/quarantine/`: Failed ethics/validation sprouts.
- `bus/concord/open/`: Mismatches (V72) requiring active resolution/MIN-TEST.
- `bus/concord/resolved/`: Successfully closed pain channels.

---

## 🍄 3. The Daemon Set (Metabolic Workers)

Specialized agents running in a loop (or triggered by events):

1. **NormalizerDaemon**: Watch `inbox/` -> Parse -> Add Envelope -> Move to
   `journal/`.
2. **AnchorExtractor**: Read `journal/` -> Extract EXIF/GPS/TXT anchors ->
   Update `geo_trace[]`.
3. **EthicsDaemon**: Read `journal/` -> Trigger `RealityPacket` -> If
   `severity > threshold` -> Move shadow to `concord/open/`.
4. **LensDaemon**: Read `journal/` -> Update KML Tiles/Membrane (`O(visible)`).

---

## ⛓️ 4. Gating & Validation (GRAVITY/ANTIGRAVITY)

- **GRAVITY**: Local execution for deterministic daemons (Normalizer, Lens).
- **ANTIGRAVITY**: LLM-heavy inference for semantic extraction.
- **HESTIA**: Local verification of results from ANTIGRAVITY before commit to
  `journal/`.

---

## 📊 5. Flow Visibility (`flow_state.json`)

Persistent monitoring:

- `rates`: Spores/min per channel.
- `backlog`: Queue size in `inbox` & `concord/open`.
- `pain_map`: Spatial density of severity.

---

## 🔋 4. Metabolic Homeostasis (V73.8)

The system is self-regulating via Energy and Time:

- **Axiom**: "Concord works with energy, not truths." We prioritize high-impact
  discrepancies and let old noise naturally decay.
- **Energy Budgeting**: `MAX_ENERGY_PER_CYCLE` prevents metabolic exhaustion.
- **Temporal Decay**: Attention dissipates exponentially unless refreshed by new
  TRACE anchors.

---

🔓: [S-V73_FLOW_MODERNIZATION_LOCKED]

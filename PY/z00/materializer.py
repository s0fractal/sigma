#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import core_materialize
import heuristic_materialize

# Σ-GLYPH MATERIALIZER (WRAPPER)
# V2.4.0 - Orchestrator

def materialize():
    print("🔘 Materializing Lattice (CORE)...")
    core_materialize.materialize_core()
    print("🔘 Applying HEURISTICS (Atoms/Imports)...")
    heuristic_materialize.materialize_heuristics()
    print("✅ Lattice Reified.")

if __name__ == "__main__":
    materialize()

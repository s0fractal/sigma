#!/bin/bash
# s0fractal Structure Guard (Python)
# Enforces topology and sigma canons using a Unicode-safe engine.

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
python3 "$REPO_ROOT/tools/py/guard.py" "$@"

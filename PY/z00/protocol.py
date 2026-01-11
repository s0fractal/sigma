# Σ-GLYPH Protocol Constants (Sync with protocol.json)
from __future__ import annotations
import json
from pathlib import Path

def get_repo_root() -> Path:
    """Deterministic repository root discovery."""
    cur = Path(__file__).resolve()
    for parent in [cur] + list(cur.parents):
        if (parent / ".git").exists():
            return parent
    return Path.cwd()

ROOT = get_repo_root()
PROTOCOL_PATH = ROOT / "sigma" / "m32" / "protocol.json"

try:
    _data = json.loads(PROTOCOL_PATH.read_text())
except:
    # Hardcoded fallback to ensure bootstrapping
    _data = {
        "OPCODES": {"LITERAL": 0, "REF": 1, "APPLY": 2, "LAMBDA": 3, "DISSONANCE": 255},
        "FLAGS": {"F_ATOM": 1, "F_LEFT": 2, "F_RIGHT": 4}
    }

OP_LITERAL = _data["OPCODES"]["LITERAL"]
OP_REF = _data["OPCODES"]["REF"]
OP_APPLY = _data["OPCODES"]["APPLY"]
OP_LAMBDA = _data["OPCODES"]["LAMBDA"]
OP_DISSONANCE = _data["OPCODES"]["DISSONANCE"]

F_ATOM = _data["FLAGS"]["F_ATOM"]
F_LEFT = _data["FLAGS"]["F_LEFT"]
F_RIGHT = _data["FLAGS"]["F_RIGHT"]

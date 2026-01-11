import os
import hashlib
from pathlib import Path
from typing import Optional

class CASStore:
    def __init__(self, root: Path):
        self.root = root / "cas"
        self.root.mkdir(parents=True, exist_ok=True)

    def _get_path(self, h: str) -> Path:
        return self.root / h[:2] / h[2:]

    def put(self, data: bytes) -> str:
        h = hashlib.sha256(data).hexdigest()
        path = self._get_path(h)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        return h

    def get(self, h: str) -> Optional[bytes]:
        path = self._get_path(h)
        if not path.exists(): return None
        data = path.read_bytes()
        # Full hash verification
        if hashlib.sha256(data).hexdigest() != h:
            raise ValueError(f"CAS Corruption: Hash mismatch for {h}")
        return data

    def exists(self, h: str) -> bool:
        return self._get_path(h).exists()

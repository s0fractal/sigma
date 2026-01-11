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

    def manifest(self) -> set[str]:
        """Returns a set of all Content-Addressed hashes currently stored."""
        keys = set()
        # Structure is root/xx/yyyyyyyy...
        # We need to traverse deterministically, though set order doesn't matter.
        if not self.root.exists(): return keys
        
        for parent in self.root.iterdir():
            if parent.is_dir() and len(parent.name) == 2:
                for child in parent.iterdir():
                    if child.is_file():
                        keys.add(parent.name + child.name)
        return keys

    def delta(self, remote_manifest: set[str]) -> set[str]:
        """
        Anti-Entropy: Returns the set of keys present in remote_manifest 
        but MISSING from this local store. (What I need to pull).
        """
        local = self.manifest()
        return remote_manifest - local

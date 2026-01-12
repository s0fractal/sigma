"""
Σ-GLYPH Akasha CAS
Content-Addressed Storage for immutable blobs
V2.4.0 - LUT Authority
"""

import hashlib
from pathlib import Path
import tempfile
import os


class AkashaStore:
    """
    Content-Addressed Storage for immutable blobs.
    
    Properties:
    - Blobs stored by SHA-256 hash
    - Prefix sharding (first 2 chars) for filesystem performance
    - Atomic writes (temp file + rename)
    - No mutation - blobs are immutable
    """
    
    def __init__(self, root: Path):
        """
        Initialize Akasha store.
        
        Args:
            root: Repository root path
        """
        self.root = root / "AKASHA" / "blobs"
        self.root.mkdir(parents=True, exist_ok=True)
    
    def _blob_path(self, hash_hex: str) -> Path:
        """
        Get path for blob with prefix sharding.
        
        Args:
            hash_hex: SHA-256 hash (64 hex chars)
        
        Returns:
            Path to blob file
        """
        if len(hash_hex) != 64:
            raise ValueError(f"Invalid hash length: {len(hash_hex)} (expected 64)")
        
        prefix = hash_hex[:2]
        return self.root / prefix / hash_hex
    
    def put(self, data: bytes) -> str:
        """
        Store blob and return its hash.
        
        Args:
            data: Raw blob bytes
        
        Returns:
            SHA-256 hash (hex string)
        """
        # Compute hash
        blob_hash = hashlib.sha256(data).hexdigest()
        blob_path = self._blob_path(blob_hash)
        
        # Skip if already exists
        if blob_path.exists():
            # Verify existing blob
            existing_data = blob_path.read_bytes()
            if existing_data != data:
                raise ValueError(f"Hash collision detected: {blob_hash}")
            return blob_hash
        
        # Atomic write: temp file + rename
        blob_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode='wb',
            dir=blob_path.parent,
            delete=False,
            prefix='.tmp_'
        ) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        
        try:
            os.rename(tmp_path, blob_path)
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise e
        
        return blob_hash
    
    def get(self, hash_hex: str) -> bytes:
        """
        Retrieve blob by hash.
        
        Args:
            hash_hex: SHA-256 hash (hex string)
        
        Returns:
            Raw blob bytes
        
        Raises:
            FileNotFoundError: Blob not found
            ValueError: Blob corruption detected
        """
        blob_path = self._blob_path(hash_hex)
        
        if not blob_path.exists():
            raise FileNotFoundError(
                f"Blob not found in Akasha: {hash_hex}\n"
                f"Expected path: {blob_path}"
            )
        
        data = blob_path.read_bytes()
        
        # Verify integrity
        actual_hash = hashlib.sha256(data).hexdigest()
        if actual_hash != hash_hex:
            raise ValueError(
                f"Blob corruption detected!\n"
                f"Expected: {hash_hex}\n"
                f"Actual:   {actual_hash}"
            )
        
        return data
    
    def verify(self, hash_hex: str) -> bool:
        """
        Verify blob exists and matches hash.
        
        Args:
            hash_hex: SHA-256 hash (hex string)
        
        Returns:
            True if blob exists and is valid, False otherwise
        """
        try:
            self.get(hash_hex)
            return True
        except (FileNotFoundError, ValueError):
            return False
    
    def exists(self, hash_hex: str) -> bool:
        """
        Check if blob exists (without verification).
        
        Args:
            hash_hex: SHA-256 hash (hex string)
        
        Returns:
            True if blob file exists, False otherwise
        """
        blob_path = self._blob_path(hash_hex)
        return blob_path.exists()

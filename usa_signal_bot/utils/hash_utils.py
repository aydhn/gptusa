"""Hash utilities for USA Signal Bot."""

import hashlib

def sha256_bytes(data: bytes) -> str:
    """Computes the SHA256 hash of a byte string."""
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()

def sha256_text(text: str) -> str:
    """Computes the SHA256 hash of a string."""
    return sha256_bytes(text.encode("utf-8"))

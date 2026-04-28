"""File integrity utilities for storage layer."""

import os
import hashlib
from pathlib import Path
from typing import Any

from usa_signal_bot.utils.file_utils import file_exists
from usa_signal_bot.core.exceptions import StorageIntegrityError, StoragePathError

def sha256_file(path: Path) -> str:
    """Computes the SHA256 checksum of a file."""
    validate_file_exists(path)
    hasher = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def file_size_bytes(path: Path) -> int:
    """Returns the size of a file in bytes."""
    validate_file_exists(path)
    return path.stat().st_size

def validate_file_exists(path: Path) -> None:
    """Raises an error if the file does not exist."""
    if not file_exists(path):
        raise StorageIntegrityError(f"File not found: {path}")

def validate_file_under_root(path: Path, root: Path) -> None:
    """Raises an error if the path escapes the root directory."""
    try:
        resolved_path = path.resolve()
        resolved_root = root.resolve()
        # Verify that resolved_path starts with resolved_root
        if not str(resolved_path).startswith(str(resolved_root)):
            raise StoragePathError(f"Path traversal detected: {path} escapes {root}")
    except RuntimeError as e:
         raise StoragePathError(f"Path resolution error: {e}")

def build_file_metadata(path: Path) -> dict[str, Any]:
    """Builds a metadata dictionary for a file."""
    validate_file_exists(path)
    return {
        "size_bytes": file_size_bytes(path),
        "sha256": sha256_file(path),
        "modified_at": path.stat().st_mtime
    }

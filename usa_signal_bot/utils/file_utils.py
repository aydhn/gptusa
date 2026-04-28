"""File system utility functions."""

import os
from pathlib import Path

import tempfile
import shutil
import uuid
import re

def ensure_parent_dir(path: Path) -> None:
    """Ensures that the parent directory of a path exists."""
    safe_mkdir(path.parent)

def atomic_write_bytes(path: Path, data: bytes) -> Path:
    """Writes bytes to a file atomically."""
    ensure_parent_dir(path)
    temp_path = path.with_name(f"{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with open(temp_path, 'wb') as f:
            f.write(data)
        # Use replace for atomic operation
        temp_path.replace(path)
        return path
    except Exception as e:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        raise e

def atomic_write_text(path: Path, text: str) -> Path:
    """Writes text to a file atomically."""
    return atomic_write_bytes(path, text.encode("utf-8"))

def normalize_safe_filename(name: str) -> str:
    """Normalizes a filename to make it safe for storage."""
    # Basic sanitization, allow alphanumeric, dot, dash, underscore
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', name)
    # Remove path traversal characters just in case
    safe_name = safe_name.replace('..', '_')
    if not safe_name:
        safe_name = "unnamed_file"
    return safe_name

def assert_relative_filename(name: str) -> None:
    """Asserts that a filename does not contain path traversal elements."""
    if '..' in name or '/' in name or '\\' in name or Path(name).is_absolute():
        from usa_signal_bot.core.exceptions import PathError
        raise PathError(f"Path traversal detected in filename: {name}")


def safe_mkdir(path: Path) -> None:
    """Creates a directory safely, including parents."""
    path.mkdir(parents=True, exist_ok=True)

def read_text_file(path: Path) -> str:
    """Reads and returns the content of a text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_text_file(path: Path, content: str) -> None:
    """Writes content to a text file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def append_text_file(path: Path, content: str) -> None:
    """Appends content to a text file."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)

def file_exists(path: Path) -> bool:
    """Checks if a file exists."""
    return path.exists() and path.is_file()

def is_writable_dir(path: Path) -> bool:
    """Checks if a directory exists and is writable."""
    return path.exists() and path.is_dir() and os.access(path, os.W_OK)

def read_last_lines(path: Path, n: int) -> list[str]:
    """Reads the last n lines from a file efficiently."""
    if not file_exists(path):
        return []

    # Simple implementation, can be optimized for huge files
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines[-n:] if n > 0 else []

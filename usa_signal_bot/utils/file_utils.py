"""File system utility functions."""

import os
from pathlib import Path

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

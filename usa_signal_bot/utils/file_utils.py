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

def file_exists(path: Path) -> bool:
    """Checks if a file exists."""
    return path.exists() and path.is_file()

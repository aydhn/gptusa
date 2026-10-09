"""Shared plain-file IO helpers for paper_* store modules.

Behavior mirrors the previously duplicated per-package helpers exactly:
default text encoding, ``indent=2`` JSON, no key sorting, non-atomic writes.
"""
import json
from pathlib import Path
from typing import Any, Iterable, List, Optional


def ensure_dir(path: Path) -> Path:
    """Create ``path`` (parents included) if missing and return it."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, data: Any, *, indent: Optional[int] = 2, ensure_parent: bool = True) -> Path:
    """Write ``data`` as JSON to ``path`` (overwrite). Returns ``path``."""
    if ensure_parent:
        ensure_dir(path.parent)
    with open(path, "w") as f:
        json.dump(data, f, indent=indent)
    return path


def write_jsonl(path: Path, rows: Iterable[Any], *, mode: str = "w", ensure_parent: bool = True) -> Path:
    """Write one ``json.dumps(row)`` line per row. ``mode`` is "w" or "a"."""
    if ensure_parent:
        ensure_dir(path.parent)
    with open(path, mode) as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    return path


def append_jsonl(path: Path, rows: Iterable[Any], *, ensure_parent: bool = True) -> Path:
    """Append rows as JSON lines (creates the file if missing)."""
    return write_jsonl(path, rows, mode="a", ensure_parent=ensure_parent)


def read_json(path: Path) -> Any:
    """Read JSON from ``path``. Missing file raises FileNotFoundError; bad JSON raises JSONDecodeError."""
    with open(path, "r") as f:
        return json.load(f)


def read_jsonl(path: Path) -> List[Any]:
    """Read JSON lines; blank lines are skipped. Missing file raises FileNotFoundError."""
    rows: List[Any] = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def list_files(directory: Path, pattern: str = "*", *, sort: bool = False, reverse: bool = False) -> List[Path]:
    """Glob ``pattern`` in ``directory``; missing directory yields ``[]``.

    Unsorted by default (glob order). ``sort=True`` sorts by path, ``reverse`` flips it.
    """
    if not directory.exists():
        return []
    files = list(directory.glob(pattern))
    if sort or reverse:
        files = sorted(files, reverse=reverse)
    return files


def count_files(directory: Path, pattern: str = "*") -> int:
    """Number of files matching ``pattern``; 0 if directory is missing."""
    return len(list_files(directory, pattern))


def latest_by_mtime(files: List[Path]) -> Optional[Path]:
    """Newest file by mtime, or None for an empty list."""
    if not files:
        return None
    return sorted(files, key=lambda p: p.stat().st_mtime)[-1]

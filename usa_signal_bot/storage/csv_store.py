"""CSV file storage operations."""

import csv
import io
from pathlib import Path
from typing import Any, List, Optional

from usa_signal_bot.utils.file_utils import ensure_parent_dir, atomic_write_text, write_text_file, read_text_file, file_exists
from usa_signal_bot.core.exceptions import StorageReadError, ValidationError

def infer_fieldnames(rows: List[dict[str, Any]]) -> List[str]:
    """Infers deterministic field names from a list of dictionaries."""
    if not rows:
        return []

    fields = set()
    for row in rows:
        fields.update(row.keys())

    return sorted(list(fields))

def write_csv(path: Path, rows: List[dict[str, Any]], fieldnames: Optional[List[str]] = None, atomic: bool = True) -> Path:
    """Writes a list of dictionaries to a CSV file."""
    if not rows and not fieldnames:
        raise ValidationError("Cannot write empty CSV without fieldnames.")

    if not fieldnames:
        fieldnames = infer_fieldnames(rows)

    ensure_parent_dir(path)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    # Ensure all values are stringifiable for CSV
    for row in rows:
        str_row = {k: str(v) if v is not None else "" for k, v in row.items() if k in fieldnames}
        writer.writerow(str_row)

    content = output.getvalue()

    if atomic:
        atomic_write_text(path, content)
    else:
        write_text_file(path, content)

    return path

def read_csv(path: Path) -> List[dict[str, str]]:
    """Reads a CSV file into a list of dictionaries."""
    if not csv_exists(path):
        return []

    try:
        content = read_text_file(path)
        if not content.strip():
            return []

        reader = csv.DictReader(io.StringIO(content))
        return list(reader)
    except Exception as e:
        raise StorageReadError(f"Failed to read CSV from {path}: {e}")

def csv_exists(path: Path) -> bool:
    """Checks if a CSV file exists."""
    return file_exists(path)

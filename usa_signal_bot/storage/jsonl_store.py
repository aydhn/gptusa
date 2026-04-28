"""JSONL file storage operations."""

import json
from pathlib import Path
from typing import Any, List, Optional

from usa_signal_bot.utils.file_utils import append_text_file, ensure_parent_dir, read_last_lines, atomic_write_text, write_text_file
from usa_signal_bot.utils.json_utils import to_json_line
from usa_signal_bot.core.exceptions import StorageReadError, DataValidationError

def append_jsonl(path: Path, record: dict[str, Any]) -> Path:
    """Appends a record to a JSONL file."""
    ensure_parent_dir(path)
    line = to_json_line(record)
    append_text_file(path, line)
    return path

def read_jsonl(path: Path, limit: Optional[int] = None) -> List[dict]:
    """Reads records from a JSONL file."""
    from usa_signal_bot.utils.file_utils import file_exists
    if not file_exists(path):
        return []

    records = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError as e:
                    raise DataValidationError(f"Corrupt JSONL line {line_no} in {path}: {e}")

                if limit and len(records) >= limit:
                    break
    except Exception as e:
        if isinstance(e, DataValidationError):
            raise
        raise StorageReadError(f"Failed to read JSONL from {path}: {e}")

    return records

def tail_jsonl(path: Path, n: int = 20) -> List[dict]:
    """Reads the last n records from a JSONL file."""
    lines = read_last_lines(path, n)
    records = []
    for line_no, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise DataValidationError(f"Corrupt JSONL line in tail of {path}: {e}")
    return records

def count_jsonl(path: Path) -> int:
    """Counts the number of non-empty records in a JSONL file."""
    from usa_signal_bot.utils.file_utils import file_exists
    if not file_exists(path):
        return 0

    count = 0
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                count += 1
    return count

def write_jsonl(path: Path, records: List[dict[str, Any]], atomic: bool = True) -> Path:
    """Writes a list of records to a JSONL file, overwriting if it exists."""
    ensure_parent_dir(path)
    lines = [to_json_line(record) for record in records]
    content = "".join(lines)

    if atomic:
        atomic_write_text(path, content)
    else:
        write_text_file(path, content)
    return path

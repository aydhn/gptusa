"""JSON file storage operations."""

import json
from pathlib import Path
from typing import Any

from usa_signal_bot.utils.file_utils import atomic_write_text, write_text_file, ensure_parent_dir
from usa_signal_bot.utils.json_utils import SafeJSONEncoder
from usa_signal_bot.core.serialization import serialize_value

def write_json(path: Path, data: Any, atomic: bool = True) -> Path:
    """Writes data to a JSON file."""
    ensure_parent_dir(path)
    json_str = json.dumps(data, cls=SafeJSONEncoder, indent=2, sort_keys=True)
    if atomic:
        atomic_write_text(path, json_str)
    else:
        write_text_file(path, json_str)
    return path

def read_json(path: Path) -> Any:
    """Reads data from a JSON file."""
    from usa_signal_bot.utils.file_utils import read_text_file
    from usa_signal_bot.core.exceptions import StorageReadError
    try:
        content = read_text_file(path)
        return json.loads(content)
    except Exception as e:
        raise StorageReadError(f"Failed to read JSON from {path}: {e}")

def json_exists(path: Path) -> bool:
    """Checks if a JSON file exists."""
    from usa_signal_bot.utils.file_utils import file_exists
    return file_exists(path)

def write_model_json(path: Path, model: Any, atomic: bool = True) -> Path:
    """Serializes a domain model and writes it to a JSON file."""
    serialized_data = serialize_value(model)
    return write_json(path, serialized_data, atomic)

def read_json_dict(path: Path) -> dict:
    """Reads a JSON file and ensures it returns a dictionary."""
    data = read_json(path)
    if not isinstance(data, dict):
        from usa_signal_bot.core.exceptions import StorageReadError
        raise StorageReadError(f"Expected JSON dictionary in {path}, got {type(data)}")
    return data

"""JSON formatting utilities."""

import json
from typing import Any
from pathlib import Path

class SafeJSONEncoder(json.JSONEncoder):
    """Custom encoder to handle Path objects and other non-serializable types."""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Path):
            return str(obj)
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)

def safe_json_dumps(data: Any) -> str:
    """Safely dumps data to JSON string."""
    return json.dumps(data, cls=SafeJSONEncoder)

def to_json_line(data: dict) -> str:
    """Converts a dictionary to a JSON line."""
    return safe_json_dumps(data) + "\n"

def from_json_line(line: str) -> dict:
    """Parses a JSON line into a dictionary."""
    if not line.strip():
        return {}
    return json.loads(line)

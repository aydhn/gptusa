"""Dictionary manipulation utilities."""

from typing import Dict, Any

def deep_merge_dicts(base: dict, override: dict) -> dict:
    """Recursively merges two dictionaries."""
    merged = base.copy()
    for key, value in override.items():
        if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
            merged[key] = deep_merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged

def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flattens a nested dictionary."""
    items: list = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def redact_sensitive_keys(d: dict) -> dict:
    """Redacts values for keys that look like secrets."""
    sensitive_keywords = ["token", "secret", "password", "api_key", "key"]

    def _redact(obj: Any) -> Any:
        if isinstance(obj, dict):
            redacted_obj = {}
            for k, v in obj.items():
                if any(keyword in str(k).lower() for keyword in sensitive_keywords):
                    redacted_obj[k] = "***REDACTED***"
                else:
                    redacted_obj[k] = _redact(v)
            return redacted_obj
        elif isinstance(obj, list):
            return [_redact(item) for item in obj]
        return obj

    return _redact(d)

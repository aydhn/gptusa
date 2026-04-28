"""Simple validation utilities."""

from typing import Any
from usa_signal_bot.core.exceptions import ConfigError

def ensure_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ConfigError(f"Field '{field_name}' must be a boolean.")
    return value

def ensure_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ConfigError(f"Field '{field_name}' must be an integer.")
    if value <= 0:
        raise ConfigError(f"Field '{field_name}' must be a positive integer.")
    return value

def ensure_non_negative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ConfigError(f"Field '{field_name}' must be an integer.")
    if value < 0:
        raise ConfigError(f"Field '{field_name}' must be a non-negative integer.")
    return value

def ensure_ratio(value: Any, field_name: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ConfigError(f"Field '{field_name}' must be a float.")
    float_val = float(value)
    if not (0.0 <= float_val <= 1.0):
        raise ConfigError(f"Field '{field_name}' must be between 0.0 and 1.0 inclusive.")
    return float_val

def ensure_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ConfigError(f"Field '{field_name}' must be a string.")
    if not value.strip():
        raise ConfigError(f"Field '{field_name}' cannot be empty.")
    return value

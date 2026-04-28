"""Environment variable management."""

import os
from typing import Optional
from usa_signal_bot.core.exceptions import EnvironmentConfigError

def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)

def require_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise EnvironmentConfigError(f"Required environment variable '{name}' is not set.")
    return value

def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ('true', '1', 'yes', 'y', 't')

def get_int_env(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        raise EnvironmentConfigError(f"Environment variable '{name}' must be an integer.")

def get_float_env(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        raise EnvironmentConfigError(f"Environment variable '{name}' must be a float.")

def mask_secret(value: Optional[str]) -> str:
    if value is None:
        return "<missing>"

    val_len = len(value)
    if val_len <= 6:
        return "***"

    return f"{value[:3]}***{value[-3:]}"

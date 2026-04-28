"""Storage format definitions and helpers."""

from enum import Enum
from usa_signal_bot.core.exceptions import UnsupportedOperationError

class StorageFormat(Enum):
    """Supported storage formats."""
    JSON = "json"
    JSONL = "jsonl"
    CSV = "csv"
    PARQUET_RESERVED = "parquet"

_EXTENSION_MAP = {
    StorageFormat.JSON: ".json",
    StorageFormat.JSONL: ".jsonl",
    StorageFormat.CSV: ".csv",
    StorageFormat.PARQUET_RESERVED: ".parquet",
}

_REVERSE_MAP = {v: k for k, v in _EXTENSION_MAP.items()}

def extension_for_format(fmt: StorageFormat) -> str:
    """Returns the file extension for a given StorageFormat."""
    if fmt not in _EXTENSION_MAP:
        raise ValueError(f"Unknown format: {fmt}")
    return _EXTENSION_MAP[fmt]

def format_from_extension(extension: str) -> StorageFormat:
    """Returns the StorageFormat for a given file extension."""
    if not extension.startswith('.'):
        extension = f".{extension}"
    ext = extension.lower()
    if ext not in _REVERSE_MAP:
        raise ValueError(f"Unknown extension: {extension}")
    return _REVERSE_MAP[ext]

def ensure_supported_format(fmt: StorageFormat) -> None:
    """Raises an error if the format is not supported for writing/reading."""
    if fmt == StorageFormat.PARQUET_RESERVED:
        raise UnsupportedOperationError("Parquet format is currently reserved and unsupported.")

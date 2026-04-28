"""Storage path registry and resolution."""

from pathlib import Path
from enum import Enum
from usa_signal_bot.utils.file_utils import assert_relative_filename, normalize_safe_filename, safe_mkdir

class StorageArea(Enum):
    """Standardized storage areas."""
    RAW_DATA = "raw"
    PROCESSED_DATA = "processed"
    CACHE = "cache"
    UNIVERSE = "universe"
    PAPER = "paper"
    BACKTESTS = "backtests"
    REPORTS = "reports"
    LOGS = "logs"
    FEATURES = "features"
    MODELS = "models"
    MANIFESTS = "manifests"

def get_storage_area_path(data_root: Path, area: str) -> Path:
    """Returns the absolute path for a specific storage area under the root."""
    # Validate area
    try:
        if isinstance(area, StorageArea):
            area_val = area.value
        else:
            area_val = StorageArea(area).value
    except ValueError:
        area_val = normalize_safe_filename(area) # fallback for custom areas

    path = data_root / area_val
    return path.resolve()

def ensure_storage_areas(data_root: Path) -> dict[str, Path]:
    """Ensures all standard storage areas exist and returns their paths."""
    areas = {}
    for area in StorageArea:
        path = get_storage_area_path(data_root, area)
        safe_mkdir(path)
        areas[area.value] = path
    return areas

def build_storage_path(data_root: Path, area: str, filename: str) -> Path:
    """Builds a full path for a file in a storage area, preventing traversal."""
    assert_relative_filename(filename)
    area_path = get_storage_area_path(data_root, area)

    full_path = (area_path / filename).resolve()

    # Final sanity check to ensure it's still under the data root
    if not str(full_path).startswith(str(data_root.resolve())):
        from usa_signal_bot.core.exceptions import StoragePathError
        raise StoragePathError(f"Resolved path escapes data root: {full_path}")

    return full_path

def safe_storage_filename(name: str) -> str:
    """Returns a sanitized filename safe for storage."""
    return normalize_safe_filename(name)

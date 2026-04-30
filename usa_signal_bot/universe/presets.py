from pathlib import Path
from typing import List

from usa_signal_bot.universe.models import UniverseLoadResult
from usa_signal_bot.universe.loader import load_universe_csv
from usa_signal_bot.core.exceptions import UniverseSourceError

def preset_dir(data_root: Path) -> Path:
    d = data_root / "universe" / "presets"
    d.mkdir(parents=True, exist_ok=True)
    return d

def list_preset_files(data_root: Path) -> List[Path]:
    p_dir = preset_dir(data_root)
    return sorted([p for p in p_dir.glob("*.csv") if p.is_file()])

def load_preset_universe(data_root: Path, preset_name: str) -> UniverseLoadResult:
    p_dir = preset_dir(data_root)

    # Assume the name might not have the extension
    if not preset_name.endswith(".csv"):
        preset_name += ".csv"

    p_path = p_dir / preset_name

    # Simple path traversal protection
    if not str(p_path.resolve()).startswith(str(p_dir.resolve())):
        raise UniverseSourceError(f"Invalid preset path: {preset_name}")

    if not p_path.exists():
        raise UniverseSourceError(f"Preset not found: {preset_name}")

    return load_universe_csv(p_path, preset_name_from_path(p_path))

def load_all_presets(data_root: Path) -> List[UniverseLoadResult]:
    results = []
    for p in list_preset_files(data_root):
        try:
            results.append(load_universe_csv(p, preset_name_from_path(p)))
        except Exception:
            pass # Skip invalid/corrupt preset files in bulk load
    return results

def preset_name_from_path(path: Path) -> str:
    return path.stem

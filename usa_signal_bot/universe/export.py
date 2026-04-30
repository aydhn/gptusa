import json
from pathlib import Path
from typing import List, Optional

from usa_signal_bot.universe.models import UniverseDefinition
from usa_signal_bot.universe.loader import save_universe_csv
from usa_signal_bot.core.exceptions import UniverseExportError

def export_universe_csv(universe: UniverseDefinition, path: Path) -> Path:
    _ensure_safe_export_path(path)
    return save_universe_csv(path, universe)

def export_universe_json(universe: UniverseDefinition, path: Path) -> Path:
    _ensure_safe_export_path(path)
    import json

    path.parent.mkdir(parents=True, exist_ok=True)

    import tempfile
    import os
    fd, temp_path_str = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        data = {
            "name": universe.name,
            "created_from": universe.created_from,
            "description": universe.description,
            "symbols": [
                {
                    "symbol": s.symbol,
                    "name": s.name,
                    "asset_type": s.asset_type.value if hasattr(s.asset_type, 'value') else str(s.asset_type),
                    "exchange": s.exchange,
                    "currency": s.currency,
                    "active": s.active,
                    "sector": s.sector,
                    "industry": s.industry
                } for s in universe.symbols
            ]
        }

        with open(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        os.replace(temp_path, path)
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise UniverseExportError(f"Failed to export JSON: {e}")

    return path

def export_symbols_txt(universe: UniverseDefinition, path: Path, active_only: bool = True) -> Path:
    _ensure_safe_export_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    symbols = _get_symbols_for_export(universe, active_only)

    import tempfile
    import os
    fd, temp_path_str = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        with open(fd, "w", encoding="utf-8") as f:
            for sym in symbols:
                f.write(f"{sym}\n")

        os.replace(temp_path, path)
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise UniverseExportError(f"Failed to export TXT: {e}")

    return path

def export_symbols_json(universe: UniverseDefinition, path: Path, active_only: bool = True) -> Path:
    _ensure_safe_export_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    symbols = _get_symbols_for_export(universe, active_only)

    import tempfile
    import os
    fd, temp_path_str = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    temp_path = Path(temp_path_str)

    try:
        with open(fd, "w", encoding="utf-8") as f:
            json.dump(symbols, f, indent=2)

        os.replace(temp_path, path)
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise UniverseExportError(f"Failed to export Symbols JSON: {e}")

    return path

def build_export_path(data_root: Path, name: str, extension: str) -> Path:
    exports_dir = data_root / "universe" / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    # Sanitization
    clean_name = "".join(c if c.isalnum() or c in ('-', '_') else "_" for c in name)
    clean_ext = extension.lstrip('.')

    out_path = exports_dir / f"{clean_name}.{clean_ext}"
    _ensure_safe_export_path(out_path, exports_dir)

    return out_path

def _ensure_safe_export_path(path: Path, base_dir: Optional[Path] = None) -> None:
    path_res = path.resolve()

    if base_dir:
        base_res = base_dir.resolve()
        if not str(path_res).startswith(str(base_res)):
             raise UniverseExportError(f"Path traversal detected for export: {path}")

def _get_symbols_for_export(universe: UniverseDefinition, active_only: bool) -> List[str]:
    if active_only:
        return universe.get_active_symbols()
    return [s.symbol for s in universe.symbols]

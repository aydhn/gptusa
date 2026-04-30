import csv
import shutil
from pathlib import Path
from typing import List, Optional

from usa_signal_bot.universe.models import UniverseLoadResult, UniverseValidationReport
from usa_signal_bot.universe.schema import get_all_columns, normalize_universe_row
from usa_signal_bot.universe.loader import load_universe_csv
from usa_signal_bot.universe.validator import validate_universe_csv_file
from usa_signal_bot.core.exceptions import UniverseImportError

def import_universe_csv(
    source_path: Path,
    destination_dir: Path,
    source_name: Optional[str] = None,
    overwrite: bool = False
) -> Path:
    # Security check: no URL
    if str(source_path).startswith("http://") or str(source_path).startswith("https://") or str(source_path).startswith("http:/") or str(source_path).startswith("https:/"):
        raise UniverseImportError("URL is not permitted")

    # Security check: path traversal check for source path if it tries to go up.
    if ".." in str(source_path) or (source_name and ".." in source_name):
        raise UniverseImportError("Path traversal detected")

    if not source_path.exists() or not source_path.is_file():
        raise UniverseImportError(f"Source file not found: {source_path}")

    # Resolve destination dir and ensure output path is within it
    destination_dir = destination_dir.resolve()
    destination_dir.mkdir(parents=True, exist_ok=True)

    out_path = build_import_destination_path(destination_dir, source_path, source_name)

    if out_path.exists() and not overwrite:
        raise UniverseImportError(f"Destination file already exists and overwrite is false: {out_path}")

    # Read and normalize
    return normalize_import_file(source_path, out_path)

def validate_import_file(path: Path) -> UniverseValidationReport:
    if not path.exists() or not path.is_file():
         raise UniverseImportError(f"File not found for validation: {path}")
    return validate_universe_csv_file(path)

def normalize_import_file(path: Path, output_path: Path) -> Path:
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                raise UniverseImportError(f"Empty or invalid CSV file: {path}")

            from usa_signal_bot.universe.schema import REQUIRED_UNIVERSE_COLUMNS
            missing = [c for c in REQUIRED_UNIVERSE_COLUMNS if c not in reader.fieldnames]
            if missing:
                raise UniverseImportError(f"Missing required columns: {missing}")

            rows = list(reader)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Temp file for atomic write
        import tempfile
        import os

        fd, temp_path_str = tempfile.mkstemp(dir=str(output_path.parent), suffix=".tmp")
        temp_path = Path(temp_path_str)

        try:
            with open(fd, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=get_all_columns())
                writer.writeheader()

                for row in rows:
                    norm_row = normalize_universe_row(row)

                    # Ensure all optional columns are present
                    out_row = {}
                    for col in get_all_columns():
                        out_row[col] = norm_row.get(col, "")

                    writer.writerow(out_row)

            # Atomic rename
            os.replace(temp_path, output_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise

        return output_path
    except Exception as e:
        if isinstance(e, UniverseImportError):
            raise
        raise UniverseImportError(f"Failed to normalize import file {path}: {e}")

def load_imported_universe(path: Path, universe_name: Optional[str] = None) -> UniverseLoadResult:
    return load_universe_csv(path, universe_name)

def list_import_files(imports_dir: Path) -> List[Path]:
    if not imports_dir.exists() or not imports_dir.is_dir():
        return []

    return sorted([p for p in imports_dir.glob("*.csv") if p.is_file()])

def build_import_destination_path(destination_dir: Path, source_path: Path, source_name: Optional[str] = None) -> Path:
    # Ensure no path traversal
    dest_dir_resolved = destination_dir.resolve()

    file_name = f"{source_name}.csv" if source_name else source_path.name

    # Simple sanitization of filename to prevent path traversal
    file_name = file_name.replace("/", "_").replace("\\", "_").replace("..", "_")

    out_path = (dest_dir_resolved / file_name).resolve()

    # Strict check
    if not str(out_path).startswith(str(dest_dir_resolved)):
        raise UniverseImportError("Path traversal detected")

    return out_path

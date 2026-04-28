"""LocalFileStore orchestrates access to the file-based database."""

from pathlib import Path
from typing import Any, List, Optional

from usa_signal_bot.storage.paths import ensure_storage_areas, get_storage_area_path, build_storage_path
from usa_signal_bot.storage.formats import StorageFormat, extension_for_format, ensure_supported_format
from usa_signal_bot.storage.json_store import write_json, read_json, json_exists
from usa_signal_bot.storage.jsonl_store import append_jsonl, read_jsonl, tail_jsonl
from usa_signal_bot.storage.csv_store import write_csv, read_csv, csv_exists
from usa_signal_bot.core.exceptions import StorageError, StoragePathError
from usa_signal_bot.utils.file_utils import file_exists

class LocalFileStore:
    """Gateway for all local file storage operations."""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()

    def ensure_ready(self) -> None:
        """Ensures all storage areas are created."""
        ensure_storage_areas(self.root_dir)

    def area_path(self, area: str) -> Path:
        """Returns the path for a given storage area."""
        return get_storage_area_path(self.root_dir, area)

    def path(self, area: str, filename: str) -> Path:
        """Resolves a full path for a given area and filename safely."""
        return build_storage_path(self.root_dir, area, filename)

    def write_json(self, area: str, filename: str, data: Any) -> Path:
        """Writes JSON to the specified area and filename."""
        ensure_supported_format(StorageFormat.JSON)
        p = self.path(area, filename)
        return write_json(p, data, atomic=True)

    def read_json(self, area: str, filename: str) -> Any:
        """Reads JSON from the specified area and filename."""
        p = self.path(area, filename)
        return read_json(p)

    def append_jsonl(self, area: str, filename: str, record: dict) -> Path:
        """Appends a record to a JSONL file."""
        ensure_supported_format(StorageFormat.JSONL)
        p = self.path(area, filename)
        return append_jsonl(p, record)

    def read_jsonl(self, area: str, filename: str, limit: Optional[int] = None) -> List[dict]:
        """Reads a JSONL file."""
        p = self.path(area, filename)
        return read_jsonl(p, limit)

    def tail_jsonl(self, area: str, filename: str, n: int = 20) -> List[dict]:
        """Reads the tail of a JSONL file."""
        p = self.path(area, filename)
        return tail_jsonl(p, n)

    def write_csv(self, area: str, filename: str, rows: List[dict], fieldnames: Optional[List[str]] = None) -> Path:
        """Writes a CSV file."""
        ensure_supported_format(StorageFormat.CSV)
        p = self.path(area, filename)
        return write_csv(p, rows, fieldnames, atomic=True)

    def read_csv(self, area: str, filename: str) -> List[dict[str, str]]:
        """Reads a CSV file."""
        p = self.path(area, filename)
        return read_csv(p)

    def exists(self, area: str, filename: str) -> bool:
        """Checks if a file exists in the specified area."""
        p = self.path(area, filename)
        return file_exists(p)

    def delete(self, area: str, filename: str) -> None:
        """Deletes a file, ensuring it's under the root dir."""
        p = self.path(area, filename)
        if not str(p).startswith(str(self.root_dir)):
            raise StoragePathError(f"Cannot delete file outside root dir: {p}")
        if p.exists() and p.is_file():
            p.unlink()

    def list_files(self, area: str, pattern: str = "*") -> List[Path]:
        """Lists files in an area matching a pattern."""
        ap = self.area_path(area)
        if not ap.exists() or not ap.is_dir():
            return []

        # We only want to yield files directly in the area, not recursively to avoid infinite traversal loops.
        files = []
        for p in ap.glob(pattern):
            if p.is_file() and str(p.resolve()).startswith(str(self.root_dir)):
                files.append(p)
        return sorted(files)

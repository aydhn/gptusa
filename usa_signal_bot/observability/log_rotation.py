import os
import shutil
import hashlib
from dataclasses import dataclass
from typing import List, Tuple, Optional
from pathlib import Path
import datetime

from usa_signal_bot.core.enums import LogRotationStatus
from usa_signal_bot.observability.observability_models import LogRotationResult, LogFileSummary, create_log_rotation_result_id

@dataclass
class LogRotationConfig:
    enabled: bool = True
    max_file_size_bytes: int = 5242880
    max_rotated_files: int = 5
    compress_rotated: bool = False
    dry_run: bool = False

def default_log_rotation_config() -> LogRotationConfig:
    return LogRotationConfig()

def validate_log_rotation_config(config: LogRotationConfig) -> None:
    if config.max_file_size_bytes <= 0:
        raise ValueError("max_file_size_bytes must be positive")
    if config.max_rotated_files <= 0:
        raise ValueError("max_rotated_files must be positive")

def count_log_lines(path: Path, max_lines: Optional[int] = None) -> Optional[int]:
    if not path.exists():
        return None
    c = 0
    with open(path, "rb") as f:
        for _ in f:
            c += 1
            if max_lines and c >= max_lines:
                break
    return c

def count_log_severity(path: Path) -> Tuple[Optional[int], Optional[int]]:
    if not path.exists():
        return None, None
    w, e = 0, 0
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if '"severity": "WARNING"' in line or "[WARNING]" in line:
                w += 1
            if '"severity": "ERROR"' in line or '"severity": "CRITICAL"' in line or "[ERROR]" in line or "[CRITICAL]" in line:
                e += 1
    return w, e

def calculate_log_checksum(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def log_rotation_config_to_dict(config: LogRotationConfig) -> dict:
    from dataclasses import asdict
    return asdict(config)

class LogRotationManager:
    def __init__(self, config: LogRotationConfig):
        self.config = config

    def summarize_log_file(self, path: Path) -> LogFileSummary:
        if not path.exists():
            return LogFileSummary(str(path), False, 0, None, None, None, None, None, ["File not found"])

        size = path.stat().st_size
        lines = count_log_lines(path)
        w, e = count_log_severity(path)
        mtime = datetime.datetime.fromtimestamp(path.stat().st_mtime, datetime.timezone.utc).isoformat()

        return LogFileSummary(
            path=str(path),
            exists=True,
            size_bytes=size,
            line_count=lines,
            warning_count=w,
            error_count=e,
            last_modified_utc=mtime,
            checksum=None # omit expensive hash by default
        )

    def rotate_if_needed(self, path: Path) -> LogRotationResult:
        if not path.exists():
            return LogRotationResult(create_log_rotation_result_id(), datetime.datetime.now(datetime.timezone.utc).isoformat(), LogRotationStatus.SKIPPED, str(path), None, None, None, ["File does not exist"])

        size = path.stat().st_size
        if size < self.config.max_file_size_bytes:
            return LogRotationResult(create_log_rotation_result_id(), datetime.datetime.now(datetime.timezone.utc).isoformat(), LogRotationStatus.NOT_NEEDED, str(path), None, size, None)

        return self.rotate(path)

    def list_rotated_files(self, path: Path) -> List[Path]:
        res = []
        name = path.name
        d = path.parent
        for p in d.iterdir():
            if p.is_file() and p.name.startswith(name + "."):
                try:
                    ext = p.name.split(".")[-1]
                    if ext.isdigit():
                        res.append(p)
                except ValueError:
                    pass
        return sorted(res, key=lambda x: int(x.name.split(".")[-1]))

    def rotate(self, path: Path) -> LogRotationResult:
        if not path.exists():
            return LogRotationResult(create_log_rotation_result_id(), datetime.datetime.now(datetime.timezone.utc).isoformat(), LogRotationStatus.FAILED, str(path), None, None, None, ["File does not exist"])

        size = path.stat().st_size
        if self.config.dry_run:
            return LogRotationResult(create_log_rotation_result_id(), datetime.datetime.now(datetime.timezone.utc).isoformat(), LogRotationStatus.NOT_NEEDED, str(path), None, size, None, ["Dry run enabled"])

        existing = self.list_rotated_files(path)

        # shift files
        for p in reversed(existing):
            n = int(p.name.split(".")[-1])
            new_p = p.parent / f"{path.name}.{n+1}"
            shutil.move(str(p), str(new_p))

        new_path = path.parent / f"{path.name}.1"
        shutil.move(str(path), str(new_path))

        # create new empty
        path.touch()

        self.cleanup_old_rotations(path)

        return LogRotationResult(
            create_log_rotation_result_id(),
            datetime.datetime.now(datetime.timezone.utc).isoformat(),
            LogRotationStatus.ROTATED,
            str(path),
            str(new_path),
            size,
            new_path.stat().st_size if new_path.exists() else None
        )

    def cleanup_old_rotations(self, path: Path) -> List[Path]:
        deleted = []
        if self.config.dry_run:
            return deleted

        existing = self.list_rotated_files(path)
        while len(existing) > self.config.max_rotated_files:
            p = existing.pop()
            p.unlink(missing_ok=True)
            deleted.append(p)
        return deleted

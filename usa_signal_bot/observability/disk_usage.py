import shutil
import uuid
import datetime
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from usa_signal_bot.core.enums import DiskUsageStatus

@dataclass
class DiskUsageSummary:
    summary_id: str
    created_at_utc: str
    path: str
    total_bytes: Optional[int]
    used_bytes: Optional[int]
    free_bytes: Optional[int]
    data_root_size_bytes: int
    status: DiskUsageStatus
    warning_threshold_pct: float
    critical_threshold_pct: float
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def calculate_directory_size(path: Path, max_files: Optional[int] = None) -> int:
    if not path.exists(): return 0
    total = 0
    count = 0
    try:
        for f in path.rglob('*'):
            if f.is_file():
                try:
                    total += f.stat().st_size
                except Exception:
                    pass
                count += 1
                if max_files and count >= max_files:
                    break
    except Exception:
        pass
    return total

def classify_disk_usage_status(used_pct: Optional[float], warning_threshold_pct: float, critical_threshold_pct: float) -> DiskUsageStatus:
    if used_pct is None:
        return DiskUsageStatus.UNKNOWN
    if used_pct >= critical_threshold_pct:
        return DiskUsageStatus.CRITICAL
    if used_pct >= warning_threshold_pct:
        return DiskUsageStatus.WARNING
    return DiskUsageStatus.OK

def collect_disk_usage_summary(data_root: Path, warning_threshold_pct: float = 80.0, critical_threshold_pct: float = 90.0) -> DiskUsageSummary:
    errs = []
    tot, used, free = None, None, None
    try:
        tot, used, free = shutil.disk_usage(data_root)
    except Exception as e:
        errs.append(f"Failed to get disk usage: {e}")

    ds = calculate_directory_size(data_root)

    pct = (used / tot * 100) if (used is not None and tot) else None
    st = classify_disk_usage_status(pct, warning_threshold_pct, critical_threshold_pct)

    return DiskUsageSummary(
        summary_id=f"disk_{uuid.uuid4().hex[:8]}",
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        path=str(data_root),
        total_bytes=tot,
        used_bytes=used,
        free_bytes=free,
        data_root_size_bytes=ds,
        status=st,
        warning_threshold_pct=warning_threshold_pct,
        critical_threshold_pct=critical_threshold_pct,
        warnings=[],
        errors=errs
    )

def disk_usage_summary_to_dict(summary: DiskUsageSummary) -> dict:
    from dataclasses import asdict
    return asdict(summary)

def disk_usage_summary_to_text(summary: DiskUsageSummary) -> str:
    lines = [
        f"--- Disk Usage Summary ---",
        f"Path: {summary.path}",
        f"Status: {summary.status.value}",
        f"Data Root Size: {summary.data_root_size_bytes / (1024*1024):.2f} MB"
    ]
    if summary.total_bytes and summary.used_bytes:
        pct = summary.used_bytes / summary.total_bytes * 100
        lines.append(f"Disk Usage: {pct:.1f}% ({summary.used_bytes / (1024*1024*1024):.2f} GB / {summary.total_bytes / (1024*1024*1024):.2f} GB)")
    return "\n".join(lines)

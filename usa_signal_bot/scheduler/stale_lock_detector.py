from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import uuid

from usa_signal_bot.scheduler.scheduler_models import RunLock, run_lock_to_dict
from usa_signal_bot.scheduler.lock_manager import FileRunLockManager

@dataclass
class StaleLockReport:
    report_id: str
    created_at_utc: str
    stale_count: int
    active_count: int
    stale_locks: List[RunLock] = field(default_factory=list)
    active_locks: List[RunLock] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def detect_stale_locks(lock_manager: FileRunLockManager, now_utc: Optional[str] = None) -> StaleLockReport:
    if not now_utc:
        now_utc = datetime.now(timezone.utc).isoformat()

    locks = lock_manager.list_locks()
    stale_locks = []
    active_locks = []

    for lock in locks:
        if lock_manager.is_lock_stale(lock, now_utc):
            stale_locks.append(lock)
        else:
            active_locks.append(lock)

    return StaleLockReport(
        report_id=f"stale_report_{uuid.uuid4().hex[:8]}",
        created_at_utc=now_utc,
        stale_count=len(stale_locks),
        active_count=len(active_locks),
        stale_locks=stale_locks,
        active_locks=active_locks
    )

def cleanup_stale_locks(lock_manager: FileRunLockManager, dry_run: bool = True, force: bool = False) -> Dict[str, Any]:
    report = detect_stale_locks(lock_manager)
    removed = []
    failed = []

    for lock in report.stale_locks:
        if dry_run:
            removed.append(lock.lock_id)
            continue

        success = lock_manager.remove_lock(lock, force=force)
        if success:
            removed.append(lock.lock_id)
        else:
            failed.append(lock.lock_id)

    return {
        "dry_run": dry_run,
        "stale_found": report.stale_count,
        "removed": removed,
        "failed": failed
    }

def stale_lock_report_to_dict(report: StaleLockReport) -> dict:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "stale_count": report.stale_count,
        "active_count": report.active_count,
        "stale_locks": [run_lock_to_dict(l) for l in report.stale_locks],
        "active_locks": [run_lock_to_dict(l) for l in report.active_locks],
        "warnings": report.warnings,
        "errors": report.errors
    }

def stale_lock_report_to_text(report: StaleLockReport) -> str:
    lines = [
        f"Stale Lock Report ({report.report_id}) at {report.created_at_utc}",
        f"Active Locks: {report.active_count}",
        f"Stale Locks : {report.stale_count}"
    ]
    if report.stale_count > 0:
        lines.append("Stale Locks details:")
        for l in report.stale_locks:
            lines.append(f"  - Scope: {l.scope.value}, Owner: {l.owner.owner}, ID: {l.lock_id}")
    return "\n".join(lines)

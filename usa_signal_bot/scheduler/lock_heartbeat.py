from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any

from usa_signal_bot.core.enums import RunLockScope, RunLockStatus
from usa_signal_bot.scheduler.scheduler_models import RunLock, RunIdentity
from usa_signal_bot.scheduler.lock_manager import FileRunLockManager

class LockHeartbeatManager:
    def __init__(self, lock_manager: FileRunLockManager):
        self.lock_manager = lock_manager

    def heartbeat(self, lock: RunLock, owner: RunIdentity) -> RunLock:
        return self.lock_manager.refresh_lock(lock, owner)

    def heartbeat_scope(self, scope: RunLockScope, owner: RunIdentity) -> Optional[RunLock]:
        path = self.lock_manager.lock_path_for_scope(scope)
        lock = self.lock_manager.read_lock(path)
        if lock and lock.owner.run_id == owner.run_id:
            return self.heartbeat(lock, owner)
        return None

    def heartbeat_all_owned(self, owner: RunIdentity) -> List[RunLock]:
        refreshed = []
        locks = self.lock_manager.list_locks()
        for lock in locks:
            if lock.owner.run_id == owner.run_id:
                res = self.heartbeat(lock, owner)
                if res.status == RunLockStatus.HELD:
                    refreshed.append(res)
        return refreshed

    def heartbeat_is_recent(self, lock: RunLock, max_age_seconds: Optional[int] = None) -> bool:
        if not lock.heartbeat_at_utc and not lock.acquired_at_utc:
            return False

        last_activity = lock.heartbeat_at_utc or lock.acquired_at_utc
        max_age = max_age_seconds or lock.stale_after_seconds

        try:
            last_dt = datetime.fromisoformat(last_activity)
            now_dt = datetime.now(timezone.utc)
            delta = (now_dt - last_dt).total_seconds()
            return delta <= max_age
        except Exception:
            return False

def calculate_lock_expiry(acquired_at_utc: str, stale_after_seconds: int) -> str:
    try:
        dt = datetime.fromisoformat(acquired_at_utc)
        expiry = dt + timedelta(seconds=stale_after_seconds)
        return expiry.isoformat()
    except Exception:
        return acquired_at_utc

def heartbeat_summary(locks: List[RunLock]) -> Dict[str, Any]:
    return {
        "count": len(locks),
        "locks": [{"scope": l.scope.value, "lock_id": l.lock_id, "heartbeat_at": l.heartbeat_at_utc} for l in locks]
    }

def heartbeat_summary_to_text(summary: Dict[str, Any]) -> str:
    lines = [f"Refreshed {summary['count']} locks:"]
    for l in summary["locks"]:
        lines.append(f"  - {l['scope']} ({l['lock_id']}): {l['heartbeat_at']}")
    return "\n".join(lines)

import datetime
import json
import os
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from usa_signal_bot.core.exceptions import RuntimeLockError

@dataclass
class RuntimeLockInfo:
    lock_id: str
    run_id: str
    lock_path: str
    acquired_at_utc: str
    expires_at_utc: Optional[str] = None
    owner_pid: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

def runtime_lock_info_to_dict(info: RuntimeLockInfo) -> dict:
    return {
        "lock_id": info.lock_id,
        "run_id": info.run_id,
        "lock_path": info.lock_path,
        "acquired_at_utc": info.acquired_at_utc,
        "expires_at_utc": info.expires_at_utc,
        "owner_pid": info.owner_pid,
        "metadata": info.metadata,
    }

def runtime_lock_info_from_dict(data: dict) -> RuntimeLockInfo:
    return RuntimeLockInfo(
        lock_id=data["lock_id"],
        run_id=data["run_id"],
        lock_path=data["lock_path"],
        acquired_at_utc=data["acquired_at_utc"],
        expires_at_utc=data.get("expires_at_utc"),
        owner_pid=data.get("owner_pid"),
        metadata=data.get("metadata", {})
    )

class RuntimeLockManager:
    def __init__(self, lock_dir: Path, stale_after_seconds: int = 7200):
        self.lock_dir = lock_dir
        self.stale_after_seconds = stale_after_seconds
        self._lock_file = self.lock_dir / "runtime.lock"

    def lock_path(self) -> Path:
        return self._lock_file

    def is_locked(self) -> bool:
        if not self._lock_file.exists():
            return False
        info = self.read_lock()
        if not info:
            return False

        # Check stale
        acquired = datetime.datetime.fromisoformat(info.acquired_at_utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        if (now - acquired).total_seconds() > self.stale_after_seconds:
            return False

        return True

    def read_lock(self) -> Optional[RuntimeLockInfo]:
        if not self._lock_file.exists():
            return None
        try:
            with open(self._lock_file, "r") as f:
                data = json.load(f)
            return runtime_lock_info_from_dict(data)
        except Exception:
            return None

    def acquire(self, run_id: str, force: bool = False) -> RuntimeLockInfo:
        self.lock_dir.mkdir(parents=True, exist_ok=True)

        if self.is_locked() and not force:
            existing = self.read_lock()
            raise RuntimeLockError(f"Runtime is already locked by run {existing.run_id if existing else 'unknown'}")

        now = datetime.datetime.now(datetime.timezone.utc)
        expires = now + datetime.timedelta(seconds=self.stale_after_seconds)

        info = RuntimeLockInfo(
            lock_id=str(uuid.uuid4()),
            run_id=run_id,
            lock_path=str(self._lock_file),
            acquired_at_utc=now.isoformat(),
            expires_at_utc=expires.isoformat(),
            owner_pid=os.getpid(),
        )

        # Atomic-like write
        tmp_file = self._lock_file.with_suffix(".tmp")
        with open(tmp_file, "w") as f:
            json.dump(runtime_lock_info_to_dict(info), f)
        tmp_file.replace(self._lock_file)

        return info

    def release(self, lock_info: RuntimeLockInfo) -> None:
        if not self._lock_file.exists():
            return

        current = self.read_lock()
        if current and current.lock_id == lock_info.lock_id:
            try:
                self._lock_file.unlink()
            except Exception:
                pass # Warning could be logged here

    def clear_stale_lock(self) -> bool:
        if not self._lock_file.exists():
            return False

        info = self.read_lock()
        if not info:
            self._lock_file.unlink()
            return True

        acquired = datetime.datetime.fromisoformat(info.acquired_at_utc)
        now = datetime.datetime.now(datetime.timezone.utc)
        if (now - acquired).total_seconds() > self.stale_after_seconds:
            self._lock_file.unlink()
            return True

        return False

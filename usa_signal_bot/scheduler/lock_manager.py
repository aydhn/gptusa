import json
import os
import tempfile
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from usa_signal_bot.core.enums import RunLockScope, RunLockStatus, LockAcquisitionMode
from usa_signal_bot.scheduler.scheduler_models import (
    RunLock, RunIdentity, LockAcquisitionResult, ConcurrencyPolicy,
    create_lock_id, create_lock_acquisition_result_id,
    run_lock_to_dict, validate_run_lock
)

class FileRunLockManager:
    def __init__(self, lock_dir: Path):
        self.lock_dir = lock_dir
        self.lock_dir.mkdir(parents=True, exist_ok=True)

    def lock_path_for_scope(self, scope: RunLockScope) -> Path:
        return self.lock_dir / f"{scope.value.lower()}.lock.json"

    def read_lock(self, path: Path) -> Optional[RunLock]:
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            owner_data = data.get("owner", {})
            if "run_type" in owner_data and isinstance(owner_data["run_type"], str):
                owner_data["run_type"] = RunLockScope(owner_data["run_type"])
            else:
                owner_data["run_type"] = RunLockScope.GLOBAL
            owner = RunIdentity(**owner_data)
            owner_data["run_type"] = RunLockScope(owner_data.get("run_type")) if "run_type" in owner_data else RunLockScope.GLOBAL

            return RunLock(
                lock_id=data.get("lock_id"),
                scope=RunLockScope(data.get("scope")),
                lock_path=data.get("lock_path"),
                status=RunLockStatus(data.get("status")),
                owner=owner,
                acquired_at_utc=data.get("acquired_at_utc"),
                heartbeat_at_utc=data.get("heartbeat_at_utc"),
                expires_at_utc=data.get("expires_at_utc"),
                stale_after_seconds=data.get("stale_after_seconds", 3600),
                message=data.get("message"),
                metadata=data.get("metadata", {})
            )
        except Exception:
            return None

    def write_lock(self, lock: RunLock) -> Path:
        validate_run_lock(lock)
        path = Path(lock.lock_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_path = tempfile.mkstemp(dir=path.parent, prefix="lock_tmp_", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(run_lock_to_dict(lock), f, indent=2)
            os.replace(temp_path, path)
            return path
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e

    def is_lock_stale(self, lock: RunLock, now_utc: Optional[str] = None) -> bool:
        if lock.status != RunLockStatus.HELD and lock.status != RunLockStatus.ACQUIRED:
            return False

        if not now_utc:
            now_utc = datetime.now(timezone.utc).isoformat()

        last_activity = lock.heartbeat_at_utc or lock.acquired_at_utc
        if not last_activity:
            return True

        try:
            # Need to normalize iso formats
            last_dt = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
            now_dt = datetime.fromisoformat(now_utc.replace('Z', '+00:00'))
            delta = (now_dt - last_dt).total_seconds()
            return delta > lock.stale_after_seconds
        except Exception:
            return True

    def lock_exists(self, scope: RunLockScope) -> bool:
        path = self.lock_path_for_scope(scope)
        return path.exists()

    def list_locks(self, scope: Optional[RunLockScope] = None) -> List[RunLock]:
        locks = []
        if scope:
            path = self.lock_path_for_scope(scope)
            lock = self.read_lock(path)
            if lock:
                locks.append(lock)
        else:
            for f in self.lock_dir.glob("*.lock.json"):
                lock = self.read_lock(f)
                if lock:
                    locks.append(lock)
        return locks

    def remove_lock(self, lock: RunLock, force: bool = False) -> bool:
        path = Path(lock.lock_path)
        if not path.exists():
            return True
        try:
            os.remove(path)
            return True
        except Exception:
            return False

    def acquire(self, scope: RunLockScope, owner: RunIdentity, policy: Optional[ConcurrencyPolicy] = None, mode: Optional[LockAcquisitionMode] = None) -> LockAcquisitionResult:
        if not mode:
            mode = policy.acquisition_mode if policy else LockAcquisitionMode.FAIL_FAST

        path = self.lock_path_for_scope(scope)
        now_utc = datetime.now(timezone.utc).isoformat()
        stale_after_seconds = policy.stale_after_seconds if policy else 3600

        result_id = create_lock_acquisition_result_id()
        existing_lock = self.read_lock(path)

        if existing_lock:
            stale = self.is_lock_stale(existing_lock, now_utc)
            if stale and mode != LockAcquisitionMode.STEAL_IF_STALE:
                if mode == LockAcquisitionMode.DRY_RUN:
                    return LockAcquisitionResult(result_id=result_id, created_at_utc=now_utc, status=RunLockStatus.BLOCKED, scope=scope, acquired=False, lock=None, existing_lock=existing_lock, mode=mode, warnings=["Lock is stale but not stealing (DRY_RUN)"])
                return LockAcquisitionResult(result_id=result_id, created_at_utc=now_utc, status=RunLockStatus.BLOCKED, scope=scope, acquired=False, lock=None, existing_lock=existing_lock, mode=mode, errors=["Lock is stale, but acquisition mode is not STEAL_IF_STALE"])
            elif not stale:
                if mode == LockAcquisitionMode.DRY_RUN:
                    return LockAcquisitionResult(result_id=result_id, created_at_utc=now_utc, status=RunLockStatus.BLOCKED, scope=scope, acquired=False, lock=None, existing_lock=existing_lock, mode=mode, warnings=["Lock is held and not stale (DRY_RUN)"])
                if mode == LockAcquisitionMode.FAIL_FAST or mode == LockAcquisitionMode.STEAL_IF_STALE:
                    return LockAcquisitionResult(result_id=result_id, created_at_utc=now_utc, status=RunLockStatus.BLOCKED, scope=scope, acquired=False, lock=None, existing_lock=existing_lock, mode=mode, errors=["Lock is currently held by another process"])
                if mode == LockAcquisitionMode.WAIT:
                    wait_timeout = policy.wait_timeout_seconds if policy else 10
                    start = time.time()
                    while time.time() - start < wait_timeout:
                        time.sleep(0.5)
                        existing_lock = self.read_lock(path)
                        if not existing_lock or self.is_lock_stale(existing_lock):
                            break
                    if existing_lock and not self.is_lock_stale(existing_lock):
                        return LockAcquisitionResult(result_id=result_id, created_at_utc=now_utc, status=RunLockStatus.BLOCKED, scope=scope, acquired=False, lock=None, existing_lock=existing_lock, mode=mode, errors=[f"Wait timeout ({wait_timeout}s) exceeded"])

        if mode == LockAcquisitionMode.DRY_RUN:
            dummy_lock = RunLock(lock_id=create_lock_id(scope), scope=scope, lock_path=str(path), status=RunLockStatus.ACQUIRED, owner=owner, acquired_at_utc=now_utc, heartbeat_at_utc=now_utc, expires_at_utc=None, stale_after_seconds=stale_after_seconds)
            return LockAcquisitionResult(result_id=result_id, created_at_utc=now_utc, status=RunLockStatus.ACQUIRED, scope=scope, acquired=False, lock=dummy_lock, existing_lock=existing_lock, mode=mode, warnings=["Dry run - lock not actually written"])

        new_lock = RunLock(lock_id=create_lock_id(scope), scope=scope, lock_path=str(path), status=RunLockStatus.HELD, owner=owner, acquired_at_utc=now_utc, heartbeat_at_utc=now_utc, expires_at_utc=None, stale_after_seconds=stale_after_seconds)
        self.write_lock(new_lock)

        return LockAcquisitionResult(result_id=result_id, created_at_utc=now_utc, status=RunLockStatus.ACQUIRED, scope=scope, acquired=True, lock=new_lock, existing_lock=existing_lock, mode=mode, warnings=["Stole stale lock"] if existing_lock else [])
    def release(self, lock: RunLock, owner: Optional[RunIdentity] = None) -> RunLock:
        path = Path(lock.lock_path)
        existing = self.read_lock(path)

        lock.status = RunLockStatus.RELEASED

        if not existing:
            lock.message = "Lock did not exist when releasing"
            return lock

        if owner and existing.owner.run_id != owner.run_id:
            lock.message = "Cannot release lock owned by another process"
            lock.status = RunLockStatus.FAILED
            return lock

        self.remove_lock(existing, force=True)
        return lock

    def refresh_lock(self, lock: RunLock, owner: Optional[RunIdentity] = None) -> RunLock:
        path = Path(lock.lock_path)
        existing = self.read_lock(path)
        if not existing:
            lock.status = RunLockStatus.MISSING
            return lock

        if owner and existing.owner.run_id != owner.run_id:
            lock.status = RunLockStatus.FAILED
            return lock

        existing.heartbeat_at_utc = datetime.now(timezone.utc).isoformat()
        self.write_lock(existing)
        return existing

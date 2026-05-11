import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta

from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.scheduler.run_identity import create_run_identity
from usa_signal_bot.core.enums import RunLockScope, LockAcquisitionMode, RunLockStatus

@pytest.fixture
def lock_dir():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

@pytest.fixture
def lock_manager(lock_dir):
    return FileRunLockManager(lock_dir)

def test_acquire_no_lock_success(lock_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    res = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)
    assert res.acquired is True
    assert res.status == RunLockStatus.ACQUIRED
    assert res.lock is not None
    assert lock_manager.lock_exists(RunLockScope.SCAN)

def test_acquire_existing_lock_fail_fast(lock_manager):
    identity1 = create_run_identity(RunLockScope.SCAN, owner="test1")
    identity2 = create_run_identity(RunLockScope.SCAN, owner="test2")

    lock_manager.acquire(RunLockScope.SCAN, identity1, mode=LockAcquisitionMode.FAIL_FAST)
    res = lock_manager.acquire(RunLockScope.SCAN, identity2, mode=LockAcquisitionMode.FAIL_FAST)

    assert res.acquired is False
    assert res.status == RunLockStatus.BLOCKED
    assert res.existing_lock is not None

def test_release_own_lock(lock_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    acq_res = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)
    assert lock_manager.lock_exists(RunLockScope.SCAN)

    lock_manager.release(acq_res.lock, identity)
    assert not lock_manager.lock_exists(RunLockScope.SCAN)

def test_stale_lock_detection(lock_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    acq_res = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)
    lock = acq_res.lock

    now_utc = datetime.now(timezone.utc)
    future_utc = (now_utc + timedelta(seconds=lock.stale_after_seconds + 10)).isoformat()

    assert lock_manager.is_lock_stale(lock, future_utc) is True

def test_steal_if_stale(lock_manager):
    identity1 = create_run_identity(RunLockScope.SCAN, owner="test1")
    identity2 = create_run_identity(RunLockScope.SCAN, owner="test2")

    # Manually create a stale lock
    acq_res = lock_manager.acquire(RunLockScope.SCAN, identity1, mode=LockAcquisitionMode.FAIL_FAST)
    lock = acq_res.lock
    lock.acquired_at_utc = (datetime.now(timezone.utc) - timedelta(seconds=lock.stale_after_seconds + 10)).isoformat()
    lock.heartbeat_at_utc = lock.acquired_at_utc
    lock_manager.write_lock(lock)

    res = lock_manager.acquire(RunLockScope.SCAN, identity2, mode=LockAcquisitionMode.STEAL_IF_STALE)
    assert res.acquired is True
    assert res.status == RunLockStatus.ACQUIRED
    assert "Stole stale lock" in res.warnings

def test_dry_run_acquire(lock_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    res = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.DRY_RUN)

    assert res.acquired is False
    assert res.status == RunLockStatus.ACQUIRED
    assert not lock_manager.lock_exists(RunLockScope.SCAN)

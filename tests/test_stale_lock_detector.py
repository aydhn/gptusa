import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta

from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.scheduler.stale_lock_detector import detect_stale_locks, cleanup_stale_locks, stale_lock_report_to_text
from usa_signal_bot.scheduler.run_identity import create_run_identity
from usa_signal_bot.core.enums import RunLockScope, LockAcquisitionMode

@pytest.fixture
def lock_manager():
    with tempfile.TemporaryDirectory() as td:
        yield FileRunLockManager(Path(td))

def test_active_and_stale_counts(lock_manager):
    identity1 = create_run_identity(RunLockScope.SCAN, owner="test1")
    identity2 = create_run_identity(RunLockScope.BACKTEST, owner="test2")

    lock_manager.acquire(RunLockScope.SCAN, identity1, mode=LockAcquisitionMode.FAIL_FAST)
    acq2 = lock_manager.acquire(RunLockScope.BACKTEST, identity2, mode=LockAcquisitionMode.FAIL_FAST)

    # Make acq2 stale
    lock2 = acq2.lock
    lock2.acquired_at_utc = (datetime.now(timezone.utc) - timedelta(seconds=lock2.stale_after_seconds + 10)).isoformat()
    lock2.heartbeat_at_utc = lock2.acquired_at_utc
    lock_manager.write_lock(lock2)

    report = detect_stale_locks(lock_manager)
    assert report.active_count == 1
    assert report.stale_count == 1

def test_cleanup_stale_locks_dry_run(lock_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    acq = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)
    lock = acq.lock
    lock.acquired_at_utc = (datetime.now(timezone.utc) - timedelta(seconds=lock.stale_after_seconds + 10)).isoformat()
    lock.heartbeat_at_utc = lock.acquired_at_utc
    lock_manager.write_lock(lock)

    res = cleanup_stale_locks(lock_manager, dry_run=True)
    assert res["dry_run"] is True
    assert res["stale_found"] == 1
    assert lock_manager.lock_exists(RunLockScope.SCAN)

def test_cleanup_stale_locks_force(lock_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    acq = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)
    lock = acq.lock
    lock.acquired_at_utc = (datetime.now(timezone.utc) - timedelta(seconds=lock.stale_after_seconds + 10)).isoformat()
    lock.heartbeat_at_utc = lock.acquired_at_utc
    lock_manager.write_lock(lock)

    res = cleanup_stale_locks(lock_manager, dry_run=False, force=True)
    assert res["dry_run"] is False
    assert res["stale_found"] == 1
    assert len(res["removed"]) == 1
    assert not lock_manager.lock_exists(RunLockScope.SCAN)

def test_stale_lock_report_to_text(lock_manager):
    report = detect_stale_locks(lock_manager)
    txt = stale_lock_report_to_text(report)
    assert "Active Locks" in txt

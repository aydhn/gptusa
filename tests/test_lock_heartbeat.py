import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta

from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.scheduler.lock_heartbeat import LockHeartbeatManager, calculate_lock_expiry, heartbeat_summary
from usa_signal_bot.scheduler.run_identity import create_run_identity
from usa_signal_bot.core.enums import RunLockScope, LockAcquisitionMode

@pytest.fixture
def lock_manager():
    with tempfile.TemporaryDirectory() as td:
        yield FileRunLockManager(Path(td))

@pytest.fixture
def heartbeat_manager(lock_manager):
    return LockHeartbeatManager(lock_manager)

def test_heartbeat_updates_time(lock_manager, heartbeat_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    acq = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)

    old_heartbeat = acq.lock.heartbeat_at_utc
    refreshed = heartbeat_manager.heartbeat(acq.lock, identity)

    assert refreshed.heartbeat_at_utc != old_heartbeat
    assert datetime.fromisoformat(refreshed.heartbeat_at_utc) >= datetime.fromisoformat(old_heartbeat)

def test_heartbeat_all_owned(lock_manager, heartbeat_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)
    lock_manager.acquire(RunLockScope.BACKTEST, identity, mode=LockAcquisitionMode.FAIL_FAST)

    refreshed = heartbeat_manager.heartbeat_all_owned(identity)
    assert len(refreshed) == 2

def test_heartbeat_is_recent(lock_manager, heartbeat_manager):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    acq = lock_manager.acquire(RunLockScope.SCAN, identity, mode=LockAcquisitionMode.FAIL_FAST)

    assert heartbeat_manager.heartbeat_is_recent(acq.lock) is True

def test_calculate_lock_expiry():
    now = datetime.now(timezone.utc)
    expiry_str = calculate_lock_expiry(now.isoformat(), 3600)
    expiry = datetime.fromisoformat(expiry_str)
    assert (expiry - now).total_seconds() == 3600

def test_heartbeat_summary():
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    lock = RunLockScope.SCAN # mocking for test
    # Just checking summary text gen
    res = heartbeat_summary([])
    assert res["count"] == 0

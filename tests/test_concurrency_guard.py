import pytest
import tempfile
from pathlib import Path

from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.scheduler.concurrency_guard import ConcurrencyGuard
from usa_signal_bot.scheduler.run_identity import create_run_identity
from usa_signal_bot.core.enums import RunLockScope, ConcurrencyDecision

@pytest.fixture
def lock_manager():
    with tempfile.TemporaryDirectory() as td:
        yield FileRunLockManager(Path(td))

@pytest.fixture
def guard(lock_manager):
    return ConcurrencyGuard(lock_manager)

def test_evaluate_no_active_locks_allow(guard):
    res = guard.evaluate(RunLockScope.SCAN)
    assert res.decision == ConcurrencyDecision.ALLOW

def test_active_lock_conflict_block(guard, lock_manager):
    identity1 = create_run_identity(RunLockScope.SCAN, owner="test1")
    lock_manager.acquire(RunLockScope.SCAN, identity1)

    res = guard.evaluate(RunLockScope.SCAN)
    assert res.decision == ConcurrencyDecision.BLOCK

def test_acquire_or_block_success(guard):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    res = guard.acquire_or_block(RunLockScope.SCAN, identity)
    assert res.acquired is True

def test_acquire_or_block_conflict(guard, lock_manager):
    identity1 = create_run_identity(RunLockScope.SCAN, owner="test1")
    identity2 = create_run_identity(RunLockScope.SCAN, owner="test2")
    lock_manager.acquire(RunLockScope.SCAN, identity1)

    res = guard.acquire_or_block(RunLockScope.SCAN, identity2)
    assert res.acquired is False

def test_guard_context(guard):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    with guard.guard_context(RunLockScope.SCAN, identity):
        res = guard.evaluate(RunLockScope.SCAN)
        assert res.decision == ConcurrencyDecision.BLOCK

    res = guard.evaluate(RunLockScope.SCAN)
    assert res.decision == ConcurrencyDecision.ALLOW

def test_guard_context_exception(guard):
    identity = create_run_identity(RunLockScope.SCAN, owner="test1")
    try:
        with guard.guard_context(RunLockScope.SCAN, identity):
            raise ValueError("Test error")
    except ValueError:
        pass

    res = guard.evaluate(RunLockScope.SCAN)
    assert res.decision == ConcurrencyDecision.ALLOW

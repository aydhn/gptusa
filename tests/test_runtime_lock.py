import pytest
from pathlib import Path
from usa_signal_bot.runtime.runtime_lock import RuntimeLockManager
from usa_signal_bot.core.exceptions import RuntimeLockError

def test_runtime_lock(tmp_path):
    mgr = RuntimeLockManager(tmp_path)
    assert not mgr.is_locked()

    info = mgr.acquire("run_1")
    assert mgr.is_locked()
    assert info.run_id == "run_1"

    with pytest.raises(RuntimeLockError):
        mgr.acquire("run_2")

    info_read = mgr.read_lock()
    assert info_read.run_id == "run_1"

    mgr.release(info)
    assert not mgr.is_locked()

def test_stale_lock(tmp_path):
    mgr = RuntimeLockManager(tmp_path, stale_after_seconds=-1) # Immediate stale
    info = mgr.acquire("run_1")

    # Should be stale
    assert not mgr.is_locked()
    assert mgr.clear_stale_lock() is True
    assert not mgr.lock_path().exists()

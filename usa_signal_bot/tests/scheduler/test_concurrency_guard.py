import pytest
from usa_signal_bot.scheduler.concurrency_guard import ConcurrencyGuard
from usa_signal_bot.core.enums import RunLockScope
from usa_signal_bot.scheduler.scheduler_models import RunIdentity, LockAcquisitionMode
from unittest.mock import MagicMock, patch

def test_guard_context_handles_release_exception():
    mock_lock_manager = MagicMock()
    mock_policy = MagicMock()
    mock_policy.acquisition_mode = LockAcquisitionMode.FAIL_FAST

    # Setup mock to return a blocked decision first to test the fail path if needed,
    # but we want to test the release_if_owned exception, so let's make it acquired.

    guard = ConcurrencyGuard(mock_lock_manager, [mock_policy])

    # Mock acquire_or_block to return a successful acquisition
    mock_acq_result = MagicMock()
    mock_acq_result.acquired = True
    mock_acq_result.mode = LockAcquisitionMode.FAIL_FAST
    mock_acq_result.lock = MagicMock()

    # Make release_if_owned raise an Exception (simulate what caused the bare except pass)
    with patch.object(guard, 'acquire_or_block', return_value=mock_acq_result):
        with patch.object(guard, 'release_if_owned', side_effect=FileNotFoundError("Lock file missing")):
            owner = RunIdentity(run_id="test_run", run_type=RunLockScope.GLOBAL)
            # This should not raise an exception, the bare except swallows it
            with guard.guard_context(RunLockScope.GLOBAL, owner):
                pass

            # The exception should be swallowed and release_if_owned should be called
            guard.release_if_owned.assert_called_once_with(mock_acq_result.lock, owner)

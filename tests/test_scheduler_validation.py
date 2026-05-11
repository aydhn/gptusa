import pytest

from usa_signal_bot.scheduler.scheduler_validation import (
    validate_run_lock_report, validate_concurrency_policy_report,
    validate_no_destructive_scheduler_jobs, validate_no_sensitive_data_in_scheduler_payload,
    validate_no_live_execution_language_in_scheduler, assert_scheduler_valid,
    scheduler_validation_report_to_text
)
from usa_signal_bot.scheduler.scheduler_models import RunLock, ConcurrencyPolicy
from usa_signal_bot.scheduler.run_identity import create_run_identity
from usa_signal_bot.scheduler.scheduler_plan import build_scheduler_plan
from usa_signal_bot.core.enums import RunLockScope, RunLockStatus, LockAcquisitionMode
from usa_signal_bot.core.exceptions import SchedulerValidationError

def test_validate_run_lock():
    identity = create_run_identity(RunLockScope.SCAN)
    lock = RunLock("l1", RunLockScope.SCAN, "", RunLockStatus.HELD, identity, None, None, None, 0)
    rep = validate_run_lock_report(lock)
    assert rep.valid is False
    assert rep.error_count == 2 # path and stale

def test_validate_concurrency_policy():
    pol = ConcurrencyPolicy("p1", RunLockScope.SCAN, True, 0, False, 3600, -1, LockAcquisitionMode.FAIL_FAST)
    rep = validate_concurrency_policy_report(pol)
    assert rep.valid is False
    assert rep.error_count == 2 # concurrent runs and timeout

def test_validate_no_destructive_jobs():
    plan = build_scheduler_plan()
    rep = validate_no_destructive_scheduler_jobs(plan)
    assert rep.valid is True

    plan.jobs[0].command = "python script.py cleanup-execute"
    rep = validate_no_destructive_scheduler_jobs(plan)
    assert rep.valid is False
    assert rep.blocked_count == 1

def test_validate_no_sensitive_data():
    rep = validate_no_sensitive_data_in_scheduler_payload({"some_key": "secret_123"})
    assert rep.valid is False
    assert rep.blocked_count == 1

def test_validate_no_live_approval():
    rep = validate_no_live_execution_language_in_scheduler("This is investment advice")
    assert rep.valid is False
    assert rep.blocked_count == 1

def test_assert_scheduler_valid():
    rep = validate_no_sensitive_data_in_scheduler_payload({"some_key": "secret_123"})
    with pytest.raises(SchedulerValidationError):
        assert_scheduler_valid(rep)

    rep2 = validate_no_sensitive_data_in_scheduler_payload({"safe": "data"})
    assert_scheduler_valid(rep2) # Should not raise

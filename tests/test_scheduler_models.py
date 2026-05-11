import pytest
from usa_signal_bot.scheduler.scheduler_models import (
    RunIdentity, RunLock, LockAcquisitionResult, ConcurrencyPolicy, ConcurrencyDecisionResult,
    IdempotencyRecord, SchedulerJob, SchedulerPlan, SchedulerRunResult,
    create_run_id, create_lock_id, create_lock_acquisition_result_id,
    create_concurrency_policy_id, create_concurrency_decision_id,
    create_scheduler_job_id, create_scheduler_plan_id, create_scheduler_run_id,
    run_identity_to_dict, validate_run_lock
)
from usa_signal_bot.core.enums import RunLockScope, RunLockStatus, LockAcquisitionMode
from usa_signal_bot.core.exceptions import SchedulerValidationError

def test_run_identity_creation():
    rid = create_run_id()
    assert rid.startswith("run_")
    identity = RunIdentity(
        run_id=rid,
        run_type=RunLockScope.GLOBAL,
        owner="test_user",
        hostname="localhost",
        process_id=123,
        created_at_utc="2023-01-01T00:00:00Z"
    )
    assert identity.owner == "test_user"
    d = run_identity_to_dict(identity)
    assert d["owner"] == "test_user"

def test_run_lock_validation():
    identity = RunIdentity(
        run_id="run_1",
        run_type=RunLockScope.GLOBAL,
        owner="test_user",
        hostname="localhost",
        process_id=123,
        created_at_utc="2023-01-01T00:00:00Z"
    )
    lock = RunLock(
        lock_id="lock_1",
        scope=RunLockScope.GLOBAL,
        lock_path="test.lock",
        status=RunLockStatus.HELD,
        owner=identity,
        acquired_at_utc="2023-01-01T00:00:00Z",
        heartbeat_at_utc=None,
        expires_at_utc=None,
        stale_after_seconds=-10
    )
    with pytest.raises(SchedulerValidationError):
        validate_run_lock(lock)

    lock.stale_after_seconds = 3600
    lock.lock_path = ""
    with pytest.raises(SchedulerValidationError):
        validate_run_lock(lock)

def test_factory_functions():
    assert create_lock_id(RunLockScope.SCAN).startswith("lock_scan_")
    assert create_lock_acquisition_result_id().startswith("lock_acq_")
    assert create_concurrency_policy_id(RunLockScope.PAPER).startswith("policy_paper")
    assert create_concurrency_decision_id().startswith("concurrency_")
    assert create_scheduler_job_id("test job").startswith("job_test_job_")
    assert create_scheduler_plan_id().startswith("sched_plan_")
    assert create_scheduler_run_id().startswith("sched_run_")

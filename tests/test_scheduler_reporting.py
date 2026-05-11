import tempfile
from pathlib import Path

from usa_signal_bot.scheduler.scheduler_reporting import (
    run_identity_to_text, run_lock_to_text, lock_acquisition_result_to_text,
    concurrency_decision_to_text, scheduler_job_to_text, scheduler_plan_to_text,
    scheduler_run_result_to_text, scheduler_store_summary_to_text,
    scheduler_limitations_text, write_scheduler_report_json
)
from usa_signal_bot.scheduler.run_identity import create_run_identity
from usa_signal_bot.scheduler.scheduler_models import RunLock, LockAcquisitionResult, ConcurrencyDecisionResult, ConcurrencyPolicy
from usa_signal_bot.core.enums import RunLockScope, RunLockStatus, LockAcquisitionMode, ConcurrencyDecision
from usa_signal_bot.scheduler.scheduler_plan import build_scheduler_plan
from usa_signal_bot.scheduler.scheduler_executor import LocalSchedulerExecutor

def test_reporting_formatting():
    id1 = create_run_identity(RunLockScope.SCAN, "u1")
    assert "u1" in run_identity_to_text(id1)

    lock = RunLock("l1", RunLockScope.SCAN, "path", RunLockStatus.HELD, id1, "now", None, None, 3600)
    assert "HELD" in run_lock_to_text(lock)

    acq = LockAcquisitionResult("r1", "now", RunLockStatus.ACQUIRED, RunLockScope.SCAN, True, lock, None, LockAcquisitionMode.FAIL_FAST)
    assert "ACQUIRED" in lock_acquisition_result_to_text(acq)

    pol = ConcurrencyPolicy("p1", RunLockScope.SCAN, True, 1, False, 3600, 0, LockAcquisitionMode.FAIL_FAST)
    dec = ConcurrencyDecisionResult("d1", "now", RunLockScope.SCAN, ConcurrencyDecision.ALLOW, pol, [], "ok")
    assert "ALLOW" in concurrency_decision_to_text(dec)

def test_plan_and_run_reporting():
    plan = build_scheduler_plan()
    assert "Scheduler Plan" in scheduler_plan_to_text(plan)

    with tempfile.TemporaryDirectory() as td:
        exe = LocalSchedulerExecutor(Path(td), execute_commands=False)
        res = exe.run_plan(plan)
        txt = scheduler_run_result_to_text(res)
        assert "Scheduler Run" in txt
        assert "Executed:" in txt

def test_limitations_text():
    txt = scheduler_limitations_text()
    assert "LOCAL scheduler only" in txt
    assert "NO BROKER" in txt

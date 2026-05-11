import pytest
import tempfile
from pathlib import Path

from usa_signal_bot.scheduler.scheduler_executor import LocalSchedulerExecutor
from usa_signal_bot.scheduler.scheduler_plan import build_scheduler_plan
from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.core.enums import SchedulerPlanStatus, SchedulerJobStatus

@pytest.fixture
def data_root():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

@pytest.fixture
def lock_manager(data_root):
    return FileRunLockManager(data_root / "scheduler" / "locks")

def test_run_plan_dry_run_simulation(data_root):
    exe = LocalSchedulerExecutor(data_root, execute_commands=False)
    plan = build_scheduler_plan(dry_run=True)
    res = exe.run_plan(plan)

    assert res.status == SchedulerPlanStatus.DRY_RUN_COMPLETED
    assert len(res.executed_jobs) == len(plan.jobs)
    for j in res.executed_jobs:
        assert j.status == SchedulerJobStatus.DRY_RUN_ONLY

def test_run_plan_with_locks(data_root, lock_manager):
    exe = LocalSchedulerExecutor(data_root, lock_manager=lock_manager, execute_commands=False)
    plan = build_scheduler_plan(dry_run=True)
    res = exe.run_plan(plan)

    assert res.status == SchedulerPlanStatus.DRY_RUN_COMPLETED
    assert len(res.lock_results) == len(plan.jobs)
    for r in res.lock_results:
        # In dry run mode, acq is False but it's not a true failure
        assert r.acquired is False

def test_write_result(data_root):
    exe = LocalSchedulerExecutor(data_root, execute_commands=False)
    plan = build_scheduler_plan(dry_run=True)
    res = exe.run_plan(plan)

    paths = exe.write_result(res)
    assert len(paths) == 1
    assert paths[0].exists()

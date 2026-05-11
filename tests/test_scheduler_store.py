import pytest
import tempfile
from pathlib import Path

from usa_signal_bot.scheduler.scheduler_store import (
    scheduler_store_dir, locks_dir, scheduler_plans_dir, scheduler_runs_dir,
    write_scheduler_plan_json, write_scheduler_run_result_json,
    read_scheduler_plan_json, read_scheduler_run_result_json,
    list_scheduler_plans, list_scheduler_runs, scheduler_store_summary
)
from usa_signal_bot.scheduler.scheduler_plan import build_scheduler_plan
from usa_signal_bot.scheduler.scheduler_executor import LocalSchedulerExecutor

@pytest.fixture
def data_root():
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

def test_dirs_created(data_root):
    locks_dir(data_root)
    scheduler_plans_dir(data_root)
    scheduler_runs_dir(data_root)

    assert (data_root / "scheduler" / "locks").exists()
    assert (data_root / "scheduler" / "plans").exists()
    assert (data_root / "scheduler" / "runs").exists()

def test_write_read_plan(data_root):
    plan = build_scheduler_plan(dry_run=True)
    p = scheduler_plans_dir(data_root) / f"{plan.plan_id}.json"

    write_scheduler_plan_json(p, plan)
    assert p.exists()

    data = read_scheduler_plan_json(p)
    assert data["plan_id"] == plan.plan_id

def test_write_read_run_result(data_root):
    plan = build_scheduler_plan(dry_run=True)
    exe = LocalSchedulerExecutor(data_root, execute_commands=False)
    res = exe.run_plan(plan)

    p = scheduler_runs_dir(data_root) / f"{res.run_id}.json"
    write_scheduler_run_result_json(p, res)
    assert p.exists()

    data = read_scheduler_run_result_json(p)
    assert data["run_id"] == res.run_id

def test_lists_and_summary(data_root):
    plan = build_scheduler_plan(dry_run=True)
    p1 = scheduler_plans_dir(data_root) / f"{plan.plan_id}.json"
    write_scheduler_plan_json(p1, plan)

    assert len(list_scheduler_plans(data_root)) == 1
    summ = scheduler_store_summary(data_root)
    assert summ["plans_count"] == 1

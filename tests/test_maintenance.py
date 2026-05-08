from usa_signal_bot.release.maintenance_models import MaintenanceTask, MaintenancePlan, MaintenanceRunResult
from usa_signal_bot.core.enums import MaintenanceFrequency, MaintenanceTaskStatus
from usa_signal_bot.release.maintenance_tasks import default_maintenance_plan, run_maintenance_check
from pathlib import Path

def test_maintenance_plan_generation():
    plan = default_maintenance_plan()
    assert len(plan.tasks) > 0

def test_run_maintenance_check(tmp_path):
    res = run_maintenance_check(MaintenanceFrequency.DAILY, tmp_path, tmp_path / "data")
    assert res.status.value == "PASSED"
    assert res.passed_count > 0

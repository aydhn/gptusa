from usa_signal_bot.incident.rollback_executor import RollbackExecutor
from usa_signal_bot.incident.rollback_models import RollbackSource, RollbackStep
from usa_signal_bot.core.enums import RollbackSourceType, RollbackStepStatus
from pathlib import Path

def test_executor_dry_run_does_not_execute():
    e = RollbackExecutor(Path("."), Path("."))
    step = RollbackStep("1", "test", "src", "dst", RollbackStepStatus.PENDING, "COPY", True, False)
    res = e.execute_step(step)
    assert res.status == RollbackStepStatus.DRY_RUN_OK

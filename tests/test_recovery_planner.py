from pathlib import Path
from usa_signal_bot.incident.recovery_planner import RecoveryPlanner
from usa_signal_bot.core.enums import RecoveryPlanStatus

def test_planner_empty():
    planner = RecoveryPlanner(Path("data"), Path("."))
    plan = planner.build_plan([])
    assert plan.status == RecoveryPlanStatus.SKIPPED

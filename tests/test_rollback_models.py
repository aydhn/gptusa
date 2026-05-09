from usa_signal_bot.incident.rollback_models import RollbackSource, RollbackPlan, validate_rollback_plan
from usa_signal_bot.core.enums import RollbackSourceType, RollbackPlanStatus, RollbackSafetyStatus
from usa_signal_bot.core.exceptions import RollbackSourceError
import pytest

def test_rollback_plan_invalid_language():
    plan = RollbackPlan(
        plan_id="1", created_at_utc="", status=RollbackPlanStatus.CREATED,
        source=RollbackSource("1", RollbackSourceType.MANUAL_PATH, "path", "", "", True),
        dry_run=True, steps=[], safety_status=RollbackSafetyStatus.SAFE,
        warnings=["live approval required"]
    )
    with pytest.raises(RollbackSourceError):
        validate_rollback_plan(plan)

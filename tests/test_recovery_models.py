from usa_signal_bot.incident.recovery_models import RecoveryAction, create_recovery_action_id, validate_recovery_action
from usa_signal_bot.core.enums import RecoveryActionType, RecoveryActionStatus
from usa_signal_bot.core.exceptions import RecoveryActionError
import pytest

def test_validate_action():
    act = RecoveryAction(
        action_id=create_recovery_action_id("test"),
        action_type=RecoveryActionType.CUSTOM,
        name="",
        description="desc",
        command=None,
        dry_run=True,
        required=True,
        status=RecoveryActionStatus.PENDING
    )
    with pytest.raises(RecoveryActionError):
        validate_recovery_action(act)

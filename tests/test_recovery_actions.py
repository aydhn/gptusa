from usa_signal_bot.incident.recovery_actions import recovery_actions_for_category
from usa_signal_bot.core.enums import IncidentCategory, RecoveryActionType

def test_actions_for_config():
    acts = recovery_actions_for_category(IncidentCategory.CONFIG_ERROR)
    types = [a.action_type for a in acts]
    assert RecoveryActionType.VALIDATE_CONFIG in types
    assert RecoveryActionType.RUN_HEALTH_CHECK in types

from usa_signal_bot.paper_observation.blocked_operation_history import (
    aggregate_blocked_operation_history, blocked_operation_count,
    blocked_operations_by_type, blocked_operation_risk_flags, blocked_operation_history_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def test_blocked_operation_history():
    events = [
        {"event_type": "BLOCKED_OPERATION", "operation_type": "REAL_ORDER"},
        {"event_type": "BLOCKED_OPERATION", "operation_type": "CONFIG_PATCH"}
    ]

    assert blocked_operation_count(events) == 2

    by_type = blocked_operations_by_type(events)
    assert by_type["REAL_ORDER"] == 1

    flags = blocked_operation_risk_flags(events)
    assert ObservationRiskFlag.BLOCKED_OPERATION_HISTORY in flags
    assert ObservationRiskFlag.REAL_ORDER_RISK in flags
    assert ObservationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK in flags

    agg = aggregate_blocked_operation_history(events)
    assert agg["total_blocked"] == 2

    text = blocked_operation_history_to_text(agg)
    assert "Total Blocked: 2" in text

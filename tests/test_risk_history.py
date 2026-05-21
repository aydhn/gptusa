from usa_signal_bot.paper_observation.risk_history import (
    aggregate_risk_outcome_history, risk_warning_ratio, risk_rejection_ratio,
    risk_history_flags, risk_history_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def test_risk_history():
    sessions = [
        {"proposals": [1, 2], "risk_warning_count": 1, "risk_rejected_count": 2, "real_order_risk_detected": True}
    ]

    w_ratio = risk_warning_ratio(sessions)
    assert w_ratio == 0.5

    r_ratio = risk_rejection_ratio(sessions)
    assert r_ratio == 1.0

    flags = risk_history_flags(sessions)
    assert ObservationRiskFlag.REAL_ORDER_RISK in flags
    assert ObservationRiskFlag.RISK_REJECTION_HIGH in flags

    agg = aggregate_risk_outcome_history(sessions)
    assert agg["session_count"] == 1

    text = risk_history_to_text(agg)
    assert "Rejection Ratio: 1.00" in text

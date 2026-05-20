from usa_signal_bot.paper_observation.notification_safety_history import (
    aggregate_notification_safety_history, notification_warning_count,
    detect_unsafe_notification_history, notification_safety_risk_flags, notification_safety_history_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def test_notification_safety_history():
    sessions = [
        {"notification_warning_count": 1, "notifications": [{"text": "Gerçek emir gönderildi."}]},
        {"telegram_real_send_detected": True}
    ]

    assert notification_warning_count(sessions) == 1

    unsafe = detect_unsafe_notification_history(sessions)
    assert len(unsafe) > 0
    assert any("gerçek emir" in u for u in unsafe)

    flags = notification_safety_risk_flags(sessions)
    assert ObservationRiskFlag.NOTIFICATION_UNSAFE in flags
    assert ObservationRiskFlag.TELEGRAM_REAL_SEND_RISK in flags

    agg = aggregate_notification_safety_history(sessions)
    assert agg["warning_count"] == 1

    text = notification_safety_history_to_text(agg)
    assert "Warnings: 1" in text

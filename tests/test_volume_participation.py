from usa_signal_bot.execution.volume_participation import (
    calculate_participation_rate_pct,
    classify_participation_risk,
    volume_participation_to_text
)
from usa_signal_bot.core.enums import ExecutionRiskLevel

def test_volume_participation():
    rate = calculate_participation_rate_pct(1000.0, 100000.0)
    assert rate == 1.0

    risk = classify_participation_risk(rate)
    assert risk == ExecutionRiskLevel.LOW

    risk = classify_participation_risk(6.0)
    assert risk == ExecutionRiskLevel.HIGH

    txt = volume_participation_to_text(1000.0, 100000.0, rate)
    assert "1.0000%" in txt

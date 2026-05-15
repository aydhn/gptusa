import pytest
from usa_signal_bot.regime_map.regime_map_validation import validate_no_live_execution_language_in_regime_map

def test_validate_no_live_execution_language_in_regime_map():
    report = validate_no_live_execution_language_in_regime_map("This is live approved")
    assert not report.valid
    assert "Prohibited certainty/live language" in report.issues[0].message

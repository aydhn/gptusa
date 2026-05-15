import pytest
from usa_signal_bot.regime_map.breadth_proxy import classify_breadth_regime, breadth_proxy_summary_to_text
from usa_signal_bot.core.enums import BreadthRegime
from usa_signal_bot.regime_map.regime_map_models import MultiTimeframeRegimeConfirmation

def test_classify_breadth_insufficient():
    assert classify_breadth_regime([]) == BreadthRegime.INSUFFICIENT_DATA

def test_breadth_proxy_summary_to_text():
    text = breadth_proxy_summary_to_text({
        "regime": "RISK_ON",
        "breadth_score": 80.0,
        "uptrend_ratio": 75.0,
        "momentum_positive_ratio": 85.0
    })
    assert "RISK_ON" in text
    assert "80.0" in text

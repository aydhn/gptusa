import pytest
from usa_signal_bot.regime_classification.feature_engineering.regime_feature_engineering_reporting import (
    regime_feature_engineering_limitations_text
)

def test_regime_feature_engineering_limitations_text():
    text = regime_feature_engineering_limitations_text()
    assert "Phase 127 Limitations" in text
    assert "trade signal" in text

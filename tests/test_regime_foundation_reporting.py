from usa_signal_bot.regime_classification.foundation.regime_foundation_reporting import regime_foundation_limitations_text

def test_limitations_text():
    text = regime_foundation_limitations_text()
    assert "NOT activation" in text
    assert "NOT deployment" in text

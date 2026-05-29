from usa_signal_bot.regime_classification.alignment.regime_alignment_reporting import regime_alignment_limitations_text
def test_reporting():
    assert "no execution" in regime_alignment_limitations_text()

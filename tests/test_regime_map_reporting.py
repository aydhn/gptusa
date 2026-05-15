from usa_signal_bot.regime_map.regime_map_reporting import regime_map_limitations_text

def test_limitations_text():
    text = regime_map_limitations_text()
    assert "NOT investment advice" in text
    assert "No live broker execution" in text

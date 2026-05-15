import pytest
from usa_signal_bot.regime_map.regime_map_reporting import regime_map_limitations_text

def test_regime_map_limitations_text():
    text = regime_map_limitations_text()
    assert "Does not constitute investment advice" in text

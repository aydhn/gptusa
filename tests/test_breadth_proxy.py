from usa_signal_bot.regime_map.breadth_proxy import classify_breadth_regime
from usa_signal_bot.core.enums import BreadthRegime
from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine

def test_breadth_insufficient():
    assert classify_breadth_regime([]) == BreadthRegime.INSUFFICIENT_DATA

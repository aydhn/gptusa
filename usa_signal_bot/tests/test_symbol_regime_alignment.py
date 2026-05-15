import pytest
from usa_signal_bot.regime_map.symbol_regime_alignment import evaluate_symbol_regime_alignment, symbol_regime_alignment_to_text
from usa_signal_bot.regime_map.cross_sectional_regime_map import CrossSectionalRegimeMapBuilder
from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine
from usa_signal_bot.core.enums import RegimeTimeframe

def test_evaluate_symbol_regime_alignment_insufficient():
    builder = CrossSectionalRegimeMapBuilder()
    m = builder.build_map([])

    engine = MultiTimeframeRegimeConfirmationEngine([RegimeTimeframe.DAILY])
    conf = engine.confirm_symbol("SPY", [])

    alignment = evaluate_symbol_regime_alignment(conf, m)
    assert alignment.status.value == "INSUFFICIENT_DATA"

def test_symbol_regime_alignment_to_text():
    builder = CrossSectionalRegimeMapBuilder()
    m = builder.build_map([])
    engine = MultiTimeframeRegimeConfirmationEngine([RegimeTimeframe.DAILY])
    conf = engine.confirm_symbol("SPY", [])
    alignment = evaluate_symbol_regime_alignment(conf, m)

    text = symbol_regime_alignment_to_text(alignment)
    assert "INSUFFICIENT_DATA" in text

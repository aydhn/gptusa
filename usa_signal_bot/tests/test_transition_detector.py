import pytest
from usa_signal_bot.regime_map.transition_detector import detect_symbol_regime_transition, transition_detector_summary_to_text
from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine
from usa_signal_bot.core.enums import RegimeTimeframe

def test_detect_symbol_regime_transition_no_previous():
    engine = MultiTimeframeRegimeConfirmationEngine([RegimeTimeframe.DAILY])
    conf = engine.confirm_symbol("SPY", [])
    signals = detect_symbol_regime_transition(conf)
    assert len(signals) == 0

def test_transition_detector_summary_to_text():
    text = transition_detector_summary_to_text([])
    assert "No regime transitions detected" in text

from usa_signal_bot.regime_map.transition_detector import detect_symbol_regime_transition
from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine

def test_transition_detect_none():
    engine = MultiTimeframeRegimeConfirmationEngine()
    rows = [{"date": f"2024-01-{i:02d}", "open": 100+i, "high": 110+i, "low": 90+i, "close": 105+i, "volume": 100000} for i in range(1, 28)]
    # Needs more rows for trend, but will just test the detector doesn't crash
    conf = engine.confirm_symbol("SPY", rows)
    sigs = detect_symbol_regime_transition(conf, None)
    assert isinstance(sigs, list)

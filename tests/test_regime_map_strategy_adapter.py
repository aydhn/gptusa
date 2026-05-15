from usa_signal_bot.regime_map.strategy_adapter import attach_regime_confirmation_to_signal

def test_attach_signal():
    sig = {"symbol": "SPY", "direction": "LONG"}
    out = attach_regime_confirmation_to_signal(sig, None, None, None)
    assert out["metadata"]["regime_confirmation_status"] == "UNKNOWN"

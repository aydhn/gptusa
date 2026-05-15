from usa_signal_bot.regime_map.paper_adapter import attach_regime_map_to_paper_order

def test_attach_paper():
    res = {"symbol": "SPY"}
    out = attach_regime_map_to_paper_order(res, None, None)
    assert out["metadata"]["regime_confirmation"] == "UNKNOWN"

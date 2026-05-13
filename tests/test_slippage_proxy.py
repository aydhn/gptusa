from usa_signal_bot.execution.slippage_proxy import estimate_slippage_proxy

def test_slippage_proxy():
    rows = [{"close": 100, "volume": 1000000}]
    est = estimate_slippage_proxy("SPY", rows, "long", 1000.0)
    # Slippage should be evaluated
    assert est.symbol == "SPY"

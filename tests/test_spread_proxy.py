from usa_signal_bot.execution.spread_proxy import estimate_spread_proxy_bps_from_ohlcv, estimate_spread_proxy

def test_spread_proxy():
    rows = [{"close": 100, "volume": 1000000}]
    bps = estimate_spread_proxy_bps_from_ohlcv(rows)
    assert bps == 5.0

    est = estimate_spread_proxy("SPY", rows)
    assert est.spread_proxy_bps == 5.0
    assert est.symbol == "SPY"

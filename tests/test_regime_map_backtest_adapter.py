from usa_signal_bot.regime_map.backtest_adapter import attach_regime_map_to_backtest_result

def test_attach_backtest():
    res = {"metrics": {}}
    out = attach_regime_map_to_backtest_result(res, None)
    assert out == res

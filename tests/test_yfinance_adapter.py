from usa_signal_bot.data_providers.adapters.yfinance_adapter import YFinanceMarketDataAdapter

def test_yfinance_adapter():
    adapter = YFinanceMarketDataAdapter()
    spec = adapter.adapter_spec()
    assert spec["provider_name"] == "YFINANCE"
    assert spec["network_enabled_by_default"] is False

    res = adapter.fetch_daily_ohlcv_guarded("AAPL", allow_network=False)
    assert res["network_used"] is False

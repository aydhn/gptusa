from usa_signal_bot.data_providers.adapters.stooq_adapter import StooqMarketDataAdapter

def test_stooq_adapter():
    adapter = StooqMarketDataAdapter()
    spec = adapter.adapter_spec()
    assert spec["provider_name"] == "STOOQ"
    assert spec["network_enabled_by_default"] is False

    res = adapter.fetch_daily_ohlcv_guarded("AAPL", allow_network=False)
    assert res["network_used"] is False

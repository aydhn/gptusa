from usa_signal_bot.data_provider_runtime.cache_key_builder import build_provider_cache_key

def test_build_provider_cache_key():
    key = build_provider_cache_key(
        provider_name="YFINANCE",
        capability="GET_DAILY_OHLCV",
        symbol="AAPL"
    )
    assert key.valid is True
    assert "yfinance" in key.cache_path
    assert "aapl" in key.cache_key

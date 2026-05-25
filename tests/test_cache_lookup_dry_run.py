from usa_signal_bot.data_provider_runtime.cache_lookup_dry_run import run_cache_lookup_dry_run
from usa_signal_bot.data_provider_runtime.cache_key_builder import build_provider_cache_key

def test_cache_lookup_dry_run():
    key = build_provider_cache_key("YFINANCE", "GET_DAILY_OHLCV", "AAPL")
    res = run_cache_lookup_dry_run(key, None)
    assert res.network_used is False
    assert res.cache_path_exists is False

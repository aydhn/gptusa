from usa_signal_bot.data_provider_runtime.fetch_dry_run_planner import build_fetch_dry_run_plan

def test_fetch_dry_run_planner():
    plan = build_fetch_dry_run_plan(
        provider_name="YFINANCE",
        capability="GET_DAILY_OHLCV",
        symbol="AAPL"
    )
    assert plan.allow_network is False
    assert plan.dry_run_only is True
    assert plan.cache_key is not None

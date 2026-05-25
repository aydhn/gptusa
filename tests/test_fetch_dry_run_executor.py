from usa_signal_bot.data_provider_runtime.fetch_dry_run_planner import build_fetch_dry_run_plan
from usa_signal_bot.data_provider_runtime.fetch_dry_run_executor import execute_fetch_dry_run

def test_fetch_dry_run_executor():
    plan = build_fetch_dry_run_plan(
        provider_name="YFINANCE",
        capability="GET_DAILY_OHLCV",
        symbol="AAPL",
        allow_network=False
    )
    res = execute_fetch_dry_run(plan)
    assert res.fetch_performed is False
    assert res.network_used is False
    assert res.passed is True

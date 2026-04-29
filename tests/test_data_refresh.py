from usa_signal_bot.data.refresh import CacheRefreshRequest, evaluate_cache_file_status, build_cache_refresh_plan, cache_refresh_plan_to_text
from usa_signal_bot.core.enums import CacheDecision

def test_evaluate_cache_file_status(tmp_path):
    path = tmp_path / "cache" / "market_data" / "mock_AAPL_1d_start_end.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text("{}")

    # fresh
    status = evaluate_cache_file_status(tmp_path, "mock", "AAPL", "1d", None, None, 3600)
    assert status.decision == CacheDecision.USE_CACHE

    # force
    status_force = evaluate_cache_file_status(tmp_path, "mock", "AAPL", "1d", None, None, 3600, force_refresh=True)
    assert status_force.decision == CacheDecision.REFRESH_CACHE

    # bypass
    status_bypass = evaluate_cache_file_status(tmp_path, "mock", "AAPL", "1d", None, None, 3600, use_cache=False)
    assert status_bypass.decision == CacheDecision.BYPASS_CACHE

    # stale (ttl 0)
    status_stale = evaluate_cache_file_status(tmp_path, "mock", "AAPL", "1d", None, None, 0)
    assert status_stale.decision == CacheDecision.CACHE_STALE

    # missing
    status_miss = evaluate_cache_file_status(tmp_path, "mock", "MSFT", "1d", None, None, 3600)
    assert status_miss.decision == CacheDecision.CACHE_MISSING

def test_build_cache_refresh_plan(tmp_path):
    req = CacheRefreshRequest(provider_name="mock", symbols=["AAPL", "MSFT"], timeframe="1d")
    plan = build_cache_refresh_plan(tmp_path, req, 3600, 25)

    assert len(plan.symbols_to_refresh) == 2 # both missing

    txt = cache_refresh_plan_to_text(plan)
    assert "Refresh Required: 2" in txt

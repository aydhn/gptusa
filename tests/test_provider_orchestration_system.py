from pathlib import Path
from usa_signal_bot.provider_orchestration import *

def test_orchestration_policy():
    policy = build_default_provider_orchestration_policy()
    assert policy["metadata_only"] is True
    assert policy["allow_network"] is False
    assert len(validate_provider_orchestration_policy(policy)) == 0

def test_source_blending_policy():
    policy = build_default_source_blending_policy()
    assert policy["dry_run_only"] is True
    assert len(validate_source_blending_policy(policy)) == 0

def test_provider_route_planner():
    req = build_orchestrated_data_request("AAPL")
    assert req.allow_network is False
    plan = build_provider_route_plan(req)
    assert plan.symbol == "AAPL"
    assert len(plan.errors) == 0

def test_provider_route_selector():
    req = build_orchestrated_data_request("AAPL")
    plan = build_provider_route_plan(req)
    selector = ProviderRouteSelector()
    res = selector.select_route(plan)
    assert not res.network_used
    assert not res.order_created

def test_source_blending_engine():
    engine = SourceBlendingEngine()
    inp = engine.build_blend_input("AAPL", {"A": [], "B": []}, {"A": 0.9}, {"A": 0.8})
    res = engine.blend(inp)
    assert not res.produces_trade_signal
    assert not res.network_used

def test_data_availability():
    avail = check_cache_availability("AAPL", "GET_DAILY_OHLCV")
    assert not avail.cache_available
    monitor = DataAvailabilityMonitor()
    rep = monitor.check(["AAPL"])
    assert not rep.network_used

def test_refresh_planning():
    avail = check_cache_availability("AAPL", "GET_DAILY_OHLCV")
    item = build_refresh_plan_item(avail)
    assert not item.network_allowed_now
    rep = build_refresh_plan_report(DataAvailabilityReport(availability_report_id="1", created_at_utc="", items=[avail]))
    assert rep.dry_run_only

def test_safety_validators():
    ctx = build_provider_orchestration_context()
    assert len(validate_provider_orchestration_context_safety(ctx)) == 0
    assert not source_blending_has_trade_language("research data")
    assert source_blending_has_trade_language("strong buy now")

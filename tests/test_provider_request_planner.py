
from usa_signal_bot.data_providers.provider_request_planner import build_market_data_request_plan, validate_provider_request_plan

def test_provider_request_planner():
    req = build_market_data_request_plan("AAPL")
    assert req.metadata_only is True
    assert req.allow_network is False
    errs = validate_provider_request_plan(req)
    assert len(errs) == 0

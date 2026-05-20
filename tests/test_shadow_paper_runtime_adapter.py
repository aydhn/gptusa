from usa_signal_bot.paper_shadow.paper_runtime_adapter import (
    build_shadow_context_from_paper_runtime_snapshot, copy_paper_snapshot_to_shadow_portfolio,
    validate_no_paper_runtime_mutation, attach_shadow_preview_to_paper_analytics
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def test_build_shadow_context_from_paper_runtime_snapshot():
    ctx = build_shadow_context_from_paper_runtime_snapshot({"equity": 120000.0})
    assert ctx.starting_equity_usd == 120000.0

def test_copy_paper_snapshot_to_shadow_portfolio():
    port = copy_paper_snapshot_to_shadow_portfolio({"equity": 120000.0, "positions": [{"symbol": "AAPL", "market_value": 1500.0}]})
    assert port.equity_usd == 120000.0
    assert len(port.positions) == 1
    assert port.positions[0].symbol == "AAPL"

def test_validate_no_paper_runtime_mutation():
    assert len(validate_no_paper_runtime_mutation({"a": 1}, {"a": 1})) == 0
    assert len(validate_no_paper_runtime_mutation({"a": 1}, {"a": 2})) == 1

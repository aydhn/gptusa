from usa_signal_bot.paper_shadow.shadow_rebalance import (
    build_shadow_rebalance_preview, shadow_rebalance_intents_from_portfolio,
    validate_shadow_rebalance_safe, shadow_rebalance_summary
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio

def test_build_shadow_rebalance_preview():
    ctx = build_mock_shadow_simulation_context(100000.0)
    port = initialize_shadow_portfolio(ctx)
    prev = build_shadow_rebalance_preview(port, ctx)
    assert prev["status"] == "preview_only"

def test_validate_shadow_rebalance_safe():
    assert len(validate_shadow_rebalance_safe({})) == 0

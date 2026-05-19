import pytest
from usa_signal_bot.paper_shadow.shadow_rebalance import (
    build_shadow_rebalance_preview,
    shadow_rebalance_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio, build_shadow_position

def test_shadow_rebalance():
    ctx = build_mock_shadow_simulation_context()
    port = initialize_shadow_portfolio(ctx)
    port.positions.append(build_shadow_position("AAPL", 10.0, 150.0))

    prev = build_shadow_rebalance_preview(port, ctx)
    assert len(prev["intents"]) == 1
    assert prev["is_safe"]

    text = shadow_rebalance_to_text(prev)
    assert "Shadow Rebalance Preview" in text

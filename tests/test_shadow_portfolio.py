import pytest
from usa_signal_bot.paper_shadow.shadow_portfolio import (
    initialize_shadow_portfolio,
    build_shadow_position,
    update_shadow_portfolio_with_fill,
    calculate_shadow_exposures,
    shadow_portfolio_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_models import ShadowFill
from usa_signal_bot.core.enums import ShadowFillStatus

def test_shadow_portfolio():
    ctx = build_mock_shadow_simulation_context()
    port = initialize_shadow_portfolio(ctx)

    assert port.cash_usd == 100000.0
    assert port.equity_usd == 100000.0

    pos = build_shadow_position("AAPL", 10.0, 150.0)
    assert pos.market_value_usd == 1500.0

    fill = ShadowFill(
        fill_id="test",
        created_at_utc="test",
        intent_id="test",
        symbol="AAPL",
        side="BUY",
        requested_quantity=10.0,
        filled_quantity=10.0,
        simulated_cost_usd=1500.0,
        simulated_slippage_usd=0.0,
        status=ShadowFillStatus.SIMULATED_FILLED,
        is_real_fill=False,
        warnings=[],
        errors=[],
        fill_price=150.0
    )

    port = update_shadow_portfolio_with_fill(port, fill)
    assert port.cash_usd == 98500.0 # 100000 - 1500
    assert len(port.positions) == 1
    assert port.positions[0].quantity == 10.0

    exposures = calculate_shadow_exposures(port)
    assert exposures["gross"] == 1500.0

    text = shadow_portfolio_to_text(port)
    assert "Shadow Portfolio" in text

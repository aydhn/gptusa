from usa_signal_bot.paper_shadow.shadow_portfolio import (
    initialize_shadow_portfolio, build_shadow_position, update_shadow_portfolio_with_fill,
    calculate_shadow_exposures, shadow_portfolio_summary, shadow_portfolio_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_models import ShadowFill
from usa_signal_bot.core.enums import ShadowFillStatus

def test_initialize_shadow_portfolio():
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=10000.0)
    port = initialize_shadow_portfolio(ctx)
    assert port.equity_usd == 10000.0
    assert port.cash_usd == 10000.0

def test_build_shadow_position():
    pos = build_shadow_position("AAPL", 10.0, 150.0)
    assert pos.symbol == "AAPL"
    assert pos.market_value_usd == 1500.0

def test_update_shadow_portfolio_with_fill():
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=10000.0)
    port = initialize_shadow_portfolio(ctx)
    fill = ShadowFill(
        fill_id="f1", created_at_utc="", intent_id="i1", symbol="AAPL", side="BUY",
        requested_quantity=10.0, filled_quantity=10.0, fill_price=150.0,
        simulated_cost_usd=5.0, simulated_slippage_usd=2.0, status=ShadowFillStatus.SIMULATED_FILLED,
        is_real_fill=False, warnings=[], errors=[]
    )
    port = update_shadow_portfolio_with_fill(port, fill)
    assert len(port.positions) == 1
    assert port.cash_usd == 10000.0 - 1500.0 - 5.0 - 2.0
    assert port.equity_usd == 10000.0 - 5.0 - 2.0

def test_calculate_shadow_exposures():
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=10000.0)
    port = initialize_shadow_portfolio(ctx)
    port.positions.append(build_shadow_position("AAPL", 10.0, 150.0))
    port.gross_exposure_usd = 1500.0
    exp = calculate_shadow_exposures(port)
    assert exp["gross_exposure_usd"] == 1500.0

def test_shadow_portfolio_summary():
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=10000.0)
    port = initialize_shadow_portfolio(ctx)
    s = shadow_portfolio_summary(port)
    assert s["equity_usd"] == 10000.0

def test_shadow_portfolio_to_text():
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=10000.0)
    port = initialize_shadow_portfolio(ctx)
    assert "eq=10000" in shadow_portfolio_to_text(port)

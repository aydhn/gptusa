from usa_signal_bot.paper_shadow.shadow_pnl_tracker import (
    build_shadow_pnl_snapshot, update_shadow_pnl_after_fills,
    calculate_shadow_return_pct, calculate_shadow_drawdown_pct,
    shadow_pnl_summary, shadow_pnl_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio

def test_build_shadow_pnl_snapshot():
    ctx = build_mock_shadow_simulation_context(100000.0)
    port = initialize_shadow_portfolio(ctx)
    port.equity_usd = 105000.0
    pnl = build_shadow_pnl_snapshot(port, ctx.starting_equity_usd)
    assert pnl.total_pnl_usd == 5000.0
    assert pnl.return_pct == 5.0

def test_calculate_shadow_return_pct():
    assert calculate_shadow_return_pct(105000.0, 100000.0) == 5.0
    assert calculate_shadow_return_pct(100000.0, 0.0) is None

def test_shadow_pnl_summary():
    ctx = build_mock_shadow_simulation_context(100000.0)
    port = initialize_shadow_portfolio(ctx)
    pnl = build_shadow_pnl_snapshot(port, ctx.starting_equity_usd)
    s = shadow_pnl_summary([pnl])
    assert s["count"] == 1

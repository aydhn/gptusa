import pytest
from usa_signal_bot.paper_shadow.shadow_pnl_tracker import (
    build_shadow_pnl_snapshot,
    update_shadow_pnl_after_fills,
    calculate_shadow_return_pct,
    calculate_shadow_drawdown_pct,
    shadow_pnl_to_text
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio

def test_shadow_pnl_tracker():
    ctx = build_mock_shadow_simulation_context()
    port = initialize_shadow_portfolio(ctx)

    snap = build_shadow_pnl_snapshot(port, 100000.0)
    assert snap.total_pnl_usd == 0.0

    ret = calculate_shadow_return_pct(110000.0, 100000.0)
    assert ret == 10.0

    snap2 = build_shadow_pnl_snapshot(port, 100000.0)
    snap2.equity_usd = 90000.0
    dd = calculate_shadow_drawdown_pct([snap, snap2])
    assert dd == 10.0

    text = shadow_pnl_to_text([snap, snap2])
    assert "Shadow PnL Summary" in text

import pytest
from usa_signal_bot.backtesting.performance_attribution import (
    attribution_key_for_trade, build_attribution_by_dimension,
    build_full_attribution_report, attribution_report_to_text
)
from usa_signal_bot.core.enums import AttributionDimension, TradeStatus, TradeDirection, TradeExitReason
from usa_signal_bot.backtesting.trade_ledger import TradeLedger, BacktestTrade

def build_trade(sym, direction, pnl, bars=5, dt="2024-01-01"):
    return BacktestTrade(
        trade_id=f"TEST_{sym}_{dt}",
        signal_id="sig_1",
        strategy_name="TEST",
        symbol=sym,
        timeframe="1d",
        direction=direction,
        status=TradeStatus.CLOSED,
        entry_fill_id="f1",
        exit_fill_id="f2",
        entry_time_utc=dt,
        exit_time_utc=dt,
        entry_price=100.0,
        exit_price=100.0 + pnl,
        quantity=1.0,
        gross_pnl=pnl,
        net_pnl=pnl,
        total_fees=0.0,
        total_slippage_cost=0.0,
        return_pct=pnl/100.0,
        holding_bars=bars,
        holding_seconds=0,
        exit_reason=TradeExitReason.HOLD_PERIOD_EXIT
    )

def test_attribution_key_for_trade():
    t = build_trade("SPY", TradeDirection.LONG, 10, bars=3)
    assert attribution_key_for_trade(t, AttributionDimension.STRATEGY) == "TEST"
    assert attribution_key_for_trade(t, AttributionDimension.SYMBOL) == "SPY"
    assert attribution_key_for_trade(t, AttributionDimension.TIMEFRAME) == "1d"
    assert attribution_key_for_trade(t, AttributionDimension.ACTION) == "LONG"
    assert attribution_key_for_trade(t, AttributionDimension.MONTH) == "2024-01"
    assert attribution_key_for_trade(t, AttributionDimension.YEAR) == "2024"
    assert attribution_key_for_trade(t, AttributionDimension.HOLDING_PERIOD) == "2-5"

def test_build_attribution_by_dimension():
    ledger = TradeLedger(ledger_id="l1", trades=[], open_trades=[], closed_trades=[], created_at_utc="2024-01-01T00:00:00Z")
    ledger.trades = [
        build_trade("SPY", TradeDirection.LONG, 10),
        build_trade("SPY", TradeDirection.LONG, -5),
        build_trade("QQQ", TradeDirection.SHORT, 20)
    ]

    rows = build_attribution_by_dimension(ledger, AttributionDimension.SYMBOL)
    assert len(rows) == 2

    spy_row = next(r for r in rows if r.key == "SPY")
    assert spy_row.total_trades == 2
    assert spy_row.winning_trades == 1
    assert spy_row.losing_trades == 1
    assert spy_row.net_pnl == 5

    qqq_row = next(r for r in rows if r.key == "QQQ")
    assert qqq_row.total_trades == 1
    assert qqq_row.net_pnl == 20

def test_build_full_attribution_report():
    ledger = TradeLedger(ledger_id="l1", trades=[], open_trades=[], closed_trades=[], created_at_utc="2024-01-01T00:00:00Z")
    ledger.trades = [
        build_trade("SPY", TradeDirection.LONG, 10),
        build_trade("QQQ", TradeDirection.SHORT, 30)
    ] # Total PnL = 40

    rep = build_full_attribution_report(ledger)
    assert rep.total_net_pnl == 40.0

    # QQQ contribution = 30/40 = 75%
    qqq_row = next((r for r in rep.rows if r.dimension == AttributionDimension.SYMBOL and r.key == "QQQ"), None)
    assert qqq_row is not None
    assert qqq_row.contribution_pct == 75.0

    txt = attribution_report_to_text(rep)
    assert "75.0" in txt
    assert "SPY" in txt
    assert "QQQ" in txt

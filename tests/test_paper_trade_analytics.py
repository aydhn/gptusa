from usa_signal_bot.paper.paper_models import PaperTrade
from usa_signal_bot.core.enums import PaperTradeStatus, PaperMetricStatus
from usa_signal_bot.paper.paper_trade_analytics import (
    calculate_paper_trade_metrics,
    paper_trade_metrics_to_text
)

def test_paper_trade_analytics():
    trades = [
        PaperTrade(trade_id="1", symbol="A", status=PaperTradeStatus.CLOSED, net_pnl=10.0, account_id="acc", timeframe="1d", quantity=1.0, gross_pnl=10.0, total_fees=0.0, entry_time_utc="", entry_order_id="", exit_order_id="", entry_fill_id="", exit_fill_id="", entry_price=0.0, exit_price=0.0, return_pct=0.0, exit_time_utc="1"),
        PaperTrade(trade_id="2", symbol="B", status=PaperTradeStatus.CLOSED, net_pnl=-5.0, account_id="acc", timeframe="1d", quantity=1.0, gross_pnl=-5.0, total_fees=0.0, entry_time_utc="", entry_order_id="", exit_order_id="", entry_fill_id="", exit_fill_id="", entry_price=0.0, exit_price=0.0, return_pct=0.0, exit_time_utc="1"),
        PaperTrade(trade_id="3", symbol="C", status=PaperTradeStatus.CLOSED, net_pnl=15.0, account_id="acc", timeframe="1d", quantity=1.0, gross_pnl=15.0, total_fees=0.0, entry_time_utc="", entry_order_id="", exit_order_id="", entry_fill_id="", exit_fill_id="", entry_price=0.0, exit_price=0.0, return_pct=0.0, exit_time_utc="1"),
        PaperTrade(trade_id="4", symbol="D", status=PaperTradeStatus.OPEN, net_pnl=0.0, account_id="acc", timeframe="1d", quantity=1.0, gross_pnl=0.0, total_fees=0.0, entry_time_utc="", entry_order_id="", exit_order_id="", entry_fill_id="", exit_fill_id="", entry_price=0.0, exit_price=0.0, return_pct=0.0, exit_time_utc="")
    ]

    metrics = calculate_paper_trade_metrics(trades)
    assert metrics.status == PaperMetricStatus.OK
    assert metrics.total_trades == 4
    assert metrics.closed_trades == 3
    assert metrics.win_rate == 2/3
    assert metrics.gross_profit == 25.0
    assert metrics.gross_loss == 5.0
    assert metrics.profit_factor == 5.0
    assert metrics.net_pnl == 20.0

    txt = paper_trade_metrics_to_text(metrics)
    assert "Win Rate:" in txt

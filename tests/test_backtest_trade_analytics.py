import pytest
from usa_signal_bot.backtesting.trade_analytics import (
    TradeAnalytics, calculate_trade_analytics,
    calculate_strategy_trade_breakdown, calculate_symbol_trade_breakdown,
    trade_analytics_to_text
)
from usa_signal_bot.backtesting.trade_ledger import TradeLedger, BacktestTrade
from usa_signal_bot.core.enums import TradeDirection, TradeStatus, TradeExitReason

@pytest.fixture
def empty_ledger():
    return TradeLedger("l1", [], [], [], "now")

@pytest.fixture
def populated_ledger():
    t1 = BacktestTrade("1", "AAPL", "1d", TradeDirection.LONG, TradeStatus.CLOSED, None, None, None, None, 100.0, 110.0, 10.0, 100.0, 98.0, 2.0, 0.0, 0.1, 5, None, TradeExitReason.UNKNOWN, None, "stratA")
    t2 = BacktestTrade("2", "MSFT", "1d", TradeDirection.LONG, TradeStatus.CLOSED, None, None, None, None, 100.0, 90.0, 10.0, -100.0, -102.0, 2.0, 0.0, -0.1, 5, None, TradeExitReason.UNKNOWN, None, "stratA")
    t3 = BacktestTrade("3", "AAPL", "1d", TradeDirection.LONG, TradeStatus.CLOSED, None, None, None, None, 100.0, 120.0, 10.0, 200.0, 198.0, 2.0, 0.0, 0.2, 5, None, TradeExitReason.UNKNOWN, None, "stratB")
    return TradeLedger("l2", [t1, t2, t3], [], [t1, t2, t3], "now")

def test_empty_ledger_analytics(empty_ledger):
    ta = calculate_trade_analytics(empty_ledger)
    assert ta.total_trades == 0
    assert len(ta.warnings) == 1

def test_populated_ledger_analytics(populated_ledger):
    ta = calculate_trade_analytics(populated_ledger)
    assert ta.total_trades == 3
    assert ta.winning_trades == 2
    assert ta.losing_trades == 1
    assert ta.win_rate == 2/3
    assert ta.gross_profit == 296.0 # 98 + 198
    assert ta.gross_loss == -102.0
    assert ta.profit_factor == pytest.approx(296.0 / 102.0)
    assert ta.average_trade == pytest.approx((296 - 102) / 3)

def test_strategy_breakdown(populated_ledger):
    sb = calculate_strategy_trade_breakdown(populated_ledger)
    assert len(sb) == 2
    strat_a = next(s for s in sb if s.strategy_name == "stratA")
    assert strat_a.total_trades == 2
    assert strat_a.net_pnl == -4.0 # 98 - 102

def test_symbol_breakdown(populated_ledger):
    sb = calculate_symbol_trade_breakdown(populated_ledger)
    assert len(sb) == 2
    aapl = next(s for s in sb if s.symbol == "AAPL")
    assert aapl.total_trades == 2
    assert aapl.net_pnl == 296.0

def test_trade_analytics_to_text(populated_ledger):
    ta = calculate_trade_analytics(populated_ledger)
    txt = trade_analytics_to_text(ta)
    assert "Total Trades:  3" in txt
    assert "Win Rate:      66.7%" in txt

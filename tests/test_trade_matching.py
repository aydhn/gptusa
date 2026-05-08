import pytest
from usa_signal_bot.core.enums import MatchStatus
from usa_signal_bot.comparison.trade_matching import (
    match_paper_and_backtest_trades, calculate_trade_price_gap_pct,
    calculate_trade_return_gap_pct, matched_trades_to_text
)

def test_exact_match():
    p = [{"symbol": "AAPL", "trade_id": "pt1", "entry_price": 100.0, "timeframe": "1d", "strategy_name": "s1"}]
    b = [{"symbol": "AAPL", "id": "bt1", "entry_price": 101.0, "timeframe": "1d", "strategy_name": "s1"}]

    res = match_paper_and_backtest_trades(p, b)
    assert len(res) == 1
    assert res[0].match_status == MatchStatus.MATCHED
    assert res[0].symbol == "AAPL"
    assert res[0].price_gap_pct == -0.9900990099009901

def test_unmatched_trades():
    p = [{"symbol": "AAPL", "trade_id": "pt1"}]
    b = [{"symbol": "MSFT", "id": "bt1"}]

    res = match_paper_and_backtest_trades(p, b)
    assert len(res) == 2
    statuses = [r.match_status for r in res]
    assert MatchStatus.PAPER_ONLY in statuses
    assert MatchStatus.BACKTEST_ONLY in statuses

def test_gap_calculations():
    assert calculate_trade_price_gap_pct(105, 100) == 5.0
    assert calculate_trade_price_gap_pct(None, 100) is None
    assert calculate_trade_return_gap_pct(10, 5, 100) == 5.0

def test_text_output():
    p = [{"symbol": "AAPL", "trade_id": "pt1", "entry_price": 100.0}]
    b = [{"symbol": "AAPL", "id": "bt1", "entry_price": 101.0}]
    res = match_paper_and_backtest_trades(p, b)
    txt = matched_trades_to_text(res)
    assert "AAPL" in txt
    assert "MATCHED" in txt

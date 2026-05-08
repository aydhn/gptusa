import pytest
from usa_signal_bot.core.enums import MatchStatus
from usa_signal_bot.comparison.order_fill_matching import (
    match_order_fills, calculate_quantity_gap, calculate_fill_price_gap_pct,
    matched_order_fills_to_text
)

def test_match_fills_unmatched():
    # Current implementation is just a stub that returns unmatched pairs
    p_fills = [{"symbol": "AAPL", "quantity": 10, "fill_price": 100.0, "fees": 1.0}]
    b_fills = [{"symbol": "AAPL", "quantity": 10, "fill_price": 101.0, "fees": 0.5}]

    res = match_order_fills([], p_fills, [], b_fills)
    assert len(res) == 2

    statuses = [r.match_status for r in res]
    assert MatchStatus.PAPER_ONLY in statuses
    assert MatchStatus.BACKTEST_ONLY in statuses

def test_fill_gap_calculations():
    assert calculate_quantity_gap(10.0, 5.0) == 5.0
    assert calculate_fill_price_gap_pct(101.0, 100.0) == 1.0

def test_text_output():
    p_fills = [{"symbol": "AAPL", "fill_price": 100.0}]
    res = match_order_fills([], p_fills, [], [])
    txt = matched_order_fills_to_text(res)
    assert "PAPER_ONLY" in txt
    assert "AAPL" in txt

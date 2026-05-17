import pytest
from usa_signal_bot.portfolio_rebalance.portfolio_state import (
    build_empty_current_state,
    build_current_state_from_positions,
    build_current_state_from_paper_payload,
    current_state_symbol_map,
    current_portfolio_state_to_text
)

def test_empty_current_state():
    state = build_empty_current_state(100000.0)
    assert state.total_equity_usd == 100000.0
    assert state.gross_exposure_usd == 0.0
    assert state.net_exposure_usd == 0.0
    assert len(state.positions) == 0

def test_build_current_state_from_positions():
    positions = [
        {"symbol": "AAPL", "market_value_usd": 1000.0, "side": "LONG"},
        {"symbol": "MSFT", "market_value_usd": 500.0, "side": "SHORT"}
    ]
    state = build_current_state_from_positions(positions, total_equity_usd=10000.0)

    assert state.gross_exposure_usd == 1500.0
    assert state.net_exposure_usd == 500.0  # 1000 - 500
    assert len(state.positions) == 2
    assert state.positions[0].weight_pct_equity == 10.0
    assert state.positions[1].weight_pct_equity == 5.0

def test_build_current_state_from_paper_payload():
    payload = {
        "total_equity_usd": 50000.0,
        "cash_usd": 40000.0,
        "positions": [
            {"symbol": "TSLA", "market_value_usd": 10000.0, "side": "LONG"}
        ]
    }
    state = build_current_state_from_paper_payload(payload)
    assert state.total_equity_usd == 50000.0
    assert state.gross_exposure_usd == 10000.0
    assert len(state.positions) == 1
    assert state.positions[0].symbol == "TSLA"

def test_symbol_map():
    positions = [
        {"symbol": "AAPL", "market_value_usd": 1000.0, "side": "LONG"}
    ]
    state = build_current_state_from_positions(positions)
    smap = current_state_symbol_map(state)
    assert "AAPL" in smap
    assert smap["AAPL"].market_value_usd == 1000.0

def test_text_output():
    state = build_empty_current_state()
    text = current_portfolio_state_to_text(state)
    assert "Current Portfolio State:" in text
    assert "Total Equity:" in text

import pytest
from usa_signal_bot.portfolio_rebalance.target_extractor import (
    build_target_state_from_allocations,
    build_target_state_from_construction_plan,
    target_state_symbol_map,
    target_portfolio_state_to_text
)

def test_build_target_state_from_allocations():
    allocations = [
        {"symbol": "AAPL", "target_notional_usd": 2000.0, "side": "LONG", "status": "APPROVED"},
        {"symbol": "MSFT", "target_notional_usd": 1000.0, "side": "SHORT", "status": "APPROVED"},
        {"symbol": "TSLA", "target_notional_usd": 5000.0, "side": "LONG", "status": "BLOCKED"}
    ]
    state = build_target_state_from_allocations(allocations, total_equity_usd=10000.0)

    # TSLA should be excluded due to BLOCKED status
    assert len(state.target_positions) == 2
    assert state.target_gross_exposure_usd == 3000.0
    assert state.target_net_exposure_usd == 1000.0 # 2000 - 1000

    assert state.target_positions[0].weight_pct_equity == 20.0

def test_build_target_state_from_construction_plan():
    plan = {
        "plan_id": "plan_123",
        "capital_state": {"total_equity_usd": 20000.0},
        "final_allocations": [
            {"symbol": "GOOG", "target_notional_usd": 4000.0, "side": "LONG", "status": "APPROVED"}
        ]
    }
    state = build_target_state_from_construction_plan(plan)

    assert state.source_plan_id == "plan_123"
    assert state.total_equity_usd == 20000.0
    assert len(state.target_positions) == 1
    assert state.target_positions[0].weight_pct_equity == 20.0

def test_target_symbol_map():
    allocations = [
        {"symbol": "AAPL", "target_notional_usd": 2000.0, "side": "LONG", "status": "APPROVED"}
    ]
    state = build_target_state_from_allocations(allocations)
    smap = target_state_symbol_map(state)
    assert "AAPL" in smap
    assert smap["AAPL"].market_value_usd == 2000.0

def test_target_text_output():
    allocations = []
    state = build_target_state_from_allocations(allocations, 10000.0)
    text = target_portfolio_state_to_text(state)
    assert "Target Portfolio State:" in text
    assert "Target Gross Exposure: $0.00" in text

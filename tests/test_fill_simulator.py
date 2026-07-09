import pytest
from usa_signal_bot.core.enums import TransactionSide, FillSimulationStatus
from usa_signal_bot.transaction_costs.fill_simulator import simulate_fill_price, simulate_fill
from usa_signal_bot.transaction_costs.cost_models import TransactionCostBreakdown, create_transaction_cost_breakdown_id, FillSimulationRequest
from usa_signal_bot.core.enums import CostAdjustmentStatus, CostRealismStatus
from datetime import datetime

def test_buy_fill_price():
    p = simulate_fill_price("SPY", TransactionSide.BUY, 100.0, 50.0)
    assert p > 100.0

def test_sell_fill_price():
    p = simulate_fill_price("SPY", TransactionSide.SELL, 100.0, 50.0)
    assert p < 100.0

def test_simulate_fill():
    brk = TransactionCostBreakdown(
        breakdown_id=create_transaction_cost_breakdown_id("SPY"),
        symbol="SPY", created_at_utc=datetime.now().isoformat(),
        side=TransactionSide.BUY, notional_usd=1000.0, total_cost_bps=50.0,
        total_cost_usd=5.0, components_bps={}, components_usd={},
        status=CostAdjustmentStatus.APPLIED, realism_status=CostRealismStatus.CONSERVATIVE,
        warnings=[], errors=[], metadata={}
    )
    res = simulate_fill(
        FillSimulationRequest(
            symbol="SPY",
            side=TransactionSide.BUY,
            quantity=10,
            notional_usd=1000.0,
            reference_price=100.0,
            cost_breakdown=brk,
            market_impact=None
        )
    )
    assert res.simulated_fill_price > 100.0
    assert res.status == FillSimulationStatus.FILLED

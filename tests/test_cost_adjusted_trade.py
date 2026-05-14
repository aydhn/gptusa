import pytest
from usa_signal_bot.core.enums import TransactionSide
from usa_signal_bot.transaction_costs.cost_adjusted_trade import apply_costs_to_trade
from usa_signal_bot.transaction_costs.cost_models import TransactionCostBreakdown, create_transaction_cost_breakdown_id, FillSimulationResult, create_fill_simulation_id
from usa_signal_bot.core.enums import CostAdjustmentStatus, CostRealismStatus, FillSimulationStatus
from datetime import datetime

def test_apply_costs_to_trade():
    brk = TransactionCostBreakdown(
        breakdown_id=create_transaction_cost_breakdown_id("SPY"),
        symbol="SPY", created_at_utc=datetime.now().isoformat(),
        side=TransactionSide.BUY, notional_usd=1000.0, total_cost_bps=50.0,
        total_cost_usd=5.0, components_bps={}, components_usd={},
        status=CostAdjustmentStatus.APPLIED, realism_status=CostRealismStatus.CONSERVATIVE,
        warnings=[], errors=[], metadata={}
    )
    sim = FillSimulationResult(
        fill_id=create_fill_simulation_id("SPY"), symbol="SPY", created_at_utc=datetime.now().isoformat(),
        side=TransactionSide.BUY, requested_quantity=10, requested_notional_usd=1000.0,
        reference_price=100.0, simulated_fill_price=100.5, simulated_filled_quantity=10, simulated_filled_notional_usd=1005.0,
        status=FillSimulationStatus.FILLED, cost_breakdown=brk, market_impact=None, warnings=[], errors=[], metadata={}
    )

    res = apply_costs_to_trade("SPY", TransactionSide.BUY, 100.0, 10.0, 1000.0, sim)
    assert res.total_cost_usd == 5.0
    assert res.net_pnl_usd == 95.0
    assert res.net_return_pct == 9.5

import pytest
from usa_signal_bot.transaction_costs.signal_adapter import suppress_candidate_if_cost_too_high, attach_cost_estimate_to_signal
from usa_signal_bot.transaction_costs.cost_models import TransactionCostBreakdown, create_transaction_cost_breakdown_id
from usa_signal_bot.core.enums import TransactionSide, CostAdjustmentStatus, CostRealismStatus
from datetime import datetime

def test_signal_adapter_suppression():
    brk = TransactionCostBreakdown(
        breakdown_id=create_transaction_cost_breakdown_id("SPY"),
        symbol="SPY", created_at_utc=datetime.now().isoformat(),
        side=TransactionSide.BUY, notional_usd=1000.0, total_cost_bps=300.0,
        total_cost_usd=30.0, components_bps={}, components_usd={},
        status=CostAdjustmentStatus.APPLIED, realism_status=CostRealismStatus.CONSERVATIVE,
        warnings=[], errors=[], metadata={}
    )
    cand = {"symbol": "SPY"}
    res = suppress_candidate_if_cost_too_high(cand, brk, 250.0)
    assert res.get("suppressed_by_transaction_cost") is True

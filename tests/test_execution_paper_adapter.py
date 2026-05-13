from usa_signal_bot.execution.paper_adapter import (
    attach_execution_realism_to_paper_order,
    paper_fill_allowed_by_tradability
)
from usa_signal_bot.execution.liquidity_models import TradabilityGuardResult
from usa_signal_bot.core.enums import TradabilityStatus, ExecutionRiskLevel

def test_paper_adapter():
    res = TradabilityGuardResult(
        guard_id="id",
        symbol="SPY",
        created_at_utc="",
        status=TradabilityStatus.TRADABLE,
        risk_level=ExecutionRiskLevel.LOW,
        liquidity_profile=None,
        spread_estimate=None,
        slippage_estimate=None,
        reasons=[],
        recommended_guards=[]
    )
    order = {}
    order = attach_execution_realism_to_paper_order(order, res)
    assert order["metadata"]["tradability_status"] == "TRADABLE"

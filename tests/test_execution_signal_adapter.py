from usa_signal_bot.execution.signal_adapter import (
    attach_tradability_to_signal,
    attach_execution_realism_to_candidate,
    suppress_candidate_if_untradable
)
from usa_signal_bot.execution.liquidity_models import TradabilityGuardResult
from usa_signal_bot.core.enums import TradabilityStatus, ExecutionRiskLevel
import datetime

def test_signal_adapter():
    res = TradabilityGuardResult(
        guard_id="id",
        symbol="SPY",
        created_at_utc="",
        status=TradabilityStatus.BLOCK_SIGNAL,
        risk_level=ExecutionRiskLevel.CRITICAL,
        liquidity_profile=None,
        spread_estimate=None,
        slippage_estimate=None,
        reasons=[],
        recommended_guards=[]
    )

    sig = {}
    sig = attach_tradability_to_signal(sig, res)
    assert sig["metadata"]["tradability_status"] == "BLOCK_SIGNAL"
    assert sig["metadata"]["suppressed_by_execution_guard"] == True

    cand = {}
    cand = suppress_candidate_if_untradable(cand, res)
    assert cand["metadata"]["suppressed"] == True

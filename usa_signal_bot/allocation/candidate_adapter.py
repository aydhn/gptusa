from typing import Any, Dict, List
from usa_signal_bot.core.enums import PositionSizeStatus
from usa_signal_bot.allocation.allocation_models import SizingInput, PositionSizeResult, CapitalState, RiskBudget, create_sizing_input_id
from usa_signal_bot.allocation.adaptive_sizing_engine import AdaptiveSizingEngine

def sizing_input_from_candidate(candidate: Dict[str, Any]) -> SizingInput:
    return SizingInput(
        sizing_input_id=create_sizing_input_id(candidate.get("symbol", "UNKNOWN")),
        symbol=candidate.get("symbol", "UNKNOWN"),
        strategy_name=candidate.get("strategy", "UNKNOWN"),
        side=candidate.get("side"),
        reference_price=candidate.get("close"),
        signal_score=candidate.get("composite_score", candidate.get("score")),
        metadata={
            "liquidity": {"status": candidate.get("liquidity_status", "NORMAL")},
            "regime": {"regime_state": candidate.get("regime_state", "UNKNOWN")}
        }
    )

def attach_position_size_to_candidate(candidate: Dict[str, Any], result: PositionSizeResult) -> Dict[str, Any]:
    cand = dict(candidate)
    cand["recommended_local_notional_usd"] = result.final_notional_usd
    cand["recommended_local_quantity"] = result.final_quantity
    cand["position_size_status"] = result.status.value
    cand["risk_pct_equity"] = result.risk_pct_equity
    cand["sizing_adjustment_reasons"] = [a.reason.value for a in result.adjustments]
    cand["sizing_warnings"] = result.warnings
    cand["sizing_is_paper_only"] = True
    return cand

def apply_sizing_to_candidates(candidates: List[Dict[str, Any]], engine: AdaptiveSizingEngine, capital_state: CapitalState, risk_budget: RiskBudget) -> List[Dict[str, Any]]:
    sized_candidates = []
    for cand in candidates:
        inp = sizing_input_from_candidate(cand)
        res = engine.size_position(inp, capital_state, risk_budget)
        sized_cand = attach_position_size_to_candidate(cand, res)
        sized_cand = suppress_candidate_if_size_blocked(sized_cand, res)
        sized_candidates.append(sized_cand)
    return sized_candidates

def suppress_candidate_if_size_blocked(candidate: Dict[str, Any], result: PositionSizeResult) -> Dict[str, Any]:
    cand = dict(candidate)
    if result.status in [PositionSizeStatus.BLOCKED, PositionSizeStatus.SUPPRESSED]:
        cand["status"] = "SUPPRESSED"
        cand["suppression_reason"] = f"Sizing status is {result.status.value}"
    return cand

def candidate_sizing_summary(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_approved = 0
    total_blocked = 0
    total_notional = 0.0
    for cand in candidates:
        if cand.get("position_size_status") == PositionSizeStatus.APPROVED.value:
            total_approved += 1
        elif cand.get("position_size_status") in [PositionSizeStatus.BLOCKED.value, PositionSizeStatus.SUPPRESSED.value]:
            total_blocked += 1
        total_notional += cand.get("recommended_local_notional_usd", 0.0)

    return {
        "total_approved": total_approved,
        "total_blocked_suppressed": total_blocked,
        "total_recommended_notional_usd": total_notional
    }

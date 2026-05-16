from typing import Any, Dict, List
from usa_signal_bot.core.enums import PositionSizeStatus
from usa_signal_bot.allocation.allocation_models import PositionSizeResult, CapitalState, RiskBudget
from usa_signal_bot.allocation.adaptive_sizing_engine import AdaptiveSizingEngine
from usa_signal_bot.allocation.candidate_adapter import sizing_input_from_candidate

def apply_sizing_to_paper_order(order: Dict[str, Any], result: PositionSizeResult) -> Dict[str, Any]:
    p = dict(order)
    p["local_quantity"] = result.final_quantity
    p["local_notional_usd"] = result.final_notional_usd
    p["sizing_status"] = result.status.value
    p["sizing_warnings"] = result.warnings
    p["is_paper_only"] = True

    for bad_field in ["broker_order_id", "live_order_id", "sent_to_broker"]:
        p.pop(bad_field, None)

    return p

def apply_sizing_to_paper_candidate(candidate: Dict[str, Any], engine: AdaptiveSizingEngine, capital_state: CapitalState, risk_budget: RiskBudget) -> Dict[str, Any]:
    inp = sizing_input_from_candidate(candidate)
    res = engine.size_position(inp, capital_state, risk_budget)

    cand = dict(candidate)
    cand["paper_local_notional_usd"] = res.final_notional_usd
    cand["paper_local_quantity"] = res.final_quantity
    cand["paper_sizing_status"] = res.status.value
    cand["is_paper_allowed"] = paper_order_allowed_by_sizing(res)
    return cand

def paper_order_allowed_by_sizing(result: PositionSizeResult) -> bool:
    return result.status not in [PositionSizeStatus.BLOCKED, PositionSizeStatus.SUPPRESSED, PositionSizeStatus.INSUFFICIENT_DATA]

def paper_sizing_summary(orders_or_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    allowed = sum(1 for c in orders_or_candidates if c.get("is_paper_allowed", False) or c.get("sizing_status") == "APPROVED")
    return {
        "total_paper_allowed": allowed,
        "total_paper_items": len(orders_or_candidates)
    }

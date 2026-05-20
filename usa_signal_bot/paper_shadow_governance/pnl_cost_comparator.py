from typing import Any, Dict
from usa_signal_bot.core.enums import ShadowAcceptanceGateType, ShadowAcceptanceStatus
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceGate, create_shadow_acceptance_gate_id

def compare_shadow_pnl_cost(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> Dict[str, Any]:
    bm = baseline_payload.get("metrics", {})
    cm = candidate_payload.get("metrics", {})
    p_delta = cm.get("simulated_pnl_usd", 0.0) - bm.get("simulated_pnl_usd", 0.0)
    c_delta = cm.get("simulated_total_cost_usd", 0.0) - bm.get("simulated_total_cost_usd", 0.0)
    return {"pnl_delta": p_delta, "cost_delta": c_delta}

def compare_shadow_cost_regression(baseline_metrics: Dict[str, Any], candidate_metrics: Dict[str, Any]) -> ShadowAcceptanceGate:
    b = baseline_metrics.get("simulated_total_cost_usd", 0.0)
    c = candidate_metrics.get("simulated_total_cost_usd", 0.0)
    status = ShadowAcceptanceStatus.WARNING if c > b else ShadowAcceptanceStatus.PASS
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.COST_NOT_WORSE),
        gate_type=ShadowAcceptanceGateType.COST_NOT_WORSE,
        status=status,
        threshold=b,
        observed_value=c,
        description="Check if cost regressed",
        risk_flags=[], warnings=[], errors=[]
    )

def compare_shadow_pnl_regression(baseline_metrics: Dict[str, Any], candidate_metrics: Dict[str, Any]) -> ShadowAcceptanceGate:
    b = baseline_metrics.get("simulated_pnl_usd", 0.0)
    c = candidate_metrics.get("simulated_pnl_usd", 0.0)
    status = ShadowAcceptanceStatus.WARNING if c < b else ShadowAcceptanceStatus.PASS
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.PNL_NOT_WORSE),
        gate_type=ShadowAcceptanceGateType.PNL_NOT_WORSE,
        status=status,
        threshold=b,
        observed_value=c,
        description="Check if PnL regressed",
        risk_flags=[], warnings=[], errors=[]
    )

def compare_shadow_turnover_proxy(baseline_metrics: Dict[str, Any], candidate_metrics: Dict[str, Any]) -> ShadowAcceptanceGate:
    # Basic turnover proxy implementation
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.UNKNOWN),
        gate_type=ShadowAcceptanceGateType.UNKNOWN,
        status=ShadowAcceptanceStatus.PASS,
        threshold=0, observed_value=0, description="Turnover proxy",
        risk_flags=[], warnings=[], errors=[]
    )

def pnl_cost_comparator_to_text(payload: Dict[str, Any]) -> str:
    return str(payload)

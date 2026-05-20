from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowGovernanceRiskFlag

def compare_shadow_drawdown_delta(baseline_metrics: Dict[str, Any], candidate_metrics: Dict[str, Any]) -> Dict[str, Any]:
    b_dd = baseline_metrics.get("max_drawdown_pct", 0.0)
    c_dd = candidate_metrics.get("max_drawdown_pct", 0.0)
    return {"drawdown_delta": c_dd - b_dd}

def compare_shadow_exposure_delta(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> Dict[str, Any]:
    # Placeholder for actual exposure calculations
    return {"exposure_delta": 0.0}

def compare_shadow_blocked_intent_delta(baseline_metrics: Dict[str, Any], candidate_metrics: Dict[str, Any]) -> Dict[str, Any]:
    b_blk = baseline_metrics.get("blocked_intent_count", 0)
    c_blk = candidate_metrics.get("blocked_intent_count", 0)
    return {"blocked_delta": c_blk - b_blk}

def calculate_shadow_risk_delta(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> Dict[str, Any]:
    bm = baseline_payload.get("metrics", {})
    cm = candidate_payload.get("metrics", {})
    res = {}
    res.update(compare_shadow_drawdown_delta(bm, cm))
    res.update(compare_shadow_exposure_delta(baseline_payload, candidate_payload))
    res.update(compare_shadow_blocked_intent_delta(bm, cm))
    return res

def shadow_risk_delta_flags(delta: Dict[str, Any]) -> List[ShadowGovernanceRiskFlag]:
    flags = []
    if delta.get("drawdown_delta", 0) > 0.05:
        flags.append(ShadowGovernanceRiskFlag.RISK_REGRESSION)
    if delta.get("blocked_delta", 0) > 5:
        flags.append(ShadowGovernanceRiskFlag.BLOCKED_INTENTS_HIGH)
    return flags

def shadow_risk_delta_to_text(delta: Dict[str, Any]) -> str:
    return str(delta)

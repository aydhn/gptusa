from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowGovernanceRiskFlag

def count_shadow_safety_flags(payload: Dict[str, Any]) -> Dict[str, int]:
    flags = payload.get("safety_flags", [])
    counts = {}
    for f in flags:
        counts[f] = counts.get(f, 0) + 1
    return counts

def safety_flags_increased(baseline_flags: Dict[str, int], candidate_flags: Dict[str, int]) -> bool:
    b_total = sum(baseline_flags.values())
    c_total = sum(candidate_flags.values())
    return c_total > b_total

def calculate_shadow_safety_delta(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> Dict[str, Any]:
    b_flags = count_shadow_safety_flags(baseline_payload)
    c_flags = count_shadow_safety_flags(candidate_payload)
    return {
        "baseline_flags": b_flags,
        "candidate_flags": c_flags,
        "increased": safety_flags_increased(b_flags, c_flags)
    }

def shadow_safety_delta_risk_flags(delta: Dict[str, Any]) -> List[ShadowGovernanceRiskFlag]:
    flags = []
    c_flags = delta.get("candidate_flags", {})
    if "REAL_ORDER_RISK" in c_flags:
        flags.append(ShadowGovernanceRiskFlag.REAL_ORDER_RISK)
    if "PAPER_MUTATION_RISK" in c_flags:
        flags.append(ShadowGovernanceRiskFlag.PAPER_STATE_MUTATION_RISK)
    if delta.get("increased"):
        flags.append(ShadowGovernanceRiskFlag.SAFETY_FLAGS_INCREASED)
    return flags

def shadow_safety_delta_to_text(delta: Dict[str, Any]) -> str:
    return str(delta)

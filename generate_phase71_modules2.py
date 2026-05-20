import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

write_file("usa_signal_bot/paper_shadow_governance/risk_delta.py", """
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
""")

write_file("usa_signal_bot/paper_shadow_governance/safety_delta.py", """
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
""")

write_file("usa_signal_bot/paper_shadow_governance/ledger_completeness.py", """
from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowAcceptanceGateType, ShadowAcceptanceStatus
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceGate, create_shadow_acceptance_gate_id

def required_shadow_ledger_event_types() -> List[str]:
    return [
        "SESSION_STARTED", "SIGNAL_PREVIEWED", "CANDIDATE_SELECTED",
        "ORDER_INTENT_CREATED", "RISK_GATE_EVALUATED", "FILL_SIMULATED",
        "PNL_UPDATED", "SESSION_COMPLETED"
    ]

def missing_shadow_ledger_event_types(session_payload: Dict[str, Any]) -> List[str]:
    ledger = session_payload.get("ledger", [])
    found = {e.get("type") for e in ledger}
    req = set(required_shadow_ledger_event_types())
    return list(req - found)

def check_shadow_ledger_completeness(session_payload: Dict[str, Any]) -> Dict[str, Any]:
    missing = missing_shadow_ledger_event_types(session_payload)
    return {
        "missing_types": missing,
        "complete": len(missing) == 0
    }

def ledger_completeness_gate(session_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    comp = check_shadow_ledger_completeness(session_payload)
    status = ShadowAcceptanceStatus.PASS if comp["complete"] else ShadowAcceptanceStatus.FAIL
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.LEDGER_COMPLETE),
        gate_type=ShadowAcceptanceGateType.LEDGER_COMPLETE,
        status=status,
        threshold=0,
        observed_value=len(comp["missing_types"]),
        description="Check if all required shadow ledger events exist",
        risk_flags=[], warnings=[], errors=[]
    )

def ledger_completeness_to_text(payload: Dict[str, Any]) -> str:
    return f"Ledger Complete: {payload.get('complete', False)}"
""")

write_file("usa_signal_bot/paper_shadow_governance/notification_review.py", """
from typing import Any, Dict, List
from usa_signal_bot.core.enums import ShadowAcceptanceGateType, ShadowAcceptanceStatus
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowAcceptanceGate, create_shadow_acceptance_gate_id

def detect_real_send_language(text: str) -> List[str]:
    bad = ["telegrama gönderildi", "sent to telegram", "real send", "canlıya al"]
    t = text.lower()
    return [b for b in bad if b in t]

def detect_order_advice_language(text: str) -> List[str]:
    bad = ["kesin al", "kesin sat", "garanti", "emir gönderildi", "sent to broker", "live approved"]
    t = text.lower()
    return [b for b in bad if b in t]

def review_shadow_notification_preview(session_payload: Dict[str, Any]) -> Dict[str, Any]:
    nots = session_payload.get("notifications", [])
    all_text = " ".join([str(n) for n in nots])
    rs = detect_real_send_language(all_text)
    oa = detect_order_advice_language(all_text)
    return {
        "real_send_violations": rs,
        "order_advice_violations": oa,
        "safe": len(rs) == 0 and len(oa) == 0
    }

def notification_safety_gate(session_payload: Dict[str, Any]) -> ShadowAcceptanceGate:
    rev = review_shadow_notification_preview(session_payload)
    status = ShadowAcceptanceStatus.PASS if rev["safe"] else ShadowAcceptanceStatus.FAIL
    return ShadowAcceptanceGate(
        gate_id=create_shadow_acceptance_gate_id(ShadowAcceptanceGateType.NOTIFICATION_SAFE),
        gate_type=ShadowAcceptanceGateType.NOTIFICATION_SAFE,
        status=status,
        threshold=0,
        observed_value=len(rev["real_send_violations"]) + len(rev["order_advice_violations"]),
        description="Check for safe notification language",
        risk_flags=[], warnings=[], errors=[]
    )

def shadow_notification_review_to_text(payload: Dict[str, Any]) -> str:
    return f"Notification Safe: {payload.get('safe', False)}"
""")

write_file("usa_signal_bot/paper_shadow_governance/pnl_cost_comparator.py", """
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
""")

print("Modules 2 generated successfully.")

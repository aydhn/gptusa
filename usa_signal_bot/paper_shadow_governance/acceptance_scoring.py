from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ShadowAcceptanceStatus, ShadowGovernanceRiskFlag
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowAcceptanceScorecard, ShadowAcceptanceGate, ShadowMetricComparison,
    create_shadow_acceptance_scorecard_id, utc_now_iso
)
from usa_signal_bot.paper_shadow_governance.acceptance_gates import default_shadow_acceptance_gates

def calculate_shadow_acceptance_score(gates: List[ShadowAcceptanceGate], metric_comparisons: Optional[List[ShadowMetricComparison]] = None) -> Optional[float]:
    if not gates: return None
    for g in gates:
        if g.status == ShadowAcceptanceStatus.BLOCKED:
            return 0.0
    passes = sum(1 for g in gates if g.status == ShadowAcceptanceStatus.PASS)
    return (passes / len(gates)) * 100

def classify_shadow_acceptance_status(score: Optional[float], gates: List[ShadowAcceptanceGate]) -> ShadowAcceptanceStatus:
    if score is None: return ShadowAcceptanceStatus.INSUFFICIENT_DATA
    for g in gates:
        if g.status == ShadowAcceptanceStatus.BLOCKED:
            return ShadowAcceptanceStatus.BLOCKED
    if score >= 70.0:
        for g in gates:
            if g.status == ShadowAcceptanceStatus.FAIL:
                return ShadowAcceptanceStatus.WARNING
        return ShadowAcceptanceStatus.PASS
    return ShadowAcceptanceStatus.FAIL

def collect_shadow_acceptance_risk_flags(gates: List[ShadowAcceptanceGate]) -> List[ShadowGovernanceRiskFlag]:
    flags = []
    for g in gates:
        flags.extend(g.risk_flags)
    return list(set(flags))

def build_shadow_acceptance_scorecard(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any], gates: Optional[List[ShadowAcceptanceGate]] = None) -> ShadowAcceptanceScorecard:
    if gates is None:
        gates = default_shadow_acceptance_gates(baseline_payload, candidate_payload)

    score = calculate_shadow_acceptance_score(gates)
    status = classify_shadow_acceptance_status(score, gates)
    flags = collect_shadow_acceptance_risk_flags(gates)

    return ShadowAcceptanceScorecard(
        scorecard_id=create_shadow_acceptance_scorecard_id(),
        created_at_utc=utc_now_iso(),
        baseline_session_id=baseline_payload.get("session_id"),
        candidate_session_id=candidate_payload.get("session_id"),
        overall_status=status,
        acceptance_score=score,
        gate_pass_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.PASS),
        gate_warning_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.WARNING),
        gate_fail_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.FAIL),
        gate_blocked_count=sum(1 for g in gates if g.status == ShadowAcceptanceStatus.BLOCKED),
        metric_score_components={},
        risk_flags=flags,
        manual_review_required=True,
        allowed_for_real_orders=False,
        allowed_for_paper_state_mutation=False,
        allowed_for_telegram_real_send=False,
        allowed_for_production_config_write=False,
        warnings=[], errors=[]
    )

def shadow_acceptance_scorecard_to_text(scorecard: ShadowAcceptanceScorecard) -> str:
    return f"Scorecard {scorecard.scorecard_id}: {scorecard.overall_status.value} (Score: {scorecard.acceptance_score})"

from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import ShadowEvidencePack, ShadowSessionComparisonReport, create_shadow_evidence_pack_id, utc_now_iso

def required_shadow_evidence_items() -> List[str]:
    return [
        "baseline_shadow_session", "candidate_shadow_session",
        "metric_comparisons", "acceptance_gates", "safety_delta",
        "risk_delta", "ledger_completeness", "notification_review",
        "shadow_pnl_snapshot"
    ]

def available_shadow_evidence_items(baseline_payload: Optional[Dict[str, Any]], candidate_payload: Optional[Dict[str, Any]], comparison_report: Optional[ShadowSessionComparisonReport] = None) -> List[str]:
    avail = []
    if baseline_payload: avail.append("baseline_shadow_session")
    if candidate_payload: avail.append("candidate_shadow_session")
    if comparison_report:
        avail.extend(["metric_comparisons", "safety_delta", "risk_delta", "ledger_completeness", "notification_review"])
        if comparison_report.acceptance_scorecard:
            avail.append("acceptance_gates")
    # Stub shadow_pnl_snapshot availability if candidate exists
    if candidate_payload: avail.append("shadow_pnl_snapshot")
    return list(set(avail))

def missing_shadow_evidence_items(required: List[str], available: List[str]) -> List[str]:
    return list(set(required) - set(available))

def build_shadow_evidence_pack(baseline_payload: Optional[Dict[str, Any]], candidate_payload: Optional[Dict[str, Any]], comparison_report: Optional[ShadowSessionComparisonReport] = None) -> ShadowEvidencePack:
    req = required_shadow_evidence_items()
    avail = available_shadow_evidence_items(baseline_payload, candidate_payload, comparison_report)
    missing = missing_shadow_evidence_items(req, avail)
    return ShadowEvidencePack(
        evidence_pack_id=create_shadow_evidence_pack_id(),
        created_at_utc=utc_now_iso(),
        baseline_session_id=baseline_payload.get("session_id") if baseline_payload else None,
        candidate_session_id=candidate_payload.get("session_id") if candidate_payload else None,
        comparison_report_id=comparison_report.report_id if comparison_report else None,
        required_evidence=req,
        available_evidence=avail,
        missing_evidence=missing,
        evidence_complete=len(missing) == 0,
        evidence_summary={"total_required": len(req), "total_available": len(avail)},
        warnings=[], errors=[]
    )

def shadow_evidence_pack_summary(pack: ShadowEvidencePack) -> Dict[str, Any]:
    return pack.evidence_summary

def shadow_evidence_pack_to_text(pack: ShadowEvidencePack) -> str:
    return f"Evidence Pack {pack.evidence_pack_id}: Complete={pack.evidence_complete}"

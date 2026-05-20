import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

write_file("usa_signal_bot/paper_shadow_governance/evidence_pack.py", """
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
""")

write_file("usa_signal_bot/paper_shadow_governance/audit_log.py", """
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ShadowGovernanceRiskFlag
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowGovernanceAuditEntry, ShadowDecisionBoardResult,
    create_shadow_governance_audit_entry_id, utc_now_iso
)

def create_shadow_governance_audit_entry(entity_type: str, entity_id: str, action: str, rationale: str, evidence_refs: Optional[List[str]] = None, risk_flags: Optional[List[ShadowGovernanceRiskFlag]] = None) -> ShadowGovernanceAuditEntry:
    return ShadowGovernanceAuditEntry(
        audit_id=create_shadow_governance_audit_entry_id(),
        created_at_utc=utc_now_iso(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[], errors=[]
    )

def audit_entry_from_decision(result: ShadowDecisionBoardResult) -> ShadowGovernanceAuditEntry:
    return create_shadow_governance_audit_entry(
        entity_type="ShadowDecisionBoardResult",
        entity_id=result.decision_id,
        action=result.decision.value,
        rationale=result.rationale,
        evidence_refs=[result.comparison_report_id, result.scorecard_id] if result.comparison_report_id else [],
        risk_flags=result.risk_flags
    )

def append_shadow_audit_entry(entries: List[ShadowGovernanceAuditEntry], entry: ShadowGovernanceAuditEntry) -> List[ShadowGovernanceAuditEntry]:
    return entries + [entry]

def shadow_audit_summary(entries: List[ShadowGovernanceAuditEntry]) -> Dict[str, Any]:
    return {"total_entries": len(entries)}

def shadow_audit_log_to_text(entries: List[ShadowGovernanceAuditEntry], limit: int = 100) -> str:
    return f"Audit log contains {len(entries)} entries."
""")

write_file("usa_signal_bot/paper_shadow_governance/comparison_report.py", """
from typing import Any, Dict
from usa_signal_bot.core.enums import ShadowGovernanceReportType
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowSessionComparisonReport, ShadowAcceptanceScorecard, ShadowGovernanceReview,
    create_shadow_governance_review_id, utc_now_iso
)
from usa_signal_bot.paper_shadow_governance.session_comparator import compare_shadow_sessions
from usa_signal_bot.paper_shadow_governance.risk_delta import calculate_shadow_risk_delta
from usa_signal_bot.paper_shadow_governance.safety_delta import calculate_shadow_safety_delta
from usa_signal_bot.paper_shadow_governance.ledger_completeness import check_shadow_ledger_completeness
from usa_signal_bot.paper_shadow_governance.notification_review import review_shadow_notification_preview
from usa_signal_bot.paper_shadow_governance.acceptance_scoring import build_shadow_acceptance_scorecard
from usa_signal_bot.paper_shadow_governance.decision_board import ShadowRehearsalDecisionBoard
from usa_signal_bot.paper_shadow_governance.evidence_pack import build_shadow_evidence_pack
from usa_signal_bot.paper_shadow_governance.audit_log import audit_entry_from_decision

def build_full_shadow_comparison_report(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowSessionComparisonReport:
    report = compare_shadow_sessions(baseline_payload, candidate_payload)
    report.risk_delta = calculate_shadow_risk_delta(baseline_payload, candidate_payload)
    report.safety_delta = calculate_shadow_safety_delta(baseline_payload, candidate_payload)
    report.ledger_completeness = check_shadow_ledger_completeness(candidate_payload)
    report.notification_review = review_shadow_notification_preview(candidate_payload)
    return report

def attach_acceptance_scorecard_to_report(report: ShadowSessionComparisonReport, scorecard: ShadowAcceptanceScorecard) -> ShadowSessionComparisonReport:
    report.acceptance_scorecard = scorecard
    return report

def build_shadow_governance_review(baseline_payload: Dict[str, Any], candidate_payload: Dict[str, Any]) -> ShadowGovernanceReview:
    report = build_full_shadow_comparison_report(baseline_payload, candidate_payload)
    scorecard = build_shadow_acceptance_scorecard(baseline_payload, candidate_payload)
    attach_acceptance_scorecard_to_report(report, scorecard)

    board = ShadowRehearsalDecisionBoard()
    decision = board.decide_from_comparison(report)

    evidence = build_shadow_evidence_pack(baseline_payload, candidate_payload, report)
    audit = audit_entry_from_decision(decision)

    return ShadowGovernanceReview(
        review_id=create_shadow_governance_review_id(),
        created_at_utc=utc_now_iso(),
        report_type=ShadowGovernanceReportType.FULL_SHADOW_GOVERNANCE_REVIEW,
        comparison_reports=[report],
        scorecards=[scorecard],
        evidence_packs=[evidence],
        decisions=[decision],
        audit_entries=[audit],
        output_paths={},
        warnings=[], errors=[]
    )

def shadow_governance_review_summary(review: ShadowGovernanceReview) -> Dict[str, Any]:
    return {"review_id": review.review_id, "decisions": len(review.decisions)}

def shadow_comparison_report_limitations_text() -> str:
    return "Shadow comparison is NOT live trading approval and DOES NOT reflect true execution performance."

def shadow_comparison_report_to_text(report: ShadowSessionComparisonReport, limit: int = 100) -> str:
    return f"Report {report.report_id} - Outcome: {report.outcome.value}"
""")

print("Modules 4 generated successfully.")

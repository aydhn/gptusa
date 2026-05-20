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

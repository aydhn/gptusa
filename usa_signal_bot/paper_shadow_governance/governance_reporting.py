from typing import Any, Dict
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowMetricComparison, ShadowAcceptanceGate, ShadowAcceptanceScorecard,
    ShadowSessionComparisonReport, ShadowEvidencePack, ShadowDecisionBoardResult,
    ShadowGovernanceAuditEntry, ShadowGovernanceReview
)

def shadow_metric_comparison_to_text(item: ShadowMetricComparison) -> str:
    return f"{item.metric_name}: {item.baseline_value} -> {item.candidate_value} ({item.direction.value})"

def shadow_acceptance_gate_to_text(item: ShadowAcceptanceGate) -> str:
    return f"Gate {item.gate_type.value}: {item.status.value}"

def shadow_acceptance_scorecard_to_text(item: ShadowAcceptanceScorecard) -> str:
    return f"Scorecard: {item.overall_status.value} (Score: {item.acceptance_score})"

def shadow_session_comparison_report_to_text(item: ShadowSessionComparisonReport, limit: int = 100) -> str:
    return f"Comparison Report: Outcome={item.outcome.value}"

def shadow_evidence_pack_to_text(item: ShadowEvidencePack) -> str:
    return f"Evidence Pack: Complete={item.evidence_complete}"

def shadow_decision_board_result_to_text(item: ShadowDecisionBoardResult) -> str:
    return f"Decision: {item.decision.value}"

def shadow_governance_audit_entry_to_text(item: ShadowGovernanceAuditEntry) -> str:
    return f"Audit: {item.action} on {item.entity_type}"

def shadow_governance_review_to_text(item: ShadowGovernanceReview, limit: int = 100) -> str:
    return f"Governance Review {item.review_id}: {len(item.decisions)} decisions."

def shadow_governance_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return str(summary)

def shadow_governance_limitations_text() -> str:
    return (
        "LIMITATIONS:\n"
        "- Shadow governance is a local simulation governance only.\n"
        "- Shadow PnL is not real portfolio performance.\n"
        "- Acceptance scores are NOT investment advice.\n"
        "- Decisions do NOT constitute paper/live/demo trading approval.\n"
        "- No broker API calls, real orders, or paper mutations are executed."
    )

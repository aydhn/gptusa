from typing import Any
from usa_signal_bot.research_governance.governance_models import (
    GovernanceEvidencePack, GovernanceChecklistItem, PromotionReview,
    ReleaseCandidatePackage, DecisionBoardResult, PromotionDecisionLogEntry,
    GovernanceAuditTrail, GovernanceReview
)

def evidence_pack_to_text(item: GovernanceEvidencePack) -> str:
    return f"Evidence Pack {item.evidence_pack_id}"

def governance_checklist_item_to_text(item: GovernanceChecklistItem) -> str:
    return f"Checklist {item.name}: {item.status.value}"

def promotion_review_to_text(item: PromotionReview) -> str:
    return f"Promotion Review {item.review_id}: {item.proposed_decision.value}"

def release_candidate_to_text(item: ReleaseCandidatePackage) -> str:
    return f"Release Candidate {item.candidate_id}: {item.status.value}"

def decision_board_result_to_text(item: DecisionBoardResult) -> str:
    return f"Decision Board {item.board_result_id}: {item.final_decision.value}"

def promotion_decision_log_entry_to_text(item: PromotionDecisionLogEntry) -> str:
    return f"Log {item.entry_id}: {item.decision.value}"

def governance_audit_trail_to_text(item: GovernanceAuditTrail) -> str:
    return f"Audit Trail {item.audit_id}"

def governance_review_to_text(item: GovernanceReview, limit: int = 100) -> str:
    return "Governance Review Summary\n- No broker/live/demo order\n- No auto promotion\n- No production config patch"

def governance_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"

def governance_limitations_text() -> str:
    return "Governance is local research metadata. Candidate result does not guarantee future performance. PASS is not live approval."

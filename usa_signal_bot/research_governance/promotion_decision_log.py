from typing import Optional, Any
from datetime import datetime
from usa_signal_bot.research_governance.governance_models import (
    PromotionDecision, GovernanceRiskFlag, PromotionDecisionLogEntry, DecisionBoardResult,
    create_promotion_decision_log_entry_id
)

def create_promotion_decision_log_entry(
    entity_type: str, entity_id: str, decision: PromotionDecision, rationale: str,
    evidence_refs: Optional[list[str]] = None, risk_flags: Optional[list[GovernanceRiskFlag]] = None,
    made_by: str = "local_governance_board"
) -> PromotionDecisionLogEntry:
    return PromotionDecisionLogEntry(
        entry_id=create_promotion_decision_log_entry_id(),
        created_at_utc=datetime.utcnow().isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        made_by=made_by,
        warnings=[], errors=[]
    )

def decision_log_from_board_result(result: DecisionBoardResult) -> PromotionDecisionLogEntry:
    return create_promotion_decision_log_entry(
        entity_type="DecisionBoardResult",
        entity_id=result.board_result_id,
        decision=result.final_decision,
        rationale=result.rationale,
        evidence_refs=[result.review_id] if result.review_id else [],
        risk_flags=result.risk_flags
    )

def append_promotion_decision_log(entries: list[PromotionDecisionLogEntry], entry: PromotionDecisionLogEntry) -> list[PromotionDecisionLogEntry]:
    entries.append(entry)
    return entries

def promotion_decision_log_summary(entries: list[PromotionDecisionLogEntry]) -> dict[str, Any]:
    return {"count": len(entries)}

def promotion_decision_log_to_text(entries: list[PromotionDecisionLogEntry], limit: int = 100) -> str:
    return "Promotion Decision Logs"

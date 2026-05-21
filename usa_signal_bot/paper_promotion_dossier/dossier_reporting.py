from typing import Any, Dict, List
from .dossier_models import (
    PromotionEvidenceIndex,
    ObserverPromotionDossier,
    FinalSafetyBoardGate,
    PromotionRiskRegisterItem,
    FinalSafetyBoardReview,
    ReadinessStagePlan,
    StagedPaperReadinessPackage,
    PromotionDossierAuditEntry,
    PromotionDossierReview
)

def promotion_evidence_index_to_text(item: PromotionEvidenceIndex) -> str:
    return f"Evidence Index {item.evidence_index_id}. Score: {item.evidence_score}."

def observer_promotion_dossier_to_text(item: ObserverPromotionDossier) -> str:
    return f"Dossier {item.dossier_id}. Status: {item.status.value}."

def final_safety_board_gate_to_text(item: FinalSafetyBoardGate) -> str:
    return f"Gate {item.gate_name}: {item.status.value}."

def promotion_risk_register_item_to_text(item: PromotionRiskRegisterItem) -> str:
    return f"Risk {item.risk_flag.value}. Severity: {item.severity}."

def final_safety_board_review_to_text(item: FinalSafetyBoardReview, limit: int = 100) -> str:
    return f"Safety Board {item.board_review_id}. Decision: {item.decision.value}."

def readiness_stage_plan_to_text(item: ReadinessStagePlan) -> str:
    return f"Stage Plan {item.stage.value}. Execution Enabled: {item.execution_enabled}."

def staged_paper_readiness_package_to_text(item: StagedPaperReadinessPackage, limit: int = 100) -> str:
    return f"Package {item.package_id}. Status: {item.status.value}."

def promotion_dossier_audit_entry_to_text(item: PromotionDossierAuditEntry) -> str:
    return f"Audit {item.entity_type} {item.action}: {item.decision}."

def promotion_dossier_review_to_text(item: PromotionDossierReview, limit: int = 100) -> str:
    return f"Review {item.review_id}. Dossiers: {len(item.dossiers)}."

def promotion_dossier_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store Summary: {summary}"

def promotion_dossier_limitations_text() -> str:
    from .dossier_report import promotion_dossier_limitations_text as inner
    return inner()

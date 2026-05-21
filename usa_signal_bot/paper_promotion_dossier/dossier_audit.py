from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.core.enums import PromotionDossierRiskFlag
from .dossier_models import (
    PromotionDossierAuditEntry,
    create_promotion_dossier_audit_id,
    ObserverPromotionDossier,
    FinalSafetyBoardReview,
    StagedPaperReadinessPackage
)

def create_promotion_dossier_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[PromotionDossierRiskFlag]] = None
) -> PromotionDossierAuditEntry:
    return PromotionDossierAuditEntry(
        audit_id=create_promotion_dossier_audit_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[]
    )

def audit_entry_from_dossier(dossier: ObserverPromotionDossier) -> PromotionDossierAuditEntry:
    return create_promotion_dossier_audit_entry(
        entity_type="ObserverPromotionDossier",
        entity_id=dossier.dossier_id,
        action="DOSSIER_CREATED",
        rationale="Automated dossier generation based on observer governance.",
        decision=dossier.decision.value,
        evidence_refs=dossier.evidence_index.evidence_refs if dossier.evidence_index else [],
        risk_flags=dossier.safety_flags
    )

def audit_entry_from_board_review(board: FinalSafetyBoardReview) -> PromotionDossierAuditEntry:
    return create_promotion_dossier_audit_entry(
        entity_type="FinalSafetyBoardReview",
        entity_id=board.board_review_id,
        action="BOARD_REVIEWED",
        rationale=board.rationale,
        decision=board.decision.value,
        evidence_refs=[],
        risk_flags=[]
    )

def audit_entry_from_readiness_package(package: StagedPaperReadinessPackage) -> PromotionDossierAuditEntry:
    return create_promotion_dossier_audit_entry(
        entity_type="StagedPaperReadinessPackage",
        entity_id=package.package_id,
        action="PACKAGE_CREATED",
        rationale="Staged non-executing readiness package generated.",
        decision=package.status.value,
        evidence_refs=package.evidence_refs,
        risk_flags=package.safety_flags
    )

def append_promotion_dossier_audit_entry(entries: List[PromotionDossierAuditEntry], entry: PromotionDossierAuditEntry) -> List[PromotionDossierAuditEntry]:
    entries.append(entry)
    return entries

def promotion_dossier_audit_summary(entries: List[PromotionDossierAuditEntry]) -> Dict[str, Any]:
    return {
        "total_entries": len(entries),
        "actions": list(set(e.action for e in entries))
    }

def promotion_dossier_audit_to_text(entries: List[PromotionDossierAuditEntry], limit: int = 100) -> str:
    lines = [f"Audit Log ({len(entries)} entries):"]
    for e in entries[:limit]:
        lines.append(f"[{e.created_at_utc}] {e.entity_type} {e.entity_id}: {e.action} - {e.decision}")
    return "\n".join(lines)

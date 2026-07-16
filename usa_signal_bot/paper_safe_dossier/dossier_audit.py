from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_safe_dossier.paper_safe_dossier_models import (
    PaperSafeDossierAuditEntry, create_paper_safe_dossier_audit_id,
    PaperSafeGateDossier, NonExecutionAcceptanceSeal, PrePaperLocalRuntimeMap
)
from usa_signal_bot.core.enums import PaperSafeDossierRiskFlag

def utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class PaperSafeDossierAuditParams:
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    decision: Optional[str] = None
    evidence_refs: Optional[List[str]] = None
    risk_flags: Optional[List[PaperSafeDossierRiskFlag]] = None


def create_paper_safe_dossier_audit_entry(params: PaperSafeDossierAuditParams) -> PaperSafeDossierAuditEntry:
    return PaperSafeDossierAuditEntry(
        audit_id=create_paper_safe_dossier_audit_id(),
        created_at_utc=utcnow_iso(),
        entity_type=params.entity_type,
        entity_id=params.entity_id,
        action=params.action,
        decision=params.decision,
        rationale=params.rationale,
        evidence_refs=params.evidence_refs or [],
        risk_flags=params.risk_flags or [],
        warnings=[],
        errors=[]
    )

def audit_entry_from_paper_safe_dossier(dossier: PaperSafeGateDossier) -> PaperSafeDossierAuditEntry:
    return create_paper_safe_dossier_audit_entry(PaperSafeDossierAuditParams(
        entity_type="PaperSafeGateDossier",
        entity_id=dossier.dossier_id,
        action="CREATE_DOSSIER",
        rationale="Automated generation of paper safe gate dossier.",
        decision=dossier.decision.value if dossier.decision else None,
        evidence_refs=dossier.evidence_refs,
        risk_flags=dossier.safety_flags
    ))

def audit_entry_from_non_execution_seal(seal: NonExecutionAcceptanceSeal) -> PaperSafeDossierAuditEntry:
    return create_paper_safe_dossier_audit_entry(PaperSafeDossierAuditParams(
        entity_type="NonExecutionAcceptanceSeal",
        entity_id=seal.seal_id,
        action="CREATE_SEAL",
        rationale="Automated generation of non-execution acceptance seal.",
        decision=seal.decision.value if seal.decision else None,
        evidence_refs=[],
        risk_flags=seal.risk_flags
    ))

def audit_entry_from_runtime_map(runtime_map: PrePaperLocalRuntimeMap) -> PaperSafeDossierAuditEntry:
    return create_paper_safe_dossier_audit_entry(PaperSafeDossierAuditParams(
        entity_type="PrePaperLocalRuntimeMap",
        entity_id=runtime_map.runtime_map_id,
        action="CREATE_RUNTIME_MAP",
        rationale="Automated generation of pre-paper local runtime map.",
        decision=runtime_map.decision.value if runtime_map.decision else None,
        evidence_refs=[],
        risk_flags=runtime_map.risk_flags
    ))

def append_paper_safe_dossier_audit_entry(entries: List[PaperSafeDossierAuditEntry], entry: PaperSafeDossierAuditEntry) -> List[PaperSafeDossierAuditEntry]:
    entries.append(entry)
    return entries

def paper_safe_dossier_audit_summary(entries: List[PaperSafeDossierAuditEntry]) -> Dict[str, Any]:
    return {
        "total": len(entries),
        "actions": list(set(e.action for e in entries))
    }

def paper_safe_dossier_audit_to_text(entries: List[PaperSafeDossierAuditEntry], limit: int = 100) -> str:
    lines = [f"Audit Entries: {len(entries)}"]
    for i, e in enumerate(entries[:limit]):
        lines.append(f" - {e.created_at_utc} | {e.entity_type} {e.entity_id} | {e.action} -> {e.decision}")
    if len(entries) > limit:
         lines.append(f" - ... and {len(entries)-limit} more.")
    return "\n".join(lines)

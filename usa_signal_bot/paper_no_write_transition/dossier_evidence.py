from typing import Any, Optional
import datetime
from usa_signal_bot.core.enums import TransitionDossierEvidenceStatus, NoWriteTransitionRiskFlag
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    TransitionDossierEvidenceItem,
    create_transition_evidence_id
)

def required_transition_dossier_evidence_types() -> list[str]:
    return [
        "admission_review_full_report",
        "paper_mode_admission_review",
        "ledger_reconciliation",
        "admission_evidence_seal",
        "final_no_write_transition_checkpoint",
        "dry_admission_full_review",
        "dry_admission_run",
        "write_lock_refresh",
        "human_approval_ledger",
        "no_write_admission_full_review",
        "no_write_contract",
        "paper_readiness_board_review",
        "validation_reports",
        "audit_trails"
    ]

def evidence_item_from_admission_source(
    evidence_type: str,
    source: Optional[Any],
    source_ref_id: Optional[str] = None,
    source_path: Optional[str] = None
) -> TransitionDossierEvidenceItem:

    available = source is not None
    required = evidence_type in required_transition_dossier_evidence_types()

    if available:
        status = TransitionDossierEvidenceStatus.FRESH
        fresh = True
        stale = False
    else:
        status = TransitionDossierEvidenceStatus.MISSING
        fresh = False
        stale = False

    return TransitionDossierEvidenceItem(
        evidence_id=create_transition_evidence_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        evidence_type=evidence_type,
        source_ref_id=source_ref_id,
        source_path=source_path,
        status=status,
        required=required,
        available=available,
        fresh=fresh,
        stale=stale,
        summary={},
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def collect_transition_dossier_evidence(admission_payload: dict[str, Any]) -> list[TransitionDossierEvidenceItem]:
    items = []

    # We mock out extraction of all required types based on their presence in the payload
    # For now, just generate ones that are strictly keys in the payload
    for e_type in required_transition_dossier_evidence_types():
        # A real implementation would parse deep within the admission payload tree
        # e.g., admission_payload.get("reports", {}).get(e_type)
        # Here we just look for exact keys or assume MISSING for now if not present
        source = admission_payload.get(e_type)
        items.append(evidence_item_from_admission_source(e_type, source))

    return items

def transition_evidence_missing_types(items: list[TransitionDossierEvidenceItem]) -> list[str]:
    return [item.evidence_type for item in items if item.required and not item.available]

def transition_evidence_stale_types(items: list[TransitionDossierEvidenceItem]) -> list[str]:
    return [item.evidence_type for item in items if item.stale]

def transition_evidence_score(items: list[TransitionDossierEvidenceItem]) -> Optional[float]:
    if not items:
        return None
    available = sum(1 for i in items if i.available)
    return (available / len(items)) * 100.0

def transition_evidence_summary(items: list[TransitionDossierEvidenceItem]) -> dict[str, Any]:
    return {
        "total": len(items),
        "available": sum(1 for i in items if i.available),
        "missing": len(transition_evidence_missing_types(items)),
        "stale": len(transition_evidence_stale_types(items)),
        "score": transition_evidence_score(items)
    }

def dossier_evidence_to_text(items: list[TransitionDossierEvidenceItem], limit: int = 100) -> str:
    lines = [f"Dossier Evidence Summary (Score: {transition_evidence_score(items)}%):"]
    for i, item in enumerate(items[:limit]):
        lines.append(f"  - {item.evidence_type}: {item.status.value}")
    return "\n".join(lines)

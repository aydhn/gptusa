from typing import Any
import datetime

from usa_signal_bot.core.enums import DryAdmissionDossierReportType
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_models import (
    DryAdmissionDossierFullReview,
    DryAdmissionGateDossier,
    DryAdmissionAcceptanceSeal,
    PaperModeRehearsalBlockerEvent,
    create_dry_admission_dossier_full_review_id
)
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier import build_dry_admission_gate_dossier
from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_audit import audit_entry_from_dry_admission_dossier, audit_entry_from_dry_admission_acceptance_seal, audit_entry_from_rehearsal_blocker_events

def dry_admission_dossier_limitations_text() -> str:
    return (
        "Dry-Admission Dossier Limitations:
"
        "- No broker/live/demo order.
"
        "- No active paper enable.
"
        "- No paper admission.
"
        "- No shadow launch.
"
        "- No paper-mode launch.
"
        "- No rehearsal.
"
        "- No real paper mutation.
"
        "- No paper order.
"
        "- No Telegram real send.
"
        "- No production config patch.
"
        "- Dry-admission dossier is not activation.
"
        "- Dry-admission acceptance seal is metadata-only.
"
        "- Rehearsal blocker denies rehearsal.
"
        "- Not investment advice.
"
    )

def build_dry_admission_dossier_full_review(payload: dict[str, Any]) -> DryAdmissionDossierFullReview:
    dossier = build_dry_admission_gate_dossier(payload)
    return build_dry_admission_dossier_review_from_parts(
        dossier=dossier,
        seal=dossier.acceptance_seal,
        blocker_events=dossier.rehearsal_blocker_events
    )

def build_dry_admission_dossier_review_from_parts(
    dossier: DryAdmissionGateDossier,
    seal: DryAdmissionAcceptanceSeal | None = None,
    blocker_events: list[PaperModeRehearsalBlockerEvent] | None = None
) -> DryAdmissionDossierFullReview:
    now = datetime.datetime.utcnow().isoformat() + "Z"

    audits = [audit_entry_from_dry_admission_dossier(dossier)]
    if seal:
        audits.append(audit_entry_from_dry_admission_acceptance_seal(seal))
    if blocker_events:
        audits.append(audit_entry_from_rehearsal_blocker_events(blocker_events))

    return DryAdmissionDossierFullReview(
        review_id=create_dry_admission_dossier_full_review_id(),
        created_at_utc=now,
        report_type=DryAdmissionDossierReportType.FULL_DRY_ADMISSION_DOSSIER_REVIEW,
        dossiers=[dossier],
        evidence_items=dossier.evidence_items,
        acceptance_seals=[seal] if seal else [],
        rehearsal_blocker_rules=[],
        rehearsal_blocker_events=blocker_events or [],
        audit_entries=audits,
        output_paths={},
        warnings=[],
        errors=[]
    )

def dry_admission_dossier_full_review_summary(review: DryAdmissionDossierFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "dossiers": len(review.dossiers),
        "seals": len(review.acceptance_seals),
        "blocker_events": len(review.rehearsal_blocker_events),
        "audits": len(review.audit_entries)
    }

def dry_admission_dossier_full_review_to_text(review: DryAdmissionDossierFullReview, limit: int = 100) -> str:
    summary = dry_admission_dossier_full_review_summary(review)
    return f"Dry-Admission Full Review [{review.review_id}]: Dossiers={summary['dossiers']}, Seals={summary['seals']}, Events={summary['blocker_events']}"

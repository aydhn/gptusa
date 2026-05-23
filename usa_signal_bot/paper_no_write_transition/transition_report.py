from typing import Any, Optional
import datetime
from usa_signal_bot.core.enums import NoWriteTransitionReportType
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionFullReview,
    NoWriteTransitionDossier,
    AdmissionEvidenceSealValidation,
    AdmissionEvidenceSealRefresh,
    PaperSandboxBridgeEnvelope,
    create_transition_full_review_id
)

def no_write_transition_limitations_text() -> str:
    return """
LIMITATIONS & DISCLAIMERS:
- The No-Write Transition Dossier is a local metadata collection ONLY.
- It is NOT an active paper deployment.
- It is NOT a live trading approval.
- No broker orders will be sent.
- No real paper state mutation will occur.
- No Telegram messages will be sent to real channels.
- No production configurations will be patched.
- Admission Evidence Seal Refresh is strictly metadata-only.
- Final Paper Sandbox Bridge is a no-write metadata bridge, not a real paper runtime.
- The contents of this report do not constitute financial or investment advice.
"""

def build_no_write_transition_review_from_parts(
    dossier: NoWriteTransitionDossier,
    seal_validation: Optional[AdmissionEvidenceSealValidation] = None,
    seal_refresh: Optional[AdmissionEvidenceSealRefresh] = None,
    bridge_envelope: Optional[PaperSandboxBridgeEnvelope] = None
) -> NoWriteTransitionFullReview:

    return NoWriteTransitionFullReview(
        review_id=create_transition_full_review_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        report_type=NoWriteTransitionReportType.FULL_NO_WRITE_TRANSITION_REVIEW,
        dossiers=[dossier],
        evidence_items=dossier.evidence_items,
        seal_validations=[seal_validation] if seal_validation else [],
        seal_refreshes=[seal_refresh] if seal_refresh else [],
        bridge_envelopes=[bridge_envelope] if bridge_envelope else [],
        bridge_routes=bridge_envelope.routes if bridge_envelope else [],
        audit_entries=[], # Populated later
        output_paths={},
        warnings=[],
        errors=[]
    )

def build_no_write_transition_full_review(admission_payload: dict[str, Any]) -> NoWriteTransitionFullReview:
    from usa_signal_bot.paper_no_write_transition.transition_decision import NoWriteTransitionDecisionEngine
    from usa_signal_bot.paper_no_write_transition.evidence_seal_validator import validate_admission_evidence_seal_from_payload
    from usa_signal_bot.paper_no_write_transition.evidence_seal_refresh import refresh_admission_evidence_seal_metadata
    from usa_signal_bot.paper_no_write_transition.sandbox_bridge_envelope import build_paper_sandbox_bridge_envelope
    from usa_signal_bot.paper_no_write_transition.transition_audit import (
        audit_entry_from_transition_dossier,
        audit_entry_from_seal_validation,
        audit_entry_from_bridge_envelope
    )

    seal_validation = validate_admission_evidence_seal_from_payload(admission_payload)
    engine = NoWriteTransitionDecisionEngine()

    # Needs a dummy evidence list for now
    dossier = engine.decide(admission_payload, [], seal_validation)

    seal_refresh = refresh_admission_evidence_seal_metadata(seal_validation, dossier.evidence_items)
    bridge_envelope = build_paper_sandbox_bridge_envelope(
        dossier_id=dossier.dossier_id,
        candidate_id=dossier.candidate_id,
        evidence_seal_id=seal_validation.validation_id
    )

    review = build_no_write_transition_review_from_parts(dossier, seal_validation, seal_refresh, bridge_envelope)

    review.audit_entries.append(audit_entry_from_transition_dossier(dossier))
    review.audit_entries.append(audit_entry_from_seal_validation(seal_validation))
    review.audit_entries.append(audit_entry_from_bridge_envelope(bridge_envelope))

    return review

def no_write_transition_full_review_summary(review: NoWriteTransitionFullReview) -> dict[str, Any]:
    return {
        "review_id": review.review_id,
        "dossier_status": review.dossiers[0].status.value if review.dossiers else "N/A",
        "seal_valid": len(review.seal_validations) > 0 and review.seal_validations[0].status.value == "VALID",
        "bridge_envelope_safe": len(review.bridge_envelopes) > 0 and review.bridge_envelopes[0].bridge_is_no_write
    }

def no_write_transition_full_review_to_text(review: NoWriteTransitionFullReview, limit: int = 100) -> str:
    text = f"Full No-Write Transition Review: {review.review_id}\n"
    if review.dossiers:
        text += f"Dossier Status: {review.dossiers[0].status.value}\n"
    text += no_write_transition_limitations_text()
    return text

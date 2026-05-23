from typing import Any, Optional
import datetime
import hashlib
import json

from usa_signal_bot.core.enums import (
    NoWriteTransitionDossierStatus,
    NoWriteTransitionDecision,
    NoWriteTransitionRiskFlag
)
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    NoWriteTransitionDossier,
    TransitionDossierEvidenceItem,
    AdmissionEvidenceSealValidation,
    AdmissionEvidenceSealRefresh,
    PaperSandboxBridgeEnvelope,
    create_transition_dossier_id
)
from usa_signal_bot.paper_no_write_transition.eligibility_checker import no_write_transition_safety_flags_from_admission

def stable_no_write_transition_dossier_hash(payload: dict[str, Any]) -> str:
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def collect_transition_dossier_safety_flags(
    admission_payload: dict[str, Any],
    evidence_items: list[TransitionDossierEvidenceItem]
) -> list[NoWriteTransitionRiskFlag]:

    flags = no_write_transition_safety_flags_from_admission(admission_payload)
    for item in evidence_items:
        flags.extend(item.risk_flags)
    return list(set(flags))

def build_no_write_transition_dossier(admission_payload: dict[str, Any]) -> NoWriteTransitionDossier:
    from usa_signal_bot.paper_no_write_transition.dossier_evidence import collect_transition_dossier_evidence
    from usa_signal_bot.paper_no_write_transition.eligibility_checker import evaluate_no_write_transition_eligibility, transition_dossier_status_from_decision

    decision = evaluate_no_write_transition_eligibility(admission_payload)
    status = transition_dossier_status_from_decision(decision)
    evidence_items = collect_transition_dossier_evidence(admission_payload)
    safety_flags = collect_transition_dossier_safety_flags(admission_payload, evidence_items)

    return NoWriteTransitionDossier(
        dossier_id=create_transition_dossier_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=status,
        decision=decision,
        candidate_id=admission_payload.get("candidate_id"),
        source_admission_report_id=admission_payload.get("report_id"),
        source_admission_review_id=None,
        source_transition_checkpoint_id=None,
        source_evidence_seal_id=None,
        evidence_items=evidence_items,
        evidence_seal_validation=None,
        evidence_seal_refresh=None,
        bridge_envelope=None,
        evidence_refs=[item.evidence_id for item in evidence_items],
        dossier_hash=stable_no_write_transition_dossier_hash(admission_payload),
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        transition_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=safety_flags,
        required_followups=[],
        warnings=[],
        errors=[]
    )

def build_default_no_write_transition_dossier(candidate_id: Optional[str] = None) -> NoWriteTransitionDossier:
    return NoWriteTransitionDossier(
        dossier_id=create_transition_dossier_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=NoWriteTransitionDossierStatus.CREATED,
        decision=NoWriteTransitionDecision.CREATE_NO_WRITE_TRANSITION_DOSSIER,
        candidate_id=candidate_id,
        source_admission_report_id=None,
        source_admission_review_id=None,
        source_transition_checkpoint_id=None,
        source_evidence_seal_id=None,
        evidence_items=[],
        evidence_seal_validation=None,
        evidence_seal_refresh=None,
        bridge_envelope=None,
        evidence_refs=[],
        dossier_hash="default_hash",
        sealed=True,
        immutable=True,
        manual_review_required=True,
        activation_denied=True,
        activation_allowed=False,
        transition_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        safety_flags=[],
        required_followups=[],
        warnings=[],
        errors=[]
    )

def no_write_transition_dossier_summary(dossier: NoWriteTransitionDossier) -> dict[str, Any]:
    return {
        "dossier_id": dossier.dossier_id,
        "status": dossier.status.value,
        "decision": dossier.decision.value,
        "sealed": dossier.sealed,
        "evidence_count": len(dossier.evidence_items)
    }

def no_write_transition_dossier_to_text(dossier: NoWriteTransitionDossier, limit: int = 100) -> str:
    return f"Transition Dossier {dossier.dossier_id} [{dossier.status.value}] Decision: {dossier.decision.value}"

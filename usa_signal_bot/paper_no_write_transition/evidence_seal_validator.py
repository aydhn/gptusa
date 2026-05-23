from typing import Any, Optional
import datetime
import hashlib
import json

from usa_signal_bot.core.enums import (
    AdmissionEvidenceSealValidationStatus,
    AdmissionEvidenceSealRefreshDecision,
    NoWriteTransitionRiskFlag
)
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    AdmissionEvidenceSealValidation,
    TransitionDossierEvidenceItem,
    create_seal_validation_id
)
from usa_signal_bot.paper_no_write_transition.admission_ingestion import extract_admission_evidence_seal

def stable_transition_evidence_hash(payload: dict[str, Any]) -> str:
    # Deterministic hash of payload
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def extract_expected_seal_hash(admission_payload: dict[str, Any]) -> Optional[str]:
    seal = extract_admission_evidence_seal(admission_payload)
    if seal:
        return seal.get("seal_hash")
    return None

def extract_observed_seal_hash(admission_payload: dict[str, Any], evidence_items: Optional[list[TransitionDossierEvidenceItem]] = None) -> Optional[str]:
    seal = extract_admission_evidence_seal(admission_payload)
    if not seal:
        return None
    # Assuming the seal dictionary is what we hash for verification purposes in this simplified model.
    return stable_transition_evidence_hash(seal.get("payload", {}))

def validate_admission_evidence_seal_from_payload(
    admission_payload: dict[str, Any],
    evidence_items: Optional[list[TransitionDossierEvidenceItem]] = None
) -> AdmissionEvidenceSealValidation:

    seal = extract_admission_evidence_seal(admission_payload)
    if not seal:
        return AdmissionEvidenceSealValidation(
            validation_id=create_seal_validation_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            status=AdmissionEvidenceSealValidationStatus.MISSING,
            decision=AdmissionEvidenceSealRefreshDecision.REQUEST_EVIDENCE_REFRESH,
            candidate_id=admission_payload.get("candidate_id"),
            source_seal_id=None,
            expected_hash=None,
            observed_hash=None,
            hash_matches=False,
            sealed=False,
            immutable=False,
            evidence_ref_count=0,
            missing_evidence_count=0,
            stale_evidence_count=0,
            risk_flags=[NoWriteTransitionRiskFlag.EVIDENCE_SEAL_MISSING],
            required_followups=[],
            warnings=["Evidence seal missing"],
            errors=[]
        )

    expected_hash = extract_expected_seal_hash(admission_payload)
    observed_hash = extract_observed_seal_hash(admission_payload, evidence_items)
    hash_matches = expected_hash == observed_hash and expected_hash is not None

    sealed = seal.get("sealed", False)
    immutable = seal.get("immutable", False)

    status = AdmissionEvidenceSealValidationStatus.VALID
    decision = AdmissionEvidenceSealRefreshDecision.REFRESH_SEAL_METADATA
    risk_flags = []

    if not hash_matches:
        status = AdmissionEvidenceSealValidationStatus.FAILED
        decision = AdmissionEvidenceSealRefreshDecision.BLOCK
        risk_flags.append(NoWriteTransitionRiskFlag.EVIDENCE_SEAL_FAILED)

    if not sealed or not immutable:
        status = AdmissionEvidenceSealValidationStatus.FAILED
        decision = AdmissionEvidenceSealRefreshDecision.BLOCK
        risk_flags.append(NoWriteTransitionRiskFlag.EVIDENCE_SEAL_FAILED)

    return AdmissionEvidenceSealValidation(
        validation_id=create_seal_validation_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=status,
        decision=decision,
        candidate_id=admission_payload.get("candidate_id"),
        source_seal_id=seal.get("seal_id"),
        expected_hash=expected_hash,
        observed_hash=observed_hash,
        hash_matches=hash_matches,
        sealed=sealed,
        immutable=immutable,
        evidence_ref_count=len(evidence_items) if evidence_items else 0,
        missing_evidence_count=0,
        stale_evidence_count=0,
        risk_flags=risk_flags,
        required_followups=[],
        warnings=[],
        errors=[]
    )

def seal_validation_risk_flags(validation: AdmissionEvidenceSealValidation) -> list[NoWriteTransitionRiskFlag]:
    return validation.risk_flags

def seal_validation_followups(validation: AdmissionEvidenceSealValidation) -> list[str]:
    return validation.required_followups

def evidence_seal_validation_to_text(validation: AdmissionEvidenceSealValidation) -> str:
    return f"Seal Validation [{validation.status.value}] Match: {validation.hash_matches} Sealed: {validation.sealed}"

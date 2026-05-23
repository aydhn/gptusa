from typing import Any, Optional
import datetime

from usa_signal_bot.core.enums import (
    AdmissionEvidenceSealValidationStatus,
    AdmissionEvidenceSealRefreshDecision,
    NoWriteTransitionRiskFlag
)
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import (
    AdmissionEvidenceSealValidation,
    AdmissionEvidenceSealRefresh,
    TransitionDossierEvidenceItem,
    create_seal_refresh_id
)

def refresh_admission_evidence_seal_metadata(
    validation: AdmissionEvidenceSealValidation,
    evidence_items: list[TransitionDossierEvidenceItem]
) -> AdmissionEvidenceSealRefresh:

    decision = validation.decision
    if decision == AdmissionEvidenceSealRefreshDecision.BLOCK:
        status = AdmissionEvidenceSealValidationStatus.BLOCKED
    else:
        status = AdmissionEvidenceSealValidationStatus.VALID

    return AdmissionEvidenceSealRefresh(
        refresh_id=create_seal_refresh_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=status,
        decision=decision,
        candidate_id=validation.candidate_id,
        source_validation_id=validation.validation_id,
        refreshed_hash=validation.observed_hash,
        refreshed_evidence_refs=[item.evidence_id for item in evidence_items],
        sealed=True,
        immutable=True,
        refresh_is_metadata_only=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=validation.risk_flags.copy(),
        warnings=[],
        errors=[]
    )

def build_default_evidence_seal_refresh(candidate_id: Optional[str] = None) -> AdmissionEvidenceSealRefresh:
    return AdmissionEvidenceSealRefresh(
        refresh_id=create_seal_refresh_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=AdmissionEvidenceSealValidationStatus.VALID,
        decision=AdmissionEvidenceSealRefreshDecision.REFRESH_SEAL_METADATA,
        candidate_id=candidate_id,
        source_validation_id=None,
        refreshed_hash=None,
        refreshed_evidence_refs=[],
        sealed=True,
        immutable=True,
        refresh_is_metadata_only=True,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        risk_flags=[],
        warnings=[],
        errors=[]
    )

def validate_evidence_seal_refresh_safety(refresh: AdmissionEvidenceSealRefresh) -> list[str]:
    errors = []
    if not refresh.refresh_is_metadata_only:
        errors.append("Refresh must be metadata-only.")
    if refresh.allows_active_paper:
        errors.append("Refresh allows active paper.")
    return errors

def evidence_seal_refresh_summary(refresh: AdmissionEvidenceSealRefresh) -> dict[str, Any]:
    return {
        "status": refresh.status.value,
        "decision": refresh.decision.value,
        "sealed": refresh.sealed,
        "immutable": refresh.immutable
    }

def evidence_seal_refresh_to_text(refresh: AdmissionEvidenceSealRefresh) -> str:
    return f"Seal Refresh [{refresh.status.value}] metadata-only: {refresh.refresh_is_metadata_only}"

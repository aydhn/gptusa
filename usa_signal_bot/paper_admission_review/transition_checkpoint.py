from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import (
    NoWriteTransitionCheckpointStatus,
    NoWriteTransitionCheckpointDecision,
    AdmissionReviewRiskFlag,
    PaperModeAdmissionReviewDecision
)
from .admission_review_models import (
    FinalNoWriteTransitionCheckpoint,
    create_transition_checkpoint_id,
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def transition_checkpoint_required_followups(flags: List[AdmissionReviewRiskFlag]) -> List[str]:
    followups = []
    if AdmissionReviewRiskFlag.LEDGER_MISSING in flags or AdmissionReviewRiskFlag.LEDGER_SCOPE_MISSING in flags:
        followups.append("Complete ledger reconciliation")
    if AdmissionReviewRiskFlag.EVIDENCE_MISSING in flags or AdmissionReviewRiskFlag.EVIDENCE_SEAL_FAILED in flags:
        followups.append("Provide missing evidence and refresh seal")
    if AdmissionReviewRiskFlag.WRITE_LOCK_REFRESH_FAILED in flags:
        followups.append("Refresh write lock proof")
    return followups

def default_final_no_write_transition_checkpoint(candidate_id: Optional[str] = None) -> FinalNoWriteTransitionCheckpoint:
    return FinalNoWriteTransitionCheckpoint(
        checkpoint_id=create_transition_checkpoint_id(),
        created_at_utc=_now(),
        status=NoWriteTransitionCheckpointStatus.DRAFT,
        decision=NoWriteTransitionCheckpointDecision.INCONCLUSIVE,
        activation_denied=True,
        activation_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        transition_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        required_followups=[],
        safety_flags=[],
        warnings=[],
        errors=[],
        candidate_id=candidate_id
    )

def build_final_no_write_transition_checkpoint(
    admission_review: PaperModeAdmissionReview,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    evidence_seal: Optional[AdmissionEvidenceSeal] = None
) -> FinalNoWriteTransitionCheckpoint:

    flags = list(set(admission_review.safety_flags))
    if reconciliation:
        flags.extend([f for f in reconciliation.safety_flags if f not in flags])

    status = NoWriteTransitionCheckpointStatus.VALIDATED_NO_WRITE
    decision = NoWriteTransitionCheckpointDecision.CONTINUE_TO_NO_WRITE_TRANSITION_DOSSIER

    if admission_review.decision != PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT:
         status = NoWriteTransitionCheckpointStatus.BLOCKED
         decision = NoWriteTransitionCheckpointDecision.REQUEST_ADMISSION_REVIEW_REFRESH
    elif reconciliation and reconciliation.decision != "ACCEPT_NO_WRITE_ACKNOWLEDGEMENT":
         status = NoWriteTransitionCheckpointStatus.BLOCKED
         decision = NoWriteTransitionCheckpointDecision.REQUEST_LEDGER_RECONCILIATION_REFRESH
    elif not evidence_seal or evidence_seal.status != "SEALED":
         status = NoWriteTransitionCheckpointStatus.BLOCKED
         decision = NoWriteTransitionCheckpointDecision.REQUEST_EVIDENCE_SEAL_REFRESH

    followups = transition_checkpoint_required_followups(flags)

    return FinalNoWriteTransitionCheckpoint(
        checkpoint_id=create_transition_checkpoint_id(),
        created_at_utc=_now(),
        status=status,
        decision=decision,
        activation_denied=True,
        activation_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        transition_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        required_followups=followups,
        safety_flags=flags,
        warnings=[],
        errors=[],
        candidate_id=admission_review.candidate_id,
        source_admission_review_id=admission_review.admission_review_id,
        source_reconciliation_id=reconciliation.reconciliation_id if reconciliation else None,
        source_evidence_seal_id=evidence_seal.seal_id if evidence_seal else None
    )

def transition_checkpoint_summary(checkpoint: FinalNoWriteTransitionCheckpoint) -> Dict[str, Any]:
    return {
        "status": checkpoint.status,
        "decision": checkpoint.decision,
        "activation_denied": checkpoint.activation_denied,
        "transition_allowed": checkpoint.transition_allowed,
        "safety_flags_count": len(checkpoint.safety_flags)
    }

def transition_checkpoint_to_text(checkpoint: FinalNoWriteTransitionCheckpoint) -> str:
    return json.dumps(transition_checkpoint_summary(checkpoint), indent=2)

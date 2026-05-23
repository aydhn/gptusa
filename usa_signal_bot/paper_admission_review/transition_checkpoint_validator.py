from typing import Any, Dict, List
import json
from .admission_review_models import FinalNoWriteTransitionCheckpoint

def validate_transition_checkpoint_safety(checkpoint: FinalNoWriteTransitionCheckpoint) -> List[str]:
    errors = []
    if not checkpoint.activation_denied:
        errors.append("activation_denied is false")
    if checkpoint.activation_allowed:
        errors.append("activation_allowed is true")
    if checkpoint.transition_allowed:
        errors.append("transition_allowed is true")
    if not checkpoint.all_writes_blocked:
        errors.append("all_writes_blocked is false")
    if checkpoint.mutation_detected:
        errors.append("mutation_detected is true")

    for allow_attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
        if getattr(checkpoint, allow_attr, True):
             errors.append(f"{allow_attr} is true")

    return errors

def transition_checkpoint_allows_activation(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return checkpoint.activation_allowed or not checkpoint.activation_denied

def transition_checkpoint_allows_transition(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return checkpoint.transition_allowed

def transition_checkpoint_requires_followup(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return len(checkpoint.required_followups) > 0

def transition_checkpoint_blocks_next_stage(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return checkpoint.decision in ["REJECT", "BLOCK", "REQUEST_ADMISSION_REVIEW_REFRESH", "REQUEST_LEDGER_RECONCILIATION_REFRESH", "REQUEST_EVIDENCE_SEAL_REFRESH", "REQUEST_MANUAL_REVIEW"] or len(validate_transition_checkpoint_safety(checkpoint)) > 0

def transition_checkpoint_validator_summary(checkpoint: FinalNoWriteTransitionCheckpoint) -> Dict[str, Any]:
    return {
        "safe": len(validate_transition_checkpoint_safety(checkpoint)) == 0,
        "allows_activation": transition_checkpoint_allows_activation(checkpoint),
        "blocks_next_stage": transition_checkpoint_blocks_next_stage(checkpoint)
    }

def transition_checkpoint_validator_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)

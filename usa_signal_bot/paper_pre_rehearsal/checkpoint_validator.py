from typing import Any, Dict, List
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import ActivationDeniedCheckpoint

def validate_activation_checkpoint_safety(checkpoint: ActivationDeniedCheckpoint) -> List[str]:
    violations = []
    if not checkpoint.activation_denied:
        violations.append("activation_denied is False")
    if checkpoint.allows_active_paper:
        violations.append("allows_active_paper is True")
    if checkpoint.allows_broker_execution:
        violations.append("allows_broker_execution is True")
    if checkpoint.allows_paper_state_mutation:
        violations.append("allows_paper_state_mutation is True")
    if checkpoint.allows_config_patch:
        violations.append("allows_config_patch is True")
    if checkpoint.allows_telegram_real_send:
        violations.append("allows_telegram_real_send is True")
    return violations

def activation_checkpoint_allows_activation(checkpoint: ActivationDeniedCheckpoint) -> bool:
    return (
        not checkpoint.activation_denied or
        checkpoint.allows_active_paper or
        checkpoint.allows_broker_execution or
        checkpoint.allows_paper_state_mutation or
        checkpoint.allows_config_patch or
        checkpoint.allows_telegram_real_send
    )

def activation_checkpoint_requires_followup(checkpoint: ActivationDeniedCheckpoint) -> bool:
    return len(checkpoint.required_followups) > 0

def activation_checkpoint_blocks_next_audit(checkpoint: ActivationDeniedCheckpoint) -> bool:
    from usa_signal_bot.core.enums import ActivationDeniedDecision
    return checkpoint.decision in [
        ActivationDeniedDecision.BLOCK,
        ActivationDeniedDecision.REJECT,
        ActivationDeniedDecision.REQUEST_FIREWALL_REPLAY
    ]

def activation_checkpoint_validator_summary(checkpoint: ActivationDeniedCheckpoint) -> Dict[str, Any]:
    return {
        "safe": len(validate_activation_checkpoint_safety(checkpoint)) == 0,
        "allows_activation": activation_checkpoint_allows_activation(checkpoint),
        "blocks_next_audit": activation_checkpoint_blocks_next_audit(checkpoint)
    }

def activation_checkpoint_validator_to_text(payload: Dict[str, Any]) -> str:
    return f"Checkpoint Validation: Safe={payload['safe']}, Allows Activation={payload['allows_activation']}"

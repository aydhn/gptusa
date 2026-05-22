from typing import Any, Dict, List, Optional
import datetime
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import (
    ActivationDeniedCheckpoint,
    PrePaperDryRehearsalRun,
    create_activation_denied_checkpoint_id,
    validate_activation_denied_checkpoint
)
from usa_signal_bot.core.enums import ActivationDeniedCheckpointStatus, ActivationDeniedDecision, PrePaperRiskFlag

def activation_denied_reasons(run: PrePaperDryRehearsalRun) -> List[str]:
    reasons = ["Guarded pre-paper dry rehearsal is complete but active paper is not allowed"]
    if any(not e.blocked for e in run.firewall_events):
        reasons.append("Unblocked firewall events detected")
    return reasons

def activation_denied_required_followups(run: PrePaperDryRehearsalRun) -> List[str]:
    return [
        "Review mutation firewall logs",
        "Perform zero-mutation audit",
        "Generate safety report"
    ]

def build_activation_denied_checkpoint(run: PrePaperDryRehearsalRun) -> ActivationDeniedCheckpoint:
    reasons = activation_denied_reasons(run)
    decision = ActivationDeniedDecision.DENY_ACTIVATION_AND_CONTINUE_AUDIT
    if "Unblocked firewall events detected" in reasons:
        decision = ActivationDeniedDecision.REQUEST_FIREWALL_REPLAY

    cp = ActivationDeniedCheckpoint(
        checkpoint_id=create_activation_denied_checkpoint_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=ActivationDeniedCheckpointStatus.CREATED,
        decision=decision,
        candidate_id=run.candidate_id,
        source_run_id=run.run_id,
        source_plan_id=run.plan.plan_id if run.plan else None,
        activation_denied=True,
        denial_reason="; ".join(reasons),
        required_followups=activation_denied_required_followups(run),
        safety_flags=run.safety_flags.copy(),
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        warnings=[],
        errors=[]
    )
    validate_activation_denied_checkpoint(cp)
    return cp

def default_activation_denied_checkpoint(candidate_id: Optional[str] = None) -> ActivationDeniedCheckpoint:
    cp = ActivationDeniedCheckpoint(
        checkpoint_id=create_activation_denied_checkpoint_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        status=ActivationDeniedCheckpointStatus.DENIED_BY_DEFAULT,
        decision=ActivationDeniedDecision.DENY_ACTIVATION_AND_CONTINUE_AUDIT,
        candidate_id=candidate_id,
        source_run_id=None,
        source_plan_id=None,
        activation_denied=True,
        denial_reason="Default denial prior to full rehearsal",
        required_followups=["Complete pre-paper dry rehearsal"],
        safety_flags=[],
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        warnings=[],
        errors=[]
    )
    validate_activation_denied_checkpoint(cp)
    return cp

def activation_denied_checkpoint_summary(checkpoint: ActivationDeniedCheckpoint) -> Dict[str, Any]:
    return {
        "checkpoint_id": checkpoint.checkpoint_id,
        "decision": checkpoint.decision.value,
        "activation_denied": checkpoint.activation_denied
    }

def activation_denied_checkpoint_to_text(checkpoint: ActivationDeniedCheckpoint) -> str:
    s = activation_denied_checkpoint_summary(checkpoint)
    return f"Checkpoint {s['checkpoint_id']}: Denied={s['activation_denied']}, Decision={s['decision']}"

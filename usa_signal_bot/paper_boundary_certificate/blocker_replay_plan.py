from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_boundary_certificate.boundary_certificate_models import AdmissionBlockerReplayPlan, create_blocker_replay_plan_id
from usa_signal_bot.core.enums import PaperAdmissionAttemptType

def required_admission_blocker_replay_attempt_types() -> list[str]:
    return [
        PaperAdmissionAttemptType.ENABLE_ACTIVE_PAPER.value,
        PaperAdmissionAttemptType.ENABLE_PAPER_RUNTIME.value,
        PaperAdmissionAttemptType.ADMIT_CANDIDATE_TO_PAPER.value,
        PaperAdmissionAttemptType.CREATE_PAPER_SESSION.value,
        PaperAdmissionAttemptType.CREATE_PAPER_ORDER.value,
        PaperAdmissionAttemptType.COMMIT_PAPER_STATE.value,
        PaperAdmissionAttemptType.PATCH_PAPER_CONFIG.value,
        PaperAdmissionAttemptType.SEND_BROKER_ORDER.value,
        PaperAdmissionAttemptType.SEND_TELEGRAM_REAL.value,
        PaperAdmissionAttemptType.UNLOCK_PAPER_GATE.value
    ]

def build_admission_blocker_replay_plan(no_order_payload: dict[str, Any]) -> AdmissionBlockerReplayPlan:
    return AdmissionBlockerReplayPlan(
        replay_plan_id=create_blocker_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=no_order_payload.get("candidate_id"),
        source_no_order_dossier_id=no_order_payload.get("dossier", {}).get("dossier_id"),
        source_blocker_rule_refs=[],
        required_attempt_types=required_admission_blocker_replay_attempt_types(),
        require_all_attempts_blocked=True,
        execution_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )

def build_default_blocker_replay_plan(candidate_id: str | None = None) -> AdmissionBlockerReplayPlan:
    return AdmissionBlockerReplayPlan(
        replay_plan_id=create_blocker_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        source_no_order_dossier_id=None,
        source_blocker_rule_refs=[],
        required_attempt_types=required_admission_blocker_replay_attempt_types(),
        require_all_attempts_blocked=True,
        execution_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )

def validate_blocker_replay_plan_safety(plan: AdmissionBlockerReplayPlan) -> list[str]:
    errors = []
    if plan.execution_enabled: errors.append("execution_enabled is True")
    if plan.active_paper_enabled: errors.append("active_paper_enabled is True")
    if plan.paper_admission_enabled: errors.append("paper_admission_enabled is True")
    if plan.broker_execution_enabled: errors.append("broker_execution_enabled is True")
    if plan.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled is True")
    if plan.config_patch_enabled: errors.append("config_patch_enabled is True")
    if plan.telegram_real_send_enabled: errors.append("telegram_real_send_enabled is True")
    return errors

def blocker_replay_plan_summary(plan: AdmissionBlockerReplayPlan) -> dict[str, Any]:
    return {"id": plan.replay_plan_id, "safe": len(validate_blocker_replay_plan_safety(plan)) == 0}

def blocker_replay_plan_to_text(plan: AdmissionBlockerReplayPlan) -> str:
    return str(blocker_replay_plan_summary(plan))

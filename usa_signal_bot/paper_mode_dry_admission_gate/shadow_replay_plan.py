from datetime import datetime, timezone
from typing import Any, List
from usa_signal_bot.paper_mode_dry_admission_gate.dry_admission_gate_models import (
    ShadowLaunchReplayPlan,
    create_shadow_replay_plan_id
)
from usa_signal_bot.paper_mode_dry_admission_gate.board_dossier_ingestion import (
    extract_board_dossier_candidate_id,
    extract_board_dossier,
    extract_acceptance_board_seal
)

def required_shadow_replay_attempt_types() -> List[str]:
    return [
        "START_PAPER_MODE",
        "START_LOCAL_PAPER_RUNTIME",
        "SHADOW_LAUNCH_CANDIDATE",
        "ADMIT_CANDIDATE_TO_PAPER",
        "CREATE_PAPER_SESSION",
        "CREATE_PAPER_ORDER",
        "COMMIT_PAPER_STATE",
        "PATCH_PAPER_CONFIG",
        "SEND_BROKER_ORDER",
        "SEND_TELEGRAM_REAL",
        "UNLOCK_SHADOW_LAUNCH_GATE"
    ]

def build_shadow_launch_replay_plan(board_payload: dict[str, Any]) -> ShadowLaunchReplayPlan:
    candidate_id = extract_board_dossier_candidate_id(board_payload)
    dossier = extract_board_dossier(board_payload)
    dossier_id = dossier.get("dossier_id") if dossier else None

    seal = extract_acceptance_board_seal(board_payload)
    seal_id = seal.get("seal_id") if seal else None

    plan = ShadowLaunchReplayPlan(
        replay_plan_id=create_shadow_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        source_board_dossier_id=dossier_id,
        source_acceptance_seal_id=seal_id,
        required_attempt_types=required_shadow_replay_attempt_types(),
        require_all_attempts_blocked=True,
        execution_enabled=False,
        shadow_launch_enabled=False,
        paper_mode_launch_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )
    return plan

def build_default_shadow_replay_plan(candidate_id: str | None = None) -> ShadowLaunchReplayPlan:
    plan = ShadowLaunchReplayPlan(
        replay_plan_id=create_shadow_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        required_attempt_types=required_shadow_replay_attempt_types(),
        require_all_attempts_blocked=True,
        execution_enabled=False,
        shadow_launch_enabled=False,
        paper_mode_launch_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )
    return plan

def validate_shadow_replay_plan_safety(plan: ShadowLaunchReplayPlan) -> List[str]:
    errors = []
    if plan.execution_enabled: errors.append("execution_enabled must be False")
    if plan.shadow_launch_enabled: errors.append("shadow_launch_enabled must be False")
    if plan.paper_mode_launch_enabled: errors.append("paper_mode_launch_enabled must be False")
    if plan.active_paper_enabled: errors.append("active_paper_enabled must be False")
    if plan.paper_admission_enabled: errors.append("paper_admission_enabled must be False")
    if plan.broker_execution_enabled: errors.append("broker_execution_enabled must be False")
    if plan.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled must be False")
    if plan.config_patch_enabled: errors.append("config_patch_enabled must be False")
    if plan.telegram_real_send_enabled: errors.append("telegram_real_send_enabled must be False")
    return errors

def shadow_replay_plan_summary(plan: ShadowLaunchReplayPlan) -> dict[str, Any]:
    return {
        "replay_plan_id": plan.replay_plan_id,
        "candidate_id": plan.candidate_id,
        "required_attempt_types": plan.required_attempt_types,
        "require_all_attempts_blocked": plan.require_all_attempts_blocked,
        "safe": len(validate_shadow_replay_plan_safety(plan)) == 0
    }

def shadow_replay_plan_to_text(plan: ShadowLaunchReplayPlan) -> str:
    summary = shadow_replay_plan_summary(plan)
    return f"Shadow Replay Plan {summary['replay_plan_id']}\nCandidate: {summary['candidate_id']}\nSafe: {summary['safe']}"

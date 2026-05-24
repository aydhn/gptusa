from typing import Any, List
from datetime import datetime, timezone
from usa_signal_bot.pre_paper_handoff_freeze_gate.handoff_freeze_models import SandboxRuntimeAdmissionReplayPlan, create_sandbox_replay_plan_id

def required_sandbox_runtime_admission_replay_attempt_types() -> List[str]:
    return [
        "START_PAPER_SANDBOX_RUNTIME",
        "ADMIT_CANDIDATE_TO_SANDBOX_RUNTIME",
        "START_SANDBOX_PAPER_SESSION",
        "CREATE_SANDBOX_PAPER_SESSION",
        "CREATE_SANDBOX_PAPER_ORDER",
        "COMMIT_SANDBOX_PAPER_STATE",
        "PATCH_SANDBOX_RUNTIME_CONFIG",
        "SEND_SANDBOX_BROKER_ORDER",
        "SEND_SANDBOX_TELEGRAM_REAL",
        "UNLOCK_SANDBOX_RUNTIME_ADMISSION_GATE"
    ]

def build_sandbox_runtime_admission_replay_plan(payload: dict[str, Any]) -> SandboxRuntimeAdmissionReplayPlan:
    plan = build_default_sandbox_runtime_admission_replay_plan(payload.get("candidate_id"))
    plan.source_simulator_dossier_id = payload.get("simulator_dossier_id")
    plan.source_acceptance_seal_id = payload.get("simulator_acceptance_seal_id")
    plan.errors = validate_sandbox_runtime_admission_replay_plan_safety(plan)
    return plan

def build_default_sandbox_runtime_admission_replay_plan(candidate_id: str | None = None) -> SandboxRuntimeAdmissionReplayPlan:
    return SandboxRuntimeAdmissionReplayPlan(
        replay_plan_id=create_sandbox_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        source_simulator_dossier_id=None,
        source_acceptance_seal_id=None,
        required_attempt_types=required_sandbox_runtime_admission_replay_attempt_types(),
        require_all_attempts_blocked=True,
        execution_enabled=False,
        sandbox_runtime_admission_enabled=False,
        paper_sandbox_runtime_enabled=False,
        simulator_admission_enabled=False,
        local_paper_simulator_enabled=False,
        active_paper_enabled=False,
        paper_admission_enabled=False,
        broker_execution_enabled=False,
        paper_state_mutation_enabled=False,
        config_patch_enabled=False,
        telegram_real_send_enabled=False,
        warnings=[],
        errors=[]
    )

def validate_sandbox_runtime_admission_replay_plan_safety(plan: SandboxRuntimeAdmissionReplayPlan) -> List[str]:
    errors = []
    if not plan.require_all_attempts_blocked:
        errors.append("require_all_attempts_blocked must be True")
    if plan.execution_enabled:
        errors.append("execution_enabled must be False")
    if plan.sandbox_runtime_admission_enabled:
        errors.append("sandbox_runtime_admission_enabled must be False")
    if plan.paper_sandbox_runtime_enabled:
        errors.append("paper_sandbox_runtime_enabled must be False")
    if plan.simulator_admission_enabled:
        errors.append("simulator_admission_enabled must be False")
    if plan.local_paper_simulator_enabled:
        errors.append("local_paper_simulator_enabled must be False")
    if plan.active_paper_enabled:
        errors.append("active_paper_enabled must be False")
    if plan.paper_admission_enabled:
        errors.append("paper_admission_enabled must be False")
    if plan.broker_execution_enabled:
        errors.append("broker_execution_enabled must be False")
    if plan.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled must be False")
    if plan.config_patch_enabled:
        errors.append("config_patch_enabled must be False")
    if plan.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled must be False")
    return errors

def sandbox_runtime_admission_replay_plan_summary(plan: SandboxRuntimeAdmissionReplayPlan) -> dict[str, Any]:
    return {
        "replay_plan_id": plan.replay_plan_id,
        "valid": len(plan.errors) == 0,
        "error_count": len(plan.errors)
    }

def sandbox_runtime_admission_replay_plan_to_text(plan: SandboxRuntimeAdmissionReplayPlan) -> str:
    res = f"Sandbox Replay Plan: {plan.replay_plan_id}\n"
    res += f"Valid: {len(plan.errors) == 0}\n"
    if plan.errors:
        res += "Errors:\n"
        for e in plan.errors:
            res += f"- {e}\n"
    return res

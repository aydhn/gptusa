from typing import Any
from usa_signal_bot.paper_no_write_admission.no_write_admission_models import ActivationReplayPlan
import datetime

def required_activation_replay_attempt_types() -> list[str]:
    return ["ENABLE_ACTIVE_PAPER", "ENABLE_CANDIDATE_STRATEGY", "PATCH_PAPER_CONFIG", "COMMIT_PAPER_STATE", "CREATE_PAPER_ORDER", "SEND_BROKER_ORDER", "SEND_TELEGRAM_REAL", "UNLOCK_ARCHIVE", "UNLOCK_FINAL_LOCK"]

def build_activation_replay_plan(board_payload: dict[str, Any]) -> ActivationReplayPlan:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActivationReplayPlan(
        replay_plan_id="p1", created_at_utc=now, candidate_id=None, source_board_review_id=None, required_attempt_types=required_activation_replay_attempt_types(),
        required_rule_count=0, require_all_attempts_denied=True, execution_enabled=False, active_paper_enabled=False, broker_execution_enabled=False,
        paper_state_mutation_enabled=False, config_patch_enabled=False, telegram_real_send_enabled=False, warnings=[], errors=[]
    )

def build_default_activation_replay_plan(candidate_id: str | None = None) -> ActivationReplayPlan:
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActivationReplayPlan(
        replay_plan_id="p1", created_at_utc=now, candidate_id=candidate_id, source_board_review_id=None, required_attempt_types=required_activation_replay_attempt_types(),
        required_rule_count=0, require_all_attempts_denied=True, execution_enabled=False, active_paper_enabled=False, broker_execution_enabled=False,
        paper_state_mutation_enabled=False, config_patch_enabled=False, telegram_real_send_enabled=False, warnings=[], errors=[]
    )

def validate_activation_replay_plan_safety(plan: ActivationReplayPlan) -> list[str]:
    return []

def activation_replay_plan_summary(plan: ActivationReplayPlan) -> dict[str, Any]:
    return {}

def activation_replay_plan_to_text(plan: ActivationReplayPlan) -> str:
    return "Plan"

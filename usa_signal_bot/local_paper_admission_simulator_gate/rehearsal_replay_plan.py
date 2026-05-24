from typing import Any
from .simulator_gate_models import RehearsalReplayPlan, create_rehearsal_replay_plan_id
from datetime import datetime, timezone

def required_rehearsal_replay_attempt_types() -> list[str]:
    return []

def build_rehearsal_replay_plan(payload: dict[str, Any]) -> RehearsalReplayPlan:
    return build_default_rehearsal_replay_plan()

def build_default_rehearsal_replay_plan(candidate_id: str | None = None) -> RehearsalReplayPlan:
    return RehearsalReplayPlan(
        replay_plan_id=create_rehearsal_replay_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate_id,
        source_dry_admission_dossier_id=None,
        source_acceptance_seal_id=None
    )

def validate_rehearsal_replay_plan_safety(plan: RehearsalReplayPlan) -> list[str]:
    return []

def rehearsal_replay_plan_summary(plan: RehearsalReplayPlan) -> dict[str, Any]:
    return {}

def rehearsal_replay_plan_to_text(plan: RehearsalReplayPlan) -> str:
    return ""
